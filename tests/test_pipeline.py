import unittest
from prefect import flow
from hpi_data_pipeline import load_hpi_data, preprocess_hpi_data, feature_engineering

class TestPipeline(unittest.TestCase):

    @flow
    def test_load_hpi_data(self):
        # Test loading data using Prefect flow
        data = load_hpi_data.submit().result()
        self.assertIsNotNone(data)
        self.assertFalse(data.empty)

    @flow
    def test_preprocess_data(self):
        # Test preprocessing using Prefect flow
        data = load_hpi_data.submit().result()
        preprocessed_data = preprocess_hpi_data.submit(data).result()

        # Check that essential columns are present after preprocessing
        self.assertIn('date', preprocessed_data.columns)

        # Adjust this line to expect 'index_sa' to remain, but others might not:
        self.assertIn('index_sa', preprocessed_data.columns)

        # Ensure no missing values remain in 'index_sa'
        self.assertFalse(preprocessed_data['index_sa'].isnull().any())

    @flow
    def test_feature_engineering(self):
        # Test feature engineering using Prefect flow
        data = load_hpi_data.submit().result()
        preprocessed_data = preprocess_hpi_data.submit(data).result()
        engineered_data, _ = feature_engineering.submit(preprocessed_data).result()
        self.assertGreater(engineered_data.shape[1], preprocessed_data.shape[1])

if __name__ == '__main__':
    unittest.main()

