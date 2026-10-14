# Student Insight Dashboard — Statistik Deskriptif

Dashboard lokal berbasis Streamlit, dengan tema hijau sage dan kuning, chart interaktif Plotly, CSS kustom, dan komponen JavaScript untuk jam live.

## Isi folder
- `app.py` — aplikasi dashboard
- `latihan1.csv` — dataset yang disediakan
- `style.css` — referensi warna CSS
- `script.js` — tempat pengembangan interaksi JavaScript tambahan
- `requirements.txt` — dependensi

## Menjalankan di Windows (lokal)
1. Ekstrak ZIP ini.
2. Buka folder hasil ekstrak.
3. Klik address bar File Explorer, ketik `cmd`, lalu tekan Enter.
4. Jalankan:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   python -m pip install -r requirements.txt
   streamlit run app.py
   ```
5. Browser akan terbuka. Jika tidak, buka `http://localhost:8501`.

Pastikan Python sudah terpasang. Untuk menghentikan server, tekan `Ctrl+C` di CMD.

## Catatan
Aplikasi ini berjalan lokal di komputer Anda; belum dipublikasikan ke internet. File CSV harus berada di folder yang sama dengan `app.py`.
