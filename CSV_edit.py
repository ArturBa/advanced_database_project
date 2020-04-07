import pandas as pd

text = open("waqi-covid19-airqualitydata.csv", "r", encoding="utf8")
text = ''.join([i for i in text]) \
    .replace("Washington, D.C.", "Washington. D.C.")
x = open("edited.csv", "w", encoding="utf8")
x.writelines(text)
x.close()
data = pd.read_csv("edited.csv", skiprows=6)
df = pd.DataFrame(data)
filtered_col = df.drop(columns=['count', 'min', 'max', 'variance'])
filtered_rows = filtered_col[filtered_col['Specie'].isin(['pm25', 'pm10', 'o3', 'so2', 'no2'])]
filtered_rows.reset_index(drop=True, inplace=True)
sorted_data = filtered_rows.sort_values(by=['City', 'Date', 'Specie']).reset_index(drop=True)
final = sorted_data.pivot_table(
    values='median',
    index=['City', 'Date', 'Country'],
    columns='Specie'
)
final.reset_index(inplace=True)
final.columns.name = None
final.to_csv(r'final.csv', index=False)
