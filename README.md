# 🛡️ Network Security — Phishing Website Detection

An end-to-end Machine Learning project that detects **phishing websites** using network/URL-based features. Built with a full MLOps pipeline covering data ingestion, validation, transformation, model training with experiment tracking, and automated CI/CD deployment to AWS.

---

## 📌 Problem Statement

Phishing attacks are one of the most common cybersecurity threats. This project builds a classification model that predicts whether a given website is **phishing or legitimate** based on network-level features extracted from URLs and web data.

---

## 🏗️ Architecture Overview

```
MongoDB (Raw Data)
       ↓
  Data Ingestion
       ↓
  Data Validation  (Schema Check)
       ↓
  Data Transformation  (KNN Imputer + Preprocessing)
       ↓
  Model Training  (5 Models + GridSearchCV + MLflow Tracking)
       ↓
  Best Model saved to final_model/
       ↓
  AWS S3 Sync (Model Artifacts)
       ↓
  FastAPI App  (/train  |  /predict)
       ↓
  Docker + GitHub Actions CI/CD → AWS ECR → EC2 Deployment
```

---

## 🔧 Tech Stack

| Layer               | Technology                   |
|---------------------|------------------------------|
| Data Storage        | MongoDB Atlas                |
| ML Framework        | Scikit-learn                 |
| Experiment Tracking | MLflow + DagsHub             |
| API Server          | FastAPI + Uvicorn            |
| Cloud Storage       | AWS S3                       |
| Containerization    | Docker                       |
| Container Registry  | AWS ECR                      |
| CI/CD               | GitHub Actions               |
| Deployment          | AWS EC2 (self-hosted runner) |
| Language            | Python 3.x                   |

---

## 📁 Project Structure

```
NetworkSecurity/
│
├── networksecurity/
│   ├── components/                # Core pipeline steps
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   ├── pipeline/
│   │   └── training_pipeline.py   # Orchestrates full pipeline
│   ├── entity/
│   │   ├── config_entity.py       # Config dataclasses
│   │   └── artifact_entity.py     # Artifact dataclasses
│   ├── constant/
│   │   └── training_pipeline/     # All constants (paths, names)
│   ├── cloud/
│   │   └── s3_syncer.py           # AWS S3 sync utility
│   ├── utils/                     # Helper functions
│   ├── exception/                 # Custom exception handler
│   └── logging/                   # Custom logger
│
├── .github/workflows/main.yml     # CI/CD GitHub Actions
├── app.py                         # FastAPI application
├── main.py                        # Manual pipeline runner
├── push_data.py                   # Push raw CSV to MongoDB
├── Dockerfile                     # Docker container setup
├── requirements.txt               # Python dependencies
├── setup.py                       # Package setup
├── data_schema/schema.yaml        # Column schema for validation
├── final_model/                   # Saved model & preprocessor
├── prediction_output/             # CSV output of predictions
└── Network_Data/                  # Raw phishing dataset
```

---

## 🔄 Pipeline Steps

### 1. Data Ingestion
- Reads raw phishing data from **MongoDB Atlas**
- Saves to local feature store
- Splits into **train (80%)** and **test (20%)** sets

### 2. Data Validation
- Validates all columns against `data_schema/schema.yaml`
- Ensures data types and structure are correct before processing

### 3. Data Transformation
- Handles missing values using **KNNImputer**
- Applies preprocessing and saves the fitted **preprocessor.pkl**
- Converts data to numpy arrays for model training

### 4. Model Training
Trains and tunes **5 classification models** using GridSearchCV:

| Model               | Hyperparameters Tuned                        |
|---------------------|----------------------------------------------|
| Random Forest       | `n_estimators`                               |
| Decision Tree       | `criterion`                                  |
| Gradient Boosting   | `learning_rate`, `subsample`, `n_estimators` |
| Logistic Regression | default                                      |
| AdaBoost            | `learning_rate`, `n_estimators`              |

- Selects the **best model** based on test score
- Evaluates using **F1 Score, Precision, Recall**
- Logs all experiments to **MLflow via DagsHub**
- Saves best model to `final_model/model.pkl`

### 5. Cloud Sync
- Syncs trained model artifacts to **AWS S3** for persistent storage

---

## 🚀 API Endpoints

| Endpoint   | Method | Description                                           |
|------------|--------|-------------------------------------------------------|
| `/`        | GET    | Redirects to interactive Swagger docs (`/docs`)       |
| `/train`   | GET    | Triggers the full training pipeline                   |
| `/predict` | POST   | Upload a CSV file → returns predictions as HTML table |

### Running Locally

```bash
# 1. Clone the repo
git clone https://github.com/itsranjith95/NetworkSecurity.git
cd NetworkSecurity

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
# Create a .env file with:
# MONGO_DB_URL=your_mongodb_connection_string

# 4. Push data to MongoDB (first time only)
python push_data.py

# 5. Run the FastAPI app
python app.py
```

App will be available at: `http://localhost:8000/docs`

---

## ⚙️ CI/CD Pipeline

Automated pipeline via **GitHub Actions** on every push to `main`:

```
Push to main branch
       ↓
[1] Continuous Integration
    - Checkout code
    - Lint & Unit Tests
       ↓
[2] Continuous Delivery
    - Build Docker image
    - Push to AWS ECR (tagged :latest)
       ↓
[3] Continuous Deployment (Self-hosted EC2)
    - Pull latest image from ECR
    - Run container on port 8080
    - Clean up old Docker images
```

### Required GitHub Secrets

| Secret Name             | Description                    |
|-------------------------|--------------------------------|
| `AWS_ACCESS_KEY_ID`     | AWS IAM access key             |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key             |
| `AWS_REGION`            | AWS region (e.g. `ap-south-1`)|
| `ECR_REPOSITORY_NAME`   | ECR repository name            |
| `AWS_ECR_LOGIN_URI`     | ECR login URI                  |

---

## 🐳 Docker

```bash
# Build the image
docker build -t networksecurity .

# Run the container
docker run -d -p 8080:8080 networksecurity
```

---

## 📊 Experiment Tracking

All model experiments (F1, Precision, Recall) are tracked using **MLflow** integrated with **DagsHub**.

View experiments at: [https://dagshub.com/itsranjith95/NetworkSecurity](https://dagshub.com/itsranjith95/NetworkSecurity)

---

## 📋 Environment Variables

Create a `.env` file in the root directory:

```
MONGO_DB_URL=mongodb+srv://<username>:<password>@cluster.mongodb.net/
```

---

## 👤 Author

**Ranjith** — [GitHub](https://github.com/itsranjith95)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
