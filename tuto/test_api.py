import os
from dotenv import load_dotenv


# load .env into environment
load_dotenv()

# Check if API key is loaded
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    print(f"API Key loaded: {api_key[:8]}...{api_key[-4:]}")
else:
    print("API Key NOT FOUND - check your .env file")

from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",  
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Make a test call
response = llm.invoke("Say 'API is working!' if you can read this.")
print(response.content)