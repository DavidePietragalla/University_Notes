# FDS Challenge: Pokémon Battle Prediction

This project is a submission for the "FDS Pokémon Battles Prediction 2025" competition. The goal is to predict the winner of a Pokémon battle given a timeline of events up to a certain point.

## Project Overview

This notebook provides a complete pipeline for:

1. **Data Loading:** Reading and parsing the `train.jsonl` and `test.jsonl` files.

2. **Feature Engineering:** Extracting meaningful features from the battle timelines and Pokémon stats.

3. **Model Training:** Training baseline models (Logistic Regression and Gradient Boosting) using 5-fold cross-validation.

4. **Submission:** Generating `submission1.csv` (from Logistic Regression) and `submission3.csv` (from Gradient Boosting) in the correct format for the competition.

## Data

The data is provided in JSON Lines (`.jsonl`) format:

* `train.jsonl`: Contains battle data, including timelines and the final outcome (`player_won`).

* `test.jsonl`: Contains battle data without the final outcome, used for generating predictions.

## Feature Engineering

The current feature set extracted from the battle data includes:

* **HP Stats:** Mean remaining HP percentage for both Player 1 and Player 2.

* **Team Status:** Number of surviving (HP > 0) Pokémon for each player.

* **Status Score:** A score based on the number of Pokémon affected by a status condition and other active effects.

* **Base Stat Differences:** The difference between Player 1's team and Player 2's known team in total base stats (Speed, Attack, Defense, Special Attack, Special Defense, and HP).

## Models

Two baseline models are implemented with 5-fold stratified cross-validation:

1. **Logistic Regression:** A linear model (`model1`) providing a solid baseline.

2. **Gradient Boosting Classifier:** A more complex tree-based ensemble model (`model3`).

Both models are evaluated on Training AUC, Validation Accuracy, Validation AUC, Precision, Recall, and F1-score.

## How to Run

1. **Environment:** This notebook is set up to run in an environment like Google Colab or a local Jupyter server.

2. **Dependencies:** Ensure you have the following Python libraries installed:

   * `pandas`

   * `numpy`

   * `scikit-learn`

   * `tqdm`

3. **Data Path:** Before running, you must update the `COMPETITION_NAME` and `DATA_PATH` variables in the **first code cell** of the `challenge_FDS.ipynb` notebook. This tells the notebook where to find your data files.

   The snippet to edit looks like this:

   ```python
   import os
   
   # --- Define the path to our data ---
   COMPETITION_NAME = 'fds-pokemon-battles-prediction-2025'
   # Update this path to point to your data directory
   DATA_PATH = os.path.join('/content/drive/MyDrive', COMPETITION_NAME) # Example for Google Drive
