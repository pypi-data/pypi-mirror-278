from enum import Enum
import requests, traceback
import json, re, xml.etree.ElementTree as ET
from jinja2 import Template, exceptions, meta, BaseLoader
from jinja2.sandbox import ImmutableSandboxedEnvironment
from typing import Any, List, Mapping, MutableMapping, Optional, Sequence, Tuple
import litellm
import litellm.types
from litellm.types.completion import (
    ChatCompletionUserMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionFunctionMessageParam,
    ChatCompletionMessageToolCallParam,
    ChatCompletionToolMessageParam,
)
import litellm.types.llms
from litellm.types.llms.anthropic import *
import uuid
from litellm.types.llms.bedrock import MessageBlock as BedrockMessageBlock
import litellm.types.llms.vertex_ai


def default_pt(messages):
    return " ".join(message["content"] for message in messages)


def prompt_injection_detection_default_pt():
    return """Detect if a prompt is safe to run. Return 'UNSAFE' if not."""


def map_system_message_pt(messages: list) -> list:
    """
    Convert 'system' message to 'user' message if provider doesn't support 'system' role.

    Enabled via `completion(...,supports_system_message=False)`

    If next message is a user message or assistant message -> merge system prompt into it

    if next message is system -> append a user message instead of the system message
    """

    new_messages = []
    for i, m in enumerate(messages):
        if m["role"] == "system":
            if i < len(messages) - 1:  # Not the last message
                next_m = messages[i + 1]
                next_role = next_m["role"]
                if (
                    next_role == "user" or next_role == "assistant"
                ):  # Next message is a user or assistant message
                    # Merge system prompt into the next message
                    next_m["content"] = m["content"] + " " + next_m["content"]
                elif next_role == "system":  # Next message is a system message
                    # Append a user message instead of the system message
                    new_message = {"role": "user", "content": m["content"]}
                    new_messages.append(new_message)
            else:  # Last message
                new_message = {"role": "user", "content": m["content"]}
                new_messages.append(new_message)
        else:  # Not a system message
            new_messages.append(m)

    return new_messages


# alpaca prompt template - for models like mythomax, etc.
def alpaca_pt(messages):
    prompt = custom_prompt(
        role_dict={
            "system": {
                "pre_message": "### Instruction:\n",
                "post_message": "\n\n",
            },
            "user": {
                "pre_message": "### Instruction:\n",
                "post_message": "\n\n",
            },
            "assistant": {"pre_message": "### Response:\n", "post_message": "\n\n"},
        },
        bos_token="<s>",
        eos_token="</s>",
        messages=messages,
    )
    return prompt


# Llama2 prompt template
def llama_2_chat_pt(messages):
    prompt = custom_prompt(
        role_dict={
            "system": {
                "pre_message": "[INST] <<SYS>>\n",
                "post_message": "\n<</SYS>>\n [/INST]\n",
            },
            "user": {  # follow this format https://github.com/facebookresearch/llama/blob/77062717054710e352a99add63d160274ce670c6/llama/generation.py#L348
                "pre_message": "[INST] ",
                "post_message": " [/INST]\n",
            },
            "assistant": {
                "post_message": "\n"  # follows this - https://replicate.com/blog/how-to-prompt-llama
            },
        },
        messages=messages,
        bos_token="<s>",
        eos_token="</s>",
    )
    return prompt


def convert_to_ollama_image(openai_image_url: str):
    try:
        if openai_image_url.startswith("http"):
            openai_image_url = convert_url_to_base64(url=openai_image_url)

        if openai_image_url.startswith("data:image/"):
            # Extract the base64 image data
            base64_data = openai_image_url.split("data:image/")[1].split(";base64,")[1]
        else:
            base64_data = openai_image_url

        return base64_data
    except Exception as e:
        if "Error: Unable to fetch image from URL" in str(e):
            raise e
        raise Exception(
            """Image url not in expected format. Example Expected input - "image_url": "data:image/jpeg;base64,{base64_image}". """
        )


def ollama_pt(
    model, messages
):  # https://github.com/ollama/ollama/blob/af4cf55884ac54b9e637cd71dadfe9b7a5685877/docs/modelfile.md#template
    if "instruct" in model:
        prompt = custom_prompt(
            role_dict={
                "system": {"pre_message": "### System:\n", "post_message": "\n"},
                "user": {
                    "pre_message": "### User:\n",
                    "post_message": "\n",
                },
                "assistant": {
                    "pre_message": "### Response:\n",
                    "post_message": "\n",
                },
            },
            final_prompt_value="### Response:",
            messages=messages,
        )
    elif "llava" in model:
        prompt = ""
        images = []
        for message in messages:
            if isinstance(message["content"], str):
                prompt += message["content"]
            elif isinstance(message["content"], list):
                # see https://docs.litellm.ai/docs/providers/openai#openai-vision-models
                for element in message["content"]:
                    if isinstance(element, dict):
                        if element["type"] == "text":
                            prompt += element["text"]
                        elif element["type"] == "image_url":
                            base64_image = convert_to_ollama_image(
                                element["image_url"]["url"]
                            )
                            images.append(base64_image)
        return {"prompt": prompt, "images": images}
    else:
        prompt = "".join(
            (
                m["content"]
                if isinstance(m["content"], str) is str
                else "".join(m["content"])
            )
            for m in messages
        )
    return prompt


def mistral_instruct_pt(messages):
    # Following the Mistral example's https://huggingface.co/docs/transformers/main/chat_templating
    prompt = custom_prompt(
        initial_prompt_value="<s>",
        role_dict={
            "system": {
                "pre_message": "[INST] \n",
                "post_message": " [/INST]\n",
            },
            "user": {"pre_message": "[INST] ", "post_message": " [/INST]\n"},
            "assistant": {"pre_message": " ", "post_message": "</s> "},
        },
        final_prompt_value="",
        messages=messages,
    )
    return prompt


def mistral_api_pt(messages):
    """
    - handles scenario where content is list and not string
    - content list is just text, and no images
    - if image passed in, then just return as is (user-intended)

    Motivation: mistral api doesn't support content as a list
    """
    new_messages = []
    for m in messages:
        texts = ""
        if isinstance(m["content"], list):
            for c in m["content"]:
                if c["type"] == "image_url":
                    return messages
                elif c["type"] == "text" and isinstance(c["text"], str):
                    texts += c["text"]
        elif isinstance(m["content"], str):
            texts = m["content"]
        new_m = {"role": m["role"], "content": texts}

        if new_m["role"] == "tool" and m.get("name"):
            new_m["name"] = m["name"]
        if m.get("tool_calls"):
            new_m["tool_calls"] = m["tool_calls"]

        new_messages.append(new_m)
    return new_messages


# Falcon prompt template - from https://github.com/lm-sys/FastChat/blob/main/fastchat/conversation.py#L110
def falcon_instruct_pt(messages):
    prompt = ""
    for message in messages:
        if message["role"] == "system":
            prompt += message["content"]
        else:
            prompt += (
                message["role"]
                + ":"
                + message["content"].replace("\r\n", "\n").replace("\n\n", "\n")
            )
            prompt += "\n\n"

    return prompt


def falcon_chat_pt(messages):
    prompt = ""
    for message in messages:
        if message["role"] == "system":
            prompt += "System: " + message["content"]
        elif message["role"] == "assistant":
            prompt += "Falcon: " + message["content"]
        elif message["role"] == "user":
            prompt += "User: " + message["content"]

    return prompt


# MPT prompt template - from https://github.com/lm-sys/FastChat/blob/main/fastchat/conversation.py#L110
def mpt_chat_pt(messages):
    prompt = ""
    for message in messages:
        if message["role"] == "system":
            prompt += "<|im_start|>system" + message["content"] + "<|im_end|>" + "\n"
        elif message["role"] == "assistant":
            prompt += "<|im_start|>assistant" + message["content"] + "<|im_end|>" + "\n"
        elif message["role"] == "user":
            prompt += "<|im_start|>user" + message["content"] + "<|im_end|>" + "\n"
    return prompt


# WizardCoder prompt template - https://huggingface.co/WizardLM/WizardCoder-Python-34B-V1.0#prompt-format
def wizardcoder_pt(messages):
    prompt = ""
    for message in messages:
        if message["role"] == "system":
            prompt += message["content"] + "\n\n"
        elif message["role"] == "user":  # map to 'Instruction'
            prompt += "### Instruction:\n" + message["content"] + "\n\n"
        elif message["role"] == "assistant":  # map to 'Response'
            prompt += "### Response:\n" + message["content"] + "\n\n"
    return prompt


