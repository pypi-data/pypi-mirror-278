import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
import xgboost as xgb
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import shap
    

def query_transform_dataframe(connection, query, columns_selected):
    """
    query and transform data into dataframe

    Parameters:
    -----------
    connection : mysql.connector.connection.MySQLConnection
        An active connection  object to the MySQL database.

    query : str
        The SQL query to be executed.

    columns_selected: List[str]
        A list of column names to be included in the returned DataFrame.

    Returns: 
    -----------
    pd.DataFrame
        A dataframe that contains all the information that has been queried and chosen.

    Examples:
    -----------
    >>> query_transform_dataframe(mysql.connector.connect(host = cpsc368-project-group1-init_db-1', user = 'system', password = '123456', database = 'bee_population_analysis_db', port = 3306), "SELECT * FROM GasConditions", ['GasName', 'State', 'Year', 'MeanValue', 'AverageAQI'])
    """
    cursor = connection.cursor()
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    dataframe = pd.DataFrame(rows, columns=columns_selected)

    return dataframe


def combined_dataframe(monitor_station_df, monitor_df):
    """
    Merge the DataFrames on 'CentroidLongitude', 'CentroidLatitude', and 'Year'

    Parameters:
    -----------
    monitor_station_df : pd.DataFrame
        The monitor station dataframe.

    monitor_df : pd.DataFrame
        The monitor dataframe.

    Returns: 
    -----------
    pd.DataFrame
        A combined dataframe derived from monitor and monitor station dataframe.

    Examples:
    -----------
    >>> combined_dataframe(df_monitor_station, df_monitor)
    """
    combined_df = pd.merge(
        monitor_station_df, 
        monitor_df, 
        how='inner', 
        left_on=['CentroidLongitude', 'CentroidLatitude', 'Year'],
        right_on=['CentroidLongitude', 'CentroidLatitude', 'StationYear']
        )
    
    return combined_df


def temp_dataframe(combined_df):
    """
    Selecting specific columns and creating a new DataFrame
    
    Parameters:
    -----------
    combined_df : pd.DataFrame
        A combined dataframe derived from monitor and monitor station dataframe.

    Returns: 
    -----------
    pd.DataFrame
        A dataframe contains three columns ("State", "Year", "AverageTemperature") derived from combined_df.

    Examples:
    -----------
    >>> combined_dataframe(df_monitor_station, df_monitor)
    """
    temp_df = combined_df[['RiskFactorsReportedState', 'Year', 'AverageTemperature']].copy()

    # Renaming the column 'RiskFactorsReportedState' to 'State'
    temp_df.rename(columns={'RiskFactorsReportedState': 'State'}, inplace=True)

    return temp_df


def final_dataframe(temp_df, pesticide_df, gas_conditions_df, bee_df):
    """
    Merge everything as a final dataframe 

    Parameters:
    ----------- 
    temp_df : pd.DataFrame
        A dataframe contains three columns ("State", "Year", "AverageTemperature") derived from combined_df..
    
    pesticide_df : pd.DataFrame
        The pesticide dataframe.

    gas_conditions_df : pd.DataFrame
        The gas condition dataframe.

    bee_df : pd.DataFrame
        The bee dataframe.

    Returns:
    -----------
    pd.DataFrame
        The final dataframe ready for the analysis.

    Examples:
    -----------
    >>> final_dataframe(df_temp, df_pesticide, bee_df)
    """ 
    merged1 = pd.merge(temp_df, gas_conditions_df, how='inner', 
                left_on=['State', 'Year'], right_on=['State', 'Year'])

    # select response variable %loss from bee_df, and merge by 'State' and 'Year'
    bee1 = bee_df[['PercentLost', 'State', 'Year', 'PercentLostByDisease']].copy()
    data1 = pd.merge(merged1, bee1, how='inner', 
                    left_on=['State', 'Year'], right_on=['State', 'Year'])

    # Pivot the table to transform GasName values into separate columns, with MeanValue as values
    data_pivot = data1.pivot_table(index=['State', 'Year', 'AverageTemperature', 
                                        'PercentLost', 'PercentLostByDisease'],
                                columns='GasName', 
                                values='MeanValue').reset_index()

    # Rename columns to add '_conc' suffix to gas concentration columns
    data_pivot.columns = [str(col) + '_conc' if col not in ['State', 'Year',
                                                            'AverageTemperature', 'PercentLost', 
                                                            'PercentLostByDisease'] else col for col in data_pivot.columns]

    # Now merge the pivoted data back with AverageAQI and PercentLost, and also add pesticide data
    data2 = pd.merge(data_pivot, data1[['State', 'Year', 'PercentLost', 'PercentLostByDisease']].drop_duplicates(), 
                        on=['State', 'Year', 'PercentLost', 'PercentLostByDisease'], 
                        how='left')
    pesticide_df['PesticideEstimate'] = pesticide_df[['LowEstimate', 'HighEstimate']].mean(axis=1)

    # Drop the LowEstimate and HighEstimate columns
    pesticide_df.drop(['LowEstimate', 'HighEstimate'], axis=1, inplace=True)

    data = pd.merge(data2, pesticide_df, on=['State', 'Year'])

    # Drop the O3_conc column
    data.drop('O3_conc', axis=1, inplace=True)

    # Display the final merged DataFrame for analysis
    return data


