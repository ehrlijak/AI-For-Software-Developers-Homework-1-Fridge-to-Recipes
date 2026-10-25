import os
import time
from google import genai


def get_ingredients():
    raw = input("Enter ingredients you have, separated by commas: ")
    return [item.strip() for item in raw.split(",") if item.strip()]


def get_constraints():
    print("\nOptional constraints (press Enter to skip any):")
    dietary = input("Dietary restriction (e.g. vegetarian, vegan): ").strip()
    cuisine = input("Cuisine (e.g. Italian, Mexican): ").strip()
    max_time = input("Max cook time in minutes: ").strip()
    servings = input("Servings: ").strip()

    constraints = {}
    if dietary:
        constraints["dietary"] = dietary
    if cuisine:
        constraints["cuisine"] = cuisine
    if max_time:
        constraints["max_time"] = max_time
    if servings:
        constraints["servings"] = servings

    return constraints


def build_prompt(ingredients, constraints):
    prompt = (
        "You are a recipe assistant. Given the ingredients and constraints below, "
        "suggest exactly 3 recipes. For each recipe, return:\n"
        "- title\n"
        "- full ingredient list, marking which items are missing from what the user has\n"
        "- step-by-step instructions\n"
        "- estimated cook time\n\n"
        f"Ingredients on hand: {', '.join(ingredients)}\n"
    )
    if constraints:
        prompt += "Constraints:\n"
        for key, value in constraints.items():
            prompt += f"- {key}: {value}\n"
    return prompt


def call_ai_api(prompt, max_retries=3):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return None

    client = genai.Client(api_key=api_key)

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                time.sleep(attempt * 3)
            else:
                print("All retry attempts failed.")
                return None


def main():
    ingredients = get_ingredients()
    constraints = get_constraints()

    prompt = build_prompt(ingredients, constraints)

    result = call_ai_api(prompt)
    if result:
        print("\n--- Recipes ---")
        print(result)
    else:
        print("Could not get recipes.")


if __name__ == "__main__":
    main()