import json
from openai.types.chat import (
    ChatCompletionMessage,
    ChatCompletionMessageToolCall,
    ChatCompletion,
)
from openai.types.chat.chat_completion_message_tool_call import Function
from openai.types.chat.chat_completion_chunk import (
    ChatCompletionChunk,
    ChoiceDeltaToolCall,
    ChoiceDelta,
    ChoiceDeltaToolCallFunction,
    Choice as Choice_Chunk,
)
from openai.types.completion_usage import CompletionUsage
from openai.types.chat.chat_completion import Choice
from openai import OpenAI, AsyncOpenAI
import uuid
from typing import List, Dict, Any, Union, Tuple
import re
import time
from jinja2 import Environment, FileSystemLoader

def process_messages(messages, add_generation_prompt=True, bos_token="<|begin_of_text|>"):
    """
    Applies the Jinja template to an array of messages.

    Args:
        messages (list): A list of dictionaries, each representing a message with
                         'role' and 'content' keys.
        add_generation_prompt (bool): Whether to add an "assistant" header for
                                    generation. Defaults to False.
        bos_token (str): The beginning of stream token to prepend to the first
                         message. Defaults to "<|begin_of_text|>".

    Returns:
        str: The rendered Jinja template with the processed messages.
    """

    # Create a Jinja environment for template rendering
    env = Environment(loader=FileSystemLoader('.'))

    # Define the Jinja template string
    template = """{% set loop_messages = messages %}{% for message in loop_messages %}{% set content = '<|start_header_id|>' + message['role'] + '<|end_header_id|>\n\n'+ message['content'] | trim + '<|eot_id|>' %}{% if loop.index0 == 0 %}{% set content = bos_token + content %}{% endif %}{{ content }}{% endfor %}{% if add_generation_prompt %}{{ '<|start_header_id|>assistant<|end_header_id|>\n\n' }}{% endif %}"""

    # Render the template with the provided messages
    return env.from_string(template).render(messages=messages,
                                          add_generation_prompt=add_generation_prompt,
                                          bos_token=bos_token)


TOOL_SYSTEM_PROMPT = (
    "You have access to the following tools:\n{tool_text}"
    "Use the following format if using a tool:\n"
    "```\n"
    "Action: tool name (one of [{tool_names}]).\n"
    "Action Input: the input to the tool, in a JSON format representing the kwargs (e.g. ```{example_input}```)\n"
    "```\n"
)


def generate_json_format_example(
    tool_parameters: Dict[str, Any], examples: List[Dict[str, Any]]
) -> str:
    example_input = '{"input": "hello world", "num_beams": 5}'  # Default example input
    if examples:
        # Use the first example as the example input
        example_input = json.dumps(examples[0])
    else:
        example_kwargs = {}
        for name, param in tool_parameters.items():
            example_value = "example_value"
            if param.get("type") == "integer":
                example_value = 1
            elif param.get("type") == "boolean":
                example_value = True
            example_kwargs[name] = example_value
        example_input = json.dumps(example_kwargs)
    return example_input


def default_tool_formatter(tools: List[Dict[str, Any]]) -> str:
    tool_text = ""
    tool_names = []
    example_inputs = []
    for tool in tools:
        param_text = ""
        parameters = tool["function"]["parameters"]
        for name, param in parameters.get("properties", {}).items():
            required = ", required" if name in parameters.get("required", []) else ""
            enum = (
                ", should be one of [{}]".format(", ".join(param["enum"]))
                if param.get("enum", None)
                else ""
            )
            items = (
                ", where each item should be {}".format(param["items"].get("type", ""))
                if param.get("items")
                else ""
            )
            param_text += "  - {name} ({type}{required}): {desc}{enum}{items}\n".format(
                name=name,
                type=param.get("type", ""),
                required=required,
                desc=param.get("description", ""),
                enum=enum,
                items=items,
            )

        tool_text += "> Tool Name: {name}\nTool Description: {desc}\nTool Args:\n{args}\n".format(
            name=tool["function"]["name"],
            desc=tool["function"].get("description", ""),
            args=param_text,
        )
        tool_names.append(tool["function"]["name"])
        example_inputs.append(
            generate_json_format_example(parameters.get("properties", {}), [])
        )

    if not tool_text:
        return "No tools available."
    example_input_text = " or ".join(example_inputs)

    return TOOL_SYSTEM_PROMPT.format(
        tool_text=tool_text,
        tool_names=", ".join(tool_names),
        example_input='{"input": "hello world", "num_beams": 5}',
    )