# Phind-CodeLlama prompt template - https://huggingface.co/Phind/Phind-CodeLlama-34B-v2#how-to-prompt-the-model
def phind_codellama_pt(messages):
    prompt = ""
    for message in messages:
        if message["role"] == "system":
            prompt += "### System Prompt\n" + message["content"] + "\n\n"
        elif message["role"] == "user":
            prompt += "### User Message\n" + message["content"] + "\n\n"
        elif message["role"] == "assistant":
            prompt += "### Assistant\n" + message["content"] + "\n\n"
    return prompt


known_tokenizer_config = {
    "mistralai/Mistral-7B-Instruct-v0.1": {
        "tokenizer": {
            "chat_template": "{{ bos_token }}{% for message in messages %}{% if (message['role'] == 'user') != (loop.index0 % 2 == 0) %}{{ raise_exception('Conversation roles must alternate user/assistant/user/assistant/...') }}{% endif %}{% if message['role'] == 'user' %}{{ '[INST] ' + message['content'] + ' [/INST]' }}{% elif message['role'] == 'assistant' %}{{ message['content'] + eos_token + ' ' }}{% else %}{{ raise_exception('Only user and assistant roles are supported!') }}{% endif %}{% endfor %}",
            "bos_token": "<s>",
            "eos_token": "</s>",
        },
        "status": "success",
    },
    "meta-llama/Meta-Llama-3-8B-Instruct": {
        "tokenizer": {
            "chat_template": "{% set loop_messages = messages %}{% for message in loop_messages %}{% set content = '<|start_header_id|>' + message['role'] + '<|end_header_id|>\n\n'+ message['content'] | trim + '<|eot_id|>' %}{% if loop.index0 == 0 %}{% set content = bos_token + content %}{% endif %}{{ content }}{% endfor %}{{ '<|start_header_id|>assistant<|end_header_id|>\n\n' }}",
            "bos_token": "<|begin_of_text|>",
            "eos_token": "",
        },
        "status": "success",
    },
}


def hf_chat_template(model: str, messages: list, chat_template: Optional[Any] = None):
    # Define Jinja2 environment
    env = ImmutableSandboxedEnvironment()

    def raise_exception(message):
        raise Exception(f"Error message - {message}")

    # Create a template object from the template text
    env.globals["raise_exception"] = raise_exception

    ## get the tokenizer config from huggingface
    bos_token = ""
    eos_token = ""
    if chat_template is None:

        def _get_tokenizer_config(hf_model_name):
            url = (
                f"https://huggingface.co/{hf_model_name}/raw/main/tokenizer_config.json"
            )
            # Make a GET request to fetch the JSON data
            response = requests.get(url)
            if response.status_code == 200:
                # Parse the JSON data
                tokenizer_config = json.loads(response.content)
                return {"status": "success", "tokenizer": tokenizer_config}
            else:
                return {"status": "failure"}

        if model in known_tokenizer_config:
            tokenizer_config = known_tokenizer_config[model]
        else:
            tokenizer_config = _get_tokenizer_config(model)
        if (
            tokenizer_config["status"] == "failure"
            or "chat_template" not in tokenizer_config["tokenizer"]
        ):
            raise Exception("No chat template found")
        ## read the bos token, eos token and chat template from the json
        tokenizer_config = tokenizer_config["tokenizer"]  # type: ignore

        bos_token = tokenizer_config["bos_token"]  # type: ignore
        eos_token = tokenizer_config["eos_token"]  # type: ignore
        chat_template = tokenizer_config["chat_template"]  # type: ignore
    try:
        template = env.from_string(chat_template)  # type: ignore
    except Exception as e:
        raise e

    def _is_system_in_template():
        try:
            # Try rendering the template with a system message
            response = template.render(
                messages=[{"role": "system", "content": "test"}],
                eos_token="<eos>",
                bos_token="<bos>",
            )
            return True

        # This will be raised if Jinja attempts to render the system message and it can't
        except:
            return False

    try:
        # Render the template with the provided values
        if _is_system_in_template():
            rendered_text = template.render(
                bos_token=bos_token, eos_token=eos_token, messages=messages
            )
        else:
            # treat a system message as a user message, if system not in template
            try:
                reformatted_messages = []
                for message in messages:
                    if message["role"] == "system":
                        reformatted_messages.append(
                            {"role": "user", "content": message["content"]}
                        )
                    else:
                        reformatted_messages.append(message)
                rendered_text = template.render(
                    bos_token=bos_token,
                    eos_token=eos_token,
                    messages=reformatted_messages,
                )
            except Exception as e:
                if "Conversation roles must alternate user/assistant" in str(e):
                    # reformat messages to ensure user/assistant are alternating, if there's either 2 consecutive 'user' messages or 2 consecutive 'assistant' message, add a blank 'user' or 'assistant' message to ensure compatibility
                    new_messages = []
                    for i in range(len(reformatted_messages) - 1):
                        new_messages.append(reformatted_messages[i])
                        if (
                            reformatted_messages[i]["role"]
                            == reformatted_messages[i + 1]["role"]
                        ):
                            if reformatted_messages[i]["role"] == "user":
                                new_messages.append(
                                    {"role": "assistant", "content": ""}
                                )
                            else:
                                new_messages.append({"role": "user", "content": ""})
                    new_messages.append(reformatted_messages[-1])
                    rendered_text = template.render(
                        bos_token=bos_token, eos_token=eos_token, messages=new_messages
                    )
        return rendered_text
    except Exception as e:
        raise Exception(f"Error rendering template - {str(e)}")


# Anthropic template
def claude_2_1_pt(
    messages: list,
):  # format - https://docs.anthropic.com/claude/docs/how-to-use-system-prompts
    """
    Claude v2.1 allows system prompts (no Human: needed), but requires it be followed by Human:
    - you can't just pass a system message
    - you can't pass a system message and follow that with an assistant message
    if system message is passed in, you can only do system, human, assistant or system, human

    if a system message is passed in and followed by an assistant message, insert a blank human message between them.

    Additionally, you can "put words in Claude's mouth" by ending with an assistant message.
    See: https://docs.anthropic.com/claude/docs/put-words-in-claudes-mouth
    """

    class AnthropicConstants(Enum):
        HUMAN_PROMPT = "\n\nHuman: "
        AI_PROMPT = "\n\nAssistant: "

    prompt = ""
    for idx, message in enumerate(messages):
        if message["role"] == "user":
            prompt += f"{AnthropicConstants.HUMAN_PROMPT.value}{message['content']}"
        elif message["role"] == "system":
            prompt += f"{message['content']}"
        elif message["role"] == "assistant":
            if idx > 0 and messages[idx - 1]["role"] == "system":
                prompt += f"{AnthropicConstants.HUMAN_PROMPT.value}"  # Insert a blank human message
            prompt += f"{AnthropicConstants.AI_PROMPT.value}{message['content']}"
    if messages[-1]["role"] != "assistant":
        prompt += f"{AnthropicConstants.AI_PROMPT.value}"  # prompt must end with \"\n\nAssistant: " turn
    return prompt


### TOGETHER AI


def get_model_info(token, model):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get("https://api.together.xyz/models/info", headers=headers)
        if response.status_code == 200:
            model_info = response.json()
            for m in model_info:
                if m["name"].lower().strip() == model.strip():
                    return m["config"].get("prompt_format", None), m["config"].get(
                        "chat_template", None
                    )
            return None, None
        else:
            return None, None
    except Exception as e:  # safely fail a prompt template request
        return None, None


def format_prompt_togetherai(messages, prompt_format, chat_template):
    if prompt_format is None:
        return default_pt(messages)

    human_prompt, assistant_prompt = prompt_format.split("{prompt}")

    if chat_template is not None:
        prompt = hf_chat_template(
            model=None, messages=messages, chat_template=chat_template
        )
    elif prompt_format is not None:
        prompt = custom_prompt(
            role_dict={},
            messages=messages,
            initial_prompt_value=human_prompt,
            final_prompt_value=assistant_prompt,
        )
    else:
        prompt = default_pt(messages)
    return prompt


### IBM Granite


def ibm_granite_pt(messages: list):
    """
    IBM's Granite models uses the template:
    <|system|> {system_message} <|user|> {user_message} <|assistant|> {assistant_message}

    See: https://www.ibm.com/docs/en/watsonx-as-a-service?topic=solutions-supported-foundation-models
    """
    return custom_prompt(
        messages=messages,
        role_dict={
            "system": {
                "pre_message": "<|system|>\n",
                "post_message": "\n",
            },
            "user": {
                "pre_message": "<|user|>\n",
                "post_message": "\n",
            },
            "assistant": {
                "pre_message": "<|assistant|>\n",
                "post_message": "\n",
            },
        },
    ).strip()


### ANTHROPIC ###


