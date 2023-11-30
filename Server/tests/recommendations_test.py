import unittest
from unittest.mock import patch
import pandas as pd
import sys
import os

lambda_dir_path = os.path.join(os.path.dirname(__file__), '..', 'lambda')

sys.path.append(lambda_dir_path)

from recommendation_functions import get_date_range, get_weights, fetch_stock_data


class TestGetDateRange(unittest.TestCase):

    def test_weekly_frequency(self):
        start_date, end_date = get_date_range('Weekly')
        self.assertTrue((end_date - start_date).days <= 30)

    def test_monthly_frequency(self):
        start_date, end_date = get_date_range('Monthly')
        self.assertTrue((end_date - start_date).days <= 90)

    def test_quarterly_frequency(self):
        start_date, end_date = get_date_range('Quarterly')
        self.assertTrue((end_date - start_date).days <= 180)

    def test_semi_annually_frequency(self):
        start_date, end_date = get_date_range('Semi-Annually')
        self.assertTrue((end_date - start_date).days <= 365)

    def test_annually_frequency(self):
        start_date, end_date = get_date_range('Annually')
        self.assertTrue((end_date - start_date).days <= 730)

    def test_invalid_frequency(self):
        with self.assertRaises(ValueError):
            get_date_range('Invalid')


class TestGetWeights(unittest.TestCase):

    def test_low_risk(self):
        expected_weights = {'Monthly Returns': 0.1, 'Volatility': 0.6, 'Momentum': 0.1, 'Sharpe Ratio': 0.2}
        self.assertEqual(get_weights('Low'), expected_weights)

    def test_medium_risk(self):
        expected_weights = {'Monthly Returns': 0.3, 'Volatility': 0.2, 'Momentum': 0.3, 'Sharpe Ratio': 0.2}
        self.assertEqual(get_weights('Medium'), expected_weights)

    def test_high_risk(self):
        expected_weights = {'Monthly Returns': 0.4, 'Volatility': 0.1, 'Momentum': 0.4, 'Sharpe Ratio': 0.1}
        self.assertEqual(get_weights('High'), expected_weights)

    def test_invalid_risk(self):
        with self.assertRaises(ValueError):
            get_weights('Invalid')


class TestFetchStockData(unittest.TestCase):

    @patch('yfinance.download')
    def test_fetch_data(self, mock_download):
        mock_download.return_value = pd.DataFrame({'Adj Close': [100, 101, 102]},
                                                  index=[pd.Timestamp('2023-01-01'), pd.Timestamp('2023-01-02'),
                                                         pd.Timestamp('2023-01-03')])
        data = fetch_stock_data(['AAPL'], '2023-01-01', '2023-01-03')
        self.assertTrue(not data.empty)
        self.assertIn('AAPL', data.columns)


if __name__ == '__main__':
    unittest.main()
