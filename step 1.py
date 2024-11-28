import pandas as pd
import matplotlib.pyplot as plt

# Membaca file CSV
df = pd.read_csv("C:/Users/62823/Downloads/avocado-prices (2)/avocado.csv")

# Periksa nama kolom
print("Kolom yang tersedia:", df.columns)

# Memfilter data untuk region Albany
albany_df = df[df['region'] == "Albany"]

# Periksa apakah filter berhasil
print("Data Albany:", albany_df.head())

# Mengatur indeks menjadi kolom tanggal, gunakan nama kolom yang sesuai
if 'Date' in albany_df.columns:
    albany_df.set_index("Date", inplace=True)
elif 'date' in albany_df.columns:
    albany_df.set_index("date", inplace=True)
else:
    print("Kolom tanggal tidak ditemukan. Periksa dataset Anda.")
    exit()

# Plot data 'AveragePrice' untuk Albany
albany_df['AveragePrice'].plot()
plt.show()
