import pandas as pd
import numpy as np


try:
    df = pd.read_csv("C:/Users/62823/Downloads/archive/Minimum Wage Data.csv", encoding='latin-1')
    print("File berhasil dibaca.")
except FileNotFoundError:
    print("File tidak ditemukan. Periksa path file.")
    exit()
except UnicodeDecodeError:
    print("Encoding tidak sesuai. Ganti dengan encoding yang benar.")
    exit()


df.rename(columns=lambda x: x.strip(), inplace=True)
if "Low.2018" not in df.columns:
    print("Kolom 'Low.2018' tidak ditemukan. Periksa struktur file.")
    exit()

try:
    df.to_csv("C:/Users/62823/Downloads/archive/Minimum_Wage_Data_Processed.csv", encoding="utf-8", index=False)
    print("File berhasil disimpan dengan nama Minimum_Wage_Data_Processed.csv.")
except Exception as e:
    print(f"Error saat menyimpan file: {e}")
    exit()

try:
    gb = df.groupby("State")
    print("Data berhasil dikelompokkan berdasarkan State.")
except KeyError as e:
    print(f"Kolom 'State' tidak ditemukan: {e}")
    exit()

try:
    alabama_data = gb.get_group("Alabama").set_index("Year").head()
    print("Data untuk Alabama:")
    print(alabama_data)
except KeyError:
    print("Data untuk 'Alabama' tidak ditemukan.")
    exit()

act_min_wage = pd.DataFrame()

for name, group in df.groupby("State"):
    if act_min_wage.empty:
        try:
            act_min_wage = group.set_index("Year")[["Low.2018"]].rename(columns={"Low.2018": name})
        except KeyError:
            print(f"Kolom 'Low.2018' tidak ditemukan untuk {name}.")
    else:
        try:
            act_min_wage = act_min_wage.join(
                group.set_index("Year")[["Low.2018"]].rename(columns={"Low.2018": name})
            )
        except KeyError:
            print(f"Kolom 'Low.2018' tidak ditemukan untuk {name}.")
            continue

print("Deskripsi Statistik:")

min_wage_corr = act_min_wage.replace(0, np.NaN).dropna(axis=1).corr()
print("Korelasi antar negara bagian:")
print(min_wage_corr.head())

issue_df = df[df['Low.2018'] == 0]
print("Data dengan nilai 'Low.2018' = 0:")
print(issue_df.head())
print("Negara bagian dengan data yang hilang:", issue_df['State'].unique())

for problem in issue_df['State'].unique():
    if problem in min_wage_corr.columns:
        print(f"Korelasi hilang untuk {problem}.")

grouped_issues = issue_df.groupby("State")

try:
    alabama_issues = grouped_issues.get_group("Alabama").head(3)
    print("Data masalah untuk Alabama:")
    print(alabama_issues)
    print("Jumlah total nilai 'Low.2018' untuk Alabama:", grouped_issues.get_group("Alabama")['Low.2018'].sum())
except KeyError:
    print("Tidak ada data masalah untuk 'Alabama'.")

for state, data in grouped_issues:
    if data['Low.2018'].sum() != 0.0:
        print(f"Data ditemukan untuk {state}.")
