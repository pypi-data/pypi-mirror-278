import pandas as pd
import us


def read_data(data1_origin, data2_origin, data3_origin, data4_origin):
    """
    read all four parquest files, and return them as output

    Parameters:
    -----------
    data1_origin : str
        The path where average_monthly_temperature_by_state_1950-2022.parquet is stored.

    data2_origin : str
        The path where epest_county_estimates.parquet is stored.

    data3_origin : str
        The path where save_the_bees.parquet is stored.

    data4_origin : str
        The path where pollution_2000_2021.parquet is stored.

    Returns:
    -----------
    data1 : pd.DataFrame
        The dataframe that was read from the file named average_monthly_temperature_by_state_1950-2022.parquet.

    data2 : pd.DataFrame
        The dataframe that was read from the file named epest_county_estimates.parquet.

    data3 : pd.DataFrame
        The dataframe that was read from the file named save_the_bees.parquet.

    data4 : pd.DataFrame
        The dataframe that was read from the file named pollution_2000_2021.parquet.

    Examples:
    -----------
    >>> read_data("data/original/average_monthly_temperature_by_state_1950-2022.parquet", "data/original/epest_county_estimates.parquet", "data/original/save_the_bees.parquet", "data/original/pollution_2000_2021.parquet")
    """
    data1 = pd.read_parquet(data1_origin)
    data2 = pd.read_parquet(data2_origin)
    data3 = pd.read_parquet(data3_origin)
    data4 = pd.read_parquet(data4_origin)

    return data1, data2, data3, data4


def clean_data1(data1):
    """
    group by years and states, drop states that are missing from the other three datasets, and calculate the means. 
    Restrict the year from 2015-2019, reset the index, return the output dataframe

    Parameters:
    -----------
    data1 : pd.DataFrame
        The dataframe that was read from the file named average_monthly_temperature_by_state_1950-2022.parquet.

    Returns:
    -----------
    pd.DataFrame
        The filtered dataframe.
    
    Examples:
    -----------
    >>> clean_data1(pd.read_parquet("data/original/average_monthly_temperature_by_state_1950-2022.parquet"))
    """
    group1 = data1.groupby(["year", "state"])
    data1["average_temp"] = group1["average_temp"].transform('mean')
    data1 = data1[["year", "state", "average_temp", "centroid_lon", "centroid_lat"]]
    data1 = data1.drop_duplicates()
    data1 = data1[(data1.year >= 2015) & (data1.year <= 2019)]
    data1 = data1[(data1.state != "Nevada") &
                (data1.state != "Rhode Island") &
                (data1.state != "Michigan") &
                (data1.state != "Delaware") &
                (data1.state != "New Hampshire") &
                (data1.state != 'Nebraska') &
                (data1.state != 'Montana') &
                (data1.state != 'West Virginia') &
                (data1.state != 'Wisconsin') &
                (data1.state != "Iowa") &
                (data1.state != "Vermont") &
                (data1.state != "South Carolina") &
                (data1.state != "Idaho")]

    data1_list = pd.DataFrame(data1["state"].value_counts())
    data1_list = data1_list.index 

    data1.reset_index(drop=True, inplace=True)

    return data1

def clean_data2(data2):
    """
    group by years, states, and name of the comounds, drop states that are missing from the other three datasets and calculate the means. 
    decode the flps code into actual names of the states, restrict the year from 2015-2019, reset the index, return the output dataframe

    Parameters:
    -----------
    data2 : pd.DataFrame
        The dataframe that was read from the file named epest_county_estimates.parquet.

    Returns:
    -----------
    pd.DataFrame
        The filtered dataframe.

    Examples:
    -----------
    >>> clean_data2(pd.read_parquet("data/original/epest_county_estimates.parquet"))
    """
    group2 = data2.groupby(["YEAR", "COMPOUND", "STATE_FIPS_CODE"])
    data2["EPEST_LOW_KG"] = group2["EPEST_LOW_KG"].transform('mean')
    data2["EPEST_HIGH_KG"] = group2["EPEST_HIGH_KG"].transform('mean')
    data2 = data2[["COMPOUND", "YEAR", "STATE_FIPS_CODE", "EPEST_LOW_KG", "EPEST_HIGH_KG"]]
    data2 = data2[(data2["COMPOUND"] == "2,4-D") |
                (data2["COMPOUND"] == "DICAMBA") |
                (data2["COMPOUND"] == "METRIBUZIN") |
                (data2["COMPOUND"] == "GLYPHOSATE") |
                (data2["COMPOUND"] == "CHLORPYRIFOS")]

    data2 = data2.drop_duplicates()

    data2["STATE"] = data2["STATE_FIPS_CODE"].map(lambda x: str(us.states.lookup("0" + str(x))) if len(str(x)) == 1 else str(us.states.lookup(str(x))))
    data2 = data2.drop(["STATE_FIPS_CODE"], axis = 1)
    data2 = data2[(data2.YEAR >= 2015) & (data2.YEAR <= 2019)]

    data2 = data2[(data2.STATE != "Nevada") &
                (data2.STATE != "Idaho") &
                (data2.STATE != "Michigan") &
                (data2.STATE != "Delaware") &
                (data2.STATE != "New Hampshire") &
                (data2.STATE != 'Nebraska') &
                (data2.STATE != 'Montana') &
                (data2.STATE != 'West Virginia') &
                (data2.STATE != 'Wisconsin') &
                (data2.STATE != "Iowa") &
                (data2.STATE != "Vermont") &
                (data2.STATE != "South Carolina") &
                (data2.STATE != "Idaho") &
                (data2.STATE != "Rhode Island")]

    data2_list = pd.DataFrame(data2["STATE"].value_counts())
    data2_list = data2_list.index 

    data2.reset_index(drop=True, inplace=True)

    return data2 


