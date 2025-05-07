from openai import OpenAI
import base64
import json
import os
import sqlite3

client = OpenAI(
    api_key='')

content = '''
You are a kitchen assistant. You will receive a dish picture and must output exactly one JSON array with four keys per item:
• "proteins" (list of protein ingredients)
• "sides" (list of side ingredients)
• "sauces" (list of sauces or drizzles)
• "garnishes" (list of final garnishes)

Rules:
1. For each item, assign each ingredient to the first matching category in this order: proteins → sides → sauces → garnishes.
2. Do not use parentheses, qualifiers, or words like "possibly."
3. Output must be valid JSON and nothing else (no prose).
4. If there are two or more different items in the image, produce one object per item in the array.

Example output:
[
  {"proteins":["cheese"],  "sides":["bread"],        "sauces":[],                     "garnishes":[]},
  {"proteins":[],            "sides":["tomato soup"], "sauces":["balsamic reduction"],"garnishes":[]}
]
'''

"""
We later convert the dictionary output into a list to run the database query
however we keep the data in a dictionary format from the start because it gives
more flexibility to improve the program without changing the data flow.
For example, we could weigh the results to certain categories like proteins
when suggesting recipes to the user
"""


def fetch_dishes(image_path):
    with open(image_path, "rb") as i:
        img_bytes = i.read()
    # Converting to base64 for OpenAI to read image
    b64 = base64.b64encode(img_bytes).decode("utf-8")
    data_uri = f"data:image/jpeg;base64,{b64}"

    response = client.responses.create(
        # GPT 4.1 seems to be the optimal cost and accuracy model
        # 4.1 mini works as well slightly cheaper but slightly less accurate
        # Running at a 1/5 of a penny cost per request
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

    return json.loads(response.output_text)


def write_each_dish_to_file(dish):
    # Creates a json file for each dish component named dish_(id)
    # Saving in separate files so that a grilled cheese stays separate from tomato soup
    os.makedirs("components", exist_ok=True)
    for id, dish in enumerate(dish, start=1):
        # looping through the list returned from the output of the ai
        # Then writing the contents to a file called dish_id.json
        path = os.path.join("components", f"dish_{id}.json")
        with open(path, "w", encoding="utf-8") as file:
            # Writing json to file
            # dish = {"proteins": ["cheese"], "sides": ["bread"], "sauces": [], "garnishes": []}
            json.dump(dish, file, ensure_ascii=False, indent=2)


def find_recipes_by_json(db_path, components):
    # Creating an empty list to hold values to search database
    search_terms = []
    for items in components.values():
        for item in items:
            # append the list
            search_terms.append(item)

    # Builds the WHERE conditions based on number of search terms
    # Example: 'i.ingredient LIKE ? OR i.ingredient LIKE ? OR i.ingredient LIKE ?'
    conditions = ' OR '.join('i.ingredient LIKE ?' for _ in search_terms)

    # Add % to each search term for partial matching '%beef%' Will match with 'beef tenderloin'
    # Example: ['%cheese%', '%bread%']
    search_terms = [f'%{term}%' for term in search_terms]

    query = f'''
        SELECT r.id, r.name, d.name AS dish_name, i.ingredient
        FROM ingredients i
        JOIN recipes r ON i.recipe_id = r.id
        JOIN dishes d ON r.dish_id = d.id
        WHERE {conditions}
        ORDER BY r.id;
        '''


    '''
    SQL query to search for recipes that contain ingredients of search_terms

    r.id -> the recipes ID in database
    r.name -> the name of the recipe
    d.name AS dish_name -> the name of the fish from the database
    i.ingredient -> the ingredient from the ingredients table matching the search
    "Give me the recipe ID, recipe name, dish name, and the matching ingredient"

    FROM ingredients i
    "Start from the ingredients table and call it i for short"

    JOIN recipes r ON i.recipe_id = r.id -> connects each ingredient.recipe_id to recipes.id
    "Find the recipe this ingredient belongs to"

    JOIN dishes d ON r.dish_id = d.id -> connects each recipe.dish_id to dishes.id
    "Find the dish this recipe is a part of"

    WHERE i.ingredient LIKE ? OR i.ingredient LIKE ? -> filter for matches | ? is a palceholder for search_terms[]
    "Only return where the ingredient contains search terms"

    ORDER BY r.id
    "order rows by recipe ID"
    '''

    # Connect to database, execute query, assign results, close connection
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(query, search_terms)
    results = cursor.fetchall()
    connection.close()

    return results


def get_recipe_steps(db_path, recipe_id):
    # Takes result from earlier query and returns all steps for matches
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('''
        SELECT step_order, instruction
        FROM steps
        WHERE recipe_id = ?
        ORDER BY step_order;
    ''', (recipe_id,))
    steps = cursor.fetchall()
    connection.close()
    return steps


def load_components_from_file(filepath):
    # This just reads a file for the input to find_recipes_by_json()
    # so we dont have to include it in the function
    with open(filepath, 'r', encoding='utf-8') as file:
        components = json.load(file)

    print("Loaded components:", components)

    return components


if __name__ == "__main__":

    # -----This code handles the AI recognition of the image and saves to components-----
    '''
    dishes = fetch_dishes("Food/HerbCrustedTenderloin.jpg")
    write_each_dish_to_file(dishes)
    print(f"Jobs done, wrote {len(dishes)} files.")
    '''
    # -----Proceeding code searches the database based on the components of the dish.json file-----
    #                  --------------------TO DO--------------------
    # Write a for loop here to iterate this section through the files inside components
    # at end of loop delete the file that has been iterated through



    matches = find_recipes_by_json('recipes.db', load_components_from_file('components/dish_1.json'))
    print("Matches: ", matches)
    if matches:
        seen_recipes = set()
        for recipe_id, recipe_name, dish_name, count in matches:
            if recipe_id not in seen_recipes:
                print(f"{dish_name} → {recipe_name} (matched {count} ingredients)")
                steps = get_recipe_steps('recipes.db', recipe_id)
                print("Steps:")
                for step_number, description in steps:
                    print(f"  {step_number}. {description}")
                seen_recipes.add(recipe_id)

    else:

        print("No matches")
