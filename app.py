import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import streamlit.components.v1 as components

st.set_page_config(page_title="Student Insight | Statistik Deskriptif", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "latihan1.csv"

# Theme colors: sage green + warm yellow
SAGE = "#7F9B78"
DARK = "#243A2D"
PALE = "#EEF2E6"
YELLOW = "#F3D46B"
GOLD = "#D8B647"
MUTED = "#6F7C70"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --sage:#7F9B78; --dark:#243A2D; --pale:#EEF2E6; --yellow:#F3D46B; --gold:#D8B647; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:#F7F8F2; color:var(--dark); }
[data-testid="stHeader"] { background:rgba(247,248,242,.92); }
[data-testid="stSidebar"] { background:#E9EFE3; border-right:1px solid #DCE4D7; }
[data-testid="stSidebar"] * { color:#243A2D; }
.block-container { padding-top:1.5rem; padding-bottom:2rem; max-width:1500px; }
.hero { background:linear-gradient(115deg,#243A2D 0%,#42654B 72%,#7F9B78 100%); border-radius:24px; padding:30px 34px; color:white; position:relative; overflow:hidden; margin-bottom:22px; }
.hero:after { content:""; position:absolute; width:230px;height:230px;border-radius:50%;background:rgba(243,212,107,.17);right:-48px;top:-95px; }
.hero-kicker { color:#F3D46B; text-transform:uppercase;letter-spacing:2px;font-size:11px;font-weight:800; }
.hero h1 { font-family:Manrope,sans-serif; font-size:32px; line-height:1.2; margin:8px 0 8px; color:white; font-weight:800; }
.hero p { color:#E5EDE2; margin:0; font-size:14px; max-width:720px; }
.pill { display:inline-block;background:#F3D46B;color:#243A2D;padding:7px 12px;border-radius:100px;font-size:11px;font-weight:800;margin-top:18px; }
.section-title { font-family:Manrope,sans-serif;font-size:20px;font-weight:800;color:#243A2D;margin:12px 0 3px; }
.section-sub { color:#718071;font-size:12px;margin-bottom:14px; }
div[data-testid="stMetric"] { background:#FFFFFF;border:1px solid #E4E9DF;border-radius:17px;padding:17px 18px;box-shadow:0 5px 18px rgba(36,58,45,.035); }
div[data-testid="stMetricLabel"] { color:#758174;font-size:12px;font-weight:700; }
div[data-testid="stMetricValue"] { color:#243A2D;font-family:Manrope,sans-serif;font-size:27px;font-weight:800; }
div[data-testid="stMetricDelta"] { font-size:11px; }
.chart-card { background:white;border:1px solid #E4E9DF;border-radius:18px;padding:12px 14px 2px; }
.insight { background:#FFFFFF;border:1px solid #E4E9DF;border-left:5px solid #7F9B78;border-radius:13px;padding:15px 17px;margin:8px 0;color:#334638;font-size:13px; }
.insight.yellow { border-left-color:#D8B647;background:#FFFDF3; }
.insight strong { color:#243A2D; }
.stButton>button { border-radius:10px;border:0;background:#243A2D;color:white;font-weight:700; }
.stButton>button:hover { background:#42654B;color:white; }
.stDownloadButton>button { border-radius:10px;background:#F3D46B;color:#243A2D;border:0;font-weight:800; }
[data-testid="stDataFrame"] { border-radius:12px;overflow:hidden; }
hr { border-color:#E2E8DE; }
footer {visibility:hidden;}
#MainMenu {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# JS enhancement: live local clock and a small greeting banner
components.html("""
<div id="live-note" style="font-family:'DM Sans',sans-serif;color:#6F7C70;font-size:11px;text-align:right;padding:0 4px 4px;"></div>
<script>
(function(){
 const el=document.getElementById('live-note');
 function tick(){
   const d=new Date();
   el.textContent='DASHBOARD LIVE  •  '+d.toLocaleDateString('id-ID',{weekday:'long',day:'2-digit',month:'long',year:'numeric'})+'  '+d.toLocaleTimeString('id-ID',{hour:'2-digit',minute:'2-digit'});
 }
 tick(); setInterval(tick,60000);
})();
</script>
""", height=28)

@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        return None
    data = pd.read_csv(DATA_PATH)
    data.columns = [c.strip() for c in data.columns]
    return data

df = load_data()
if df is None:
    st.error("File latihan1.csv belum ditemukan. Letakkan file CSV di folder yang sama dengan app.py.")
    st.stop()

# Sidebar controls
st.sidebar.markdown("## 🌿 Student Insight")
st.sidebar.caption("STATISTIK DESKRIPTIF")
st.sidebar.markdown("---")
gender_col = "Gender" if "Gender" in df.columns else None
if gender_col:
    genders = ["Semua"] + sorted(df[gender_col].dropna().astype(str).unique().tolist())
    selected_gender = st.sidebar.selectbox("Filter gender", genders)
else:
    selected_gender = "Semua"
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
default_metrics = [c for c in ["Study_Hours","Sleep_Hours","Attendance","Exam_Score","Screen_Hours","Satisfaction","Monthly_Spending"] if c in numeric_cols]
metric_options = st.sidebar.multiselect("Variabel untuk ringkasan", numeric_cols, default=default_metrics[:5])
st.sidebar.markdown("---")
st.sidebar.caption("Sumber: latihan1.csv")
st.sidebar.caption(f"{len(df):,} baris • {len(df.columns)} kolom")

filtered = df.copy()
if gender_col and selected_gender != "Semua":
    filtered = filtered[filtered[gender_col].astype(str) == selected_gender]
if filtered.empty:
    st.warning("Tidak ada data untuk filter ini.")
    st.stop()

st.markdown("""
<div class="hero">
  <div class="hero-kicker">DATA • INSIGHT • DECISION</div>
  <h1>Student Insight Dashboard</h1>
  <p>Ringkasan statistik deskriptif untuk memahami pola belajar, tidur, kehadiran, nilai ujian, penggunaan layar, dan kepuasan mahasiswa.</p>
  <span class="pill">🌱 SAGE GREEN × BUTTER YELLOW</span>
</div>
""", unsafe_allow_html=True)

# Identify common fields safely
def col(*names):
    for name in names:
        if name in filtered.columns: return name
    return None
score_c = col("Exam_Score","Nilai_Ujian","Score")
study_c = col("Study_Hours","Jam_Belajar")
sleep_c = col("Sleep_Hours","Jam_Tidur")
attendance_c = col("Attendance","Kehadiran")
screen_c = col("Screen_Hours","Jam_Layar")
satisfaction_c = col("Satisfaction","Kepuasan")
spending_c = col("Monthly_Spending","Pengeluaran_Bulanan")
age_c = col("Age","Usia")
id_c = col("Student_ID","ID")

st.markdown('<div class="section-title">Ringkasan utama</div><div class="section-sub">Angka berubah mengikuti filter yang dipilih di panel kiri.</div>', unsafe_allow_html=True)
m1,m2,m3,m4 = st.columns(4)
m1.metric("Jumlah mahasiswa", f"{len(filtered):,}", f"{len(filtered)/len(df)*100:.0f}% dari data")
if score_c:
    m2.metric("Rata-rata nilai", f"{filtered[score_c].mean():.1f}", f"Median {filtered[score_c].median():.1f}")
if study_c:
    m3.metric("Rata-rata jam belajar", f"{filtered[study_c].mean():.1f} jam", f"Rentang {filtered[study_c].min():g}–{filtered[study_c].max():g}")
if satisfaction_c:
    m4.metric("Kepuasan rata-rata", f"{filtered[satisfaction_c].mean():.1f}/10", f"Median {filtered[satisfaction_c].median():.1f}")

st.markdown("---")
left,right = st.columns([1.12, .88], gap="large")
with left:
    st.markdown('<div class="section-title">Distribusi nilai ujian</div><div class="section-sub">Melihat sebaran nilai dan konsentrasi mahasiswa.</div>', unsafe_allow_html=True)
    if score_c:
        fig = px.histogram(filtered, x=score_c, nbins=12, color_discrete_sequence=[SAGE], marginal="box")
        fig.update_layout(height=330, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="white", margin=dict(l=10,r=10,t=18,b=10), xaxis_title="Nilai ujian", yaxis_title="Jumlah mahasiswa", font=dict(color=DARK), bargap=.08)
        fig.update_xaxes(showgrid=False); fig.update_yaxes(gridcolor="#EDF0E9")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Kolom nilai ujian tidak ditemukan.")
with right:
    st.markdown('<div class="section-title">Profil gender</div><div class="section-sub">Komposisi responden pada data yang sedang dipilih.</div>', unsafe_allow_html=True)
    if gender_col:
        counts = filtered[gender_col].astype(str).value_counts().rename_axis("Gender").reset_index(name="Jumlah")
        fig = px.pie(counts, names="Gender", values="Jumlah", hole=.68, color_discrete_sequence=[SAGE,YELLOW,"#B6C9A9"])
        fig.update_traces(textposition="outside", textinfo="label+percent", marker=dict(line=dict(color="white",width=3)))
        fig.update_layout(height=330, paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=15,r=15,t=20,b=10), showlegend=False, font=dict(color=DARK))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Kolom gender tidak ditemukan.")

st.markdown('<div class="section-title">Perbandingan variabel</div><div class="section-sub">Pilih variabel untuk membandingkan rata-rata dan variasinya.</div>', unsafe_allow_html=True)
numeric_non_id = [c for c in numeric_cols if c != id_c]
if numeric_non_id:
    c1,c2 = st.columns([1,2])
    with c1:
        compare_cols = st.multiselect("Variabel yang ditampilkan", numeric_non_id, default=[c for c in [study_c,sleep_c,attendance_c,score_c,satisfaction_c] if c in numeric_non_id])
    with c2:
        if compare_cols:
            means = filtered[compare_cols].mean().reset_index()
            means.columns=["Variabel","Rata-rata"]
            fig=px.bar(means,x="Variabel",y="Rata-rata",color="Rata-rata",color_continuous_scale=["#E8EDDF",SAGE,YELLOW])
            fig.update_layout(height=330,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="white",margin=dict(l=5,r=5,t=15,b=5),font=dict(color=DARK),coloraxis_showscale=False,xaxis_title="",yaxis_title="Rata-rata")
            fig.update_xaxes(tickangle=-20,showgrid=False);fig.update_yaxes(gridcolor="#EDF0E9")
            st.plotly_chart(fig,use_container_width=True)
        else:
            st.info("Pilih minimal satu variabel.")

st.markdown('<div class="section-title">Statistik deskriptif</div><div class="section-sub">Mean, median, simpangan baku, nilai minimum, dan maksimum.</div>', unsafe_allow_html=True)
desc_cols = metric_options if metric_options else numeric_non_id
if desc_cols:
    desc = filtered[desc_cols].describe().T
    desc = desc.rename(columns={"count":"Jumlah","mean":"Rata-rata","std":"Std. deviasi","min":"Minimum","25%":"Q1","50%":"Median","75%":"Q3","max":"Maksimum"})
    st.dataframe(desc.style.format("{:,.2f}"), use_container_width=True, height=300)
    st.download_button("⬇ Unduh tabel statistik (CSV)", desc.to_csv().encode("utf-8-sig"), "statistik_deskriptif.csv", "text/csv")

st.markdown('<div class="section-title">Hubungan antarvariabel</div><div class="section-sub">Korelasi Pearson menunjukkan arah dan kekuatan hubungan linear, bukan sebab-akibat.</div>', unsafe_allow_html=True)
corr_cols = [c for c in numeric_non_id if filtered[c].nunique() > 1]
if len(corr_cols) >= 2:
    corr = filtered[corr_cols].corr(numeric_only=True)
    fig=px.imshow(corr,text_auto=".2f",color_continuous_scale=["#DCE8D6","#FFFFFF",YELLOW],zmin=-1,zmax=1,aspect="auto")
    fig.update_layout(height=440,paper_bgcolor="rgba(0,0,0,0)",margin=dict(l=5,r=5,t=15,b=5),font=dict(color=DARK),coloraxis_colorbar=dict(title="Korelasi"))
    st.plotly_chart(fig,use_container_width=True)
else:
    st.info("Data numerik belum cukup untuk menghitung korelasi.")

# Automatic narrative insights
st.markdown('<div class="section-title">Analisis & rekomendasi keputusan</div><div class="section-sub">Temuan deskriptif untuk membantu menentukan prioritas tindak lanjut.</div>', unsafe_allow_html=True)
insights=[]
if score_c and study_c:
    r=filtered[[score_c,study_c]].corr().iloc[0,1]
    direction="positif" if r>=0 else "negatif"
    strength="kuat" if abs(r)>=.7 else ("sedang" if abs(r)>=.4 else "lemah")
    insights.append(("yellow",f"Jam belajar vs nilai",f"Korelasi {direction} {strength} (r = {r:.2f}) antara jam belajar dan nilai. Gunakan sebagai sinyal untuk mengevaluasi kebiasaan belajar; korelasi tidak membuktikan sebab-akibat."))
if score_c:
    avg=filtered[score_c].mean()
    below=(filtered[score_c]<70).sum()
    pct=below/len(filtered)*100
    insights.append(("", "Dukungan akademik",f"Rata-rata nilai {avg:.1f}; ada {below} mahasiswa ({pct:.0f}%) dengan nilai di bawah 70. Prioritaskan pemeriksaan kebutuhan belajar bagi kelompok ini jika 70 merupakan ambang kelulusan yang relevan."))
if sleep_c:
    avg_sleep=filtered[sleep_c].mean()
    insights.append(("", "Keseimbangan rutinitas",f"Rata-rata tidur {avg_sleep:.1f} jam. Tinjau mahasiswa dengan durasi tidur rendah bersama beban belajar dan nilai, tanpa menganggap tidur sebagai satu-satunya penyebab hasil akademik."))
if screen_c:
    avg_screen=filtered[screen_c].mean()
    insights.append(("yellow", "Penggunaan layar",f"Rata-rata penggunaan layar {avg_screen:.1f} jam. Bila fokus belajar menjadi kendala, uji strategi jeda layar dan pemantauan waktu secara sukarela."))
for cls,title,body in insights:
    cl = "insight yellow" if cls=="yellow" else "insight"
    st.markdown(f'<div class="{cl}"><strong>{title}</strong><br>{body}</div>',unsafe_allow_html=True)

st.markdown('<div class="section-title">Data mahasiswa</div><div class="section-sub">Tabel data setelah filter gender diterapkan.</div>', unsafe_allow_html=True)
st.dataframe(filtered, use_container_width=True, height=330)
st.download_button("⬇ Unduh data yang sedang difilter (CSV)", filtered.to_csv(index=False).encode("utf-8-sig"), "data_mahasiswa_filtered.csv", "text/csv")

st.markdown("---")
st.caption("Catatan metodologi: statistik ini menggambarkan data yang tersedia (bukan otomatis mewakili populasi yang lebih luas). Periksa definisi variabel, kualitas data, dan ambang penilaian sebelum membuat keputusan formal.")
