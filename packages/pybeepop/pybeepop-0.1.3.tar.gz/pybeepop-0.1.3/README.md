# pybeepop
[![codecov](https://codecov.io/gh/Choudoufuhezi/pybeepop/graph/badge.svg?token=UPHVWGO1C7)](https://codecov.io/gh/Choudoufuhezi/pybeepop)

Assessing the Influence of Pesticide Usage, Parasitic Factors, and Climate on Honey Bee Populations in the United States (2015-2019)

## Installation

```bash
$ pip install pybeepop
```

## Usage

The `pybeepop` has 4 modules ("analysis", "clean_data", "eda", and "to_ddl"), with the goal of analyzing the bee population project.

```
from pybeepop.analysis import *
from pybeepop.clean_data import *
from pybeepop.eda import *
from pybeepop.to_ddl import *

# read the raw data

data1_path_origin = '../tests/data/original/average_monthly_temperature_by_state_1950-2022.parquet'
data2_path_origin = '../tests/data/original/epest_county_estimates.parquet'
data3_path_origin = '../tests/data/original/save_the_bees.parquet'
data4_path_origin = '../tests/data/original/pollution_2000_2021.parquet'

data1, data2, data3, data4 = read_data(data1_path_origin, data2_path_origin, data3_path_origin, data4_path_origin)

# Write the sql file and load it to database

sql_path = "../tests/scripts/output.sql"
temperature_data_path = "../tests/data/processed/average_monthly_temperature_by_state_1950-2022.csv"

init_tables(sql_path)
create_sql_MonitorStation(temperature_data_path, sql_path)
connection = connect_to_db(3307, 'localhost')
load_sql_to_db(connection, sql_path)

# fetch data from the database and return it as a dataframe

query_monitor_station = """
    SELECT *
    FROM MonitorStation
"""
columns_monitor_station = ['CentroidLongitude', 'CentroidLatitude', 'Year', 'AverageTemperature']
monitor_station_df = query_transform_dataframe(connection, query_monitor_station, columns_monitor_station)

# combine plots into 2 x 2 scale

concat_plots(Illinois_plot_1, Massachusetts_plot_1, Kansas_plot_1, Georgia_plot_1, loss_disease_parasite_path)

# check variance inflation factor (VIF)

vif_path = "../tests/data/processed/vif.csv"
check_vif(data)

# check and generate correlation matrix

correlation_path = "../tests/images/correlation_matrix.png"
correlation(data, correlation_path)

# run linear and non-linear models

linear_model_path = "../tests/models/linear_model.pkl"
shap_train_path = "../tests/images/shap_train.png"
shap_overall_path = "../tests/images/shap_overall.png"
X, y, model = linear_model(data, linear_model_path)
non_linear_model(X, y, shap_train_path, shap_overall_path)

```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`pybeepop` was created by Hanlin Zhao. It is licensed under the terms of the MIT license.

## Credits

`pybeepop` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
