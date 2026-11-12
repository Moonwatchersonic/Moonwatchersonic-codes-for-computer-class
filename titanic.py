
# TITANIC SURVIVAL PREDICTOR
# Custom Historical Algorithm + Machine Learning

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# --------------------------------
# 1. LOAD THE TITANIC DATASET
# --------------------------------

url = "https://zenodo.org/records/22983324/files/titanic.csv?download=1"

data = pd.read_csv(url)

# Prepare the data
data["sex"] = data["sex"].astype(str).str.lower().str.strip()
data["class"] = data["class"].astype(str).str.lower().str.strip()

data["CrewStatus"] = data["class"].eq("crew")

data["age"] = pd.to_numeric(data["age"], errors="coerce")
data["survived"] = pd.to_numeric(data["survived"], errors="coerce")

# Keep usable records
data = data[
    data["sex"].isin(["male", "female"]) &
    data["survived"].isin([0, 1])
].copy()

# Fill missing ages with the median
data["age"] = data["age"].fillna(data["age"].median())

# --------------------------------
# 2. PREPARE THE DATA
# --------------------------------

X = data[["age", "sex", "CrewStatus"]]
y = data["survived"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# --------------------------------
# 3. CUSTOM HISTORICAL ALGORITHM
# --------------------------------

def get_age_group(age):
    if age <= 12:
        return "Child"
    elif age <= 17:
        return "Teen"
    elif age <= 59:
        return "Adult"
    else:
        return "Senior"


training_data = X_train.copy()
training_data["survived"] = y_train

training_data["AgeGroup"] = training_data["age"].apply(
    get_age_group
)

# Calculate historical survival rates
global_rate = training_data["survived"].mean()

group_stats = training_data.groupby(
    ["AgeGroup", "sex", "CrewStatus"]
)["survived"].agg(["mean", "count"])

fallback_stats = training_data.groupby(
    ["sex", "CrewStatus"]
)["survived"].agg(["mean", "count"])


def custom_prediction(age, sex, crew):
    age_group = get_age_group(age)

    key = (age_group, sex, crew)

    if key in group_stats.index:
        stats = group_stats.loc[key]
    elif (sex, crew) in fallback_stats.index:
        stats = fallback_stats.loc[(sex, crew)]
    else:
        return global_rate

    # Smooth the estimate so small groups
    # do not produce extreme predictions
    prior = global_rate
    survivors = stats["mean"] * stats["count"]

    probability = (
        survivors + 10 * prior
    ) / (
        stats["count"] + 10
    )

    return probability


# Test the custom algorithm
custom_test_predictions = []

for _, row in X_test.iterrows():
    probability = custom_prediction(
        row["age"],
        row["sex"],
        row["CrewStatus"]
    )

    custom_test_predictions.append(
        1 if probability >= 0.5 else 0
    )

custom_accuracy = accuracy_score(
    y_test,
    custom_test_predictions
)

# --------------------------------
# 4. MACHINE LEARNING MODEL
# --------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "age",
            SimpleImputer(strategy="median"),
            ["age"]
        ),
        (
            "categories",
            OneHotEncoder(handle_unknown="ignore"),
            ["sex", "CrewStatus"]
        )
    ]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000))
    ]
)

model.fit(X_train, y_train)

ml_predictions = model.predict(X_test)

ml_accuracy = accuracy_score(
    y_test,
    ml_predictions
)

# --------------------------------
# 5. DISPLAY MODEL ACCURACY
# --------------------------------

print("===================================")
print("       TITANIC SURVIVAL PREDICTOR")
print("===================================")

print(f"Custom Algorithm Accuracy: {custom_accuracy:.1%}")
print(f"Machine Learning Accuracy: {ml_accuracy:.1%}")

# --------------------------------
# 6. GET USER INPUT
# --------------------------------

print("\nEnter your information below.")

# AGE VALIDATION
while True:
    try:
        age = float(input("Enter your age: "))

        if 0 <= age <= 100:
            break
        else:
            print("Error: Please enter an age between 0 and 100.")

    except ValueError:
        print("Error: Please enter a valid number.")

# GENDER VALIDATION
while True:
    sex = input("Enter your gender (male/female): ").lower().strip()

    if sex in ["male", "female"]:
        break
    else:
        print("Error: Please enter male or female.")

# CREW STATUS VALIDATION
while True:
    crew_input = input("Are you a crew member? (yes/no): ").lower().strip()

    if crew_input in ["yes", "no"]:
        break
    else:
        print("Error: Please enter yes or no.")

crew = crew_input == "yes"

# --------------------------------
# 7. MAKE PREDICTIONS
# --------------------------------

user_data = pd.DataFrame({
    "age": [age],
    "sex": [sex],
    "CrewStatus": [crew]
})

# Custom algorithm prediction
custom_probability = custom_prediction(
    age,
    sex,
    crew
)

# Machine learning prediction
ml_probability = model.predict_proba(
    user_data
)[0][1]

# --------------------------------
# 8. DISPLAY RESULTS
# --------------------------------

print("\n===================================")
print("          YOUR RESULTS")
print("===================================")

print(
    f"Your survival rate (Custom Algorithm) is: "
    f"{custom_probability:.1%}"
)

print(
    f"Your survival rate (Machine Learning) is: "
    f"{ml_probability:.1%}"
)

print("===================================")
print("Thank you for using the predictor!")
print("===================================")
