import pandas as pd
import numpy as np
from scipy.stats import kurtosis, spearmanr, pearsonr, kendalltau
from statsmodels.tsa.stattools import adfuller

# Finance
import yfinance as yf
from datetime import datetime
import os


class econometrics:
    @staticmethod
    def descriptives(data):
        """
        Computes descriptive statistics for each numeric column in a DataFrame.

        Parameters:
        data: pandas.DataFrame
            The DataFrame from which the statistics will be calculated.

        Returns:
        pandas.DataFrame
            A DataFrame where each row represents a specific statistic (Mean, Median,
            Min, Max, Standard Deviation, Quartile Deviation, Kurtosis Fisher, Kurtosis
            Pearson, Skewness, Coefficient of Quartile Deviation) and each column
            corresponds to a numeric column from the input DataFrame.
        """
        all_descriptives = []  
        statistics_labels = ["Mean", "Median", "Min", "Max", "St. Deviation", "Quartile Deviation", "Kurtosis Fisher", "Kurtosis Pearson", "Skewness", "Co-efficient of Q.D"]
        first_column = True  

        for name in data.columns:
            if pd.api.types.is_numeric_dtype(data[name]):
                column_data = data[name].dropna()

                statistics_values = [
                    round(column_data.mean(), 2), 
                    round(column_data.median(), 2),
                    round(column_data.min(), 2), 
                    round(column_data.max(), 2), 
                    round(column_data.std(), 2), 
                    round((np.percentile(column_data, 75) - np.percentile(column_data, 25)) / 2, 2),
                    round(kurtosis(column_data, fisher=True, nan_policy='omit'), 4),
                    round(kurtosis(column_data, fisher=False, nan_policy='omit'), 4),
                    round(column_data.skew(), 4),
                    round((np.percentile(column_data, 75) - np.percentile(column_data, 25)) / 2 / column_data.median(), 4) if column_data.median() != 0 else 0
                ]

                if first_column:
                    descriptive_df = pd.DataFrame({'STATISTICS': statistics_labels, name: statistics_values})
                    first_column = False
                else:
                    descriptive_df = pd.DataFrame({name: statistics_values})

                all_descriptives.append(descriptive_df)

        result_df = pd.concat(all_descriptives, axis=1)
        return result_df
        
    @staticmethod
    def correlation(df, method="Pearson", p=False):
        """
        Calculates and prints the correlation matrix and p-values for numeric columns 
        in the provided DataFrame. Supports Pearson, Spearman, and Kendall correlation methods.

        Parameters:
        df: pandas.DataFrame
            The DataFrame for which correlations are calculated.
        method: str, optional
            The method of correlation ('Pearson', 'Spearman', or 'Kendall'). Default is 'Pearson'.
        p: bool, optional
            If True, p-value matrix is also printed; if False, only correlation matrix 
            is printed. Default is False.

        Returns:
        None
            This function prints the correlation matrix and optionally the p-value
            matrix directly to the console.
        """
        def format_p_value(p_value):
            formatted = f"{p_value:0.3f}"
            if formatted.startswith("0."):
                return formatted[1:]
            return formatted

        numeric_df = df.select_dtypes(include=[np.number])
        if method == "Pearson":
            print("=" * 21 + f"\n {method} Correlation\n" + "=" * 21)
        elif method == "Spearman":
            print("=" * 27 + f"\n {method} Rank Correlation\n" + "=" * 27)
        elif method == "Kendall":
            print("=" * 25 + f"\n {method} Tau Correlation\n" + "=" * 25)

        corr_matrix = pd.DataFrame(index=numeric_df.columns, columns=numeric_df.columns)
        pmatrix = pd.DataFrame(index=numeric_df.columns, columns=numeric_df.columns)

        keys = numeric_df.columns.tolist()

        for i, key1 in enumerate(keys):
            for j, key2 in enumerate(keys):
                if i > j:
                    continue

                data1 = numeric_df[key1].dropna()
                data2 = numeric_df[key2].dropna()

                common_index = data1.index.intersection(data2.index)
                data1 = data1.loc[common_index]
                data2 = data2.loc[common_index]

                if len(common_index) < 2:
                    corr_matrix.at[key1, key2] = 'nan'
                    corr_matrix.at[key2, key1] = 'nan'
                    continue

                if method == 'Spearman':
                    correlation, p_value = spearmanr(data1, data2)
                elif method == 'Pearson':
                    correlation, p_value = pearsonr(data1, data2)
                elif method == 'Kendall':
                    correlation, p_value = kendalltau(data1, data2)

                pmatrix.at[key1, key2] = format_p_value(p_value)
                pmatrix.at[key2, key1] = format_p_value(p_value)

                stars = "     "
                if p_value < 0.001:
                    stars = " *** "
                elif p_value < 0.01:
                    stars = " **  "
                elif p_value < 0.05:
                    stars = " *   "
                elif p_value < 0.1:
                    stars = " .   "

                correlation_str = f"{format_p_value(correlation)}{stars}"
                corr_matrix.at[key1, key2] = correlation_str
                corr_matrix.at[key2, key1] = correlation_str

        corr_matrix_str = corr_matrix.to_string(sparsify=True, justify='center')
        explanation = "\n\n--\nSignif. codes:  0.001 '***', 0.01 '**', 0.05 '*', 0.1 '.'"

        print("\n\n>> Correlation Matrix <<\n")
        print(corr_matrix_str + explanation)

        if p:
            print("\n\n>> P-Value Matrix <<\n")
            print(pmatrix.to_string())
            print("\n")
        else:
            print("\n")

    @staticmethod
    def adf(dataframe, maxlag=None, regression='c', autolag='AIC', store=False, regresults=False, handle_na='drop'):
        """
        Perform Augmented Dickey-Fuller (ADF) test on each column in the DataFrame and return a summary table.

        Parameters:
        dataframe: pandas.DataFrame
            The DataFrame containing time series data to be tested.
        maxlag: int, optional
            Maximum number of lags to use. Default is None, which means the lag length is automatically determined.
        regression: str {'c', 'ct', 'ctt', 'nc'}, optional
            Type of regression trend. Default is 'c' for constant only.
            'c' : constant only (default)
            'ct' : constant and trend
            'ctt' : constant, and linear and quadratic trend
            'nc' : no constant, no trend
        autolag: str, optional
            Method to use when automatically determining the lag length among 'AIC', 'BIC', 't-stat'. Default is 'AIC'.
        store: bool, optional
            If True, then the entire regression result is returned. Default is False.
        regresults: bool, optional
            If True, the full regression results are returned. Default is False.
        handle_na: str {'drop', 'fill'}, optional
            How to handle missing values:
            'drop' : drop missing values (default)
            'fill' : fill missing values forward and then backward

        Returns:
        None
            Prints a summary table of the ADF test results for each column in the DataFrame.

        The summary table includes:
        - ADF Statistic
        - Significance codes
        - P-value
        - Number of lags used
        - Number of observations
        - Information Criterion
        - Critical values at 1%, 5%, and 10%
        """
        def adf_test(series):
            # Handle NaN and infinite values
            if handle_na == 'drop':
                series = series.dropna()
            elif handle_na == 'fill':
                series = series.fillna(method='ffill').fillna(method='bfill')

            # Ensure no infinite values
            series = series[np.isfinite(series)]
            
            if series.size == 0:
                return {
                    'adf_stat': np.nan,
                    'Signif. codes': np.nan,
                    'p-value': np.nan,
                    'usedlag': np.nan,
                    'nobs': np.nan,
                    'icbest': np.nan,
                    'critical value 1%': np.nan,
                    'critical value 5%': np.nan,
                    'critical value 10%': np.nan
                }
            
            result = adfuller(series, maxlag=maxlag, regression=regression, autolag=autolag, store=store, regresults=regresults)
            adf_stat = round(result[0], 3)
            p_value = result[1]
            used_lag = result[2]
            n_obs = result[3]
            critical_values = result[4]
            ic_best = round(result[5], 3) if autolag is not None else None

            # Determine significance codes
            if result[1] < 0.001:
                signif_code = '***'
            elif result[1] < 0.01:
                signif_code = '**'
            elif result[1] < 0.05:
                signif_code = '*'
            elif result[1] < 0.1:
                signif_code = '.'
            else:
                signif_code = ' '
                
            summary = {
                'ADF Stat.': adf_stat,
                ' ': signif_code,
                'Number of Lags Used': used_lag,
                'Number of Observations': n_obs,
                'Information Criterion': ic_best,
                '': '',
                'P-Value': format(p_value, '.3f')[1:] if p_value < 1 else format(p_value, '.3f')
            }

            # Adding critical values to the summary
            for key, value in critical_values.items():
                summary[f'critical value {key}'] = round(value, 3)

            if store:
                summary['resstore'] = result[6]

            return summary

        # Apply the ADF test to each column in the DataFrame
        adf_results = dataframe.apply(adf_test)

        # Transform the results into a DataFrame with the desired structure
        result_dict = {series_name: results for series_name, results in adf_results.items()}

        # Create the result DataFrame
        results_df = pd.DataFrame(result_dict)

        print("="*(len("Augmented Dickey-Fuller Test")+2)+"\n"+" Augmented Dickey-Fuller Test"+"\n"+"="*(len("Augmented Dickey-Fuller Test")+2)+"\n")
        print(results_df)
        print("\n--\n"+ "Signif. codes:  0.001 '***', 0.01 '**', 0.05 '*', 0.1 '.'\n")
        

class finance:
    @staticmethod
    def data(ticker_symbol: str, start_date: str, end_date: str, interval: str) -> pd.DataFrame:
        def convert_date_format(date_string):
            return datetime.strptime(date_string, '%d-%m-%Y').strftime('%Y-%m-%d')

        start_date = convert_date_format(start_date)
        end_date = convert_date_format(end_date)

        stock_data = yf.download(ticker_symbol, start=start_date, end=end_date, interval=interval)
        stock_data['Returns'] = stock_data['Adj Close'].pct_change()

        folder_name = "Stocks"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        file_name = f"{folder_name}/{ticker_symbol}_{interval}.csv"
        stock_data.to_csv(file_name)

        return stock_data
