# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 12:27:58 2023

@author: anish
"""

# Importing the required packages
import pandas as pd
import matplotlib.pyplot as plt


def read_data(filename):
    '''
    This is a function which takes the filename (dataset) as the input and
    return the tuple having two dataframes one with year as columns and other
    with country names as columns.
    '''

    # List of the selected indicator
    indicator_list = [
        "Electricity production from oil sources (% of total)",
        "Electricity production from nuclear sources (% of total)",
        "Electricity production from natural gas sources (% of total)",
        "Electricity production from hydroelectric sources (% of total)",
        "Electricity production from coal sources (% of total)",
        "Electric power consumption (kWh per capita)",
        "Population, total"]

    # List of selected Countries
    country_list = ["Australia", "Bangladesh", "Canada", "Germany",
                    "France", "Japan", "Sri Lanka", "United States",
                    "United Kingdom"]

    # Dictonary for mapping the indicators
    col_map = {
        "Electricity production from oil sources (% of total)":
            "Electricity by Oil",
        "Electricity production from nuclear sources (% of total)":
            "Electricity by Nuclear",
        "Electricity production from natural gas sources (% of total)":
            "Electricity by Natural Gas",
        "Electricity production from hydroelectric sources (% of total)":
            "Electricity by Hydroelectric",
        "Electricity production from coal sources (% of total)":
            "Electricity by Coal",
        "Electric power consumption (kWh per capita)":
            "Electric power consumption",
        "Population, total":
            "Total population"}

    # Reading the dataframe as CSV and skipping the first 4 rows
    df = pd.read_csv(filename, skiprows=4)

    # Dropping the column names 'Unnamed: 67'
    df.drop("Unnamed: 67", axis=1, inplace=True)

    # Get the selected fields and data from the originial dataframe
    df_sub = df[df["Indicator Name"].isin(indicator_list) & df["Country Name"].
                isin(country_list)]

    # Drop the Unnecessary colunns from the data
    df_sub.drop(["Country Code", "Indicator Code"], axis=1, inplace=True)

    # Drop NaN values using dropna along columns
    clean_data = df_sub.dropna(axis=1)

    # Replace the field names using replace method in dataframe
    clean_data.replace(col_map, inplace=True)

    # Set the multiindex using Country name and Indicator name
    year_col_df = clean_data.set_index(['Country Name', 'Indicator Name'])

    # Creating a dataframe having countries as column names
    country_col_df = year_col_df.stack().unstack(level=0)

    # Returns a tuple with year as column and countries as column
    return year_col_df, country_col_df

def stats_analysis(df, country_name):

    '''
    This is a function which takes a dataframe and country name as arguments
    and gives out some statistical anaylsis (Mean, Standard Deviation...etc) on
    the data with respective to the countries. It also show the dataframe
    describe method which gives out information regarding the data such as
    count, min, max, mean..etc.
    '''

    # Extraction of the data
    df_country = df.loc[:, country_name].unstack()
    df_country_describe = df_country.T.describe()
    print(df_country_describe)

    # Data for plotting
    mean_data = df_country_describe.loc["mean"]
    std_data = df_country_describe.loc["std"]

    # Intialization of the figure
    plt.figure(figsize=(8, 4))

    # Calling the plot function to display lineplot
    plt.scatter(mean_data.index, mean_data, label="Mean")
    plt.scatter(std_data.index, std_data,
             label="Standard Deviation")

    # Define the plot title
    plt.title("Statistical Analysis on " + country_name + " data")

    # Axes labelling
    plt.xlabel("Indicator Name")

    # Mention ticks
    plt.xticks(rotation=45)

    # Display grid
    plt.grid()

    # Display legend
    plt.legend()

    # Display plot
    plt.show()


def energy_consumption_plot(df):
    '''
    This is a function to create a barplot using the dataframe. Here we take
    the data from the dataframe and plot subplots for two different year
    periods and plot grouped bar plot for variation in energy consumption with
    respective to year.
    '''

    # Data for plotting
    bar_90_to_94 = df.loc[:, "1990":"1994"]
    bar_90_to_94 = bar_90_to_94.loc[bar_90_to_94.index.get_level_values(
        "Indicator Name") == "Electric power consumption"]
    bar_90_to_94 = bar_90_to_94.droplevel("Indicator Name")

    bar_10_to_14 = df.loc[:, "2010":"2014"]
    bar_10_to_14 = bar_10_to_14.loc[bar_10_to_14.index.get_level_values(
        "Indicator Name") == "Electric power consumption"]
    bar_10_to_14 = bar_10_to_14.droplevel("Indicator Name")

    # Intialization of the figure and subplots
    fig, ax = plt.subplots(1, 2, figsize=(15, 8))

    # Plotting on the first subplot (ax1)
    ax1 = plt.subplot(1, 2, 1)
    bar_90_to_94.plot(kind="bar", ax=ax1, colormap='Paired')
    ax1.legend()
    ax1.grid()

    # Plotting on the second subplot (ax2)
    ax2 = plt.subplot(1, 2, 2)
    bar_10_to_14.plot(kind="bar", ax=ax2, colormap="rainbow")
    ax2.legend()
    ax2.grid()

    # Define the suptitle for the plot
    plt.suptitle("Electric power consumption (kWh per capita)")

    # Adjust space between subplots
    plt.tight_layout()

    # Save figure as png
    plt.savefig("electricity.png")

    # To display the plot
    plt.show()


def population_plot(df):
    '''
    This is a function to create a barplot using the dataframe. Here we take
    the data from the dataframe and plot subplots for two different year
    periods and plot grouped bar plot for variation in total population of
    different countries with respective to year.
    '''

    # Data for plotting
    bar_90_to_94 = df.loc[:, "1990":"1994"]
    bar_90_to_94 = bar_90_to_94.loc[bar_90_to_94.index.get_level_values(
        "Indicator Name") == "Total population"]
    bar_90_to_94 = bar_90_to_94.droplevel("Indicator Name")

    bar_10_to_14 = df.loc[:, "2010":"2014"]
    bar_10_to_14 = bar_10_to_14.loc[bar_10_to_14.index.get_level_values(
        "Indicator Name") == "Total population"]
    bar_10_to_14 = bar_10_to_14.droplevel("Indicator Name")

    # Intialization of the figure and subplots
    fig, ax = plt.subplots(1, 2, figsize=(15, 8))

    # Plotting on the first subplot (ax1)
    ax1 = plt.subplot(1, 2, 1)
    bar_90_to_94.plot(kind="bar", ax=ax1, colormap='Paired')
    ax1.legend()
    ax1.grid()

    # Plotting on the second subplot (ax2)
    ax2 = plt.subplot(1, 2, 2)
    bar_10_to_14.plot(kind="bar", ax=ax2, colormap="rainbow")
    ax2.legend()
    ax2.grid()

    # Define the title for the plot
    plt.suptitle("Population Total")

    # Adjust space between subplots
    plt.tight_layout()

    # Save figure as png
    plt.savefig("population.png")

    # To display the plot
    plt.show()


def electricity_sources_plot(df, country_name):
    '''
    This is a function to create a lineplot using the dataframe and a country
    name. Here we take the data from the dataframe and plot line graph for
    different soucres of Electricity Production in the given country.
    '''

    # Intialization of the figure
    plt.figure()

    # Data for plotting
    country_df = df.loc[df.index.get_level_values(
        "Country Name") == country_name]

    # Drop the unwanted data fields
    string_to_drop = ["Electric power consumption", "Total population"]
    for s in string_to_drop:
        country_df = country_df[country_df.index.get_level_values(
            "Indicator Name") != s]
    country_df = country_df.droplevel("Country Name")

    # Calling the plot function to plot bar graph
    country_df.T.plot(kind='line', figsize=(10, 6))

    # Define the suptitle for the plot
    plt.suptitle("Electricity Production from different sources (% of total)")

    # Define the title for the plot
    plt.title(country_name)

    # Save figure as png
    plt.savefig("electricity_sources.png")

    # To display the plot
    plt.show()


def correlation_country_plot(df, country_name):
    '''
    This is a function to create a correlation matrix using the dataframe and a
    country name. Here we take the data from the dataframe and compare the
    correlation of each indicator with the other and plot it.
    '''

    # Intialization of the figure
    plt.figure()

    # Data for plotting
    df_country = df.loc[df.index.get_level_values("Country Name")
                        == country_name]

    # Drop the unwanted data fields
    df_country = df_country.droplevel("Country Name")

    # Create the correlation matrix
    corr_matrix = df_country.T.corr()

    # Intialization of the figure with figsize
    plt.figure(figsize=(6, 6))

    # Display the plot
    plt.imshow(corr_matrix)

    # Set the color map
    plt.set_cmap("cool")

    # Display the color bar
    plt.colorbar()

    # Display the values on the matrix
    for i in range(len(corr_matrix)):
        for j in range(len(corr_matrix)):
            plt.text(
                j, i, f"{corr_matrix.iloc[i, j]:.2f}", ha='center', va='center'
                , color='black')

    # Define the title for the plot
    plt.title(country_name)

    # To set the current tick locations and labels of the x-axis and y-axis
    plt.xticks(range(len(corr_matrix)), corr_matrix.columns, rotation=90)
    plt.yticks(range(len(corr_matrix)), corr_matrix.columns)

    # Save figure as png
    plt.savefig("correlation_"+ country_name +".png")

    # To display the plot
    plt.show()


def main():
    # Get the dataframe by calling the read_data method
    year_col_df, country_col_df = read_data("API_19_DS2_en_csv_v2_5998250.csv")

    # Calling the energy consumption function for bar plot
    energy_consumption_plot(year_col_df)

    # Calling the Population plot function for bar plot
    population_plot(year_col_df)

    # Calling the electricity sources function for line plot
    electricity_sources_plot(year_col_df, "United Kingdom")

    # Calling correlation function for the correlation matrix plot
    correlation_country_plot(year_col_df, "United Kingdom")
    correlation_country_plot(year_col_df, "United States")

    # Calling the stats_analysis method to do some statistics analysis
    stats_analysis(country_col_df, "United States")

if __name__ == "__main__":
    # Start of the program from here by calling main()
    main()