def check_linearity(data, variable, path):
    """
    Plot to check linearity

    Parameters:
    -----------
    data : pd.DataFrame
        The final dataframe ready for the analysis.

    variable : str
        The variable chosen to investigate its relationship with the percentage lost.

    path : str
        The path to store the plot.

    Returns:
    -----------
    matplotlib.axes.Axes
        The current axes of the plot for further customization, such as setting labels and titles.

    Examples:
    -----------
    >>> check_linearity(data, "AverageTemperature", "images/average_temperature_linearity.png")
    """
    plt.figure(figsize=(10, 6))
    sns.lmplot(x=variable, y='PercentLost', data=data, aspect=1.5)
    plt.suptitle(f'Relationship between {variable} and PercentLost')
    plt.savefig(path)
    plt.close()
    graph = plt.gca()
    return graph

def check_vif(data):
    """
    checking multicollinearity measured by VIF score
    """
    features = data[['AverageTemperature', 'CO_conc', 'NO2_conc', 'SO2_conc', 'PercentLostByDisease', 'PesticideEstimate']]

    # Calculating VIF for each feature
    vif_data = pd.DataFrame()
    vif_data['Variable'] = features.columns
    vif_data['VIF'] = [variance_inflation_factor(features.values, i) for i in range(len(features.columns))]
    return vif_data

def correlation(data, path):
    """
    generate correlation matrix

    Parameters:
    -----------
    data : pd.DataFrame
        The final dataframe ready for the analysis.

    path : str
        The path to store the correlation matrix plot.

    Returns:
    -----------
    matplotlib.axes.Axes
        The current axes of the correlation matrix plot for further customization, such as setting labels and titles.

    Examples:
    -----------
    >>> correlation(data, "images/correlation_matrix.png")
    """
    correlation_matrix = data[['AverageTemperature', 'CO_conc', 'NO2_conc', 'SO2_conc', 'PercentLostByDisease', 'PesticideEstimate']].corr()

    # Set up the matplotlib figure
    plt.figure(figsize=(13, 12))

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='Blues', 
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    
    plt.savefig(path)
    plt.close()
    graph = plt.gca()
    return graph


def linear_model(data, path):
    """
    fit a ordinary least squares(OLS) model 

    Parameters:
    -----------
    data : pd.DataFrame
        The final dataframe ready for the analysis.

    path : str
        The path to store the ordinary least squares(OLS) model.
    
    Returns:
    -----------
    X : pd.DataFrame
        The full dataset for the predictor variables.

    y : pd.Series
        The full dataset for the target(response) variable.

    model : statsmodels.regression.linear_model.RegressionResultsWrapper
        The ordinary least squares(OLS) model.

        
    Examples:
    -----------
    >>> linear_model(data, "models/linear_model.pkl")
    """
    encoder = OrdinalEncoder()

    data['State_encoded'] = encoder.fit_transform(data[['State']])
    # Drop the non-numeric 'State' column if it's still in the DataFrame
    X = data.drop(['PercentLost', 'State'], axis=1)

    # Ensure that 'State_encoded' is used as a predictor
    X['State_encoded'] = data['State_encoded']

    # Add a constant to the model (intercept)
    X = sm.add_constant(X)

    y = data['PercentLost']  # Response variable

    # Fit the regression model
    model = sm.OLS(y, X).fit()

    with open(path, "wb") as p:
        pickle.dump(model, p)

    return X, y, model


def non_linear_model(X, y, shap_train_path, shap_overall_path):
    """
    fit a XGBoost model

    Parameters:
    -----------
    X : pd.DataFrame
        The full dataset for the predictor variables.

    y : pd.Series
        The full dataset for the target(response) variable.
    
    shap_train_path : str
        The path to store the model's shape value summary plot of the training set.

    shap_overall_path : str
        The path to store the model's shape value summary plot of the overall data.

    Returns:
    -----------
    xgb.XGBRegressor
        The XGBoost model

    Examples:
    -----------
    >>> non_linear_model(X, y, "images/shap_train.png", "images/shap_overall.png")
    """
    # train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

    # Initialize XGBoost regressor
    xgb_model = xgb.XGBRegressor(objective ='reg:squarederror', colsample_bytree = 0.3, learning_rate = 0.1,
                                max_depth = 5, alpha = 10, n_estimators = 100)

    # Fit the model
    xgb_model.fit(X_train, y_train)

    # Predict the model
    y_pred = xgb_model.predict(X_test)

    # Compute and print the performance metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")

    # Compute SHAP values
    explainer = shap.TreeExplainer(xgb_model)
    shap_values = explainer.shap_values(X_train)

    # Plot the SHAP values - summary plot
    shap.summary_plot(shap_values, X_train)
    plt.savefig(shap_train_path)
    plt.close()

    shap.summary_plot(shap_values, X, plot_type="bar")
    plt.savefig(shap_overall_path)
    plt.close()

    return xgb_model