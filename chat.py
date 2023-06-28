
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader

import openai
import json
import os





def generate_response(index,user_input):

    # documents = SimpleDirectoryReader('./data').load_data()
    # index = GPTVectorStoreIndex(documents)

    chat_history = []
    prompt = "".join([f"{message['role']}: {message['content']}" for message in chat_history[-5:]])
    prompt += f"User: {user_input}"
    query_engine = index.as_query_engine()
    response = query_engine.query(prompt)

    message = {"name": "assistant", "message": response.response}
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append(message)
    print(response.response)
    return str(response.response).replace("\n", "")



# print(generate_response("Hello!"))
    # while True:
    #     user_input = input("You: ")
    #     if user_input.lower() in ["bye", "goodbye"]:
    #         print("Bot: Goodbye!")
    #         bot.save_chat_history("chat_history.json")
    #         break
    #     response = bot.generate_response(user_input)
    #     print(f"Bot: {response['content']}")

