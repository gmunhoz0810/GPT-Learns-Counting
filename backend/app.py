from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
import json
from datetime import datetime

app = FastAPI()

# Update CORS settings for deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://gmunhoz0810.github.io"],  # Replace with your GitHub Pages URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use environment variable for API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Query(BaseModel):
    query: str

class Conversation:
    def __init__(self):
        self.messages = [
            {"role": "system", "content": """You are an AI assistant that helps count occurrences of letters or words in phrases, as well as the total number of characters in a text.
            Use the count_occurrences function to count letters or words, and the count_characters function to count total characters. 
            You need to determine the 'needle' (what to count) and the 'haystack' (where to count) from the user's query for count_occurrences. 
            For count_characters, you just need to determine the text to count.
            Be careful with plurals: if a user says "count the As in strawberry", they likely mean to count 'a', not 'as'.
            Use your best judgment to interpret the user's intent.
            Always provide clear and concise responses, explaining your interpretation if necessary.
            Remember previous interactions in the conversation to provide context-aware responses."""}
        ]

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_messages(self):
        return self.messages

    def reset(self):
        self.__init__()

conversation = Conversation()

def count_occurrences(needle: str, haystack: str) -> int:
    return haystack.lower().count(needle.lower())

def count_characters(text: str) -> int:
    return len(text)

def get_delivery_date(order_id: str) -> str:
    # Simulating a database query
    # In a real application, you would query your database here
    # For this example, we'll just return a fixed date
    return "2024-09-05"

@app.post("/query")
async def process_query(query: Query):
    try:
        conversation.add_message("user", query.query)

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "count_occurrences",
                    "description": "Count occurrences of a letter or word in a phrase",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "needle": {"type": "string", "description": "The letter or word to count"},
                            "haystack": {"type": "string", "description": "The phrase to search in"}
                        },
                        "required": ["needle", "haystack"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "count_characters",
                    "description": "Count total characters in a word or phrase",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "The text to count characters in"}
                        },
                        "required": ["text"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_delivery_date",
                    "description": "Get the delivery date for a customer's order",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "order_id": {"type": "string", "description": "The customer's order ID"}
                        },
                        "required": ["order_id"]
                    }
                }
            }
        ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=conversation.get_messages(),
            tools=tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                if function_name == "count_occurrences":
                    needle = function_args.get("needle")
                    haystack = function_args.get("haystack")
                    count = count_occurrences(needle, haystack)
                    function_response = f"The letter or word '{needle}' appears {count} time(s) in the text '{haystack}'."
                elif function_name == "count_characters":
                    text = function_args.get("text")
                    count = count_characters(text)
                    function_response = f"The text '{text}' contains {count} character(s)."
                elif function_name == "get_delivery_date":
                    order_id = function_args.get("order_id")
                    delivery_date = get_delivery_date(order_id)
                    function_response = f"The delivery date for order {order_id} is {delivery_date}."
                
                conversation.add_message("function", function_response)

        # Generate final response from AI
        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=conversation.get_messages()
        )

        ai_response = final_response.choices[0].message.content
        conversation.add_message("assistant", ai_response)

        return {
            "response": ai_response,
            "conversation_ended": False
        }

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return {"response": error_message, "conversation_ended": False}

@app.post("/reset")
async def reset_conversation():
    conversation.reset()
    return {"message": "Conversation reset successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))