import json
import os
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

class Recipe:
    def __init__(self, name, ingredients, steps, health_info=None):
        self.name = name
        self.ingredients = ingredients
        self.steps = steps
        self.health_info = health_info

    def display_ingredients(self):
        print("Ingredients:")
        ingredients_text = "Ingredients: "
        for ingredient in self.ingredients:
            print(f"- {ingredient}")
            ingredients_text += f"{ingredient}, "
        
        tts = gTTS(text=ingredients_text, lang='en')
        tts.save("ingredients.mp3")
        playsound("ingredients.mp3")
        os.remove("ingredients.mp3")

    def display_steps(self):
        print("Steps:")
        for index, step in enumerate(self.steps, start=1):
            print(f"{index}. {step}")
            tts = gTTS(text=step, lang='en')
            tts.save("step.mp3")
            playsound("step.mp3")
            os.remove("step.mp3")
            
            while True:
                response = recognize_speech("Have you finished this step? (say 'yes' or 'no') ")
                if response is not None and response.lower() == 'yes': # type: ignore
                    break
                elif response is not None and response.lower() == 'no': # type: ignore
                    pass
                else:
                    print("Could not recognize the response. Please try again.")

    def display_health_info(self):
        if self.health_info is not None:
            print("Health Information:")
            for key, value in self.health_info.items():
                print(f"{key}: {value}")
        else:
            print("No health information available for this recipe.")

 

def load_recipe_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return Recipe(data["name"], data["ingredients"], data["steps"], data.get("health_info"))
    except FileNotFoundError:
        print(f"Error: Could not find file '{file_path}'.")
        return None

def recognize_speech(prompt=None):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        if prompt is not None:
            print(prompt)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand the audio. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Error: {e}")
        return None

def recognize_ingredient():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for ingredient...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized ingredient: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand the audio. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Error: {e}")
        return None

def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    recipe_directory = os.path.join(current_directory, 'recipes')
    recipe_files = [
        os.path.join(recipe_directory, 'scrambled_eggs.json'),
        os.path.join(recipe_directory, 'grilled_cheese.json'),
        os.path.join(recipe_directory, 'lasagna.json'),
        os.path.join(recipe_directory, 'steak.json'),
        os.path.join(recipe_directory, 'spaghetti.json'),
        os.path.join(recipe_directory, 'fried_rice.json'),
        os.path.join(recipe_directory, 'fried_sandwich.json'),
        os.path.join(recipe_directory, 'fried_cream_salad.json'),
        os.path.join(recipe_directory, 'pizza.json'),
        os.path.join(recipe_directory, 'spicy_prawn_soup.json'),
    ]
    recipes = [load_recipe_from_file(recipe_file) for recipe_file in recipe_files]
    recipes = [recipe for recipe in recipes if recipe is not None]

    if not recipes:
        print("No recipe files found. Please check your file paths.")
        return
    
    recipe_names = [recipe.name for recipe in recipes]

    while True:
        print("\nAvailable recipes:")
        for index, recipe in enumerate(recipes, start=1):
            print(f"{index}. {recipe.name}")

        recipe_names_text = ', '.join(recipe_names)
        tts = gTTS(text=f"The available recipes are {recipe_names_text}", lang='en')
        tts.save("recipe_names.mp3")
        playsound("recipe_names.mp3")
        os.remove("recipe_names.mp3")
        
        print("\nSay the number of the recipe you want to display or 'exit' to quit:")
        choice_text = recognize_speech()

        if choice_text is not None and choice_text.lower() == 'exit': # type: ignore
            print("Goodbye!")
            break

        if choice_text is not None and choice_text.isdigit(): # type: ignore
            choice = int(choice_text) - 1 # type: ignore
            if 0 <= choice < len(recipes):
                selected_recipe = recipes[choice]

                print(f"\nRecipe: {selected_recipe.name}\n")
                selected_recipe.display_ingredients()
                print()

                print("Say an ingredient you want to check in the recipe (or 'skip' to skip):")
                ingredient_text = recognize_ingredient()

                if ingredient_text is not None and ingredient_text.lower() == 'skip': # type: ignore
                    pass
                elif ingredient_text is not None:
                    if any(ingredient.lower() in ingredient_text.lower() for ingredient in selected_recipe.ingredients): # type: ignore
                        print("The ingredient is in the recipe.")
                    else:
                        print("The ingredient is not in the recipe.")

                selected_recipe.display_steps()
                selected_recipe.display_health_info()

                while True:
                    print("Have you finished these steps yet? (yes or no)")
                    response = recognize_speech()
                    if response is not None and response.lower() == 'yes': # type: ignore
                        break
                    elif response is not None and response.lower() == 'no': # type: ignore
                        selected_recipe.display_steps()
                    else:
                        print("Could not recognize the response. Please try again.")
            else:
                print("Invalid choice. Please try again.")
        else:
            print("Could not recognize the choice. Please try again.")

