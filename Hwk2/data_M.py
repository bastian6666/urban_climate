import pandas as pd 
import numpy as np

class data_explore: 

    """
    A class for exploring and cleaning data.

    Attributes:
        df (DataFrame): The input data frame.
        name (str): The name of the file.
    """

    def __init__(self, df1, df2, df3) -> None:

        self.df1 = df1
        self.df2 = df2
        self.df3 = df3  

        """
        The input data frame.   

        Args:
            df (DataFrame): The input data frame.
        """
    
    def mean_hours_value(self):

        """
        Match the time in two data frames.
        """

        # Convert the "time" column to datetime format
        self.df1["T_Local"] = pd.to_datetime(self.df1["T_Local"])
        self.df2["T_Local"] = pd.to_datetime(self.df2["T_Local"])
        self.df3["T_Local"] = pd.to_datetime(self.df3["T_Local"])

        # Set the "time" column as the index
        self.df1.set_index("T_Local", inplace=True)
        self.df2.set_index("T_Local", inplace=True)
        self.df3.set_index("T_Local", inplace=True)

        # Resample the data to hourly frequency and calculate the mean
        df1 = self.df1.resample("H").mean()
        df2 = self.df2.resample("H").mean()
        df3 = self.df3.resample("H").mean()

        # Reset the index
        df1.reset_index(inplace=True)
        df2.reset_index(inplace=True)
        df3.reset_index(inplace=True)

        return df1, df2, df3











        

        

    