def default_tool_extractor(content: str) -> Union[str, Tuple[str, str]]:
    regex = re.compile(r"Action:\s*([a-zA-Z0-9_]+).*?Action Input:\s*(.*)", re.DOTALL)
    action_match = re.search(regex, content)
    if not action_match:
        return content

    tool_name = action_match.group(1).strip()
    tool_input = action_match.group(2).strip().strip('"').strip("```")
    try:
        arguments = json.loads(tool_input)
    except json.JSONDecodeError:
        return content
    return tool_name, json.dumps(arguments, ensure_ascii=False)


class CustomOpenAIClient(OpenAI):

    def __init__(self, client):
        super().__init__(api_key=client.api_key)
        self.client = client

        if isinstance(client, OpenAI):
            self.chat.completions.create = self.chat_completion

        if isinstance(client, AsyncOpenAI):
            self.chat.completions.create = self.chat_completion_async

    async def format_async_chunks(self, response, model: str):
        is_tool = False
        function_name: str = ""
        is_tool_arg = False
        
        async for chunk in response:
            content = chunk.choices[0].delta.content
            if content == None:
                continue
            if content == "Action":
                is_tool = True
                continue
            if content == ":":
                continue
            if is_tool:
                function_name += content
            if content == "\n":
                is_tool = False
                function_name = function_name.strip()
                # yield in above format
                yield ChatCompletionChunk(
                    id=str(uuid.uuid4()),
                    choices=[
                        Choice_Chunk(
                            delta=ChoiceDelta(
                                content=None,
                                function_call=None,
                                role="assistant",
                                tool_calls=[
                                    ChoiceDeltaToolCall(
                                        index=0,
                                        id=str(uuid.uuid4()),
                                        function=ChoiceDeltaToolCallFunction(
                                            arguments="", name=function_name
                                        ),
                                        type="function",
                                    )
                                ],
                            ),
                            finish_reason=None,
                            index=0,
                            logprobs=None,
                            content_filter_results={},
                        )
                    ],
                    created=int(time.time()),
                    model=model,
                    object="chat.completion.chunk",
                    system_fingerprint=None,
                    usage=None,
                )

            if content and "{" in content:
                is_tool_arg = True

            if is_tool_arg:
                yield ChatCompletionChunk(
                    id=str(uuid.uuid4()),
                    choices=[
                        Choice_Chunk(
                            delta=ChoiceDelta(
                                content=None,
                                function_call=None,
                                role="assistant",
                                tool_calls=[
                                    ChoiceDeltaToolCall(
                                        index=0,
                                        id=str(uuid.uuid4()),
                                        function=ChoiceDeltaToolCallFunction(
                                            arguments=content, name=None
                                        ),
                                        type="function",
                                    )
                                ],
                            ),
                            finish_reason=None,
                            index=0,
                            logprobs=None,
                            content_filter_results={},
                        )
                    ],
                    created=int(time.time()),
                    model=model,
                    object="chat.completion.chunk",
                    system_fingerprint=None,
                    usage=None,
                )

            if content and "}" in content:
                is_tool_arg = False

    def format_chunks(self, response, model):
        is_tool = False
        function_name = ""
        is_tool_arg = False
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content == None:
                continue
            if content == "Action":
                is_tool = True
                continue
            if content == ":":
                continue
            if is_tool:
                function_name += content
            if content == "\n":
                is_tool = False
                function_name = function_name.strip()
                # yield in above format
                yield ChatCompletionChunk(
                    id=str(uuid.uuid4()),
                    choices=[
                        Choice_Chunk(
                            delta=ChoiceDelta(
                                content=None,
                                function_call=None,
                                role="assistant",
                                tool_calls=[
                                    ChoiceDeltaToolCall(
                                        index=0,
                                        id=str(uuid.uuid4()),
                                        function=ChoiceDeltaToolCallFunction(
                                            arguments="", name=function_name
                                        ),
                                        type="function",
                                    )
                                ],
                            ),
                            finish_reason=None,
                            index=0,
                            logprobs=None,
                            content_filter_results={},
                        )
                    ],
                    created=int(time.time()),
                    model=model,
                    object="chat.completion.chunk",
                    system_fingerprint=None,
                    usage=None,
                )

            if content and "{" in content:

                is_tool_arg = True

            if is_tool_arg:
                yield ChatCompletionChunk(
                    id=str(uuid.uuid4()),
                    choices=[
                        Choice_Chunk(
                            delta=ChoiceDelta(
                                content=None,
                                function_call=None,
                                role="assistant",
                                tool_calls=[
                                    ChoiceDeltaToolCall(
                                        index=0,
                                        id=str(uuid.uuid4()),
                                        function=ChoiceDeltaToolCallFunction(
                                            arguments=content, name=None
                                        ),
                                        type="function",
                                    )
                                ],
                            ),
                            finish_reason=None,
                            index=0,
                            logprobs=None,
                            content_filter_results={},
                        )
                    ],
                    created=int(time.time()),
                    model=model,
                    object="chat.completion.chunk",
                    system_fingerprint=None,
                    usage=None,
                )

            if content and "}" in content:
                is_tool_arg = False

    async def chat_completion_async(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]] = [],
        tool_choice: Union[str, Dict[str, Any]] = "auto",
        *args,
        **kwargs,
    ):

        system_message = next(
            (msg for msg in messages if msg.get("role") == "system"), None
        )

        system_prompt = (
            system_message["content"]
            if system_message
            else "You are a helpful assistant. You have access to the following tools:\n"
        )

        system_prompt += default_tool_formatter(tools)

        messages = [{"role": "system", "content": system_prompt}] + messages

        if tool_choice != "auto" and tool_choice["type"] == "function":
            function = tool_choice["function"]
            if messages[-1]["role"] == "user":
                messages[-1]["content"] += f",  utilize the tool {function['name']} \n"

        transformed_messages = []
        for msg in messages:
            if msg.get("role") == "tool":

                msg["content"] = str({"response": msg["content"]})
                transformed_messages.append(msg)
            elif msg.get("role") == "assistant" and isinstance(
                msg.get("content"), Function
            ):
                function_content = msg["content"]
                transformed_messages.append(
                    {
                        "role": "assistant",
                        "content": f"Action: {function_content.name}\nAction Input: {function_content.arguments}",
                    }
                )

            elif msg.get("role") == "assistant" and not msg.get("content"):
                tool = msg['tool_calls'][0]
                function_content = tool['function']
                transformed_messages.append(
                    {
                        "role": "assistant",
                        "content": f"Action: {function_content['name']}\nAction Input: {function_content['arguments']}",
                    }
                )

            elif msg.get("role") == "assistant" and isinstance(
                msg.get("content"), ChatCompletionMessage
            ):
                content = msg.get("content")
                if not content.content:
                    tool = content.tool_calls[0]
                    function_content = tool.function
                    transformed_messages.append(
                        {
                            "role": "assistant",
                            "content": f"Action: {function_content.name}\nAction Input: {function_content.arguments}",
                        }
                    )
                else:
                    transformed_messages.append(
                        {
                            "role": "assistant",
                            "content": content.content,
                        }
                    )
            else:
                transformed_messages.append(msg)

        is_fireworks = False
        if kwargs.get('is_fireworks',False):
            if kwargs.get('stream'):
                raise Exception("Client does not support stream for fireworks")
            prompt = process_messages(transformed_messages)
            kwargs.pop('is_fireworks')
            is_fireworks=True
            response = await self.client.completions.create(model=model,prompt=prompt,*args, **kwargs)

        else:

            response = await self.client.chat.completions.create(
                model=model, messages=transformed_messages, *args, **kwargs
            )

        if kwargs.get("stream") and kwargs["stream"] is True:
            return self.format_async_chunks(response, model)

        if response.choices:
            if is_fireworks:
                choice = response.choices[0]
                extracted_info = default_tool_extractor(choice.text)
            else:
                choice = response.choices[0].message
                extracted_info = default_tool_extractor(choice.content)
            if isinstance(extracted_info, tuple):
                tool_name, tool_args = extracted_info
                tool_call = ChatCompletionMessageToolCall(
                    id=str(uuid.uuid4()),
                    function=Function(name=tool_name, arguments=tool_args),
                    type="function",
                )

                message = ChatCompletionMessage(
                    content=None, role="assistant", tool_calls=[tool_call]
                )
                return ChatCompletion(
                    id=str(uuid.uuid4()),
                    choices=[
                        Choice(
                            finish_reason="tool_calls",
                            index=0,
                            logprobs=None,
                            message=message,
                        )
                    ],
                    created=int(time.time()),
                    model=model,
                    object="chat.completion",
                    system_fingerprint=None,
                    usage=CompletionUsage(
                        completion_tokens=0,  # Assuming no tokens used for simplicity
                        prompt_tokens=0,  # Assuming no tokens used for simplicity
                        total_tokens=0,  # Assuming no tokens used for simplicity
                    ),
                )
            else:
                if is_fireworks:
                    finish_reason = choice.finish_reason

                    text=choice.text
                    return ChatCompletion(id=str(uuid.uuid4()),choices=[Choice(finish_reason=finish_reason,index=0,logprobs=None,message=ChatCompletionMessage(content=text,role="assistant"))],created=int(time.time()),model=model,object="chat.completion",system_fingerprint=None,usage=CompletionUsage(completion_tokens=0,prompt_tokens=0,total_tokens=0))
            
                return response
        return response

    def chat_completion(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]] = [],
        tool_choice: Union[str, Dict[str, Any]] = "auto",
        *args,
        **kwargs,
    ):
        

        system_message = next(
            (msg for msg in messages if msg.get("role") == "system"), None
        )

        system_prompt = (
            system_message["content"]
            if system_message
            else "You are a helpful assistant. You have access to the following tools:\n"
        )

        system_prompt += default_tool_formatter(tools)

        messages = [{"role": "system", "content": system_prompt}] + messages

        if tool_choice != "auto" and tool_choice["type"] == "function":
            function = tool_choice["function"]
            if messages[-1]["role"] == "user":
                messages[-1]["content"] += f",  utilize the tool {function['name']} \n"

        transformed_messages = []
        for msg in messages:
            if msg.get("role") == "tool":

                msg["content"] = str({"response": msg["content"]})
                transformed_messages.append(msg)
            elif msg.get("role") == "assistant" and isinstance(
                msg.get("content"), Function
            ):
                function_content = msg["content"]
                transformed_messages.append(
                    {
                        "role": "assistant",
                        "content": f"Action: {function_content.name}\nAction Input: {function_content.arguments}",
                    }
                )
            elif msg.get("role") == "assistant" and not msg.get("content"):
                tool = msg['tool_calls'][0]
                function_content = tool['function']
                transformed_messages.append(
                    {
                        "role": "assistant",
                        "content": f"Action: {function_content['name']}\nAction Input: {function_content['arguments']}",
                    }
                )
                
            elif msg.get("role") == "assistant" and isinstance(
                msg.get("content"), ChatCompletionMessage
            ):
                content = msg.get("content")
                if not content.content:
                    tool = content.tool_calls[0]
                    function_content = tool.function
                    transformed_messages.append(
                        {
                            "role": "assistant",
                            "content": f"Action: {function_content.name}\nAction Input: {function_content.arguments}",
                        }
                    )
                else:
                    transformed_messages.append(
                        {
                            "role": "assistant",
                            "content": content.content,
                        }
                    )
            else:
                transformed_messages.append(msg)
        is_fireworks = False
        if kwargs.get('is_fireworks',False):
            if kwargs.get('stream'):
                raise Exception("Client does not support stream for fireworks")
            prompt = process_messages(transformed_messages)
            kwargs.pop('is_fireworks')
            is_fireworks=True
            response = self.client.completions.create(model=model,prompt=prompt,*args, **kwargs)
        
        else:

            response = self.client.chat.completions.create(
                model=model, messages=transformed_messages, *args, **kwargs
            )

        if kwargs.get("stream") and kwargs["stream"] is True:
            return self.format_chunks(response, model)
        
        if response.choices:
            if is_fireworks:
                choice = response.choices[0]
                extracted_info = default_tool_extractor(choice.text)
            else:
                choice = response.choices[0].message
                extracted_info = default_tool_extractor(choice.content)
            if isinstance(extracted_info, tuple):
                tool_name, tool_args = extracted_info
                tool_call = ChatCompletionMessageToolCall(
                    id=str(uuid.uuid4()),
                    function=Function(name=tool_name, arguments=tool_args),
                    type="function",
                )

                message = ChatCompletionMessage(
                    content=None, role="assistant", tool_calls=[tool_call]
                )
                return ChatCompletion(
                    id=str(uuid.uuid4()),
                    choices=[
                        Choice(
                            finish_reason="tool_calls",
                            index=0,
                            logprobs=None,
                            message=message,
                        )
                    ],
                    created=int(time.time()),
                    model=model,
                    object="chat.completion",
                    system_fingerprint=None,
                    usage=CompletionUsage(
                        completion_tokens=0,  # Assuming no tokens used for simplicity
                        prompt_tokens=0,  # Assuming no tokens used for simplicity
                        total_tokens=0,  # Assuming no tokens used for simplicity
                    ),
                )

            else:
                if is_fireworks:
                    finish_reason = choice.finish_reason

                    text=choice.text
                    return ChatCompletion(id=str(uuid.uuid4()),choices=[Choice(finish_reason=finish_reason,index=0,logprobs=None,message=ChatCompletionMessage(content=text,role="assistant"))],created=int(time.time()),model=model,object="chat.completion",system_fingerprint=None,usage=CompletionUsage(completion_tokens=0,prompt_tokens=0,total_tokens=0))
                return response
