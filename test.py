from openai import OpenAI
import os

# Set your OpenAI API key from an environment variable.
client = OpenAI(
    api_key='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'
)

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "Tell me something interesting!",
        }
    ]
)

print()

