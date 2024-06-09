import json
import os
from openai import OpenAI
from fcoder import CoderClient,CoderExecResult
from typing import List
from typing import Dict
from PIL import Image
from io import BytesIO
import base64


# export OPENAI_API_KEY="sk-xxxx"
# export CODER_SERVER_AUTH_TOKEN="241b2687-e3f2-43b5-826b-cb91e8be6b08"
# docker run --rm -e TOKEN="241b2687-e3f2-43b5-826b-cb91e8be6b08" -p 8888:8888 fcoder-server:latest


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
coder_client = CoderClient(
    server_host="127.0.0.1",
    server_port=8888,
    auth_token=os.environ["CODER_SERVER_AUTH_TOKEN"]
)

def code_interpreter(code: str) -> CoderExecResult:
    """
    Code Interpreter is a code executor. Note that the execution environment of the code is Jupyter and the programming language is Python. Of course, you can also use the magic method % symbol supported by Jupyter and the ! symbol to execute system commands. % represents the line magic command. , such as %run is used to run external Python programs, the ! symbol is used to execute system commands, such as !ls is used to execute system commands, or !pip install requests means calling pip to update dependencies.

    Args:
        code: Python spec code or Linux command (pip3 only), This is the code to execute, do not include redundant comments

    Returns:
        CoderExecResult: Coder exec result

    """
    result = coder_client.code_interpreter(code)
    return result

history = []

coder_tool_schema = {
        "type": "function",
        "function": {
            "description": "Code Interpreter is a code executor. Note that the execution environment of the code is Jupyter and the programming language is Python. Of course, you can also use the magic method % symbol supported by Jupyter and the ! symbol to execute system commands. % represents the line magic command. , such as %run is used to run external Python programs, the ! symbol is used to execute system commands, such as !ls is used to execute system commands, or !pip install requests means calling pip to update dependencies.",
            "name": "code_interpreter",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python spec code or Linux command (pip3 only), This is the code to execute, do not include redundant comments"
                    }
                },
                "required": [
                    "code"
                ]
            },
            "annotation": "code_interpreter(code: str)"
        }
    }

def chat_with_openai(message: str,images: List[str] = None,model: str = "gpt-4o", tools: List[Dict] = None) -> str:
    """
    chat with openai

    Args:
        message: user input message
        images: base64 images
        model: choice openai model

    Returns:

    """

    images = images or []
    user_message = {
        "role": "user",
        "content": [
            {"type": "text", "text": f"{message}"},
        ]
    }


    for base64_image in images:
        user_message["content"].append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                },
            },
        )

    history.append(user_message)

    chat_completion = client.chat.completions.create(
        messages=history,
        model=model,
        tools=tools
    )
    assistant_message = chat_completion.choices[0].message

    tool_calls = assistant_message.tool_calls
    if tool_calls:
        tool_message = {
            "role": "user",
            "content": []
        }
        tool_call = tool_calls[0]
        arguments = tool_call.function.arguments
        function_name = tool_call.function.name
        print(f"tool> {function_name}({arguments})")
        history.append(
            {
                "role": "assistant",
                "content": [{"type": "text", "text": f"tool call: {function_name}({arguments})"}]
            }
        )
        if function_name == "code_interpreter":
            execute_result = code_interpreter(**json.loads(arguments))
            for item in execute_result.output:
                for mime_type,value in item.items():
                    if mime_type.startswith("text/"):
                        tool_message["content"].append(
                            {"type": "text", "text": f"Execute Result: \n{value}"},
                        )
                        print(f"exec result> {value}")
                    if mime_type.startswith("image/"):
                        tool_message["content"].append(
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{value}",
                                },
                            },
                        )
                        image_data = base64.b64decode(value)
                        image_io = BytesIO(image_data)
                        image = Image.open(image_io)
                        image.show()
            history.append(tool_message)

        continue_message = "Please analyze the execution results。"
        print(f"user> {continue_message}")
        return chat_with_openai(message=f"{continue_message}",tools=tools)
    if assistant_message.content:
        history.append({
            "role": f"{assistant_message.role}",
            "content": [
                {"type": "text", "text": f"{assistant_message.content}"},
            ]
        })

        return assistant_message.content


if __name__ == '__main__':
    while True:
        message = input("user> ")
        if message in ["quit","quit()","!quit","exit","exit()","!exit"]:
            exit(0)
        reply_result = chat_with_openai(message=message,tools=[coder_tool_schema])
        print(f"assistant> {reply_result}")

