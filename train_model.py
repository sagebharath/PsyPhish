import pandas as pd
from xgboost import XGBClassifier

# Load dataset
df = pd.read_csv("dataset.csv")

# Convert ALL columns to numeric (very important)
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Drop rows with any NaN values
df = df.dropna()

# Split features and label
X = df.drop("label", axis=1)
y = df["label"]

# Train model
model = XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    eval_metric="logloss"
)

model.fit(X, y)

# Save model
model.save_model("xgb_model.json")

print("Model trained and saved successfully")
print("Feature count:", X.shape[1])