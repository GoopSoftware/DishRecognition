# Dish Components Extraction & Recipe Lookup

A simple Python utility that:

1. **Analyzes a dish image** using OpenAI’s GPT-4.1.
2. **Saves** each dish’s components to JSON files.
3. **Searches** SQLite recipe database for matching recipes based on those components.
4. **Retrieves** and displays recipe data and step by step instructions.

---

## Table of Contents

- [Features](#features)  
- [Usage](#usage)  
  - [`fetch_dishes()`](#fetch_dishes)  
  - [`write_each_dish_to_file()`](#write_each_dish_to_file)
  - [`load_components_from_file()`](#load_components_from_file) 
  - [`find_recipes_by_json()`](#find_recipes_by_json)  
  - [`get_recipe_steps()`](#get_recipe_steps)  
- [Example Workflow](#example-workflow)  

---

## Features

- **Vision-powered**: Send any dish photo and get back categorized ingredients.
- **JSON output**: Components are stored in per-dish JSON files.
- **Database lookup**: Query a local SQLite DB for recipes containing those components.
- **Extensible**: Easily swap in different models or expand component weighting.

---

## Usage

All functions live in main.py. Here's what each does:
## fetch_dishes()
fetch_dishes(image_path) -> list[dict]
- **Input:** Path to JPEG dish image - Food/SalmonFrigger.jpg
- **Output:** A dictionary of dish components

## write_each_dish_to_file()
write_each_dish_to_file(dishes)
- **Input:** The list returned by fetch_dishes()
- **Effect:** Writes each item to a .json file

## load_components_from_file()
load_components_from_file(filepath)
- **Input:** Path to a JSON file
-  **Output:** A loaded dict of components

## find_recipes_by_json()
find_recipes_by_json(db_path, components)
- **Input:**
    - db_path - path to the database
    - components - One dishes components (JSON)
 - **Output:** A list of recipe_id, recipe_name, dish_name, matchingIngredients for any recipe matched in the database

## get_recipe_steps()
get_recipe_steps(db_path, recipe_id)
- **Input:**
    - db_path - path to the database
    - recipe_id: ID of a matching recipe
- **Output:** A list of step_order, instruction tuples in order

## Example Workflow

1. Extract components from an image
  - dishes = fetch_dishes("Food/HerbCrustedTenderloin.jpg")
2. Save each dish's components
  - write_each_dish_to_file(dishes)
3. Loop through components, load each, query recipes
for file in os.listdir("components"):
    comps = load_components_from_file(f"components/{file}")
    matches = find_recipes_by_json("recipes.db", comps)
4. Display matching recipes and their steps
