from openai import OpenAI, api_key
import os
import json
import base64
import sys


client = OpenAI(
    api_key='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'
)


def analyze_dish(image_path: str) -> dict:

    with open(image_path, "rb") as img_file:
        img_bytes = img_file.read()
    b64 = base64.b64encode(img_bytes).decode("utf-8")
    data_uri = f"data:image/jpeg;base64,{b64}"

    messages = [
        {
            "role": "system",
            "content": (
                "You are a kitchen assistant. "
                "Given an image of a plated dish, respond with a JSON object "
                "listing the components under these keys: "
                "`protein`, `sides`, `sauce`, and `garnish`. "
                "Each value should be a list of strings (or an empty list if none)."
            )
        },
        {
            "role": "user",
            "content": data_uri
        }
    ]


    response = client.chat.completions.create(
            model="o4-mini",
            messages=messages,
            temperature=0
        )

    text = response.choices[0].message.content.strip()
    try:
        return json.loads(text)
    except json.JSONDecoderError:
        import re
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise

def main():


    image_path = "Food/Filet.jpg"
    components = analyze_dish(image_path)

    print("\nDish components:")
    print(f"  Protein : {components.get('protein', [])}")
    print(f"  Sides   : {components.get('sides', [])}")
    print(f"  Sauce   : {components.get('sauce', [])}")
    print(f"  Garnish : {components.get('garnish', [])}")


if __name__ == "__main__":
    print(api_key)
    main()