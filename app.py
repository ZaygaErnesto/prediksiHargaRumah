import streamlit as st
import pandas as pd
import plotly.express as px
import locale

# Set locale for currency formatting
try:
    locale.setlocale(locale.LC_ALL, 'id_ID')
except locale.Error:
    st.warning("Locale 'id_ID' tidak ditemukan. Menggunakan format default.")

# --- Load and cache data ---
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['surface_area(m2)'] = pd.to_numeric(df['surface_area(m2)'], errors='coerce')
    df['building_area(m2)'] = pd.to_numeric(df['building_area(m2)'], errors='coerce')
    df.dropna(subset=['price', 'surface_area(m2)', 'building_area(m2)'], inplace=True)
    return df

# --- Page config ---
st.set_page_config(
    page_title="🏠 Dasbor Properti Yogyakarta",
    page_icon="🏠",
    layout="wide"
)

# --- Load Data ---
try:
    df = load_data('/mnt/data/rumah123_yogya_cleaned.csv')
except FileNotFoundError:
    st.error("File data tidak ditemukan.")
    st.stop()

# --- Mapping location ---
location_map = {
    0: "Kulon Progo",
    1: "Gunungkidul",
    2: "Sleman",
    3: "Kota Yogyakarta",
    4: "Bantul"
}
df['location'] = df['location'].replace(location_map)

# --- Sidebar Filter ---
st.sidebar.title("🔍 Filter Data")
selected_location = st.sidebar.multiselect(
    "Pilih Kabupaten/Kota:",
    options=df['location'].unique(),
    default=df['location'].unique()
)

# Filter dataset
df_filtered = df[df['location'].isin(selected_location)]

# --- Judul dan deskripsi ---
st.title("🏠 Dasbor Analisis Properti Yogyakarta")
st.markdown("Analisis interaktif harga, luas, dan distribusi properti di wilayah DI Yogyakarta. Data bersumber dari Rumah123.com.")

# --- Ringkasan Utama ---
st.header("✨ Ringkasan Data")
col1, col2, col3 = st.columns(3)

avg_price = df_filtered['price'].mean()
avg_land_area = df_filtered['surface_area(m2)'].mean()
total_listings = len(df_filtered)

with col1:
    st.metric("Rata-rata Harga", f"Rp {avg_price:,.0f}")

with col2:
    st.metric("Rata-rata Luas Tanah", f"{avg_land_area:.1f} m²")

with col3:
    st.metric("Total Properti", total_listings)

st.markdown("---")

# --- Visualisasi ---
st.header("📊 Visualisasi Data")

# Distribusi Harga
st.subheader("Distribusi Harga Properti")
fig_price_dist = px.histogram(
    df_filtered,
    x='price',
    nbins=50,
    color_discrete_sequence=['#636EFA'],
    title='Sebaran Harga Properti'
)
fig_price_dist.update_layout(
    xaxis_title='Harga (Rp)',
    yaxis_title='Jumlah Properti',
    bargap=0.1,
    plot_bgcolor='rgba(0,0,0,0)'
)
fig_price_dist.update_traces(
    hovertemplate='Harga: %{x:,.0f}<br>Jumlah: %{y}'
)
st.plotly_chart(fig_price_dist, use_container_width=True)

# Properti per Lokasi
st.subheader("Jumlah Properti per Lokasi")
location_counts = df_filtered['location'].value_counts().reset_index()
location_counts.columns = ['Lokasi', 'Jumlah']
fig_location = px.bar(
    location_counts,
    x='Lokasi',
    y='Jumlah',
    color='Lokasi',
    color_discrete_sequence=px.colors.qualitative.Set2,
    title='Jumlah Properti per Kabupaten/Kota'
)
fig_location.update_layout(
    yaxis_title='Jumlah Properti',
    xaxis_title='Kabupaten/Kota',
    plot_bgcolor='rgba(0,0,0,0)'
)
fig_location.update_traces(
    hovertemplate='Lokasi: %{x}<br>Jumlah: %{y}'
)
st.plotly_chart(fig_location, use_container_width=True)

# Scatter Plot Harga vs Luas
st.subheader("Harga vs Luas Properti")
st.caption("Periksa korelasi antara harga dengan luas tanah atau luas bangunan.")

area_choice = st.radio(
    "Pilih jenis luas:",
    ('surface_area(m2)', 'building_area(m2)'),
    horizontal=True
)

fig_scatter = px.scatter(
    df_filtered,
    x=area_choice,
    y='price',
    color='location',
    hover_data=['bed', 'bath'],
    color_discrete_sequence=px.colors.qualitative.Pastel,
    title=f'Harga vs {area_choice}'
)
fig_scatter.update_layout(
    xaxis_title='Luas (m²)',
    yaxis_title='Harga (Rp)',
    plot_bgcolor='rgba(0,0,0,0)'
)
fig_scatter.update_traces(
    marker=dict(size=8, opacity=0.7),
    hovertemplate='Luas: %{x}<br>Harga: %{y:,.0f}<br>Kamar Tidur: %{customdata[0]}<br>Kamar Mandi: %{customdata[1]}'
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Distribusi Kamar Tidur & Kamar Mandi
st.subheader("Distribusi Jumlah Kamar")
col_kt, col_km = st.columns(2)

with col_kt:
    kt_counts = df_filtered['bed'].value_counts().reset_index()
    kt_counts.columns = ['Kamar Tidur', 'Jumlah']
    fig_kt = px.bar(
        kt_counts,
        x='Kamar Tidur',
        y='Jumlah',
        color_discrete_sequence=['#00CC96'],
        title='Berdasarkan Jumlah Kamar Tidur'
    )
    fig_kt.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    fig_kt.update_traces(hovertemplate='Kamar Tidur: %{x}<br>Jumlah: %{y}')
    st.plotly_chart(fig_kt, use_container_width=True)

with col_km:
    km_counts = df_filtered['bath'].value_counts().reset_index()
    km_counts.columns = ['Kamar Mandi', 'Jumlah']
    fig_km = px.bar(
        km_counts,
        x='Kamar Mandi',
        y='Jumlah',
        color_discrete_sequence=['#EF553B'],
        title='Berdasarkan Jumlah Kamar Mandi'
    )
    fig_km.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    fig_km.update_traces(hovertemplate='Kamar Mandi: %{x}<br>Jumlah: %{y}')
    st.plotly_chart(fig_km, use_container_width=True)

st.markdown("---")

# --- Data Mentah ---
st.header("📄 Lihat Data Mentah")
if st.checkbox("Tampilkan tabel data mentah"):
    st.dataframe(df_filtered)
