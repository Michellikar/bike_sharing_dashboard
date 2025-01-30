import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("all_data.csv")  
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# Sidebar
st.sidebar.title("Bike Sharing Dashboard")
option = st.sidebar.selectbox("Pilih Visualisasi", ["Total Peminjaman", "Tren Peminjaman per Jam", 
                                                    "Peminjaman Berdasarkan Cuaca", "Pengaruh Suhu & Kelembaban"])

# Halaman utama
st.title("🚲 Dashboard Bike Sharing Dataset")

# 1️⃣ Total Peminjaman Sepeda
if option == "Total Peminjaman":
    st.subheader("📊 Total Peminjaman Sepeda")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Peminjaman", df['cnt'].sum())
    col2.metric("Casual Users", df['casual'].sum())
    col3.metric("Registered Users", df['registered'].sum())

    # Garis waktu peminjaman
    fig, ax = plt.subplots(figsize=(10, 4))
    df_daily = df.groupby("date")['cnt'].sum().reset_index()
    sns.lineplot(x="date", y="cnt", data=df_daily, ax=ax)
    ax.set_title("Total Peminjaman Sepeda per Hari")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Peminjaman")
    st.pyplot(fig)

# 2️⃣ Tren Peminjaman Berdasarkan Jam
elif option == "Tren Peminjaman per Jam":
    st.subheader("⏳ Peminjaman Sepeda Berdasarkan Jam")
    fig = px.box(df, x="hr", y="cnt", title="Distribusi Peminjaman Sepeda per Jam", color="hr")
    st.plotly_chart(fig)

# 3️⃣ Peminjaman Berdasarkan Cuaca
elif option == "Peminjaman Berdasarkan Cuaca":
    st.subheader("🌤️ Peminjaman Sepeda Berdasarkan Kondisi Cuaca")
    weather_counts = df.groupby("weathersit")["cnt"].sum().reset_index()
    weather_labels = {1: "Cerah", 2: "Mendung", 3: "Hujan"}
    weather_counts["weathersit"] = weather_counts["weathersit"].map(weather_labels)

    fig = px.pie(weather_counts, names="weathersit", values="cnt", title="Distribusi Peminjaman Berdasarkan Cuaca")
    st.plotly_chart(fig)

# 4️⃣ Pengaruh Suhu & Kelembaban
elif option == "Pengaruh Suhu & Kelembaban":
    st.subheader("🌡️ Pengaruh Suhu dan Kelembaban terhadap Peminjaman")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x="temp", y="cnt", hue="hum", data=df, palette="coolwarm", ax=ax)
    ax.set_title("Pengaruh Suhu dan Kelembaban terhadap Jumlah Peminjaman")
    st.pyplot(fig)

# Footer
st.caption(" Copyright (c) Michel Likar Falah 2025")
