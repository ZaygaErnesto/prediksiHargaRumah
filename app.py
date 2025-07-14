import streamlit as st
import pandas as pd
import plotly.express as px
import locale

# Set locale for currency formatting
try:
    locale.setlocale(locale.LC_ALL, 'id_ID')
except locale.Error:
    st.warning("Locale 'id_ID' tidak ditemukan. Menggunakan format default.")

# Function to load and cache data
@st.cache_data
def load_data(path):
    """Loads the cleaned dataset."""
    df = pd.read_csv(path)
    # Convert 'Harga' to numeric, handling potential errors
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    # Convert areas to numeric
    df['surface_area(m2)'] = pd.to_numeric(df['surface_area(m2)'], errors='coerce')
    df['building_area(m2)'] = pd.to_numeric(df['building_area(m2)'], errors='coerce')
    # Drop rows with missing critical values
    df.dropna(subset=['price', 'surface_area(m2)', 'building_area(m2)'], inplace=True)
    return df

# Page Configuration
st.set_page_config(
    page_title="Dasbor Properti Yogyakarta",
    page_icon="��",
    layout="wide"
)

# --- Load Data ---
try:
    df = load_data('rumah123_yogya_cleaned.csv')
except FileNotFoundError:
    st.error("File 'rumah123_yogya_cleaned.csv' tidak ditemukan. Pastikan file berada di direktori yang sama dengan script ini.")
    st.stop()

# Setelah df = pd.read_csv(path)
location_map = {
    0: "Kulon Progo",
    1: "Gunungkidul",
    2: "Sleman",
    3: "Kota Yogyakarta",
    4: "Bantul"
}
df['location'] = df['location'].replace(location_map)


# --- Main Application ---
st.title("🏠 Dasbor Analisis Properti di Yogyakarta")
st.markdown("Dasbor interaktif untuk menganalisis data harga dan spesifikasi properti di wilayah DI Yogyakarta berdasarkan data dari Rumah123.")

# --- Sidebar for Filters ---
st.sidebar.header("Filter Data")
selected_location = st.sidebar.multiselect(
    "Pilih Lokasi (Kabupaten/Kota):",
    options=df['location'].unique(),
    default=df['location'].unique()
)

# Filter data based on sidebar selection
df_filtered = df[df['location'].isin(selected_location)]

# --- Key Metrics ---
st.header("Ringkasan Umum")
col1, col2, col3 = st.columns(3)

avg_price = df_filtered['price'].mean()
avg_land_area = df_filtered['surface_area(m2)'].mean()
total_listings = len(df_filtered)

with col1:
    st.metric(
        label="Rata-rata Harga Properti",
        value=f"Rp {avg_price:,.0f}"
    )

with col2:
    st.metric(
        label="Rata-rata Luas Tanah",
        value=f"{avg_land_area:.1f} m²"
    )

with col3:
    st.metric(
        label="Total Jumlah Properti",
        value=total_listings
    )

st.markdown("---")

# --- Visualizations ---
st.header("Grafik Analisis Properti")

# 1. Price Distribution
st.subheader("Distribusi Harga Properti")
fig_price_dist = px.histogram(
    df_filtered,
    x='price',
    nbins=50,
    title='Sebaran Harga Properti di Lokasi Terpilih',
    labels={'price': 'Harga (dalam Rupiah)'},
    color_discrete_sequence=['#636EFA']
)
fig_price_dist.update_layout(yaxis_title='Jumlah Properti')
st.plotly_chart(fig_price_dist, use_container_width=True)


# 2. Properties per Location
st.subheader("Jumlah Properti per Lokasi")
location_counts = df_filtered['location'].value_counts().reset_index()
location_counts.columns = ['Lokasi', 'Jumlah']
fig_location = px.bar(
    location_counts,
    x='Lokasi',
    y='Jumlah',
    title='Jumlah Properti di Setiap Kabupaten/Kota',
    labels={'Lokasi': 'Kabupaten/Kota', 'Jumlah': 'Jumlah Properti'},
    color='Lokasi'
)
st.plotly_chart(fig_location, use_container_width=True)

# 3. Scatter plot: Price vs. Area
st.subheader("Hubungan Harga dengan Luas Properti")
area_choice = st.radio(
    "Pilih Tipe Luas:",
    ('surface_area(m2)', 'building_area(m2)'),
    horizontal=True
)

fig_scatter = px.scatter(
    df_filtered,
    x=area_choice,
    y='price',
    color='location',
    hover_data=['bed', 'bath'],
    title=f'Harga Properti vs. {area_choice}',
    labels={'price': 'Harga (Rupiah)'}
)
st.plotly_chart(fig_scatter, use_container_width=True)


# 4. Bedroom and Bathroom distribution
st.subheader("Distribusi Jumlah Kamar")
col_kt, col_km = st.columns(2)

with col_kt:
    kt_counts = df_filtered['bed'].value_counts().reset_index()
    kt_counts.columns = ['Kamar Tidur', 'Jumlah']
    fig_kt = px.bar(
        kt_counts,
        x='Kamar Tidur',
        y='Jumlah',
        title='Jumlah Properti Berdasarkan Kamar Tidur',
        labels={'Kamar Tidur': 'Jumlah Kamar Tidur', 'Jumlah': 'Jumlah Properti'},
        color_discrete_sequence=['#00CC96']
    )
    st.plotly_chart(fig_kt, use_container_width=True)

with col_km:
    km_counts = df_filtered['bath'].value_counts().reset_index()
    km_counts.columns = ['Kamar Mandi', 'Jumlah']
    fig_km = px.bar(
        km_counts,
        x='Kamar Mandi',
        y='Jumlah',
        title='Jumlah Properti Berdasarkan Kamar Mandi',
        labels={'Kamar Mandi': 'Jumlah Kamar Mandi', 'Jumlah': 'Jumlah Properti'},
        color_discrete_sequence=['#EF553B']
    )
    st.plotly_chart(fig_km, use_container_width=True)


st.markdown("---")

# --- Display Raw Data ---
st.header("Lihat Data Mentah")
if st.checkbox("Tampilkan data mentah yang telah difilter"):
    st.dataframe(df_filtered)