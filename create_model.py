import sys
import os
import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

iris = load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=5, random_state=42)
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)

print(f"Model accuracy: {accuracy:.2%}")
print(f"Classes: {model.classes_}")
print(f"Feature count: {model.n_features_in_}")

model_path = 'models/model_v1.0.0.pkl'
joblib.dump(model, model_path)
print(f"Model saved to {model_path}\n")

model = LogisticRegression(max_iter=200, random_state=42)
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)

print(f"Model accuracy: {accuracy:.2%}")
print(f"Classes: {model.classes_}")
print(f"Feature count: {model.n_features_in_}")

model_path = 'models/model_v1.1.0.pkl'
joblib.dump(model, model_path)
print(f"Model saved to {model_path}")
