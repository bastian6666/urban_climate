import pandas as pd
from data_M import data_explore

df1 = pd.read_csv("data/urban_warm_2013.csv")
df2 = pd.read_csv("data/grass_warm_2013.csv")
df3 = pd.read_csv("data/crop_warm_2013.csv")

df11, df22, df33 = data_explore(df1, df2, df3).mean_hours_value()

print(df11)
print(df22)
print(df33)

# Save the data frames to csv files
df11.to_csv("data_clean/urban_warm_2013.csv", index=False)
df22.to_csv("data_clean/grass_warm_2013.csv", index=False)
df33.to_csv("data_clean/crop_warm_2013.csv", index=False)