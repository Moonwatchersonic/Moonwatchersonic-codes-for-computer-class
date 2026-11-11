
# =====================================================
# TITANIC SURVIVAL PREDICTOR
# Custom Algorithm vs Machine Learning
# Google Colab Version
# =====================================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# =====================================================
# 1. LOAD HISTORICAL TITANIC DATA
# =====================================================

url = "https://zenodo.org/records/22983324/files/titanic.csv?download=1"

data = pd.read_csv(url)

print("Historical Titanic data loaded!")
print("Total people:", len(data))


# =====================================================
# 2. PREPARE THE DATA
# =====================================================

data["CrewStatus"] = (
    data["class"].str.lower() == "crew"
)

X = data[["age", "sex", "CrewStatus"]]
y = data["survived"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

median_age = X_train["age"].median()


# =====================================================
# 3. CUSTOM ALGORITHM
# =====================================================

training_data = X_train.copy()

training_data["survived"] = y_train

training_data["age"] = training_data["age"].fillna(
    median_age
)


def age_group(age):

    if age <= 12:
        return "Child"

    elif age <= 17:
        return "Teen"

    elif age <= 59:
        return "Adult"

    else:
        return "Senior"


training_data["AgeGroup"] = (
    training_data["age"].apply(age_group)
)


# Calculate historical survival statistics

group_statistics = training_data.groupby(
    ["AgeGroup", "sex", "CrewStatus"]
)["survived"].agg(["sum", "count"])


def custom_predict(age, sex, crew):

    group = age_group(age)

    key = (group, sex, crew)

    if key in group_statistics.index:

        stats = group_statistics.loc[key]

        survivors = stats["sum"]
        count = stats["count"]

    else:

        survivors = 0
        count = 0

    subgroup = training_data[
        (training_data["sex"] == sex) &
        (training_data["CrewStatus"] == crew)
    ]

    if len(subgroup) > 0:

        prior = subgroup["survived"].mean()

    else:

        prior = training_data["survived"].mean()

    probability = (
        survivors + 10 * prior
    ) / (count + 10)

    return probability


# =====================================================
# 4. MACHINE LEARNING MODEL
# =====================================================

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


model = Pipeline([
    ("preprocessing", preprocessor),

    ("classifier", LogisticRegression(max_iter=1000))
])


# Train the model

model.fit(X_train, y_train)


# =====================================================
# 5. TEST BOTH ALGORITHMS
# =====================================================

ml_predictions = model.predict(X_test)

ml_accuracy = accuracy_score(
    y_test,
    ml_predictions
)


custom_predictions = []

for _, row in X_test.iterrows():

    age = row["age"]

    if pd.isna(age):

        age = median_age

    probability = custom_predict(
        age,
        row["sex"],
        row["CrewStatus"]
    )

    custom_predictions.append(
        int(probability >= 0.5)
    )


custom_accuracy = accuracy_score(
    y_test,
    custom_predictions
)


print("\n========== MODEL ACCURACY ==========")

print(
    "Custom Algorithm:",
    round(custom_accuracy * 100, 2), "%"
)

print(
    "Machine Learning:",
    round(ml_accuracy * 100, 2), "%"
)


# =====================================================
# 6. GET USER INFORMATION
# =====================================================

print("\n====================================")
print("       TITANIC SURVIVAL PREDICTOR")
print("====================================")


# AGE VALIDATION

while True:

    try:

        age = float(input("\nEnter age: "))

        if 0 <= age <= 100:

            break

        else:

            print(
                "Invalid age! Enter an age between 0 and 100."
            )

    except ValueError:

        print(
            "Invalid input! Please enter a number."
        )


# GENDER VALIDATION

while True:

    sex = input(
        "\nEnter gender (male/female): "
    ).lower().strip()

    if sex in ["male", "female"]:

        break

    else:

        print(
            "Invalid gender! Please enter male or female."
        )


# CREW VALIDATION

while True:

    crew_input = input(
        "\nIs this person crew? (yes/no): "
    ).lower().strip()

    if crew_input in ["yes", "no"]:

        break

    else:

        print(
            "Invalid answer! Please enter yes or no."
        )


# =====================================================
# 7. MAKE PREDICTIONS
# =====================================================

crew = crew_input == "yes"


# Custom algorithm prediction

custom_probability = custom_predict(
    age,
    sex,
    crew
)


# Machine learning prediction

person = pd.DataFrame({

    "age": [age],

    "sex": [sex],

    "CrewStatus": [crew]

})


ml_probability = model.predict_proba(
    person
)[0][1]


# =====================================================
# 8. DISPLAY RESULTS
# =====================================================

print("\n====================================")
print("          PREDICTION RESULTS")
print("====================================")

print("Age:", age)

print("Gender:", sex.capitalize())

print("Crew member:", "Yes" if crew else "No")

print("------------------------------------")

print(
    "Custom Algorithm:",
    round(custom_probability * 100, 2), "%"
)

print(
    "Machine Learning:",
    round(ml_probability * 100, 2), "%"
)

print("====================================")

print(
    "\nThese are historical statistical estimates, "
    "not guaranteed individual survival chances."
)