def helper_dataset(data3):
    """
    create a intermediate dataset with two columns("percent_renovated", "percent_lost"),  
    filter out states that are not commonly shared among the existing datasets, and restrict the year 2015-2019, 
    and conduct corresponding aggregated calculation. 

    Parameters:
    -----------
    data3 : pd.DataFrame
        The dataframe that was read from the file named save_the_bees.parquet.

    Returns:
    -----------
    pd.DataFrame
        The filtered dataframe.

    Examples:
    -----------
    >>> clean_data2(pd.read_parquet("data/original/save_the_bees.parquet"))
    """
    data_helper = data3[(data3.year >= 2015) & 
                        (data3.year <= 2019) & 
                        (data3.state != "United States") & 
                        (data3.state != "Other") &
                        (data3.state != "Hawaii") &
                        (data3.state != "Michigan") &
                        (data3.state != 'Nebraska') &
                        (data3.state != 'Montana') &
                        (data3.state != 'West Virginia') &
                        (data3.state != 'Wisconsin') &
                        (data3.state != "Iowa") &
                        (data3.state != "Vermont") &
                        (data3.state != "South Carolina") &
                        (data3.state != "Idaho")]

    data_helper = data_helper.drop_duplicates()

    group_helper = data_helper.groupby(["state", "year"])

    percent_renovated = group_helper['renovated_colonies'].sum()
    percent_renovated /= group_helper['num_colonies'].sum()
    percent_renovated *= 100

    percent_lost = group_helper['lost_colonies'].sum()
    percent_lost /= group_helper['num_colonies'].sum()
    percent_lost *= 100

    percent_renovated.reset_index(drop=True, inplace=True)
    percent_lost.reset_index(drop=True, inplace=True)

    helper_dataset = pd.DataFrame({"percent_renovated": percent_renovated,
                                   "percent_lost": percent_lost})

    return helper_dataset



def clean_data3(data3, helper_dataset):
    """
    group by states and years, conduct corresponding aggrgated calculation, 
    select columns that are needed, restrict the years within the range of 2015
    -2019, and filter out states that are not commonly shared among the existing datasets,
    reset the index.

    Parameters:
    -----------
    data3 : pd.DataFrame
        The dataframe that was read from the file named save_the_bees.parquet.
    
    helper_dataset: pd.DataFrame
        A intermediate dataset with two columns("percent_renovated", "percent_lost")

    Returns:
    -----------
    pd.DataFrame
        The filtered dataframe.

    Examples:
    -----------
    >>> clean_data2(pd.read_parquet("data/original/save_the_bees.parquet"), helper_dataset(pd.read_parquet("data/original/save_the_bees.parquet")))
    """
    data3 = data3.drop_duplicates()

    group3 = data3.groupby(["state", "year"])

    data3["num_colonies"] = group3["num_colonies"].transform('sum')
    data3["max_colonies"] = group3["max_colonies"].transform('max')
    data3["lost_colonies"] = group3["lost_colonies"].transform('sum')
    data3["added_colonies"] = group3["added_colonies"].transform('sum')
    data3["renovated_colonies"] = group3["renovated_colonies"].transform('sum')
    data3["varroa_mites"] = group3["varroa_mites"].transform('mean')
    data3["diseases"] = group3["diseases"].transform('mean')

    data3 = data3[["state", 
                "year", 
                "num_colonies", 
                "max_colonies", 
                "lost_colonies", 
                "percent_lost", 
                "added_colonies", 
                "renovated_colonies", 
                "percent_renovated", 
                "varroa_mites", 
                "diseases"]]


    data3 = data3[(data3.year >= 2015) & 
                (data3.year <= 2019) &
                (data3.state != "United States") & 
                (data3.state != "Other") &
                (data3.state != "Hawaii") &
                (data3.state != "Michigan") &
                (data3.state != 'Nebraska') &
                (data3.state != 'Montana') &
                (data3.state != 'West Virginia') &
                (data3.state != 'Wisconsin') &
                (data3.state != "Iowa") &
                (data3.state != "Vermont") &
                (data3.state != "South Carolina") &
                (data3.state != "Idaho")]

    data3 = data3.drop_duplicates(subset=["state", "year"])

    data3["percent_renovated"] = helper_dataset["percent_renovated"]
    data3["percent_lost"] = helper_dataset["percent_lost"]
    
    # manipulate = pd.DataFrame(data3["state"].value_counts())
    # data3_list = manipulate.index 

    data3.reset_index(drop=True, inplace=True)

    return data3



