import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/62823/Downloads/avocado-prices (2)/avocado.csv")
df = df.copy()[df['type'] == 'organic']

df["Date"] = pd.to_datetime(df["Date"])

df.sort_values(by="Date", ascending=True, inplace=True)

print(df.head())  
print(df['region'].unique())

albany_df = df[df['region'] == "Albany"]
albany_df.set_index("Date", inplace=True)
albany_df = albany_df.sort_index()

albany_df["AveragePrice"].rolling(25).mean().plot()

albany_df["price25ma"] = albany_df["AveragePrice"].rolling(25).mean()

albany_df.head()
albany_df.tail()

graph_df = pd.DataFrame()

for region in df['region'].unique()[:16]:
    region_df = df.copy()[df['region'] == region]
    region_df.set_index('Date', inplace=True)
    region_df.sort_index(inplace=True)
    region_df[f"{region}_price25ma"] = region_df["AveragePrice"].rolling(25).mean()

    if graph_df.empty:
        graph_df = region_df[[f"{region}_price25ma"]]
    else:
        graph_df = graph_df.join(region_df[f"{region}_price25ma"])

graph_df.plot(figsize=(8,5), legend=False)

plt.xlabel("Date")
plt.ylim(1.00, 2.75)
plt.legend()
plt.show()