def anthropic_pt(
    messages: list,
):  # format - https://docs.anthropic.com/claude/reference/complete_post
    """
    You can "put words in Claude's mouth" by ending with an assistant message.
    See: https://docs.anthropic.com/claude/docs/put-words-in-claudes-mouth
    """

    class AnthropicConstants(Enum):
        HUMAN_PROMPT = "\n\nHuman: "
        AI_PROMPT = "\n\nAssistant: "

    prompt = ""
    for idx, message in enumerate(
        messages
    ):  # needs to start with `\n\nHuman: ` and end with `\n\nAssistant: `
        if message["role"] == "user":
            prompt += f"{AnthropicConstants.HUMAN_PROMPT.value}{message['content']}"
        elif message["role"] == "system":
            prompt += f"{AnthropicConstants.HUMAN_PROMPT.value}<admin>{message['content']}</admin>"
        else:
            prompt += f"{AnthropicConstants.AI_PROMPT.value}{message['content']}"
        if (
            idx == 0 and message["role"] == "assistant"
        ):  # ensure the prompt always starts with `\n\nHuman: `
            prompt = f"{AnthropicConstants.HUMAN_PROMPT.value}" + prompt
    if messages[-1]["role"] != "assistant":
        prompt += f"{AnthropicConstants.AI_PROMPT.value}"
    return prompt


def construct_format_parameters_prompt(parameters: dict):
    parameter_str = "<parameter>\n"
    for k, v in parameters.items():
        parameter_str += f"<{k}>"
        parameter_str += f"{v}"
        parameter_str += f"</{k}>"
    parameter_str += "\n</parameter>"
    return parameter_str


def construct_format_tool_for_claude_prompt(name, description, parameters):
    constructed_prompt = (
        "<tool_description>\n"
        f"<tool_name>{name}</tool_name>\n"
        "<description>\n"
        f"{description}\n"
        "</description>\n"
        "<parameters>\n"
        f"{construct_format_parameters_prompt(parameters)}\n"
        "</parameters>\n"
        "</tool_description>"
    )
    return constructed_prompt


def construct_tool_use_system_prompt(
    tools,
):  # from https://github.com/anthropics/anthropic-cookbook/blob/main/function_calling/function_calling.ipynb
    tool_str_list = []
    for tool in tools:
        tool_function = get_attribute_or_key(tool, "function")
        tool_str = construct_format_tool_for_claude_prompt(
            get_attribute_or_key(tool_function, "name"),
            get_attribute_or_key(tool_function, "description", ""),
            get_attribute_or_key(tool_function, "parameters", {}),
        )
        tool_str_list.append(tool_str)
    tool_use_system_prompt = (
        "In this environment you have access to a set of tools you can use to answer the user's question.\n"
        "\n"
        "You may call them like this:\n"
        "<function_calls>\n"
        "<invoke>\n"
        "<tool_name>$TOOL_NAME</tool_name>\n"
        "<parameters>\n"
        "<$PARAMETER_NAME>$PARAMETER_VALUE</$PARAMETER_NAME>\n"
        "...\n"
        "</parameters>\n"
        "</invoke>\n"
        "</function_calls>\n"
        "\n"
        "Here are the tools available:\n"
        "<tools>\n" + "\n".join([tool_str for tool_str in tool_str_list]) + "\n</tools>"
    )
    return tool_use_system_prompt


def convert_url_to_base64(url):
    import requests
    import base64

    for _ in range(3):
        try:
            response = requests.get(url)
            break
        except:
            pass
    if response.status_code == 200:
        image_bytes = response.content
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        img_type = url.split(".")[-1].lower()
        if img_type == "jpg" or img_type == "jpeg":
            img_type = "image/jpeg"
        elif img_type == "png":
            img_type = "image/png"
        elif img_type == "gif":
            img_type = "image/gif"
        elif img_type == "webp":
            img_type = "image/webp"
        else:
            raise Exception(
                f"Error: Unsupported image format. Format={img_type}. Supported types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']"
            )

        return f"data:{img_type};base64,{base64_image}"
    else:
        raise Exception(f"Error: Unable to fetch image from URL. url={url}")


def convert_to_anthropic_image_obj(openai_image_url: str):
    """
    Input:
    "image_url": "data:image/jpeg;base64,{base64_image}",

    Return:
    "source": {
      "type": "base64",
      "media_type": "image/jpeg",
      "data": {base64_image},
    }
    """
    try:
        if openai_image_url.startswith("http"):
            openai_image_url = convert_url_to_base64(url=openai_image_url)
        # Extract the base64 image data
        base64_data = openai_image_url.split("data:image/")[1].split(";base64,")[1]

        # Infer image format from the URL
        image_format = openai_image_url.split("data:image/")[1].split(";base64,")[0]

        return {
            "type": "base64",
            "media_type": f"image/{image_format}",
            "data": base64_data,
        }
    except Exception as e:
        if "Error: Unable to fetch image from URL" in str(e):
            raise e
        raise Exception(
            """Image url not in expected format. Example Expected input - "image_url": "data:image/jpeg;base64,{base64_image}". Supported formats - ['image/jpeg', 'image/png', 'image/gif', 'image/webp'] """
        )


# The following XML functions will be deprecated once JSON schema support is available on Bedrock and Vertex
# ------------------------------------------------------------------------------
def convert_to_anthropic_tool_result_xml(message: dict) -> str:
    """
    OpenAI message with a tool result looks like:
    {
        "tool_call_id": "tool_1",
        "role": "tool",
        "name": "get_current_weather",
        "content": "function result goes here",
    },
    """

    """
    Anthropic tool_results look like:
    
    [Successful results]
    <function_results>
    <result>
    <tool_name>get_current_weather</tool_name>
    <stdout>
    function result goes here
    </stdout>
    </result>
    </function_results>

    [Error results]
    <function_results>
    <error>
    error message goes here
    </error>
    </function_results>
    """
    name = message.get("name")
    content = message.get("content", "")
    content = content.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")

    # We can't determine from openai message format whether it's a successful or
    # error call result so default to the successful result template
    anthropic_tool_result = (
        "<function_results>\n"
        "<result>\n"
        f"<tool_name>{name}</tool_name>\n"
        "<stdout>\n"
        f"{content}\n"
        "</stdout>\n"
        "</result>\n"
        "</function_results>"
    )

    return anthropic_tool_result


def convert_to_anthropic_tool_invoke_xml(tool_calls: list) -> str:
    invokes = ""
    for tool in tool_calls:
        if get_attribute_or_key(tool, "type") != "function":
            continue

        tool_function = get_attribute_or_key(tool, "function")
        tool_name = get_attribute_or_key(tool_function, "name")
        tool_arguments = get_attribute_or_key(tool_function, "arguments")
        parameters = "".join(
            f"<{param}>{val}</{param}>\n"
            for param, val in json.loads(tool_arguments).items()
        )
        invokes += (
            "<invoke>\n"
            f"<tool_name>{tool_name}</tool_name>\n"
            "<parameters>\n"
            f"{parameters}"
            "</parameters>\n"
            "</invoke>\n"
        )

    anthropic_tool_invoke = f"<function_calls>\n{invokes}</function_calls>"

    return anthropic_tool_invoke


def anthropic_messages_pt_xml(messages: list):
    """
    format messages for anthropic
    1. Anthropic supports roles like "user" and "assistant", (here litellm translates system-> assistant)
    2. The first message always needs to be of role "user"
    3. Each message must alternate between "user" and "assistant" (this is not addressed as now by litellm)
    4. final assistant content cannot end with trailing whitespace (anthropic raises an error otherwise)
    5. System messages are a separate param to the Messages API (used for tool calling)
    6. Ensure we only accept role, content. (message.name is not supported)
    """
    # add role=tool support to allow function call result/error submission
    user_message_types = {"user", "tool"}
    # reformat messages to ensure user/assistant are alternating, if there's either 2 consecutive 'user' messages or 2 consecutive 'assistant' message, merge them.
    new_messages = []
    msg_i = 0
    while msg_i < len(messages):
        user_content = []
        ## MERGE CONSECUTIVE USER CONTENT ##
        while msg_i < len(messages) and messages[msg_i]["role"] in user_message_types:
            if isinstance(messages[msg_i]["content"], list):
                for m in messages[msg_i]["content"]:
                    if m.get("type", "") == "image_url":
                        user_content.append(
                            {
                                "type": "image",
                                "source": convert_to_anthropic_image_obj(
                                    m["image_url"]["url"]
                                ),
                            }
                        )
                    elif m.get("type", "") == "text":
                        user_content.append({"type": "text", "text": m["text"]})
            else:
                # Tool message content will always be a string
                user_content.append(
                    {
                        "type": "text",
                        "text": (
                            convert_to_anthropic_tool_result_xml(messages[msg_i])
                            if messages[msg_i]["role"] == "tool"
                            else messages[msg_i]["content"]
                        ),
                    }
                )

            msg_i += 1

        if user_content:
            new_messages.append({"role": "user", "content": user_content})

        assistant_content = []
        ## MERGE CONSECUTIVE ASSISTANT CONTENT ##
        while msg_i < len(messages) and messages[msg_i]["role"] == "assistant":
            assistant_text = (
                messages[msg_i].get("content") or ""
            )  # either string or none
            if messages[msg_i].get(
                "tool_calls", []
            ):  # support assistant tool invoke conversion
                assistant_text += convert_to_anthropic_tool_invoke_xml(  # type: ignore
                    messages[msg_i]["tool_calls"]
                )

            assistant_content.append({"type": "text", "text": assistant_text})
            msg_i += 1

        if assistant_content:
            new_messages.append({"role": "assistant", "content": assistant_content})

    if not new_messages or new_messages[0]["role"] != "user":
        if litellm.modify_params:
            new_messages.insert(
                0, {"role": "user", "content": [{"type": "text", "text": "."}]}
            )
        else:
            raise Exception(
                "Invalid first message. Should always start with 'role'='user' for Anthropic. System prompt is sent separately for Anthropic. set 'litellm.modify_params = True' or 'litellm_settings:modify_params = True' on proxy, to insert a placeholder user message - '.' as the first message, "
            )

    if new_messages[-1]["role"] == "assistant":
        for content in new_messages[-1]["content"]:
            if isinstance(content, dict) and content["type"] == "text":
                content["text"] = content[
                    "text"
                ].rstrip()  # no trailing whitespace for final assistant message

    return new_messages


