# Fridge-to-Recipes

A command-line tool that suggests three recipes based on the ingredients you have on hand, using the Google Gemini API. You can optionally specify dietary restrictions, cuisine, max cook time, and servings.

## Features

- Takes a list of ingredients plus optional constraints as input
- Returns 3 recipe suggestions, each with:
  - Title
  - Full ingredient list, marking which items you already have vs. which are missing
  - Step-by-step instructions
  - Estimated cook time
- Retries automatically (up to 3 times, with increasing delay) on transient API failures
- API key is read from an environment variable, never stored in code

## Setup

### 1. Install Python

Requires Python 3.8 or newer. Check with:

```bash
python --version
```

### 2. Clone the repo and install dependencies

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
python -m pip install google-genai
```

### 3. Get a Gemini API key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create a free API key

### 4. Set the API key as an environment variable

**Windows (PowerShell):**

```powershell
$env:GEMINI_API_KEY = "your-key-here"
```

**macOS / Linux:**

```bash
export GEMINI_API_KEY="your-key-here"
```

This only needs to be set once per terminal session. To set it permanently, see your OS's environment variable settings.

## Usage

Run the script:

```bash
python main.py
```

You'll be prompted for:

- Ingredients (comma-separated)
- Dietary restriction (optional)
- Cuisine (optional)
- Max cook time in minutes (optional)
- Servings (optional)

## Example Run

This run shows the retry logic in action: the first API call failed with a transient `503 UNAVAILABLE` error, and the program automatically retried and succeeded on the second attempt.

**Input:**

```
Enter ingredients you have, separated by commas: bread,tomateos,butter,beef,chili,butter,eggs,tortillas,cheese

Optional constraints (press Enter to skip any):
Dietary restriction (e.g. vegetarian, vegan): 
Cuisine (e.g. Italian, Mexican): mexican
Max cook time in minutes: 30
Servings: 1
```

**Output:**

```
Attempt 1 failed: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}

--- Recipes ---
Here are 3 Mexican-inspired recipes tailored for 1 serving, each taking 30 minutes or less:

---

### Recipe 1: Spicy Cheesy Beef Quesadilla with Fresh Tomato-Chili Salsa

*A classic crispy quesadilla loaded with seasoned beef and melted cheese, paired with a quick fresh salsa.*

* **Estimated Cook Time:** 15 minutes
* **Servings:** 1

**Ingredients:**
* 1 large tortilla *(On hand)*
* 3–4 oz beef (ground or cut into small strips) *(On hand)*
* 1/3 cup cheese, shredded *(On hand)*
* 1 small tomato, diced *(On hand)*
* 1/2 fresh chili pepper (jalapeño or serrano), finely minced *(On hand)*
* 1 tbsp butter *(On hand)*
* 1/4 tsp salt *(Missing)*
* 1/4 tsp ground cumin *(Missing - optional)*

**Instructions:**
1. Make the salsa: combine diced tomato, half the minced chili, and a pinch of salt. Set aside.
2. Cook the beef: melt 1/2 tbsp butter, sauté beef with remaining chili and salt until browned (3–5 min).
3. Assemble: layer cheese, beef, and more cheese on half the tortilla, fold over.
4. Toast: melt remaining butter, cook quesadilla 2–3 min per side until golden and cheese is melted.
5. Serve: cut into wedges, serve with salsa.

---

### Recipe 2: Mexican-Style Beef & Melted Cheese Torta

*A hearty, warm Mexican sandwich served on butter-toasted bread with seared beef, melted cheese, and fresh toppings.*

* **Estimated Cook Time:** 20 minutes
* **Servings:** 1

**Ingredients:**
* 1 crusty roll or 2 slices of sturdy bread *(On hand)*
* 4 oz beef, thinly sliced *(On hand)*
* 1/4 cup cheese *(On hand)*
* 1/2 tomato, sliced *(On hand)*
* 1/2 fresh chili, sliced *(On hand)*
* 1 tbsp butter *(On hand)*
* Salt and pepper *(Missing)*
* Mayonnaise or refried beans *(Missing - optional)*

**Instructions:**
1. Season beef with salt and pepper.
2. Sear beef and chili in butter, 2–4 min per side; melt cheese on top at the end.
3. Toast buttered bread in the same skillet until golden.
4. Assemble sandwich with beef, cheese, chili, and tomato.
5. Serve warm.

---

### Recipe 3: Speedy Skillet Huevos Rancheros

*A quick, vibrant breakfast-for-dinner featuring fried eggs over warm tortillas topped with a tomato-chili sauce and melted cheese.*

* **Estimated Cook Time:** 15 minutes
* **Servings:** 1

**Ingredients:**
* 2 small tortillas *(On hand)*
* 2 large eggs *(On hand)*
* 1 medium tomato, chopped *(On hand)*
* 1/2 fresh chili, minced *(On hand)*
* 1.5 tbsp butter *(On hand)*
* 2–3 tbsp cheese *(On hand)*
* Salt *(Missing)*
* 1 garlic clove *(Missing - optional)*

**Instructions:**
1. Make the ranchero sauce: cook chili (and garlic) in butter 1 min, add tomato and salt, simmer 4–5 min.
2. Warm tortillas in buttered skillet, ~30 sec per side.
3. Fry eggs in remaining butter until whites are set, yolks still runny.
4. Assemble: egg on tortilla, topped with sauce and cheese.
```

## Error Handling

If the Gemini API call fails (e.g. due to high demand or network issues), the program automatically retries up to 3 times with an increasing delay between attempts. If all retries fail, it prints an error message instead of crashing. The example run above shows this happening naturally: the first attempt hit a `503` error from Gemini, and the retry on the second attempt succeeded.

## Project Structure

```
fridge-to-recipes/
├── main.py        # Main application logic
├── README.md       # This file
└── .gitignore      # Excludes .env and cache files from Git
```

## Notes

- The API key is never hardcoded or committed. It's read at runtime via `os.environ.get("GEMINI_API_KEY")`.
- Make sure your `.gitignore` includes `.env` if you choose to store your key in a `.env` file instead of a system environment variable.