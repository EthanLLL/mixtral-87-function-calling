import json
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

api_key = 'Use your api key.'
# model = "mistral-tiny" # mistral 7b might need finetune. 🙂
model = "mistral-small" # 8*7b works like charm

client = MistralClient(api_key=api_key)

system_prompt = '''
You have access to the following tools:
[
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city or state which is required."
                },
                "unit": {
                    "type": "string",
                    "enum": [
                        "celsius",
                        "fahrenheit"
                    ]
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "get_current_location",
        "description": "Use this tool to get the current location if user does not provide a location",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]
Select one of the above tools if needed and if tool needed, respond with only a JSON object matching the following schema.:
{
    "result": "tool_use",
    "tool": <name of the selected tool, leave blank if no tools needed>,
    "tool_input": <parameters for the selected tool, matching the tool\'s JSON schema, leave blank if no tools needed>,
    "explanation": <The explanation why you choosed this tool or no need for further tools.>
}
If no further tools needed, response with only a JSON object matching the following schema:
{
    "result": "stop",
    "content": <Your response to the user.>,
    "explanation": <The explanation why you get the final answer.>
}
'''
prompt = 'What is the current weather?'

messages = [
    ChatMessage(role="system", content=system_prompt),
    ChatMessage(role="user", content=prompt),
    # ChatMessage(role='assistant', content='Should use get_current_location tool with args: {}'),
    # ChatMessage(role="user", content='I have used the get_current_location and the result is: Guangzhou. What next?'),
    # ChatMessage(role='assistant', content='Should use get_current_weather tool with args: {"location": "Guangzhou", "unit": "celsius"}'),
    # ChatMessage(role="user", content='I have used the get_current_weather tool and the result is: Rainy 7 degrees. What next?'),
]

# No streaming
chat_response = client.chat(
    model=model,
    messages=messages,
)

content = chat_response.choices[0].message.content
print(content)
res = json.loads(content)
# {
#     "tool": "get_current_location",
#     "tool_input": {},
#     "explanation": "I will use the 'get_current_location' tool to determine the user's current location, as they did not provide a specific location in their request. After obtaining the user's location, I will then use the 'get_current_weather' tool to provide the current weather for their location."
# }
