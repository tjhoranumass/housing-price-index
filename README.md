
# House Price Prediction Pipeline with Prefect

This project sets up a data pipeline using Prefect to ingest, preprocess, and train a machine learning model to predict house price indices based on the FHFA HPI dataset. It also exposes the trained model through a Flask API for predictions.

## Project Structure

```
house-price-prediction/
│
├── hpi_data_pipeline.py       # Prefect data pipeline script
├── model.pkl                  # Trained model (generated after pipeline run)
├── encoder.pkl                # Encoder model (generated after pipeline run)
├── feature_names.pkl          # Feature Names (generated after pipeline run)
├── requirements.txt           # Python dependencies
├── tests/                     # Unit tests for pipeline and Flask app
├── README.md                  # This readme file
```

## Requirements

- Python 3.7+
- Flask
- Prefect
- scikit-learn
- pandas

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/tjhoranumass/housing-price-index.git
   cd house-price-prediction
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Log in to Prefect:
   ```bash
   prefect login --key your_prefect_api_key
   ```

4. Run the Prefect pipeline to download data, preprocess, and train the model:
   ```bash
   python hpi_data_pipeline.py
   ```

5. After the pipeline finishes, the trained model will be saved as `model.pkl`.

## Deploying to Heroku

To deploy this application to Heroku, follow these steps:

1. **Create a `Procfile`** in the root of your project with the following content:
   ```plaintext
   worker: python hpi_data_pipeline.py
   ```

2. **Update `requirements.txt`** to include all necessary dependencies. You can generate this with:
   ```bash
   pip freeze > requirements.txt
   ```

3. **Create a `runtime.txt`** file in the root of your project specifying the Python version:
   ```plaintext
   python-3.12.4
   ```

4. **Set Up Environment Variables** on Heroku as needed:
   ```bash
   heroku config:set VARIABLE_NAME=value
   ```

5. **Log in to Heroku**:
   ```bash
   heroku login
   ```

6. **Create a new Heroku app**:
   ```bash
   heroku create your-app-name
   ```

7. **Add a Git remote for Heroku**:
   ```bash
   heroku git:remote -a your-app-name
   ```

8. **Deploy your application**:
   ```bash
   git add .
   git commit -m "Deploying to Heroku"
   git push heroku main
   ```

9. **Scale your worker**:
   ```bash
   heroku ps:scale worker=1
   ```

10. **Verify the Deployment** by checking the logs:
    ```bash
    heroku logs --tail
    ```

## Running Unit Tests

To run the unit tests for the Prefect pipeline and the Flask app:

1. Run the Flask tests:
   ```bash
   python -m unittest tests/test_flask_app.py
   ```

2. Run the pipeline tests:
   ```bash
   python -m unittest tests/test_pipeline.py
   ```

## Notes

- The dataset is fetched from FHFA: [FHFA HPI Data](https://www.fhfa.gov/hpi/download/monthly/hpi_master.csv)
- The model is a simple Linear Regression model to predict the **seasonally adjusted index** (`index_sa`).
