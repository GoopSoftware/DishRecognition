from openai import OpenAI
import base64

client = OpenAI(api_key='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')

content = """You are a kitchen assistant. You will receive a dish picture and must output exactly one csv object with four keys:
              • "proteins" (list of protein ingredients)
              • "sides" (list of side ingredients)
              • "sauces" (list of sauces or drizzles)
              • "garnishes" (list of final garnishes)
            
            Rules:
            1. For each item, assign each ingredient to the first matching category in this order: proteins → sides → sauces → garnishes.  
            2. Do not use parentheses, qualifiers, or words like "possibly."  
            3. Output must be valid JSON and nothing else (no prose).  
            4. If there are two or more different items in the image, produce one object per item. 
            
           
            Output:
            [
              {
                "proteins": ["cheese"],
                "sides":    ["bread"],
                "sauces":   [],
                "garnishes": []
              },
              {
                "proteins": [],
                "sides":    ["tomato soup"],
                "sauces":   ["balsamic reduction"],
                "garnishes": []
              }
            ]
            """



def extract_dish_components(image_path, output_csv_path):

    with open(image_path, "rb") as i:
        img_bytes = i.read()
    # Converting to base64 in order for OpenAI to read image
    b64 = base64.b64encode(img_bytes).decode("utf-8")
    data_uri = f"data:image/jpeg;base64,{b64}"

    response = client.responses.create(
        # GPT 4.1 seems to be the optimal cost and accuracy model
        # 4.1 mini works as well
        model="gpt-4.1",
        input=[
                {"role": "system", "content": content},
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "image_url": data_uri
                    }
                ]
            }
        ]
    )

    csv_text = response.output_text

    with open(output_csv_path, "w", encoding='utf-8', newline="") as out:
        out.write(csv_text)


def find_recipe_by_components(db_path, components, base_ingredients):

    """
    db_path - sqlite path to database
    components - dict containing components
    {
      "proteins": ["cheese"],
      "sides": ["bread", "tomato soup"],
      "sauces": ["balsamic reduction"],
      "garnishes": []
    }
    base_ingredients - list of ingredients
    """

    ''' Pseudo Code
    1. Open Database
    
    2. Create list of search terms
    ['proteins', 'sides', 'sauces', 'garnishes']
    allow for adding more later if needed]-
    
    3. Search database using ingredients from dict input
    if no ingredient inside a dict segment, skip
    
    match recipes based on if contains ingredient
    (Maybe we show all results if contains 1 ingredient for testing now)
    
    4. close database connection
    
    5. return list of recipes containing ingredients
    '''

    return None


if __name__ == "__main__":
    extract_dish_components('Food/Filet.jpg', 'test.csv')
    print("Jobs done")