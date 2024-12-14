import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for seaborn
sns.set_theme(style="whitegrid")

# Title and Introduction
st.title("Bike Sharing Data Analysis Dashboard")
st.write("""
    Selamat datang di dashboard analisis data Bike Sharing! Dashboard ini menyajikan berbagai analisis terkait pola penyewaan sepeda, 
    termasuk tren musiman, pengaruh cuaca, jam puncak penyewaan, dan pola penggunaan pada hari kerja dan hari libur.
""")

# Load Data
@st.cache
def load_data():
    hour_data = pd.read_csv("cleaned_bikeshare_hour.csv")
    day_data = pd.read_csv("cleaned_bikeshare_day.csv")
    return hour_data, day_data

hour_data, day_data = load_data()

# Sidebar Filter
st.sidebar.header("Filter Options")
season_filter = st.sidebar.multiselect("Filter by Season", options=["Winter", "Spring", "Summer", "Fall"], default=["Winter", "Spring", "Summer", "Fall"])
date_range = st.sidebar.date_input("Select Date Range", [], min_value=pd.to_datetime("2011-01-01"), max_value=pd.to_datetime("2012-12-31"))
temp_range = st.sidebar.slider("Temperature Range", float(day_data['temp'].min()), float(day_data['temp'].max()), (float(day_data['temp'].min()), float(day_data['temp'].max())))
hum_range = st.sidebar.slider("Humidity Range", float(day_data['hum'].min()), float(day_data['hum'].max()), (float(day_data['hum'].min()), float(day_data['hum'].max())))
wind_range = st.sidebar.slider("Wind Speed Range", float(day_data['windspeed'].min()), float(day_data['windspeed'].max()), (float(day_data['windspeed'].min()), float(day_data['windspeed'].max())))
show_weather_analysis = st.sidebar.checkbox("Show Weather Analysis", value=True)
show_peak_hours = st.sidebar.checkbox("Show Peak Hours Analysis", value=True)
show_holiday_analysis = st.sidebar.checkbox("Show Holiday Analysis", value=True)

# Filter data based on sidebar inputs
filtered_data = day_data[
    (day_data['season'].isin(season_filter)) &
    (day_data['temp'].between(temp_range[0], temp_range[1])) &
    (day_data['hum'].between(hum_range[0], hum_range[1])) &
    (day_data['windspeed'].between(wind_range[0], wind_range[1]))
]

if date_range and len(date_range) == 2:
    filtered_data['dteday'] = pd.to_datetime(filtered_data['dteday'])
    filtered_data = filtered_data[(filtered_data['dteday'] >= pd.to_datetime(date_range[0])) & (filtered_data['dteday'] <= pd.to_datetime(date_range[1]))]

# Seasonal Trends
st.header("Seasonal Trends in Bike Rentals")
seasonal_trends = filtered_data.groupby('season')[['casual', 'registered', 'cnt']].mean().reset_index()
st.write("Rata-rata Penyewaan Sepeda Berdasarkan Musim:")
st.bar_chart(seasonal_trends.set_index('season'))

# Weather Impact Analysis
if show_weather_analysis:
    st.header("Impact of Weather on Bike Rentals")
    st.write("**Correlation Heatmap**: Analisis hubungan antara cuaca dan penyewaan sepeda.")
    correlation_weather = filtered_data[['temp', 'hum', 'windspeed', 'cnt']].corr()
    fig, ax = plt.subplots()
    sns.heatmap(correlation_weather, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

# Peak Hours Analysis
if show_peak_hours:
    st.header("Peak Hours Analysis")
    hourly_rentals = hour_data.groupby(['hr', 'workingday'])['cnt'].mean().reset_index()
    st.write("Penyewaan rata-rata berdasarkan jam dan hari kerja:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=hourly_rentals, x='hr', y='cnt', hue='workingday', marker='o', palette='Set2', ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda per Jam (Weekday vs Weekend)")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.legend(title="Hari Kerja", labels=["Akhir Pekan (0)", "Hari Kerja (1)"])
    st.pyplot(fig)

# Holiday Impact Analysis
if show_holiday_analysis:
    st.header("Holiday Impact on Bike Rentals")
    holiday_effect = filtered_data.groupby('holiday')[['casual', 'registered', 'cnt']].mean().reset_index()
    st.write("Penyewaan sepeda rata-rata pada hari libur vs hari biasa:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=holiday_effect.melt(id_vars='holiday', var_name='User Type', value_name='Average Rentals'),
        x='holiday',
        y='Average Rentals',
        hue='User Type',
        palette='coolwarm',
        ax=ax
    )
    ax.set_title("Pengaruh Hari Libur terhadap Penyewaan Sepeda")
    ax.set_xlabel("Hari Libur (0: Non-Holiday, 1: Holiday)")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.legend(title="Tipe Pengguna")
    st.pyplot(fig)

# Footer
st.write("**Terima Kasih telah menggunakan dashboard ini!**")
