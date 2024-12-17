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
python uvicorn app.main:app --reload
```

Once the app is running, it will be accessible via the following URLs:

- **Swagger UI (for API documentation)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 5. Dockerize the Application

After training the model, you can containerize the app using Docker.

#### a) Build the Docker Image

Navigate to the root directory of the project and build the Docker image using the following command:

```bash
docker build -t heart-disease-app .
```

#### b) Run the Docker Container

Once the image is built, run the Docker container:

```bash
docker run -p 8000:8000 heart-disease-app 
```

This will start the FastAPI app inside a container and expose it on `http://127.0.0.1:8000/`.

---

---

### 6. Run App with PostgreSQL and Docker Compose


#### 1. Configuration

1. **Create a `.env` file**  
   In the root directory, create a file named `.env`. Refer to the `example` file for guidance:  
   ```
   cp .env.example .env
   ```  
   Update the values in the `.env` file according to your configuration. Example keys include:  
   - `APP_PORT`  
   - `DB_USER`  
   - `DB_PASSWORD`  
   - `DB_DATABASE`  
   - `DB_HOST`  
   - `DB_PORT`  

---

#### 2. Modify Database Configuration

- Open the file **`app/database.py`**.
- Make the following changes:  
   - **Comment out lines 16 and 17**: These lines refer to the SQLite configuration.  
   - **Uncomment lines 13 and 14**: Update the PostgreSQL database URL and engine creation lines as follows:  

   ```python
   SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
   engine = create_engine(SQLALCHEMY_DATABASE_URL)
   ```  
---

#### 3. Run the Application

To build and start the containers, run the following command in the root directory:

```bash
docker-compose up
```

This will:

- Start a PostgreSQL container named **`hd-prediction-db`** using the `postgres:17-alpine` image.  
- Start another container named **`hd-prediction-app`** to run the application code.  

---

#### 4. Verify the Containers

You can check the running containers with:

```bash
docker ps
```

---

#### Application Details

- **Database**: PostgreSQL 17 (Alpine)  
- **Backend**: Python with SQLAlchemy ORM  

---

#### Notes

- Stop the containers using `Ctrl+C` or:

   ```bash
   docker-compose down
   ```

- Ensure your `.env` file contains correct values to avoid connection issues.

---

That's it! The application should now be running successfully using Docker and PostgreSQL. 🚀

---

## Folder Structure

```
├── .github/                       # GitHub workflows for CI/CD pipeline
│   ├── workflows/                 # Contains GitHub Actions workflow files
│       ├── pipeline.yml           # CI/CD pipeline configuration for automated testing and deployment
│
├── app/                           # Application source code
│   ├── trained_model/             # Pre-trained machine learning models
│       ├── reg_model.pkl          # Pickle file containing the trained Logistic Regression model
│   ├── routers/                   # API route definitions for different functionalities
│       ├── admin.py               # Routes for admin-related operations
│       ├── auth.py                # Routes for authentication and authorization
│       ├── predict.py             # Routes for heart disease predictions
│       ├── users.py               # Routes for user management
│   ├── main.py                    # Entry point for the FastAPI application
│   ├── database.py                # Database connection and ORM engine configuration
│   ├── models.py                  # SQLAlchemy models for database tables
│
├── dataset/                       # Datasets used for training the model
│   ├── framingham_heart_disease.csv  # Dataset for heart disease prediction
│
├── research/                      # Research and experimentation work
│   ├── heart-disease-prediction-logistic-regression.ipynb  # Jupyter Notebook for model training and analysis
│
├── Dockerfile                     # Instructions to build the Docker container for the application
├── docker-compose.yml             # Configuration to manage multi-container Docker applications
├── .dockerignore                  # Files and directories to exclude during Docker image build
│
├── requirements.txt               # List of required Python packages for production
├── requirements.dev.txt           # List of required Python packages for development and testing
│
└── README.md                      # Project documentation and setup instructions

```

---
