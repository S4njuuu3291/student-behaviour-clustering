import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="Customer Segmentation Dashboard")

st.title("Customer Segmentation Dashboard")
st.write("""
Selamat datang di Dashboard Segmentasi Pelanggan Mall.  
Dashboard ini menampilkan hasil clustering pelanggan berdasarkan data demografi, pendapatan, dan perilaku belanja.  
Tujuan: Memberikan insight actionable untuk strategi marketing, loyalty, dan promosi yang lebih tepat sasaran.
""")

df = pd.read_csv("data/clustered_data.csv")

cluster_labels = {
    0: 'Medium Spender & Medium Income',
    1: 'High Spender & High Income',
    2: 'High Spender & Low Income',
    3: 'Low Spender & High Income',
    4: 'Low Spender & Low Income'
}

counts = df['Cluster'].value_counts().sort_index()
labels = [f"{cluster_labels[c]} ({counts[c]} pelanggan, {counts[c]/counts.sum()*100:.1f}%)" for c in counts.index]

st.header("Ringkasan Cluster")

# Pie chart dan summary berdampingan
col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = plt.subplots()
    ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    st.pyplot(fig)

with col2:
    st.metric("Total Customer", df.shape[0])
    st.metric("Jumlah Cluster", len(counts))

cluster_summary = df.groupby('Cluster').agg({
    'Age': ['mean', 'std'],
    'Annual Income (k$)': ['mean', 'std'],
    'Spending Score (1-100)': ['mean', 'std'],
    'Gender': lambda x: x.value_counts().index[0],  # Most common gender
})
st.dataframe(cluster_summary.style.format({
    ('Age', 'mean'): "{:.1f}",
    ('Age', 'std'): "{:.1f}",
    ('Annual Income (k$)', 'mean'): "{:.1f}",
    ('Annual Income (k$)', 'std'): "{:.1f}",
    ('Spending Score (1-100)', 'mean'): "{:.1f}",
    ('Spending Score (1-100)', 'std'): "{:.1f}"
}))

selected_cluster = st.sidebar.selectbox(
    "Pilih Cluster untuk eksplorasi detail:",
    options=list(cluster_labels.keys()),
    format_func=lambda x: cluster_labels[x]
)

filtered = df[df['Cluster'] == selected_cluster]
st.subheader(f"Preview Data untuk {cluster_labels[selected_cluster]}")
st.dataframe(filtered[['Age', 'Annual Income (k$)', 'Spending Score (1-100)', 'Gender']].head())

st.header("Visualisasi Cluster (PCA)")

pca_data = pd.read_csv("data/pca_data.csv")

fig, ax = plt.subplots(figsize=(8,6))
unique_labels = np.unique(df['Cluster'])
for label in unique_labels:
    idx = (df['Cluster'] == label).values
    ax.scatter(pca_data.loc[idx, pca_data.columns[0]], pca_data.loc[idx, pca_data.columns[1]],
               label=cluster_labels[label], alpha=0.7)
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_title('PCA plot by Cluster')
ax.legend()
st.pyplot(fig)

st.subheader(f"Profil & Saran Bisnis untuk {cluster_labels[selected_cluster]}")

if selected_cluster == 0:
    st.info("""
    Mereka pelanggan yang cukup sering belanja dan pendapatannya sedang-sedang aja.

    **Saran:**  
    Berikan mereka alasan buat sering mampir, misalnya diskon khusus atau voucher kejutan. Bisa juga ajak mereka ikut program loyalitas yang bikin mereka merasa dihargai.
    """)

elif selected_cluster == 1:
    st.success("""
    Pelanggan ini suka belanja banyak dan punya dana yang memadai.

    **Saran:**  
    Beri mereka pengalaman belanja yang spesial, seperti akses awal untuk promo atau produk baru. Jangan lupa layanan personal seperti personal shopper supaya mereka merasa istimewa.
    """)

elif selected_cluster == 2:
    st.warning("""
    Rata-rata yang memiliki umur muda, walau pendapatannya terbatas, mereka tetap sering belanja banyak—mungkin karena suka kredit atau cicilan.

    **Saran:**  
    Tawarkan kemudahan pembayaran yang fleksibel, misal cicilan ringan tanpa bunga. Ingatkan juga produk-produk hemat tapi tetap keren dan berguna. Juga dengan tetap update dengan tren generasi muda karena cenderung impulsif dan permintaan tentang barang trending juga sangat besar.
    """)

elif selected_cluster == 3:
    st.error("""
    Pelanggan kaya tapi jarang belanja. Bisa jadi mereka sibuk atau belum nemu produk favorit.

    **Saran:**  
    Coba kenalkan mereka dengan promo menarik dan layanan yang bikin belanja jadi nyaman, seperti antar jemput atau layanan concierge. Kadang yang dibutuhkan cuma sedikit perhatian ekstra.
    """)

elif selected_cluster == 4:
    st.info("""
    Mereka mungkin cuma mampir sesekali dan belanja seadanya.

    **Saran:**  
    Berikan mereka produk yang ramah di kantong dan promo yang gampang dimengerti. Event seru dan hiburan di mall juga bisa jadi alasan mereka datang lebih sering.
    """)