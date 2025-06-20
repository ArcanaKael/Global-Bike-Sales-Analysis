# 🚴‍♂️ Global Bike Sales Analysis

## 📁 Repository Structure
```
1. kibana_dashboard_screenshots folder  : Folder berisi screenshot visualisasi dashboard di Kibana
2. bike_sales_etl_dag.py                : Berisi definisi DAG yang digunakan untuk mengelola alur kerja ETL (Extract, Transform, Load)
3. data_validation_GX.ipynb             : Notebook Jupyter yang mendokumentasikan proses pembersihan data dengan menggunakan Great Expectations.
4. data_raw.csv                         : Dataset mentah penjualan sepeda yang digunakan
5. data_clean.csv                       : Dataset hasil cleaning dari proses DAG
6. query_ddl.txt                        : Skrip SQL untuk membuat dan mendefinisikan tabel dalam basis data PostgreSQL.
7. conceptual_qna.txt                   : Berisi jawaban conceptual problem.
8. DAG_workflow_graph.png              : Screenshot yang menampilkan alur graph dari DAG yang dibuat
```

---

## 🧩 Problem Background

Proyek ini bertujuan untuk menganalisis data penjualan sepeda secara global selama periode 2013 hingga 2016. Fokus utamanya adalah menggali wawasan bisnis dari perilaku pelanggan, tren penjualan, distribusi geografis, hingga efisiensi stok dan profitabilitas produk.

Dengan menyusun pipeline ETL otomatis, pembersihan data berbasis validasi eksplisit, dan visualisasi interaktif menggunakan Kibana, proyek ini menyajikan pendekatan end-to-end yang tidak hanya teknis, tetapi juga relevan secara bisnis.

---

## 📊 Project Output

Output utama berupa dashboard interaktif di **Kibana**, meliputi:

- 📈 *Tren Pendapatan Tahunan*  
- 💰 *Produk dengan Profit Tertinggi*  
- 🧑‍🤝‍🧑 *Segmentasi Pelanggan Berdasarkan Usia & Gender*  
- 🌍 *Distribusi Geografis Penjualan berdasarkan Negara dan Negara Bagian*  
- ⚖️ *Perbandingan Rata-rata Cost dan Profit per Produk*

---

## 📦 Dataset

- **Sumber**: [Kaggle - Bike Sales in Europe](https://www.kaggle.com/datasets/sadiqshah/bike-sales-in-europe)  
- **Ukuran Dataset**:  
  - Sebelum cleaning: 113,036 baris, 18 kolom  
  - Setelah cleaning: 9,866 baris, 18 kolom  
- **Kondisi Data**:  
  - Tidak ada missing values  
  - Duplikasi dihapus melalui proses DAG  
- **Periode Waktu**: 2013 – 2016

---

## 🔧 Methods & Tools

- **ETL Automation**: PostgreSQL → Airflow → Elasticsearch  
- **Data Validation**: Great Expectations  
- **Orkestrasi Workflow**: Apache Airflow  
- **Visualisasi Data**: Kibana

---

## 🛠️ Tech Stack

- PostgreSQL  
- Apache Airflow  
- Great Expectations  
- Elasticsearch  
- Kibana

---

## 📚 Reference

- [Ahmed Terry – Bike Sales Analysis (Kaggle)](https://www.kaggle.com/code/ahmedterry/bike-sales-analysis)