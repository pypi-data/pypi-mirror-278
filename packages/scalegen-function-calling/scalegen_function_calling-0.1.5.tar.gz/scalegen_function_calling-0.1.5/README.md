# Function-Calling-OpenAI-SDK
This package enhances the OpenAI Python SDK, enabling it to seamlessly integrate with ScaleGenAI's Llama-3 function calling models. It allows developers to easily incorporate advanced AI functionalities into their applications.

## Getting Started

To use this package, you need to import `CustomOpenAIClient` from `scalegen_function_calling` and `OpenAI` from the `openai` package. Here's a quick example to get you started:

## Usage 

``` python
from  scalegen_function_calling import CustomOpenAIClient
from openai import OpenAI

tools = [
   {
      "type":"function",
      "function":{
         "name":"Expense",
         "description":"",
         "parameters":{
            "type":"object",
            "properties":{
               "description":{
                  "type":"string"
               },
               "net_amount":{
                  "type":"number"
               },
               "gross_amount":{
                  "type":"number"
               },
               "tax_rate":{
                  "type":"number"
               },
               "date":{
                  "type":"string",
                  "format":"date-time"
               }
            },
            "required":[
               "description",
               "net_amount",
               "gross_amount",
               "tax_rate",
               "date"
            ]
         }
      }
   },
   {
      "type":"function",
      "function":{
         "name":"ReportTool",
         "description":"",
         "parameters":{
            "type":"object",
            "properties":{
               "report":{
                  "type":"string"
               }
            },
            "required":[
               "report"
            ]
         }
      }
   }
]

model_name = "ScaleGenAI/Llama3-70B-Function-Calling"
api_key = "<YOUR_API_KEY>"
api_endpint = "<YOUR_API_ENDPOINT>"

messages = [
    {"role":"user", "content": 'I have spend 5$ on a coffee today please track my expense. The tax rate is 0.2. plz add to expense'}
]

client = OpenAI(
    api_key=api_key,
    base_url=api_endpoint,
)

custom_client = CustomOpenAIClient(client)

response = custom_client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=tools,
            stream=False
        )
```