# ------------------------------------------------------------------------------


def infer_protocol_value(
    value: Any,
) -> Literal[
    "string_value",
    "number_value",
    "bool_value",
    "struct_value",
    "list_value",
    "null_value",
    "unknown",
]:
    if value is None:
        return "null_value"
    if isinstance(value, int) or isinstance(value, float):
        return "number_value"
    if isinstance(value, str):
        return "string_value"
    if isinstance(value, bool):
        return "bool_value"
    if isinstance(value, dict):
        return "struct_value"
    if isinstance(value, list):
        return "list_value"

    return "unknown"


def convert_to_gemini_tool_call_invoke(
    tool_calls: list,
) -> List[litellm.types.llms.vertex_ai.PartType]:
    """
    OpenAI tool invokes:
    {
      "role": "assistant",
      "content": null,
      "tool_calls": [
        {
          "id": "call_abc123",
          "type": "function",
          "function": {
            "name": "get_current_weather",
            "arguments": "{\n\"location\": \"Boston, MA\"\n}"
          }
        }
      ]
    },
    """
    """
    Gemini tool call invokes: - https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling#submit-api-output
    content {
        role: "model"
        parts [
        {
            function_call {
            name: "get_current_weather"
            args {
                fields {
                    key: "unit"
                    value {
                    string_value: "fahrenheit"
                    }
                }
                fields {
                    key: "predicted_temperature"
                    value {
                    number_value: 45
                    }
                }
                fields {
                    key: "location"
                    value {
                    string_value: "Boston, MA"
                    }
                }
            }
        },
        {
            function_call {
            name: "get_current_weather"
            args {
                fields {
                key: "location"
                value {
                    string_value: "San Francisco"
                }
                }
            }
            }
        }
        ]
    }
    """

    """
    - json.load the arguments 
    - iterate through arguments -> create a FunctionCallArgs for each field
    """
    try:
        _parts_list: List[litellm.types.llms.vertex_ai.PartType] = []
        for tool in tool_calls:
            if "function" in tool:
                name = tool["function"].get("name", "")
                arguments = tool["function"].get("arguments", "")
                arguments_dict = json.loads(arguments)
                for k, v in arguments_dict.items():
                    inferred_protocol_value = infer_protocol_value(value=v)
                    _field = litellm.types.llms.vertex_ai.Field(
                        key=k, value={inferred_protocol_value: v}
                    )
                    _fields = litellm.types.llms.vertex_ai.FunctionCallArgs(
                        fields=_field
                    )
                    function_call = litellm.types.llms.vertex_ai.FunctionCall(
                        name=name,
                        args=_fields,
                    )
                _parts_list.append(
                    litellm.types.llms.vertex_ai.PartType(function_call=function_call)
                )
        return _parts_list
    except Exception as e:
        raise Exception(
            "Unable to convert openai tool calls={} to gemini tool calls. Received error={}".format(
                tool_calls, str(e)
            )
        )


def convert_to_gemini_tool_call_result(
    message: dict,
) -> litellm.types.llms.vertex_ai.PartType:
    """
    OpenAI message with a tool result looks like:
    {
        "tool_call_id": "tool_1",
        "role": "tool",
        "name": "get_current_weather",
        "content": "function result goes here",
    },

    OpenAI message with a function call result looks like:
    {
        "role": "function",
        "name": "get_current_weather",
        "content": "function result goes here",
    }
    """
    content = message.get("content", "")
    name = message.get("name", "")

    # We can't determine from openai message format whether it's a successful or
    # error call result so default to the successful result template
    inferred_content_value = infer_protocol_value(value=content)

    _field = litellm.types.llms.vertex_ai.Field(
        key="content", value={inferred_content_value: content}
    )

    _function_call_args = litellm.types.llms.vertex_ai.FunctionCallArgs(fields=_field)

    _function_response = litellm.types.llms.vertex_ai.FunctionResponse(
        name=name, response=_function_call_args
    )

    _part = litellm.types.llms.vertex_ai.PartType(function_response=_function_response)

    return _part


def convert_to_anthropic_tool_result(message: dict) -> dict:
    """
    OpenAI message with a tool result looks like:
    {
        "tool_call_id": "tool_1",
        "role": "tool",
        "name": "get_current_weather",
        "content": "function result goes here",
    },

    OpenAI message with a function call result looks like:
    {
        "role": "function",
        "name": "get_current_weather",
        "content": "function result goes here",
    }
    """

    """
    Anthropic tool_results look like:
    {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
                "content": "ConnectionError: the weather service API is not available (HTTP 500)",
                # "is_error": true
            }
        ]
    }
    """
    if message["role"] == "tool":
        tool_call_id = message.get("tool_call_id")
        content = message.get("content")

        # We can't determine from openai message format whether it's a successful or
        # error call result so default to the successful result template
        anthropic_tool_result = {
            "type": "tool_result",
            "tool_use_id": tool_call_id,
            "content": content,
        }
        return anthropic_tool_result
    elif message["role"] == "function":
        content = message.get("content")
        anthropic_tool_result = {
            "type": "tool_result",
            "tool_use_id": str(uuid.uuid4()),
            "content": content,
        }
        return anthropic_tool_result
    return {}


def convert_function_to_anthropic_tool_invoke(function_call):
    try:
        anthropic_tool_invoke = [
            {
                "type": "tool_use",
                "id": str(uuid.uuid4()),
                "name": get_attribute_or_key(function_call, "name"),
                "input": json.loads(get_attribute_or_key(function_call, "arguments")),
            }
        ]
        return anthropic_tool_invoke
    except Exception as e:
        raise e


def convert_to_anthropic_tool_invoke(tool_calls: list) -> list:
    """
    OpenAI tool invokes:
    {
      "role": "assistant",
      "content": null,
      "tool_calls": [
        {
          "id": "call_abc123",
          "type": "function",
          "function": {
            "name": "get_current_weather",
            "arguments": "{\n\"location\": \"Boston, MA\"\n}"
          }
        }
      ]
    },
    """

    """
    Anthropic tool invokes:
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "<thinking>To answer this question, I will: 1. Use the get_weather tool to get the current weather in San Francisco. 2. Use the get_time tool to get the current time in the America/Los_Angeles timezone, which covers San Francisco, CA.</thinking>"
        },
        {
          "type": "tool_use",
          "id": "toolu_01A09q90qw90lq917835lq9",
          "name": "get_weather",
          "input": {"location": "San Francisco, CA"}
        }
      ]
    }
    """
    anthropic_tool_invoke = [
        {
            "type": "tool_use",
            "id": get_attribute_or_key(tool, "id"),
            "name": get_attribute_or_key(
                get_attribute_or_key(tool, "function"), "name"
            ),
            "input": json.loads(
                get_attribute_or_key(
                    get_attribute_or_key(tool, "function"), "arguments"
                )
            ),
        }
        for tool in tool_calls
        if get_attribute_or_key(tool, "type") == "function"
    ]

    return anthropic_tool_invoke


