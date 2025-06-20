'''
=============================================================================================================
Program ini dibuat untuk melakukan automasi transform, load data dari PostgreSQL ke ElasticSearch,
melakukan validasi data dengan Great Expectation dan melakukan automasi dengan menggunakan DAG.
Dataset yang dipakai yaitu dataset terkait penjualan sepeda di tahun 2013 sampai 2016.
=============================================================================================================
'''

# Import libraries
import datetime as dt
from datetime import datetime, timedelta
from airflow import DAG
from elasticsearch import Elasticsearch
# from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import pandas as pd
import psycopg2 as db


# fungsi untuk mengambil data dari PostgreSQL dan menyimpan ke CSV
def get_data_from_db():
    '''
    Fungsi ini digunakan untuk mengambil data mentah dari database PostgreSQL (dalam konteks Airflow)
    dan menyimpannya ke dalam file CSV untuk tahap pembersihan berikutnya.

    Proses:
    - Membuka koneksi ke PostgreSQL dengan kredensial yang sudah dikonfigurasi.
    - Mengambil maksimal 10.000 baris data dari tabel `table_m3`.
    - Menyimpan data ke file CSV bernama `data_raw.csv`.

    Output:
    - File CSV disimpan di path `/opt/airflow/dags/data_raw.csv`
    '''

    conn_string = "dbname='airflow' host='postgres' user='airflow' password='airflow'"
    conn = db.connect(conn_string)
    df = pd.read_sql("select * from table_m3 LIMIT 10000", conn)
    df.to_csv('/opt/airflow/dags/data_raw.csv', index=False)

# fungsi untuk pembersihan data
def data_preprocessing():
    '''
    Fungsi ini melakukan proses data cleaning terhadap data mentah yang diambil dari PostgreSQL.

    Proses:
    - Membaca file CSV mentah `data_raw.csv`.
    - Melakukan rename kolom menjadi snake_case untuk konsistensi dan kemudahan pemrosesan.
    - Menghapus baris-baris yang bersifat duplikat.
    - Menyimpan hasil data yang sudah dibersihkan ke file CSV `P2M3_arcana_data_clean.csv`.

    Output:
    - File CSV hasil pembersihan data disimpan di `/opt/airflow/dags/P2M3_arcana_data_clean.csv`
    '''

    # Loading CSV ke DataFrame
    df_data = pd.read_csv('/opt/airflow/dags/data_raw.csv')

    # Mengganti nama kolom
    df_data = df_data.rename(columns = {
        'Date' : 'date', 
        'Day' : 'day', 
        'Month' : 'month', 
        'Year' : 'year', 
        'Customer_Age' : 'customer_age', 
        'Age_Group' : 'age_group',
        'Customer_Gender' : 'customer_gender', 
        'Country' : 'country', 
        'State' : 'state', 
        'Product_Category' : 'product_category',
        'Sub_Category' : 'sub_category', 
        'Product' : 'product', 
        'Order_Quantity' : 'order_quantity', 
        'Unit_Cost' : 'unit_cost', 
        'Unit_Price' : 'unit_price',
        'Profit' : 'profit', 
        'Cost' : 'cost', 
        'Revenue' : 'revenue'
    })

    # Menghapus data duplikat
    df_data = df_data.drop_duplicates()
    df_data.to_csv('/opt/airflow/dags/data_clean.csv', index=False)

# fungsi untuk post data ke Kibana
def post_to_elasticsearch():
    '''
    Fungsi ini digunakan untuk mengirim data hasil pembersihan ke Elasticsearch agar dapat diindeks dan divisualisasikan melalui kibana.

    Proses:
    - Membuka koneksi ke Elasticsearch melalui endpoint `http://elasticsearch:9200`.
    - Membaca file CSV hasil data cleaning (`data_clean.csv`) dari direktori DAG.
    - Melakukan iterasi pada setiap baris DataFrame.
    - Mengubah setiap baris menjadi format JSON.
    - Mengirim setiap dokumen ke Elasticsearch pada index `table_m3`, dengan ID unik berbasis urutan baris.

    Output:
    - Setiap baris data akan dikirim dan disimpan sebagai dokumen terpisah ke Elasticsearch.
    '''

    es = Elasticsearch("http://elasticsearch:9200")
    df = pd.read_csv('/opt/airflow/dags/data_clean.csv')

    for i, r in df.iterrows():
        doc = r.to_json()
        res = es.index(index="table_m3", id=i + 1, body=doc)

# DAG setup
default_args = {
    'owner': 'cana', # nama pemilik DAG
    'depends_on_past': False, # task tidak bergantung pada keberhasilan task run sebelumnya
    'email_on_failure': False, # tidak kirim email jika task gagal
    'email_on_retry': False, # tidak kirim email saat task di-retry
    'retries': 1, # jumlah maksimal percobaan ulang jika task gagal
    'retry_delay': timedelta(minutes=1), # jeda 1 menit sebelum mencoba ulang
}

with DAG('project_bike_sales',
         description='Global Bike Sales ETL Pipeline',
         default_args=default_args,
         schedule_interval='10-30/10 9 * * 6', # menjadwalkan setiap Sabtu pukul 09:10, 09:20, dan 09:30
         start_date=dt.datetime(2024, 11, 2) + timedelta(hours=7), # (UTC -7) karena saya berada di zona pdt
         catchup=False) as dag:

    # Task to fetch data from PostgreSQL
    fetch_task = PythonOperator(
        task_id='get_data_from_db',
        python_callable=get_data_from_db
    )

    # Task that will be executed by PythonOperator
    clean_task = PythonOperator(
        task_id='cleaning_data',
        python_callable=data_preprocessing
    )

    # Task to post to Kibana
    post_to_kibana_task = PythonOperator(
        task_id='post_to_elasticsearch',
        python_callable=post_to_elasticsearch
    )

    # Set task dependencies
    fetch_task >> clean_task >> post_to_kibana_task