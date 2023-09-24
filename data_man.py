import pandas as pd 

class data_explore: 

    """
    A class for exploring and cleaning data.

    Attributes:
        df (DataFrame): The input data frame.
        name (str): The name of the file.

    Methods:
        data_cleaning(): Cleans the data by dropping rows with -9999 values and saves the cleaned data to a CSV file.
    """

    def __init__(self, df, file_name) -> None:

        self.df = df
        self.name = file_name

        """
        Initializes the data_explore object.

        Args:
            df (DataFrame): The input data frame.
            file_name (str): The name of the file.
        """

    def data_celaning(self):

        """
        Cleans the data by dropping rows with -9999 values and saves the cleaned data to a CSV file.
        """

        df_columns = ["year", "month", "day", "Mean T", "Maximum T", "Minimum T"]

        self.df.columns = df_columns

        print((self.df == -9999).any())

        for col in df_columns:
            print("Column name = ", col)

            df_clean = self.df.drop(self.df[self.df[col] == -9999].index)

        print((df_clean == -9999).any())

        df_clean.to_csv(self.name + "_Clean.csv")

        return df_clean