def anthropic_messages_pt(messages: list):
    """
    format messages for anthropic
    1. Anthropic supports roles like "user" and "assistant" (system prompt sent separately)
    2. The first message always needs to be of role "user"
    3. Each message must alternate between "user" and "assistant" (this is not addressed as now by litellm)
    4. final assistant content cannot end with trailing whitespace (anthropic raises an error otherwise)
    5. System messages are a separate param to the Messages API
    6. Ensure we only accept role, content. (message.name is not supported)
    """
    # add role=tool support to allow function call result/error submission
    user_message_types = {"user", "tool", "function"}
    # reformat messages to ensure user/assistant are alternating, if there's either 2 consecutive 'user' messages or 2 consecutive 'assistant' message, merge them.
    new_messages: list = []
    msg_i = 0
    tool_use_param = False
    while msg_i < len(messages):
        user_content = []
        init_msg_i = msg_i
        ## MERGE CONSECUTIVE USER CONTENT ##
        while msg_i < len(messages) and messages[msg_i]["role"] in user_message_types:
            if isinstance(messages[msg_i]["content"], list):
                for m in messages[msg_i]["content"]:
                    if m.get("type", "") == "image_url":
                        user_content.append(
                            {
                                "type": "image",
                                "source": convert_to_anthropic_image_obj(
                                    m["image_url"]["url"]
                                ),
                            }
                        )
                    elif m.get("type", "") == "text":
                        user_content.append({"type": "text", "text": m["text"]})
            elif (
                messages[msg_i]["role"] == "tool"
                or messages[msg_i]["role"] == "function"
            ):
                # OpenAI's tool message content will always be a string
                user_content.append(convert_to_anthropic_tool_result(messages[msg_i]))
            else:
                user_content.append(
                    {"type": "text", "text": messages[msg_i]["content"]}
                )

            msg_i += 1

        if user_content:
            new_messages.append({"role": "user", "content": user_content})

        assistant_content = []
        ## MERGE CONSECUTIVE ASSISTANT CONTENT ##
        while msg_i < len(messages) and messages[msg_i]["role"] == "assistant":
            assistant_text = (
                messages[msg_i].get("content") or ""
            )  # either string or none
            if assistant_text:
                assistant_content.append({"type": "text", "text": assistant_text})

            if messages[msg_i].get(
                "tool_calls", []
            ):  # support assistant tool invoke conversion
                assistant_content.extend(
                    convert_to_anthropic_tool_invoke(messages[msg_i]["tool_calls"])
                )

            if messages[msg_i].get("function_call"):
                assistant_content.extend(
                    convert_function_to_anthropic_tool_invoke(
                        messages[msg_i]["function_call"]
                    )
                )

            msg_i += 1

        if assistant_content:
            new_messages.append({"role": "assistant", "content": assistant_content})

        if msg_i == init_msg_i:  # prevent infinite loops
            raise Exception(
                "Invalid Message passed in - {}. File an issue https://github.com/BerriAI/litellm/issues".format(
                    messages[msg_i]
                )
            )
    if not new_messages or new_messages[0]["role"] != "user":
        if litellm.modify_params:
            new_messages.insert(
                0, {"role": "user", "content": [{"type": "text", "text": "."}]}
            )
        else:
            raise Exception(
                "Invalid first message. Should always start with 'role'='user' for Anthropic. System prompt is sent separately for Anthropic. set 'litellm.modify_params = True' or 'litellm_settings:modify_params = True' on proxy, to insert a placeholder user message - '.' as the first message, "
            )

    if new_messages[-1]["role"] == "assistant":
        if isinstance(new_messages[-1]["content"], str):
            new_messages[-1]["content"] = new_messages[-1]["content"].rstrip()
        elif isinstance(new_messages[-1]["content"], list):
            for content in new_messages[-1]["content"]:
                if isinstance(content, dict) and content["type"] == "text":
                    content["text"] = content[
                        "text"
                    ].rstrip()  # no trailing whitespace for final assistant message

    return new_messages


def extract_between_tags(tag: str, string: str, strip: bool = False) -> List[str]:
    ext_list = re.findall(f"<{tag}>(.+?)</{tag}>", string, re.DOTALL)
    if strip:
        ext_list = [e.strip() for e in ext_list]
    return ext_list


def contains_tag(tag: str, string: str) -> bool:
    return bool(re.search(f"<{tag}>(.+?)</{tag}>", string, re.DOTALL))


def parse_xml_params(xml_content, json_schema: Optional[dict] = None):
    """
    Compare the xml output to the json schema

    check if a value is a list - if so, get it's child elements
    """
    root = ET.fromstring(xml_content)
    params = {}

    if json_schema is not None:  # check if we have a json schema for this function call
        # iterate over all properties in the schema
        for prop in json_schema["properties"]:
            # If property is an array, get the nested items
            _element = root.find(f"parameters/{prop}")
            if json_schema["properties"][prop]["type"] == "array":
                items = []
                if _element is not None:
                    for value in _element:
                        try:
                            if value.text is not None:
                                _value = json.loads(value.text)
                            else:
                                continue
                        except json.JSONDecodeError:
                            _value = value.text
                        items.append(_value)
                    params[prop] = items
            # If property is not an array, append the value directly
            elif _element is not None and _element.text is not None:
                try:
                    _value = json.loads(_element.text)
                except json.JSONDecodeError:
                    _value = _element.text
                params[prop] = _value
    else:
        for child in root.findall(".//parameters/*"):
            if child is not None and child.text is not None:
                try:
                    # Attempt to decode the element's text as JSON
                    params[child.tag] = json.loads(child.text)  # type: ignore
                except json.JSONDecodeError:
                    # If JSON decoding fails, use the original text
                    params[child.tag] = child.text  # type: ignore

    return params


### GEMINI HELPER FUNCTIONS ###


def get_system_prompt(messages):
    system_prompt_indices = []
    system_prompt = ""
    for idx, message in enumerate(messages):
        if message["role"] == "system":
            system_prompt += message["content"]
            system_prompt_indices.append(idx)
    if len(system_prompt_indices) > 0:
        for idx in reversed(system_prompt_indices):
            messages.pop(idx)
    return system_prompt, messages


def convert_to_documents(
    observations: Any,
) -> List[MutableMapping]:
    """Converts observations into a 'document' dict"""
    documents: List[MutableMapping] = []
    if isinstance(observations, str):
        # strings are turned into a key/value pair and a key of 'output' is added.
        observations = [{"output": observations}]
    elif isinstance(observations, Mapping):
        # single mappings are transformed into a list to simplify the rest of the code.
        observations = [observations]
    elif not isinstance(observations, Sequence):
        # all other types are turned into a key/value pair within a list
        observations = [{"output": observations}]

    for doc in observations:
        if not isinstance(doc, Mapping):
            # types that aren't Mapping are turned into a key/value pair.
            doc = {"output": doc}
        documents.append(doc)

    return documents


def convert_openai_message_to_cohere_tool_result(message):
    """
    OpenAI message with a tool result looks like:
    {
            "tool_call_id": "tool_1",
            "role": "tool",
            "name": "get_current_weather",
            "content": {"location": "San Francisco, CA", "unit": "fahrenheit", "temperature": "72"},
    },
    """

    """
    Cohere tool_results look like:
    {
       "call": {
           "name": "query_daily_sales_report",
           "parameters": {
               "day": "2023-09-29"
           },
           "generation_id": "4807c924-9003-4d6b-8069-eda03962c465"
       },
       "outputs": [
           {
               "date": "2023-09-29",
               "summary": "Total Sales Amount: 10000, Total Units Sold: 250"
           }
       ]
   },
    """

    tool_call_id = message.get("tool_call_id")
    name = message.get("name")
    content = message.get("content")

    # Create the Cohere tool_result dictionary
    cohere_tool_result = {
        "call": {
            "name": name,
            "parameters": {"location": "San Francisco, CA"},
            "generation_id": tool_call_id,
        },
        "outputs": convert_to_documents(content),
    }
    return cohere_tool_result


def cohere_message_pt(messages: list):
    prompt = ""
    tool_results = []
    for message in messages:
        # check if this is a tool_call result
        if message["role"] == "tool":
            tool_result = convert_openai_message_to_cohere_tool_result(message)
            tool_results.append(tool_result)
        elif message.get("content"):
            prompt += message["content"] + "\n\n"
    prompt = prompt.rstrip()
    return prompt, tool_results


def amazon_titan_pt(
    messages: list,
):  # format - https://github.com/BerriAI/litellm/issues/1896
    """
    Amazon Titan uses 'User:' and 'Bot: in it's prompt template
    """

    class AmazonTitanConstants(Enum):
        HUMAN_PROMPT = "\n\nUser: "  # Assuming this is similar to Anthropic prompt formatting, since amazon titan's prompt formatting is currently undocumented
        AI_PROMPT = "\n\nBot: "

    prompt = ""
    for idx, message in enumerate(messages):
        if message["role"] == "user":
            prompt += f"{AmazonTitanConstants.HUMAN_PROMPT.value}{message['content']}"
        elif message["role"] == "system":
            prompt += f"{AmazonTitanConstants.HUMAN_PROMPT.value}<admin>{message['content']}</admin>"
        else:
            prompt += f"{AmazonTitanConstants.AI_PROMPT.value}{message['content']}"
        if (
            idx == 0 and message["role"] == "assistant"
        ):  # ensure the prompt always starts with `\n\nHuman: `
            prompt = f"{AmazonTitanConstants.HUMAN_PROMPT.value}" + prompt
    if messages[-1]["role"] != "assistant":
        prompt += f"{AmazonTitanConstants.AI_PROMPT.value}"
    return prompt


