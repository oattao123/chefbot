import json
import openai
import re

def generate_recipe(api_key):
    openai.api_key = api_key

    # Define the prompt for generating a recipe
    prompt = "Generate a recipe including name, ingredients, steps, and health information."

    # Generate recipe details using GPT-3
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        max_tokens=200,
        temperature=0.7
    )   
    recipe_name = response.choices[0].message.content.strip() # type: ignore



    # Use regex to extract the different parts of the recipe
    recipe_text = response.choices[0].text.strip() # type: ignore
    print(f"Response from GPT-3:\n{recipe_text}")  # <-- ADDED FOR DEBUGGING
    recipe_parts = re.split("\n\n", recipe_text)

    # Initialize the recipe dictionary
    recipe = {
        "name": "",
        "ingredients": [],
        "steps": [],
        "health_info": {}
    }

    # Assign the extracted parts to the recipe dictionary
    for part in recipe_parts:
        if "Recipe Name:" in part:
            recipe["name"] = part.split(":")[1].strip()
        elif "Ingredients:" in part:
            recipe["ingredients"] = [i.strip() for i in part.split(":")[1].strip().split(",")]
        elif "Steps:" in part:
            recipe["steps"] = [s.strip() for s in part.split(":")[1].strip().split(".")]
        elif "Health Info:" in part:
            for line in part.split(":")[1].strip().split(","):
                key, value = line.split(":")
                recipe["health_info"][key.strip()] = value.strip()

    print(f"Extracted recipe:\n{recipe}")  # <-- ADDED FOR DEBUGGING

    # Truncate the file name to a maximum of 50 characters
    file_name = f"{recipe['name'][:50].lower().replace(' ', '_')}.json"

    # Save recipe as a JSON file
    with open(file_name, "w") as file:
        json.dump(recipe, file, indent=4)

    print(f"Recipe '{recipe['name']}' saved as '{file_name}'.")


api_key = "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"
generate_recipe(api_key)
