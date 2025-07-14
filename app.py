import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import locale

# Set locale
try:
    locale.setlocale(locale.LC_ALL, 'id_ID')
except locale.Error:
    st.warning("Locale 'id_ID' tidak ditemukan. Menggunakan format default.")

# Load data
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['surface_area(m2)'] = pd.to_numeric(df['surface_area(m2)'], errors='coerce')
    df['building_area(m2)'] = pd.to_numeric(df['building_area(m2)'], errors='coerce')
    df.dropna(subset=['price', 'surface_area(m2)', 'building_area(m2)'], inplace=True)
    return df

# Page config
st.set_page_config(
    page_title="🏠 Dasbor Properti Yogyakarta Lengkap",
    page_icon="🏠",
    layout="wide"
)

# Load data
try:
    df = load_data('rumah123_yogya_cleaned.csv')
except FileNotFoundError:
    st.error("File data tidak ditemukan.")
    st.stop()

location_map = {0: "Kulon Progo", 1: "Gunungkidul", 2: "Sleman", 3: "Kota Yogyakarta", 4: "Bantul"}
df['location'] = df['location'].replace(location_map)

# Sidebar filter
st.sidebar.title("🔍 Filter Data")
selected_location = st.sidebar.multiselect(
    "Pilih Kabupaten/Kota:",
    options=df['location'].unique(),
    default=df['location'].unique()
)
df_filtered = df[df['location'].isin(selected_location)]

# Judul
st.title("🏠 Dasbor Analisis Properti Lengkap di Yogyakarta")
st.markdown("Analisis interaktif harga, luas, distribusi properti, dan insight tambahan. Data: Rumah123.com.")

# --- Ringkasan statistik
st.header("✨ Ringkasan Statistik")
col1, col2, col3, col4 = st.columns(4)

avg_price = df_filtered['price'].mean()
median_price = df_filtered['price'].median()
min_price = df_filtered['price'].min()
max_price = df_filtered['price'].max()
avg_land_area = df_filtered['surface_area(m2)'].mean()
median_land_area = df_filtered['surface_area(m2)'].median()
total_listings = len(df_filtered)

with col1:
    st.metric("Rata-rata Harga", f"Rp {avg_price:,.0f}")
    st.metric("Median Harga", f"Rp {median_price:,.0f}")
with col2:
    st.metric("Harga Minimum", f"Rp {min_price:,.0f}")
    st.metric("Harga Maksimum", f"Rp {max_price:,.0f}")
with col3:
    st.metric("Rata-rata Luas Tanah", f"{avg_land_area:.1f} m²")
    st.metric("Median Luas Tanah", f"{median_land_area:.1f} m²")
with col4:
    st.metric("Total Properti", total_listings)

st.markdown("---")

# --- Visualisasi utama
st.header("📊 Visualisasi Data")

# Distribusi harga
st.subheader("Distribusi Harga Properti")
fig_price = px.histogram(
    df_filtered, x='price', nbins=50, color_discrete_sequence=['#636EFA'],
    title='Sebaran Harga Properti'
)
fig_price.update_layout(
    xaxis_title='Harga (Rp)', yaxis_title='Jumlah Properti', bargap=0.1,
    plot_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig_price, use_container_width=True)

# Boxplot harga per lokasi
st.subheader("Distribusi Harga Properti per Lokasi (Boxplot)")
fig_box = px.box(
    df_filtered, x='location', y='price', color='location',
    color_discrete_sequence=px.colors.qualitative.Set2,
    title='Boxplot Harga per Lokasi'
)
fig_box.update_layout(
    xaxis_title='Kabupaten/Kota', yaxis_title='Harga (Rp)',
    plot_bgcolor='rgba(0,0,0,0)', showlegend=False
)
st.plotly_chart(fig_box, use_container_width=True)

# Jumlah properti per lokasi
st.subheader("Jumlah Properti per Lokasi")
location_counts = df_filtered['location'].value_counts().reset_index()
location_counts.columns = ['Lokasi', 'Jumlah']
fig_count = px.bar(
    location_counts, x='Lokasi', y='Jumlah', color='Lokasi',
    color_discrete_sequence=px.colors.qualitative.Pastel,
    title='Jumlah Properti per Kabupaten/Kota'
)
st.plotly_chart(fig_count, use_container_width=True)

# Pie chart proporsi listing
st.subheader("Proporsi Properti per Lokasi")
fig_pie = px.pie(
    location_counts, names='Lokasi', values='Jumlah',
    color_discrete_sequence=px.colors.qualitative.Set3,
    title='Persentase Properti di Setiap Kabupaten/Kota'
)
st.plotly_chart(fig_pie, use_container_width=True)

# Scatter harga vs luas
st.subheader("Harga vs Luas Properti")
area_choice = st.radio("Pilih jenis luas:", ('surface_area(m2)', 'building_area(m2)'), horizontal=True)
fig_scatter = px.scatter(
    df_filtered, x=area_choice, y='price', color='location',
    hover_data=['bed', 'bath'], color_discrete_sequence=px.colors.qualitative.Set1,
    title=f'Harga vs {area_choice}'
)
fig_scatter.update_traces(marker=dict(size=7, opacity=0.7))
fig_scatter.update_layout(
    xaxis_title='Luas (m²)', yaxis_title='Harga (Rp)',
    plot_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Distribusi jumlah kamar
st.subheader("Distribusi Jumlah Kamar Tidur & Kamar Mandi")
col_kt, col_km = st.columns(2)

with col_kt:
    kt_counts = df_filtered['bed'].value_counts().sort_index().reset_index()
    kt_counts.columns = ['Kamar Tidur', 'Jumlah']
    fig_kt = px.bar(
        kt_counts, x='Kamar Tidur', y='Jumlah', color_discrete_sequence=['#00CC96'],
        title='Jumlah Kamar Tidur'
    )
    st.plotly_chart(fig_kt, use_container_width=True)

with col_km:
    km_counts = df_filtered['bath'].value_counts().sort_index().reset_index()
    km_counts.columns = ['Kamar Mandi', 'Jumlah']
    fig_km = px.bar(
        km_counts, x='Kamar Mandi', y='Jumlah', color_discrete_sequence=['#EF553B'],
        title='Jumlah Kamar Mandi'
    )
    st.plotly_chart(fig_km, use_container_width=True)

# Heatmap korelasi
st.subheader("Korelasi Variabel Penting")
corr = df_filtered[['price', 'surface_area(m2)', 'building_area(m2)', 'bed', 'bath']].corr()
fig_heat = px.imshow(
    corr, text_auto=True, color_continuous_scale='RdBu', title='Matriks Korelasi'
)
st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("---")

# Data mentah
st.header("📄 Lihat Data Mentah")
if st.checkbox("Tampilkan tabel data mentah"):
    st.dataframe(df_filtered)