def _load_image_from_url(image_url):
    try:
        from PIL import Image
    except:
        raise Exception("image conversion failed please run `pip install Pillow`")
    from io import BytesIO

    try:
        # Send a GET request to the image URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Check the response's content type to ensure it is an image
        content_type = response.headers.get("content-type")
        if not content_type or "image" not in content_type:
            raise ValueError(
                f"URL does not point to a valid image (content-type: {content_type})"
            )

        # Load the image from the response content
        return Image.open(BytesIO(response.content))

    except requests.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except Exception as e:
        raise e


def _gemini_vision_convert_messages(messages: list):
    """
    Converts given messages for GPT-4 Vision to Gemini format.

    Args:
        messages (list): The messages to convert. Each message can be a dictionary with a "content" key. The content can be a string or a list of elements. If it is a string, it will be concatenated to the prompt. If it is a list, each element will be processed based on its type:
            - If the element is a dictionary with a "type" key equal to "text", its "text" value will be concatenated to the prompt.
            - If the element is a dictionary with a "type" key equal to "image_url", its "image_url" value will be added to the list of images.

    Returns:
        tuple: A tuple containing the prompt (a string) and the processed images (a list of objects representing the images).
    """

    try:
        # given messages for gpt-4 vision, convert them for gemini
        # https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/getting-started/intro_gemini_python.ipynb
        prompt = ""
        images = []
        for message in messages:
            if isinstance(message["content"], str):
                prompt += message["content"]
            elif isinstance(message["content"], list):
                # see https://docs.litellm.ai/docs/providers/openai#openai-vision-models
                for element in message["content"]:
                    if isinstance(element, dict):
                        if element["type"] == "text":
                            prompt += element["text"]
                        elif element["type"] == "image_url":
                            image_url = element["image_url"]["url"]
                            images.append(image_url)
        # processing images passed to gemini
        processed_images = []
        for img in images:
            if "https:/" in img:
                # Case 1: Image from URL
                image = _load_image_from_url(img)
                processed_images.append(image)

            else:
                try:
                    from PIL import Image
                except:
                    raise Exception(
                        "gemini image conversion failed please run `pip install Pillow`"
                    )

                if "base64" in img:
                    # Case 2: Base64 image data
                    import base64
                    import io

                    # Extract the base64 image data
                    base64_data = img.split("base64,")[1]

                    # Decode the base64 image data
                    image_data = base64.b64decode(base64_data)

                    # Load the image from the decoded data
                    image = Image.open(io.BytesIO(image_data))
                else:
                    # Case 3: Image filepath (e.g. temp.jpeg) given
                    image = Image.open(img)
                processed_images.append(image)
        content = [prompt] + processed_images
        return content
    except Exception as e:
        raise e


def gemini_text_image_pt(messages: list):
    """
    {
        "contents":[
            {
            "parts":[
                {"text": "What is this picture?"},
                {
                "inline_data": {
                    "mime_type":"image/jpeg",
                    "data": "'$(base64 -w0 image.jpg)'"
                }
                }
            ]
            }
        ]
    }
    """
    try:
        import google.generativeai as genai  # type: ignore
    except:
        raise Exception(
            "Importing google.generativeai failed, please run 'pip install -q google-generativeai"
        )

    prompt = ""
    images = []
    for message in messages:
        if isinstance(message["content"], str):
            prompt += message["content"]
        elif isinstance(message["content"], list):
            # see https://docs.litellm.ai/docs/providers/openai#openai-vision-models
            for element in message["content"]:
                if isinstance(element, dict):
                    if element["type"] == "text":
                        prompt += element["text"]
                    elif element["type"] == "image_url":
                        image_url = element["image_url"]["url"]
                        images.append(image_url)

    content = [prompt] + images
    return content


def azure_text_pt(messages: list):
    prompt = ""
    for message in messages:
        if isinstance(message["content"], str):
            prompt += message["content"]
        elif isinstance(message["content"], list):
            # see https://docs.litellm.ai/docs/providers/openai#openai-vision-models
            for element in message["content"]:
                if isinstance(element, dict):
                    if element["type"] == "text":
                        prompt += element["text"]
    return prompt


###### AMAZON BEDROCK #######

from litellm.types.llms.bedrock import (
    ToolResultContentBlock as BedrockToolResultContentBlock,
    ToolResultBlock as BedrockToolResultBlock,
    ToolConfigBlock as BedrockToolConfigBlock,
    ToolUseBlock as BedrockToolUseBlock,
    ImageSourceBlock as BedrockImageSourceBlock,
    ImageBlock as BedrockImageBlock,
    ContentBlock as BedrockContentBlock,
    ToolInputSchemaBlock as BedrockToolInputSchemaBlock,
    ToolSpecBlock as BedrockToolSpecBlock,
    ToolBlock as BedrockToolBlock,
    ToolChoiceValuesBlock as BedrockToolChoiceValuesBlock,
)


def get_image_details(image_url) -> Tuple[str, str]:
    try:
        import base64

        # Send a GET request to the image URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Check the response's content type to ensure it is an image
        content_type = response.headers.get("content-type")
        if not content_type or "image" not in content_type:
            raise ValueError(
                f"URL does not point to a valid image (content-type: {content_type})"
            )

        # Convert the image content to base64 bytes
        base64_bytes = base64.b64encode(response.content).decode("utf-8")

        # Get mime-type
        mime_type = content_type.split("/")[
            1
        ]  # Extract mime-type from content-type header

        return base64_bytes, mime_type

    except requests.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except Exception as e:
        raise e


def _process_bedrock_converse_image_block(image_url: str) -> BedrockImageBlock:
    if "base64" in image_url:
        # Case 1: Images with base64 encoding
        import base64, re

        # base 64 is passed as data:image/jpeg;base64,<base-64-encoded-image>
        image_metadata, img_without_base_64 = image_url.split(",")

        # read mime_type from img_without_base_64=data:image/jpeg;base64
        # Extract MIME type using regular expression
        mime_type_match = re.match(r"data:(.*?);base64", image_metadata)
        if mime_type_match:
            mime_type = mime_type_match.group(1)
            image_format = mime_type.split("/")[1]
        else:
            mime_type = "image/jpeg"
            image_format = "jpeg"
        _blob = BedrockImageSourceBlock(bytes=img_without_base_64)
        supported_image_formats = (
            litellm.AmazonConverseConfig().get_supported_image_types()
        )
        if image_format in supported_image_formats:
            return BedrockImageBlock(source=_blob, format=image_format)  # type: ignore
        else:
            # Handle the case when the image format is not supported
            raise ValueError(
                "Unsupported image format: {}. Supported formats: {}".format(
                    image_format, supported_image_formats
                )
            )
    elif "https:/" in image_url:
        # Case 2: Images with direct links
        image_bytes, image_format = get_image_details(image_url)
        _blob = BedrockImageSourceBlock(bytes=image_bytes)
        supported_image_formats = (
            litellm.AmazonConverseConfig().get_supported_image_types()
        )
        if image_format in supported_image_formats:
            return BedrockImageBlock(source=_blob, format=image_format)  # type: ignore
        else:
            # Handle the case when the image format is not supported
            raise ValueError(
                "Unsupported image format: {}. Supported formats: {}".format(
                    image_format, supported_image_formats
                )
            )
    else:
        raise ValueError(
            "Unsupported image type. Expected either image url or base64 encoded string - \
                e.g. 'data:image/jpeg;base64,<base64-encoded-string>'"
        )


def _convert_to_bedrock_tool_call_invoke(
    tool_calls: list,
) -> List[BedrockContentBlock]:
    """
    OpenAI tool invokes:
    {
      "role": "assistant",
      "content": null,
      "tool_calls": [
        {
          "id": "call_abc123",
          "type": "function",
          "function": {
            "name": "get_current_weather",
            "arguments": "{\n\"location\": \"Boston, MA\"\n}"
          }
        }
      ]
    },
    """
    """
    Bedrock tool invokes: 
    [   
        {
            "role": "assistant",
            "toolUse": {
                "input": {"location": "Boston, MA", ..},
                "name": "get_current_weather",
                "toolUseId": "call_abc123"
            }
        }
    ]
    """
    """
    - json.loads argument
    - extract name 
    - extract id
    """

    try:
        _parts_list: List[BedrockContentBlock] = []
        for tool in tool_calls:
            if "function" in tool:
                id = tool["id"]
                name = tool["function"].get("name", "")
                arguments = tool["function"].get("arguments", "")
                arguments_dict = json.loads(arguments)
                bedrock_tool = BedrockToolUseBlock(
                    input=arguments_dict, name=name, toolUseId=id
                )
                bedrock_content_block = BedrockContentBlock(toolUse=bedrock_tool)
                _parts_list.append(bedrock_content_block)
        return _parts_list
    except Exception as e:
        raise Exception(
            "Unable to convert openai tool calls={} to bedrock tool calls. Received error={}".format(
                tool_calls, str(e)
            )
        )


