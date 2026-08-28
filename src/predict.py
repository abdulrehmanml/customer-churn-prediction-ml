import joblib
import pandas as pd
from pathlib import Path

# =========================================================
# PROJECT PATHS
# =========================================================

# Since predict.py is inside /src, we go up two levels to reach the root directory
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "churn_prediction_pipeline.joblib"

# =========================================================
# LOAD SAVED PREDICTIVE ENGINE
# =========================================================

def load_predictive_engine():
    """
    Load the saved preprocessing pipeline,
    trained Logistic Regression model, and
    selected prediction threshold.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Predictive engine not found at:\n{MODEL_PATH}")

    artifact = joblib.load(MODEL_PATH)
    pipeline = artifact["pipeline"]
    threshold = float(artifact["threshold"])

    return pipeline, threshold


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def predict_customer(customer_data, pipeline, prediction_threshold):
    """
    Convert one customer's input into a DataFrame, run it through the saved pipeline, and return churn probability and prediction.
    """
    input_data = pd.DataFrame([customer_data])
    probability = float(pipeline.predict_proba(input_data)[0, 1])
    prediction = int(probability >= prediction_threshold)

    return probability, prediction


def calculate_risk(probability, prediction_threshold):
    """
    Convert churn probability into a GUI risk category.
    The risk bands are aligned with the selected prediction threshold.
    """
    if probability >= 0.70:
        return "High"

    if probability >= prediction_threshold:
        return "Medium"

    return "Low"


# =========================================================
# INPUT VALIDATION
# =========================================================

def validate_customer_input(customer_data):
    """
    Validate customer inputs before model inference.

    Returns:
        list[str]: validation errors
    """
    errors = []

    # Check for empty fields first
    if any(value is None for value in customer_data.values()):
        errors.append("Please fill out all fields before analyzing customer churn risk.")
        return errors  # Stop further checks if fields are empty

    tenure = customer_data["tenure"]
    monthly_charges = customer_data["MonthlyCharges"]
    total_charges = customer_data["TotalCharges"]

    # Tenure validation
    if tenure < 0:
        errors.append("Tenure cannot be less than 0.")
    elif not 0 <= tenure <= 72:
        errors.append("Tenure must be between 0 and 72 months.")

    # Monthly charge validation
    if monthly_charges < 0:
        errors.append("Monthly Charges cannot be less than 0.")
    elif not 0 <= monthly_charges <= 200:
        errors.append("Monthly Charges must be between 0 and 200.")

    # Total charge validation
    if total_charges < 0:
        errors.append("Total Charges cannot be less than 0.")
    elif not 0 <= total_charges <= 10000:
        errors.append("Total Charges must be between 0 and 10,000.")

    # Zero-tenure consistency
    if tenure == 0 and total_charges != 0:
        errors.append("A customer with zero tenure should normally have Total Charges of 0.")

    # Basic cumulative-charge consistency
    if tenure > 1 and total_charges < monthly_charges:
        errors.append("Total Charges appears unusually low relative to Monthly Charges.")

    return errors
