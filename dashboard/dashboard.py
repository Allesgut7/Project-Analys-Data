import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def create_season_summary(df):
    # Mengonversi kolom 'season' menjadi label yang lebih mudah dipahami
    df['season'] = df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

    # Melihat ringkasan total penggunaan sepeda berdasarkan musim
    season_summary = df.groupby('season')['cnt'].sum().reset_index()

    return season_summary

def create_holiday_summary(df):
    # Membuat dataframe baru yang merangkum rata-rata penggunaan sepeda pada hari libur dan hari biasa
    holiday_summary_df = df.groupby('holiday')['cnt'].sum().reset_index()

    # Mengonversi nilai 0 dan 1 pada kolom 'holiday' menjadi lebih deskriptif
    holiday_summary_df['holiday'] = holiday_summary_df['holiday'].map({0: 'Workingday', 1: 'Holiday'})

    # Menampilkan isi dataframe baru
    return holiday_summary_df

def create_weather_summary(df):
    # Mengonversi kolom 'weathersit' menjadi label yang lebih mudah dipahami
    df['weathersit'] = df['weathersit'].map({
        1: 'Cerah',
        2: 'Kabut',
        3: 'Salju ringan',
        4: 'Hujan deras'
    })

    # Membuat dataframe baru yang merangkum jumlah penggunaan sepeda berdasarkan kondisi cuaca
    weather_summary_df = df.groupby('weathersit')['cnt'].sum().reset_index()

    # Menampilkan isi dataframe baru
    return weather_summary_df

def bike_user_distribution(df):
    # Menghitung total penggunaan sepeda berdasarkan tipe pengguna
    user_summary_df = df.groupby(['casual', 'registered'])['cnt'].sum().reset_index()

    # Menambahkan kolom untuk tipe pengguna
    user_summary_df['user_type'] = user_summary_df.apply(lambda row: 'Casual' if row['casual'] > 0 else 'Registered', axis=1)

    # Menghitung total penggunaan untuk setiap tipe pengguna
    user_counts = df.groupby(['casual', 'registered']).sum()['cnt'].reset_index()
    user_counts['user_type'] = user_counts.apply(lambda row: 'Casual' if row['casual'] > 0 else 'Registered', axis=1)

    # Menghitung total penggunaan berdasarkan tipe pengguna
    total_counts = user_counts.groupby('user_type')['cnt'].sum()
    return total_counts

main_df = pd.read_csv("https://raw.githubusercontent.com/Allesgut7/Project-Analys-Data/refs/heads/main/dashboard/main_data_hour.csv")

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://static.vecteezy.com/system/resources/previews/007/535/731/original/bike-sharing-rental-service-logo-icon-with-a-bicycle-vector.jpg")

# # Menyiapkan berbagai dataframe
season_summary = create_season_summary(main_df)
holiday_summary_df = create_holiday_summary(main_df)
weather_summary_df = create_weather_summary(main_df)
total_count = bike_user_distribution(main_df)

# plot number of daily orders (2021)
st.header('Dashboard Bike Sharing :sparkles:')
st.subheader('Final Project of Dicoding')

# Visualisasi 1: Total Penggunaan Sepeda Berdasarkan Musim
st.subheader('Total Penggunaan Sepeda Berdasarkan Musim')
fig1, ax1 = plt.subplots()
sns.barplot(x='season', y='cnt', data=season_summary, palette='coolwarm', ax=ax1)
ax1.set_title('Total Penggunaan Sepeda Berdasarkan Musim')
ax1.set_xlabel('Musim')
ax1.set_ylabel('Jumlah Penggunaan Sepeda (cnt)')
st.pyplot(fig1)

# Visualisasi 2: Rata-rata Penggunaan Sepeda pada Hari Libur vs Hari Biasa
st.subheader('Rata-rata Penggunaan Sepeda pada Hari Libur vs Hari Biasa')
fig2, ax2 = plt.subplots()
sns.barplot(x='holiday', y='cnt', data=holiday_summary_df, palette='coolwarm', ax=ax2)
ax2.set_title('Rata-rata Penggunaan Sepeda pada Hari Libur vs Hari Biasa')
ax2.set_xlabel('Tipe Hari')
ax2.set_ylabel('Jumlah Penggunaan Sepeda (cnt)')
st.pyplot(fig2)

# Visualisasi 3: Rata-rata Penggunaan Sepeda Berdasarkan Kondisi Cuaca
st.subheader('Rata-rata Penggunaan Sepeda Berdasarkan Kondisi Cuaca')
fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.barplot(x='weathersit', y='cnt', data=weather_summary_df, palette='coolwarm', ax=ax3)
ax3.set_title('Rata-rata Penggunaan Sepeda Berdasarkan Kondisi Cuaca')
ax3.set_xlabel('Kondisi Cuaca')
ax3.set_ylabel('Jumlah Penggunaan Sepeda (cnt)')
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha='right')  # Memutar label untuk visibilitas yang lebih baik
st.pyplot(fig3)

# Visualisasi 4: Distribusi Penggunaan Sepeda Berdasarkan Tipe Pengguna (Pie Chart)
st.subheader('Distribusi Penggunaan Sepeda Berdasarkan Tipe Pengguna (Casual vs Registered)')
user_counts = total_count
labels = ['Casual', 'Registered']
sizes = [user_counts['Casual'], user_counts['Registered']]
colors = sns.color_palette('pastel')[0:2]  # Menggunakan palet warna Seaborn

# Membuat Pie Chart
fig4, ax4 = plt.subplots(figsize=(8, 8))
ax4.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
ax4.set_title('Persentase Penggunaan Sepeda Berdasarkan Tipe Pengguna')
ax4.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
st.pyplot(fig4)  # Menampilkan pie chart di Streamlit

# Menampilkan Rangkuman Analisis
st.subheader("Rangkuman Analisis Data Sewa Sepeda")
st.write("""
1. **Musim**: Tidak terdapat perbedaan signifikan dalam jumlah sewa sepeda antara musim-musim yang berbeda, menunjukkan bahwa faktor musiman tidak terlalu mempengaruhi keputusan pelanggan untuk menyewa sepeda.
2. **Hari Libur**: Jumlah sewa sepeda pada hari kerja jauh lebih tinggi dibandingkan dengan hari libur. Hal ini mengindikasikan bahwa pelanggan lebih cenderung menyewa sepeda untuk kebutuhan transportasi sehari-hari.
3. **Kondisi Cuaca**: Cuaca sangat mempengaruhi perilaku penyewa. Saat cuaca buruk, terutama pada hujan deras, jumlah sewa sepeda menurun secara signifikan, mencerminkan bahwa pelanggan menghindari penggunaan sepeda dalam kondisi yang tidak nyaman.

### Penutup
Analisis ini memberikan wawasan berharga yang dapat membantu penyedia layanan dalam merencanakan strategi bisnis yang lebih baik untuk meningkatkan partisipasi dan kepuasan pelanggan di masa mendatang.
""")