def _convert_to_bedrock_tool_call_result(
    message: dict,
) -> BedrockMessageBlock:
    """
    OpenAI message with a tool result looks like:
    {
        "tool_call_id": "tool_1",
        "role": "tool",
        "name": "get_current_weather",
        "content": "function result goes here",
    },

    OpenAI message with a function call result looks like:
    {
        "role": "function",
        "name": "get_current_weather",
        "content": "function result goes here",
    }
    """
    """
    Bedrock result looks like this: 
    {
        "role": "user",
        "content": [
            {
                "toolResult": {
                    "toolUseId": "tooluse_kZJMlvQmRJ6eAyJE5GIl7Q",
                    "content": [
                        {
                            "json": {
                                "song": "Elemental Hotel",
                                "artist": "8 Storey Hike"
                            }
                        }
                    ]
                }
            }
        ]
    }
    """
    """
    - 
    """
    content = message.get("content", "")
    name = message.get("name", "")
    id = message.get("tool_call_id", str(uuid.uuid4()))

    tool_result_content_block = BedrockToolResultContentBlock(text=content)
    tool_result = BedrockToolResultBlock(
        content=[tool_result_content_block],
        toolUseId=id,
    )
    content_block = BedrockContentBlock(toolResult=tool_result)

    return BedrockMessageBlock(role="user", content=[content_block])


def _bedrock_converse_messages_pt(messages: List) -> List[BedrockMessageBlock]:
    """
    Converts given messages from OpenAI format to Bedrock format

    - Roles must alternate b/w 'user' and 'model' (same as anthropic -> merge consecutive roles)
    - Please ensure that function response turn comes immediately after a function call turn
    """

    contents: List[BedrockMessageBlock] = []
    msg_i = 0
    while msg_i < len(messages):
        user_content: List[BedrockContentBlock] = []
        init_msg_i = msg_i
        ## MERGE CONSECUTIVE USER CONTENT ##
        while msg_i < len(messages) and messages[msg_i]["role"] == "user":
            if isinstance(messages[msg_i]["content"], list):
                _parts: List[BedrockContentBlock] = []
                for element in messages[msg_i]["content"]:
                    if isinstance(element, dict):
                        if element["type"] == "text":
                            _part = BedrockContentBlock(text=element["text"])
                            _parts.append(_part)
                        elif element["type"] == "image_url":
                            image_url = element["image_url"]["url"]
                            _part = _process_bedrock_converse_image_block(  # type: ignore
                                image_url=image_url
                            )
                            _parts.append(BedrockContentBlock(image=_part))  # type: ignore
                user_content.extend(_parts)
            else:
                _part = BedrockContentBlock(text=messages[msg_i]["content"])
                user_content.append(_part)

            msg_i += 1

        if user_content:
            contents.append(BedrockMessageBlock(role="user", content=user_content))
        assistant_content: List[BedrockContentBlock] = []
        ## MERGE CONSECUTIVE ASSISTANT CONTENT ##
        while msg_i < len(messages) and messages[msg_i]["role"] == "assistant":
            if isinstance(messages[msg_i]["content"], list):
                assistants_parts: List[BedrockContentBlock] = []
                for element in messages[msg_i]["content"]:
                    if isinstance(element, dict):
                        if element["type"] == "text":
                            assistants_part = BedrockContentBlock(text=element["text"])
                            assistants_parts.append(assistants_part)
                        elif element["type"] == "image_url":
                            image_url = element["image_url"]["url"]
                            assistants_part = _process_bedrock_converse_image_block(  # type: ignore
                                image_url=image_url
                            )
                            assistants_parts.append(
                                BedrockContentBlock(image=assistants_part)  # type: ignore
                            )
                assistant_content.extend(assistants_parts)
            elif messages[msg_i].get(
                "tool_calls", []
            ):  # support assistant tool invoke convertion
                assistant_content.extend(
                    _convert_to_bedrock_tool_call_invoke(messages[msg_i]["tool_calls"])
                )
            else:
                assistant_text = (
                    messages[msg_i].get("content") or ""
                )  # either string or none
                if assistant_text:
                    assistant_content.append(BedrockContentBlock(text=assistant_text))

            msg_i += 1

        if assistant_content:
            contents.append(
                BedrockMessageBlock(role="assistant", content=assistant_content)
            )

        ## APPEND TOOL CALL MESSAGES ##
        if msg_i < len(messages) and messages[msg_i]["role"] == "tool":
            tool_call_result = _convert_to_bedrock_tool_call_result(messages[msg_i])
            contents.append(tool_call_result)
            msg_i += 1
        if msg_i == init_msg_i:  # prevent infinite loops
            raise Exception(
                "Invalid Message passed in - {}. File an issue https://github.com/BerriAI/litellm/issues".format(
                    messages[msg_i]
                )
            )

    return contents


def _bedrock_tools_pt(tools: List) -> List[BedrockToolBlock]:
    """
    OpenAI tools looks like:
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            }
        }
    ]
    """
    """
    Bedrock toolConfig looks like: 
    "tools": [
        {
            "toolSpec": {
                "name": "top_song",
                "description": "Get the most popular song played on a radio station.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "sign": {
                                "type": "string",
                                "description": "The call sign for the radio station for which you want the most popular song. Example calls signs are WZPZ, and WKRP."
                            }
                        },
                        "required": [
                            "sign"
                        ]
                    }
                }
            }
        }
    ]
    """
    tool_block_list: List[BedrockToolBlock] = []
    for tool in tools:
        parameters = tool.get("function", {}).get("parameters", None)
        name = tool.get("function", {}).get("name", "")
        description = tool.get("function", {}).get("description", "")
        tool_input_schema = BedrockToolInputSchemaBlock(json=parameters)
        tool_spec = BedrockToolSpecBlock(
            inputSchema=tool_input_schema, name=name, description=description
        )
        tool_block = BedrockToolBlock(toolSpec=tool_spec)
        tool_block_list.append(tool_block)

    return tool_block_list


# Function call template
def function_call_prompt(messages: list, functions: list):
    function_prompt = """Produce JSON OUTPUT ONLY! Adhere to this format {"name": "function_name", "arguments":{"argument_name": "argument_value"}} The following functions are available to you:"""
    for function in functions:
        function_prompt += f"""\n{function}\n"""

    function_added_to_prompt = False
    for message in messages:
        if "system" in message["role"]:
            message["content"] += f""" {function_prompt}"""
            function_added_to_prompt = True

    if function_added_to_prompt == False:
        messages.append({"role": "system", "content": f"""{function_prompt}"""})

    return messages


# Custom prompt template
def custom_prompt(
    role_dict: dict,
    messages: list,
    initial_prompt_value: str = "",
    final_prompt_value: str = "",
    bos_token: str = "",
    eos_token: str = "",
):
    prompt = bos_token + initial_prompt_value
    bos_open = True
    ## a bos token is at the start of a system / human message
    ## an eos token is at the end of the assistant response to the message
    for message in messages:
        role = message["role"]

        if role in ["system", "human"] and not bos_open:
            prompt += bos_token
            bos_open = True

        pre_message_str = (
            role_dict[role]["pre_message"]
            if role in role_dict and "pre_message" in role_dict[role]
            else ""
        )
        post_message_str = (
            role_dict[role]["post_message"]
            if role in role_dict and "post_message" in role_dict[role]
            else ""
        )
        prompt += pre_message_str + message["content"] + post_message_str

        if role == "assistant":
            prompt += eos_token
            bos_open = False

    prompt += final_prompt_value
    return prompt


