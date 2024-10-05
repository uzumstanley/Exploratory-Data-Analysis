# -*- coding: utf-8 -*-
"""Task 2 - eda_starter.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Sgz8HjDNdVjSqo_gC74TaDltZYHUda3A

# Exploratory Data Analysis Starter

## Import packages
"""

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Shows plots in jupyter notebook
# %matplotlib inline

# Set plot style
sns.set(color_codes=True)

"""---

## Loading data with Pandas

We need to load `client_data.csv` and `price_data.csv` into individual dataframes so that we can work with them in Python. For this notebook and all further notebooks, it will be assumed that the CSV files will the placed in the same file location as the notebook. If they are not, please adjust the directory within the `read_csv` method accordingly.
"""

client_df = pd.read_csv('/content/drive/MyDrive/BCCG/DATA/client_data (1).csv')
price_df = pd.read_csv('/content/drive/MyDrive/BCCG/DATA/price_data (1).csv')

"""You can view the first 3 rows of a dataframe using the `head` method. Similarly, if you wanted to see the last 3, you can use `tail(3)`"""

client_df.head(10)

price_df.head(10)

"""---

## Descriptive statistics of data

### Data types

It is useful to first understand the data that you're dealing with along with the data types of each column. The data types may dictate how you transform and engineer features.

To get an overview of the data types within a data frame, use the `info()` method.
"""

client_df.info()

# Check for missing values in client_df
print(client_df.isnull().sum())

# Check for missing values in price_df
print(price_df.isnull().sum())

price_df.info()

"""### Statistics

Now let's look at some statistics about the datasets. We can do this by using the `describe()` method.
"""

client_df.describe()

price_df.describe()

"""---

## Data visualization

If you're working in Python, two of the most popular packages for visualization are `matplotlib` and `seaborn`. We highly recommend you use these, or at least be familiar with them because they are ubiquitous!

Below are some functions that you can use to get started with visualizations.
"""

def plot_stacked_bars(dataframe, title_, size_=(18, 10), rot_=0, legend_="upper right"):
    """
    Plot stacked bars with annotations
    """
    ax = dataframe.plot(
        kind="bar",
        stacked=True,
        figsize=size_,
        rot=rot_,
        title=title_
    )

    # Annotate bars
    annotate_stacked_bars(ax, textsize=14)
    # Rename legend
    plt.legend(["Retention", "Churn"], loc=legend_)
    # Labels
    plt.ylabel("Company base (%)")
    plt.show()

def annotate_stacked_bars(ax, pad=0.99, colour="white", textsize=13):
    """
    Add value annotations to the bars
    """

    # Iterate over the plotted rectanges/bars
    for p in ax.patches:

        # Calculate annotation
        value = str(round(p.get_height(),1))
        # If value is 0 do not annotate
        if value == '0.0':
            continue
        ax.annotate(
            value,
            ((p.get_x()+ p.get_width()/2)*pad-0.05, (p.get_y()+p.get_height()/2)*pad),
            color=colour,
            size=textsize
        )

def plot_distribution(dataframe, column, ax, bins_=50):
    """
    Plot variable distirbution in a stacked histogram of churned or retained company
    """
    # Create a temporal dataframe with the data to be plot
    temp = pd.DataFrame({"Retention": dataframe[dataframe["churn"]==0][column],
    "Churn":dataframe[dataframe["churn"]==1][column]})
    # Plot the histogram
    temp[["Retention","Churn"]].plot(kind='hist', bins=bins_, ax=ax, stacked=True)
    # X-axis label
    ax.set_xlabel(column)
    # Change the x-axis to plain style
    ax.ticklabel_format(style='plain', axis='x')

"""Thhe first function `plot_stacked_bars` is used to plot a stacked bar chart. An example of how you could use this is shown below:"""

churn = client_df[['id', 'churn']]
churn.columns = ['Companies', 'churn']
churn_total = churn.groupby(churn['churn']).count()
churn_percentage = churn_total / churn_total.sum() * 100
plot_stacked_bars(churn_percentage.transpose(), "Churning status", (5, 5), legend_="lower right")

"""The second function `annotate_bars` is used by the first function, but the third function `plot_distribution` helps you to plot the distribution of a numeric column. An example of how it can be used is given below:"""

consumption = client_df[['id', 'cons_12m', 'cons_gas_12m', 'cons_last_month', 'imp_cons', 'has_gas', 'churn']]

fig, axs = plt.subplots(nrows=1, figsize=(18, 5))

plot_distribution(consumption, 'cons_12m', axs)

import matplotlib.pyplot as plt
import seaborn as sns # Import seaborn for plotting

# prompt: give me more visualisation

import matplotlib.pyplot as plt
# Plot the distribution of 'cons_gas_12m'
fig, axs = plt.subplots(nrows=1, figsize=(18, 5))
plot_distribution(consumption, 'cons_gas_12m', axs)

# Plot the distribution of 'cons_last_month'
fig, axs = plt.subplots(nrows=1, figsize=(18, 5))
plot_distribution(consumption, 'cons_last_month', axs)

# Plot the distribution of 'imp_cons'
fig, axs = plt.subplots(nrows=1, figsize=(18, 5))
plot_distribution(consumption, 'imp_cons', axs)

# Boxplot of 'cons_12m' by churn status
plt.figure(figsize=(10, 6))
sns.boxplot(x='churn', y='cons_12m', data=consumption)
plt.title('Consumption in the last 12 months by Churn Status')
plt.show()

# Boxplot of 'cons_gas_12m' by churn status
plt.figure(figsize=(10, 6))
sns.boxplot(x='churn', y='cons_gas_12m', data=consumption)
plt.title('Gas Consumption in the last 12 months by Churn Status')
plt.show()

# Scatter plot of 'cons_12m' vs 'cons_gas_12m' colored by churn status
plt.figure(figsize=(10, 6))
sns.scatterplot(x='cons_12m', y='cons_gas_12m', hue='churn', data=consumption)
plt.title('Consumption vs Gas Consumption by Churn Status')
plt.show()

# Correlation matrix heatmap
# Select only numeric columns for correlation calculation
numerical_columns = client_df.select_dtypes(include=['number'])  # Selects only columns with numeric data types
correlation_matrix = numerical_columns.corr()

plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Pairplot of selected variables
sns.pairplot(client_df[['cons_12m', 'cons_gas_12m', 'has_gas', 'churn']], hue='churn')
plt.show()


# Correlation matrix heatmap
# Select only numeric columns for correlation calculation
numerical_columns = client_df.select_dtypes(include=['number'])
correlation_matrix = numerical_columns.corr()

plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Pairplot of selected variables
sns.pairplot(client_df[['cons_12m', 'cons_gas_12m', 'has_gas', 'churn']], hue='churn')
plt.show()