from google import genai
from google.genai import types

client=genai.Client(api_key="")

response=client.models.generate_content(
    model="gemini-2.5-pro",
    contents=" give the prime number till 50",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True
        )
        
    )
)

print(response)