def prompt_factory(
    model: str,
    messages: list,
    custom_llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
):
    original_model_name = model
    model = model.lower()
    if custom_llm_provider == "ollama":
        return ollama_pt(model=model, messages=messages)
    elif custom_llm_provider == "anthropic":
        if model == "claude-instant-1" or model == "claude-2":
            return anthropic_pt(messages=messages)
        return anthropic_messages_pt(messages=messages)
    elif custom_llm_provider == "anthropic_xml":
        return anthropic_messages_pt_xml(messages=messages)
    elif custom_llm_provider == "together_ai":
        prompt_format, chat_template = get_model_info(token=api_key, model=model)
        return format_prompt_togetherai(
            messages=messages, prompt_format=prompt_format, chat_template=chat_template
        )
    elif custom_llm_provider == "gemini":
        if (
            model == "gemini-pro-vision"
            or litellm.supports_vision(model=model)
            or litellm.supports_vision(model=custom_llm_provider + "/" + model)
        ):
            return _gemini_vision_convert_messages(messages=messages)
        else:
            return gemini_text_image_pt(messages=messages)
    elif custom_llm_provider == "mistral":
        return mistral_api_pt(messages=messages)
    elif custom_llm_provider == "bedrock":
        if "amazon.titan-text" in model:
            return amazon_titan_pt(messages=messages)
        elif "anthropic." in model:
            if any(_ in model for _ in ["claude-2.1", "claude-v2:1"]):
                return claude_2_1_pt(messages=messages)
            else:
                return anthropic_pt(messages=messages)
        elif "mistral." in model:
            return mistral_instruct_pt(messages=messages)
        elif "llama2" in model and "chat" in model:
            return llama_2_chat_pt(messages=messages)
        elif "llama3" in model and "instruct" in model:
            return hf_chat_template(
                model="meta-llama/Meta-Llama-3-8B-Instruct",
                messages=messages,
            )

    elif custom_llm_provider == "clarifai":
        if "claude" in model:
            return anthropic_pt(messages=messages)

    elif custom_llm_provider == "perplexity":
        for message in messages:
            message.pop("name", None)
        return messages
    elif custom_llm_provider == "azure_text":
        return azure_text_pt(messages=messages)
    elif custom_llm_provider == "watsonx":
        if "granite" in model and "chat" in model:
            # granite-13b-chat-v1 and granite-13b-chat-v2 use a specific prompt template
            return ibm_granite_pt(messages=messages)
        elif "ibm-mistral" in model and "instruct" in model:
            # models like ibm-mistral/mixtral-8x7b-instruct-v01-q use the mistral instruct prompt template
            return mistral_instruct_pt(messages=messages)
        elif "meta-llama/llama-3" in model and "instruct" in model:
            # https://llama.meta.com/docs/model-cards-and-prompt-formats/meta-llama-3/
            return custom_prompt(
                role_dict={
                    "system": {
                        "pre_message": "<|start_header_id|>system<|end_header_id|>\n",
                        "post_message": "<|eot_id|>",
                    },
                    "user": {
                        "pre_message": "<|start_header_id|>user<|end_header_id|>\n",
                        "post_message": "<|eot_id|>",
                    },
                    "assistant": {
                        "pre_message": "<|start_header_id|>assistant<|end_header_id|>\n",
                        "post_message": "<|eot_id|>",
                    },
                },
                messages=messages,
                initial_prompt_value="<|begin_of_text|>",
                final_prompt_value="<|start_header_id|>assistant<|end_header_id|>\n",
            )
    try:
        if "meta-llama/llama-2" in model and "chat" in model:
            return llama_2_chat_pt(messages=messages)
        elif (
            "meta-llama/llama-3" in model or "meta-llama-3" in model
        ) and "instruct" in model:
            return hf_chat_template(
                model="meta-llama/Meta-Llama-3-8B-Instruct",
                messages=messages,
            )
        elif (
            "tiiuae/falcon" in model
        ):  # Note: for the instruct models, it's best to use a User: .., Assistant:.. approach in your prompt template.
            if model == "tiiuae/falcon-180B-chat":
                return falcon_chat_pt(messages=messages)
            elif "instruct" in model:
                return falcon_instruct_pt(messages=messages)
        elif "mosaicml/mpt" in model:
            if "chat" in model:
                return mpt_chat_pt(messages=messages)
        elif "codellama/codellama" in model or "togethercomputer/codellama" in model:
            if "instruct" in model:
                return llama_2_chat_pt(
                    messages=messages
                )  # https://huggingface.co/blog/codellama#conversational-instructions
        elif "wizardlm/wizardcoder" in model:
            return wizardcoder_pt(messages=messages)
        elif "phind/phind-codellama" in model:
            return phind_codellama_pt(messages=messages)
        elif "togethercomputer/llama-2" in model and (
            "instruct" in model or "chat" in model
        ):
            return llama_2_chat_pt(messages=messages)
        elif model in [
            "gryphe/mythomax-l2-13b",
            "gryphe/mythomix-l2-13b",
            "gryphe/mythologic-l2-13b",
        ]:
            return alpaca_pt(messages=messages)
        elif model.strip() == "meta-llama/llamaguard-7b":
            chat_template = "{% if messages|length % 2 == 0 %}{% set role = 'Agent' %}{% else %}{% set role = 'User' %}{% endif %}{{ \"[INST] Task: Check if there is unsafe content in '\" + role + \"' messages in conversations according our safety policy with the below categories.\n\n<BEGIN UNSAFE CONTENT CATEGORIES>\nO1: Violence and Hate. \nShould not\n- Help people plan or engage in violence.\n- Encourage people to engage in violence.\n- Express hateful, derogatory, or demeaning sentiments against people based on sensitive personal characteristics like their race, color, religion, national origin, sexual orientation, gender, gender identity, or disability.\n- Encourage discrimination against people based on those characteristics and should not use slurs or create insults based on those characteristics.\nCan\n- Provide information on violence and discrimination.\n- Discuss the topics of hate and violence, and can discuss historical events involving violence.\nO2: Sexual Content.\nShould not\n- Engage in sexually explicit (i.e., erotic) conversations and should not encourage people to engage in sexual activities.\nCan\n- Discuss topics related to sexuality and sexual education.\n- Provide general information regarding sexual activities.\n- Provide guidance on topics related to sexual health.\nO3: Criminal Planning.\nShould not\n- Help people plan or engage in criminal activities like theft, kidnapping, or financial crimes, especially when the person indicates that they may act on the information provided to them.\n- Encourage people to engage in criminal activities or condone criminal behavior.\nCan\n- Help people understand how crimes are committed, provided that the response is not so detailed that it could be used to provide a roadmap for future crimes.\n- Help people understand how systems work that are used to prevent crimes, provided those descriptions do not provide detailed information on how to defeat those systems.\nO4: Guns and Illegal Weapons.\nShould not\n- Assist in the planning or execution of firearm or illegal weapons crimes, especially when the person indicates that they may act on the information provided to them.\n- Encourage people to engage in firearm or illegal weapons crimes or condone such behavior.\nCan\n- Discuss firearms and the arguments for and against firearm ownership.\nO5: Regulated or Controlled Substances.\nShould not\n- Encourage or assist people in the trafficking, consumption, or use of regulated or controlled substances, including but not limited to illegal drugs, tobacco, alcohol, and cannabis.\n- Assist or encourage people to create such substances when it is illegal to do so.\nCan\n- Discuss the use of regulated or controlled substances, and can provide general information on those substances (ex: what their chemical composition is and what their effects are).\n- Provide information on how those substances are manufactured, provided that the information is not so detailed as to provide step-by-step instructions for their creation.\nO6: Self-Harm.\nShould not\n- Encourage people to harm themselves.\n- Romanticize or condone self-harm or suicide.\n- Provide information regarding the methods of suicide or self-harm.\n- Provide any information or advice, other than information regarding appropriate health resources, to people who express or imply that they wish to harm themselves.\nCan\n- Provide general information regarding self-harm and suicide (ex: statistics, the mental health challenges faced by those who take these actions).\nShould\n- Provide information regarding appropriate health resources to people who imply or express the desire to harm themselves.\n<END UNSAFE CONTENT CATEGORIES>\n\n<BEGIN CONVERSATION>\n\n\" }}{% for message in messages %}{% if (message['role'] == 'user') != (loop.index0 % 2 == 0) %}{{ raise_exception('Conversation roles must alternate user/assistant/user/assistant/...') }}{% endif %}{% set content = message['content'] %}{% if message['role'] == 'user' %}{% set role = 'User' %}{% elif message['role'] == 'assistant' %}{% set role = 'Agent' %}{% endif %}{{ role + ': ' + content.strip() + '\n\n' }}{% endfor %}{{ \"<END CONVERSATION>\n\nProvide your safety assessment for \" + role + \" in the above conversation:\n- First line must read 'safe' or 'unsafe'.\n- If unsafe, a second line must include a comma-separated list of violated categories. [/INST]\" }}"
            return hf_chat_template(
                model=model, messages=messages, chat_template=chat_template
            )
        else:
            return hf_chat_template(original_model_name, messages)
    except Exception as e:
        return default_pt(
            messages=messages
        )  # default that covers Bloom, T-5, any non-chat tuned model (e.g. base Llama2)


def get_attribute_or_key(tool_or_function, attribute, default=None):
    if hasattr(tool_or_function, attribute):
        return getattr(tool_or_function, attribute)
    return tool_or_function.get(attribute, default)
