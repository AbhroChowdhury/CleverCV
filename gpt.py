import openai
import os

# to prevent api key from getting leaked
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_gpt(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=50, 
        temperature=0.7  
    )
    return response.choices[0].message["content"]

def main():
    print("Welcome to GPT-3 Chat!")
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        conversation.append({"role": "user", "content": user_input})
        
        gpt_response = chat_with_gpt(conversation)
        print("GPT-3:", gpt_response)
        
        conversation.append({"role": "assistant", "content": gpt_response})

if __name__ == "__main__":
    main()
