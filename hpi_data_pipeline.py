import pandas as pd
import pickle
from prefect import flow, task
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error
import numpy as np

# Task 1: Load the data from the provided URL
@task
def load_hpi_data():
    url = "https://www.fhfa.gov/hpi/download/monthly/hpi_master.csv"
    data = pd.read_csv(url)
    return data

# Task 2: Preprocess the data (filter relevant columns, handle missing values)
@task
def preprocess_hpi_data(data):
    relevant_columns = ['hpi_type', 'hpi_flavor', 'frequency', 'level', 'place_name', 'place_id', 'yr', 'period', 'index_nsa', 'index_sa']
    data = data[relevant_columns]
    data = data.dropna(subset=['index_sa'])
    data['date'] = pd.to_datetime(data['yr'].astype(str) + '-' + data['period'].astype(str), format='%Y-%m')
    return data

# Task 3: Perform feature engineering (encode categorical features using OneHotEncoder)
@task
def feature_engineering(data):
    categorical_columns = ['hpi_type', 'hpi_flavor', 'level', 'frequency', 'place_name', 'place_id']

    # Initialize OneHotEncoder
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')

    # Fit and transform categorical columns
    encoded_features = encoder.fit_transform(data[categorical_columns])

    # Create a DataFrame with the encoded features and concatenate it with the original data
    encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_columns))

    # Drop the original categorical columns and concatenate the encoded features
    data = data.drop(columns=categorical_columns)
    data = pd.concat([data.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)

    return data, encoder

# Task 4: Train a linear regression model
@task
def train_model(data):
    X = data.drop(columns=['index_sa', 'date', 'index_nsa'])
    y = data['index_sa']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    return model, X_test, y_test, y_train

# Task 5: Evaluate the model using Mean Squared Error (MSE)
@task
def evaluate_model(model, X_test, y_test, y_train):
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    # Calculate baseline MSE (predicting the mean for all)
    y_mean_pred = np.full_like(y_test, np.mean(y_train))
    baseline_mse = mean_squared_error(y_test, y_mean_pred)

    # Calculate variance of the target variable in the test set
    variance = np.var(y_test)

    # Threshold: let's say a model is good if its MSE is less than 75% of the baseline MSE
    threshold = baseline_mse * 0.75

    # Output MSE and evaluation
    print(f"Mean Squared Error (MSE) of the model: {mse}")
    print(f"Baseline MSE (predicting the mean): {baseline_mse}")
    print(f"Variance of target variable in test set: {variance}")

    # Evaluate if the MSE is good
    if mse < threshold:
        print(f"The MSE is good as it is less than {threshold:.2f} (75% of baseline MSE).")
    elif mse < variance:
        print("The MSE is acceptable as it is less than the variance of the target variable.")
    else:
        print("The MSE is relatively high. Consider improving the model.")

    print(f"Mean Squared Error: {mse}")
    return mse

# Task 6: Save the trained model, encoder, and feature names
@task
def save_model_and_encoder(model, encoder, feature_names):
    # Save the model
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)

    # Save the encoder
    with open('encoder.pkl', 'wb') as f:
        pickle.dump(encoder, f)

    # Save the feature names
    with open('feature_names.pkl', 'wb') as f:
        pickle.dump(feature_names, f)

# Prefect Flow: Complete pipeline for training the model and saving components
@flow
def house_price_index_pipeline():
    # Step 1: Load data
    hpi_data = load_hpi_data()

    # Step 2: Preprocess the data
    preprocessed_data = preprocess_hpi_data(hpi_data)

    # Step 3: Perform feature engineering
    engineered_data, encoder = feature_engineering(preprocessed_data)

    # Step 4: Train the model
    model, X_test, y_test, y_train = train_model(engineered_data)

    # Step 5: Evaluate the model
    mse = evaluate_model(model, X_test, y_test, y_train)

    # Step 6: Save model, encoder, and feature names
    save_model_and_encoder(model, encoder, list(engineered_data.columns))

# Run the flow
if __name__ == "__main__":
    house_price_index_pipeline.serve(name="house-price-deployment", cron="* * * * *")

