# Heart Disease Prediction App

This repository contains an app for predicting heart disease based on input features such as age, smoking habits, blood pressure, heart rate, and more. The model is trained using a Logistic Regression classifier from `sklearn`, with hyperparameter optimization and experiment tracking via MLflow. The app is built using FastAPI and can be easily dockerized.

## Project Overview

- **Model**: Trained using `Logistic Regression` from `sklearn` on the dataset containing the following features:
  - `age`
  - `cigsPerDay` (cigarettes per day)
  - `prevalentStroke` (whether the person had a stroke)
  - `sysBP` (systolic blood pressure)
  - `diaBP` (diastolic blood pressure)
  - `heartRate` (heart rate)
  - `glucose` (glucose level)
  
- **Model Accuracy**: Achieved an accuracy of 87% on the test data.


- **Tools & Libraries**:
  - Python 3.9.19
  - `scikit-learn`
  - `mlxtend` for performing feature selection
  - `Optuna` for hyperparameter optimization
  - `MLflow` for tracking experiments
  - `FastAPI` for building the web app
  - `Docker` for containerizing the application
  - `PostgreSQL/ sqlite` for database management
  - `Pytest` for testing the functionality of the code
  - `GitHub Actions` for CI/CD to automate building, testing, and deployment.



## Installation & Setup

### 1. Create a Python Environment

Create a new Python environment (recommended using `venv` or `conda`) and install the required dependencies. 
*Note: python 3.9.19 recommended*

```bash
# Create a new virtual environment
python3 -m venv .venv

# Activate the virtual environment

# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate

# Install required libraries
pip install -r requirements.txt
```

### 2. Start MLflow Server

MLflow is used for experiment tracking, including the hyperparameter optimization of the Logistic Regression model.

To start the MLflow server, run:

```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 127.0.0.1 --port 5000
```

This will start the MLflow server at `http://127.0.0.1:5000`, where you can view and track experiments.

### 3. Train the Model

Run the `heart-disease-prediction-logistic-regression.ipynb` notebook to train the model. The notebook includes steps for:

- Loading and preparing the data
- Training the Logistic Regression model
- Performing hyperparameter optimization
- Tracking experiments using MLflow

After running the notebook, a trained model pickle file (`reg_model.pkl`) will be saved in the `app/trained_model/` directory.

*Note: The trained model is already available in the `app/trained_model/` directory. If you want to replace it with a new model, you can retrain it by running the notebook again.*

### 4. Test the App

To test the FastAPI app, run the following command:

```bash
python app/main.py
```

Once the app is running, it will be accessible via the following URLs:

- **Main App**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Swagger UI (for API documentation)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