def helper_dataset2(data2, data3):
    """
    create a intermediate dataset with three columns("Name", "YEAR", "STATE")

    Parameters:
    -----------
    data2 : pd.DataFrame
        The dataframe that was read from the file named epest_county_estimates.parquet.

    data3 : pd.DataFrame
        The dataframe that was read from the file named save_the_bees.parquet.

    Returns:
    -----------
    pd.DataFrame
        The filtered dataframe.

    Examples:
    -----------
    >>> helper_dataset2(pd.read_parquet("data/original/epest_county_estimates.parquet"), pd.read_parquet("data/original/save_the_bees.parquet"))
    """
    data_help_2 = data3[["state", "year", "varroa_mites"]]
    data_help_2["varroa_mites"] = "varroa_mites"
    data_help_2 = data_help_2.rename(columns={"varroa_mites":"COMPOUND",
                                            "year":"YEAR",
                                            "state":"STATE"}) 
    data_help_2 = pd.concat(
        [data2, data_help_2]
    )

    data_help_2 = data_help_2.drop(["EPEST_HIGH_KG", "EPEST_LOW_KG"], axis = 1)
    data_help_2 = data_help_2.rename(columns={"COMPOUND":"Name"})
    return data_help_2


def clean_data4(data4):
    """
    group by states and years, conduct corresponding aggrgated calculation, 
    select columns that are needed, restrict the years within the range of 2015
    -2019, and filter out states that are not commonly shared among the existing datasets,
    reset the index

    Parameters:
    -----------
    data4: pd.Dataframe
        The dataframe that was read from the file named pollution_2000_2021.parquet.

    Returns:
    -----------
    pd.DataFrame
        The filtered dataframe.

    Examples:
    -----------
    >>> clean_data4(pd.read_parquet("data/original/pollution_2000_2021.parquet"))
    """
    group4 = data4.groupby(["Year", "State"]) 

    data4["O3 Mean"] = group4["O3 Mean"].transform("mean")
    data4["O3 AQI"] = group4["O3 AQI"].transform("mean")
    data4["CO Mean"] = group4["CO Mean"].transform("mean")
    data4["CO AQI"] = group4["CO AQI"].transform("mean")
    data4["SO2 Mean"] = group4["SO2 Mean"].transform("mean")
    data4["SO2 AQI"] = group4["SO2 AQI"].transform("mean")
    data4["NO2 Mean"] = group4["NO2 Mean"].transform("mean")
    data4["NO2 AQI"] = group4["NO2 AQI"].transform("mean")

    data4 = data4[["Year",
                "State",
                "O3 Mean",
                "O3 AQI",
                "CO Mean",
                "CO AQI",
                "SO2 Mean",
                "SO2 AQI", 
                "NO2 Mean", 
                "NO2 AQI"]]

    data4 = data4.drop_duplicates()
    data4 = data4[(data4.Year >= 2015) & (data4.Year <= 2019)]
    data4 = data4[(data4.State != "Hawaii") &
                (data4.State != "District Of Columbia") &
                (data4.State != "Alaska") &
                (data4.State != "Nevada") &
                (data4.State != "Rhode Island") & 
                (data4.State != "Delaware") &
                (data4.State != "New Hampshire") &
                (data4.State != "Iowa") &
                (data4.State != "Vermont") &
                (data4.State != "South Carolina") &
                (data4.State != "Idaho")]

    data4 = pd.melt(data4, id_vars=['Year', 'State'], var_name='pollution', value_name='mean/AQI')
    data4[['Pollutant', 'Metric']] = data4['pollution'].str.split(' ', expand=True)
    data4 = data4.pivot(index=["Year", "State", "Pollutant"], columns="Metric", values="mean/AQI").reset_index()
    data4.columns.name = None

    data4_list = pd.DataFrame(data4["State"].value_counts())
    data4_list
    data4_list = data4_list.index 
    return data4







