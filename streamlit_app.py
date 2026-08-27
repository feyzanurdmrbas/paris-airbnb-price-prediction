
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Paris Airbnb | Gecelik Fiyat Tahmini",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# COLOR PALETTE
# =========================================================
SAGE_DARK = "#466653"
SAGE = "#6F947E"
SAGE_SOFT = "#AFC6B7"
CREAM = "#F6F0E5"
BEIGE = "#E9DDCC"
LILAC = "#D8CDE3"
LILAC_DARK = "#9C89B8"
INK = "#233128"
MUTED = "#647168"
GOLD = "#C9A96A"
WHITE = "#FFFFFF"

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown(
    f"""
    <style>
    html, body, [class*="css"] {{
        font-family: "Segoe UI", Arial, sans-serif;
    }}

    .stApp {{
        background:
            radial-gradient(circle at 7% 7%, rgba(216,205,227,.60) 0%, rgba(216,205,227,0) 24%),
            radial-gradient(circle at 93% 14%, rgba(175,198,183,.62) 0%, rgba(175,198,183,0) 28%),
            radial-gradient(circle at 80% 82%, rgba(233,221,204,.72) 0%, rgba(233,221,204,0) 32%),
            linear-gradient(135deg, #FBFAF7 0%, #F2F6F1 46%, #F8F3EB 100%);
        color: {INK};
    }}

    .block-container {{
        max-width: 1360px;
        padding-top: 1.8rem;
        padding-bottom: 4rem;
    }}

    [data-testid="stSidebar"] {{
        background:
            linear-gradient(180deg, rgba(70,102,83,.98) 0%, rgba(55,79,65,.99) 60%, rgba(74,69,79,.98) 100%);
        border-right: 1px solid rgba(255,255,255,.12);
    }}

    [data-testid="stSidebar"] * {{
        color: #FAFCFA !important;
    }}

    [data-testid="stSidebar"] [role="radiogroup"] label {{
        background: rgba(255,255,255,.06);
        border-radius: 12px;
        padding: .35rem .45rem;
        margin-bottom: .2rem;
    }}

    h1, h2, h3 {{
        color: {INK};
        letter-spacing: -0.025em;
    }}

    .hero {{
        background:
            linear-gradient(125deg, rgba(255,255,255,.82) 0%, rgba(240,247,241,.78) 38%, rgba(243,236,247,.74) 68%, rgba(248,240,226,.78) 100%);
        border: 1px solid rgba(111,148,126,.24);
        border-radius: 28px;
        padding: 2.45rem 2.55rem;
        box-shadow: 0 18px 45px rgba(49,70,57,.10);
        backdrop-filter: blur(12px);
        margin-bottom: 1.6rem;
    }}

    .hero .eyebrow {{
        display: inline-block;
        padding: .38rem .72rem;
        border-radius: 999px;
        background: rgba(70,102,83,.10);
        color: {SAGE_DARK};
        font-weight: 700;
        font-size: .82rem;
        letter-spacing: .06em;
        text-transform: uppercase;
        margin-bottom: .9rem;
    }}

    .hero h1 {{
        font-size: 2.55rem;
        line-height: 1.08;
        margin: 0;
        color: {INK};
    }}

    .hero p {{
        color: {MUTED};
        font-size: 1.08rem;
        max-width: 900px;
        margin-top: .85rem;
        line-height: 1.7;
    }}

    .section-kicker {{
        display: inline-block;
        color: {SAGE_DARK};
        font-weight: 800;
        letter-spacing: .08em;
        font-size: .78rem;
        text-transform: uppercase;
        margin-bottom: .15rem;
    }}

    .section-title {{
        font-size: 1.75rem;
        font-weight: 800;
        color: {INK};
        margin-bottom: .4rem;
    }}

    .section-sub {{
        color: {MUTED};
        line-height: 1.65;
        margin-bottom: 1.05rem;
    }}

    .glass-card {{
        background: rgba(255,255,255,.78);
        border: 1px solid rgba(111,148,126,.18);
        border-radius: 20px;
        padding: 1.15rem 1.2rem;
        box-shadow: 0 9px 26px rgba(49,70,57,.07);
        backdrop-filter: blur(9px);
        min-height: 132px;
    }}

    .card-label {{
        color: {MUTED};
        font-size: .78rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .07em;
    }}

    .card-value {{
        color: {SAGE_DARK};
        font-size: 1.75rem;
        font-weight: 850;
        margin-top: .32rem;
    }}

    .card-note {{
        color: {MUTED};
        font-size: .84rem;
        margin-top: .28rem;
        line-height: 1.45;
    }}

    .story-card {{
        background: linear-gradient(135deg, rgba(255,255,255,.84), rgba(247,243,237,.78));
        border: 1px solid rgba(111,148,126,.18);
        border-radius: 20px;
        padding: 1.15rem 1.25rem;
        margin-bottom: .8rem;
        box-shadow: 0 8px 22px rgba(49,70,57,.06);
    }}

    .story-card b {{
        color: {SAGE_DARK};
    }}

    .insight {{
        background: linear-gradient(135deg, rgba(225,237,228,.92), rgba(244,239,248,.90));
        border-left: 5px solid {SAGE};
        border-radius: 13px;
        padding: .95rem 1.05rem;
        margin: .65rem 0 1rem;
        line-height: 1.6;
        color: {INK};
    }}

    .warning {{
        background: linear-gradient(135deg, rgba(252,245,230,.96), rgba(246,239,225,.92));
        border-left: 5px solid {GOLD};
        border-radius: 13px;
        padding: .95rem 1.05rem;
        margin: .65rem 0 1rem;
        line-height: 1.6;
        color: {INK};
    }}

    .purple-note {{
        background: linear-gradient(135deg, rgba(240,235,245,.96), rgba(236,243,238,.94));
        border-left: 5px solid {LILAC_DARK};
        border-radius: 13px;
        padding: .95rem 1.05rem;
        margin: .65rem 0 1rem;
        line-height: 1.6;
        color: {INK};
    }}

    .timeline {{
        position: relative;
        margin-left: .65rem;
        padding-left: 1.9rem;
        border-left: 2px solid rgba(111,148,126,.35);
    }}

    .timeline-item {{
        position: relative;
        background: rgba(255,255,255,.76);
        border: 1px solid rgba(111,148,126,.16);
        border-radius: 16px;
        padding: .8rem 1rem;
        margin-bottom: .72rem;
        box-shadow: 0 6px 18px rgba(49,70,57,.045);
    }}

    .timeline-item:before {{
        content: "";
        position: absolute;
        left: -2.35rem;
        top: 1.05rem;
        width: .82rem;
        height: .82rem;
        border-radius: 50%;
        background: {SAGE};
        box-shadow: 0 0 0 5px rgba(111,148,126,.13);
    }}

    .mini-chip {{
        display: inline-block;
        background: rgba(70,102,83,.09);
        color: {SAGE_DARK};
        font-size: .78rem;
        font-weight: 700;
        padding: .35rem .62rem;
        border-radius: 999px;
        margin: .12rem .18rem .12rem 0;
    }}

    .divider {{
        height: 1px;
        background: linear-gradient(90deg, rgba(111,148,126,0), rgba(111,148,126,.35), rgba(156,137,184,.3), rgba(111,148,126,0));
        margin: 2.1rem 0;
    }}

    div[data-testid="stMetric"] {{
        background: rgba(255,255,255,.78);
        border: 1px solid rgba(111,148,126,.17);
        padding: 12px 14px;
        border-radius: 16px;
        box-shadow: 0 5px 16px rgba(49,70,57,.05);
    }}

    [data-testid="stDataFrame"] {{
        background: rgba(255,255,255,.78);
        border-radius: 16px;
        overflow: hidden;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# DATA USED IN THE REPORT
# =========================================================
model_df = pd.DataFrame({
    "Model": [
        "Linear Regression", "Ridge", "Lasso", "ElasticNet",
        "Decision Tree", "Gradient Boosting", "Random Forest"
    ],
    "Train R²": [0.5590, 0.5590, 0.5586, 0.5586, 0.5899, 0.6372, 0.7562],
    "Test R²":  [0.5507, 0.5507, 0.5503, 0.5504, 0.5468, 0.6179, 0.6324],
    "RMSE (€)": [90.33, 90.33, 90.36, 90.36, 90.72, 83.30, 81.71],
    "MAE (€)":  [66.31, 66.31, 66.30, 66.32, 64.98, 59.78, 58.06],
})
model_df["Gap"] = model_df["Train R²"] - model_df["Test R²"]

size_df = pd.DataFrame({
    "Eğitim verisi": ["%10", "%25", "%50", "%75", "%100"],
    "Kullanılan oran": [10, 25, 50, 75, 100],
    "Train R²": [0.7617, 0.7656, 0.7633, 0.7586, 0.7553],
    "Test R²": [0.5835, 0.6052, 0.6179, 0.6267, 0.6313],
})
size_df["Gap"] = size_df["Train R²"] - size_df["Test R²"]

outlier_df = pd.DataFrame({
    "Değişken": [
        "price_eur", "accommodates", "bedrooms", "bathrooms", "beds",
        "number_of_reviews", "reviews_per_month", "minimum_nights", "availability_365"
    ],
    "IQR Outlier (%)": [7.85, 3.76, 3.02, 22.32, 9.31, 9.00, 5.64, 15.17, 0.00],
    "Gözlenen maksimum": [
        "97.003,05 €", "16", "33", "42", "32", "4.589", "55,49", "365", "365"
    ]
})

variables_df = pd.DataFrame({
    "Değişken": [
        "price_eur", "neighbourhood_cleansed", "latitude / longitude", "room_type",
        "accommodates", "bedrooms / bathrooms / beds", "number_of_reviews",
        "reviews_per_month", "review_scores_rating", "minimum_nights", "availability_365"
    ],
    "Açıklama": [
        "Hedef değişken; gecelik fiyat (€)",
        "İlanın bulunduğu Paris mahallesi/bölgesi",
        "Coğrafi konum koordinatları",
        "Konaklama türü",
        "Maksimum misafir kapasitesi",
        "Yatak odası, banyo ve yatak bilgileri",
        "Toplam yorum sayısı",
        "Aylık ortalama yorum sayısı",
        "Ortalama değerlendirme puanı",
        "Minimum konaklama süresi",
        "Yıl içindeki müsait gün sayısı",
    ]
})

rf_params = pd.DataFrame({
    "Parametre": ["n_estimators", "max_depth", "min_samples_split", "min_samples_leaf", "max_features"],
    "Final değer": ["80", "15", "12", "6", "0,7"]
})

# =========================================================
# HELPERS
# =========================================================
def section_header(no, title, subtitle):
    st.markdown(
        f"""
        <div>
            <div class="section-kicker">AŞAMA {no}</div>
            <div class="section-title">{title}</div>
            <div class="section-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def metric_card(label, value, note):
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="card-label">{label}</div>
            <div class="card-value">{value}</div>
            <div class="card-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def glass_story(title, text):
    st.markdown(
        f"""
        <div class="story-card">
            <b>{title}</b><br/>
            <span style="color:{MUTED}; line-height:1.58;">{text}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 🏠 Paris Airbnb")
    st.markdown("### Gecelik Fiyat Tahmini")
    st.caption("Bireysel Veri Analitiği Bitirme Projesi")
    st.markdown("---")

    view = st.radio(
        "Görünüm",
        ["🎤 Sunum Akışı", "⚡ Hızlı Özet"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**Sunum sırası**")
    for x in [
        "1 · Problem & Hipotez",
        "2 · Veri Seti",
        "3 · Temizlik & Eksikler",
        "4 · Aykırı Değerler",
        "5 · EDA",
        "6 · İstatistiksel Testler",
        "7 · Train/Test & Leakage",
        "8 · Modelleme",
        "9 · Overfitting",
        "10 · Veri Miktarı Deneyi",
        "11 · Random Forest Tuning",
        "12 · Final Karşılaştırma",
        "13 · Özellik Önemleri",
        "14 · Sonuç & Kısıtlar",
    ]:
        st.caption(x)

    st.markdown("---")
    st.caption("Feyza Nur Demirbaş · 2026")

# =========================================================
# HERO
# =========================================================
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Veri Analitiği Bitirme Projesi</div>
        <h1>Paris Airbnb İlanlarında<br/>Gecelik Fiyat Tahmini</h1>
        <p>
            Regresyon modelleri, aykırı değer analizi ve overfitting kontrolü ile
            Paris Airbnb fiyatlarını uçtan uca inceleyen karşılaştırmalı bir makine öğrenmesi çalışması.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card("Ham veri", "77.679", "Paris Airbnb ilanı")
with m2:
    metric_card("Analiz verisi", "48.402", "Geçerli fiyat sonrası")
with m3:
    metric_card("En iyi model", "Random Forest", "7 regresyon yaklaşımı arasında")
with m4:
    metric_card("Final Test R²", "0,6324", "RMSE 81,71 € · MAE 58,06 €")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================================================
# QUICK SUMMARY
# =========================================================
if view == "⚡ Hızlı Özet":
    st.markdown("## Projenin tek sayfalık özeti")

    c1, c2 = st.columns(2)
    with c1:
        glass_story(
            "Problem",
            "Paris Airbnb ilanlarında gecelik fiyatın; konum, oda tipi, kapasite, yatak odası, banyo, yorum ve müsaitlik gibi değişkenlerle ne ölçüde açıklanabileceği araştırıldı."
        )
        glass_story(
            "Kritik veri kararı",
            "IQR ile işaretlenen her uç değer silinmedi. Bathrooms değişkeninde Q1=Q3=1 olduğu için IQR=0 çıkması, mekanik outlier temizliğinin geçerli ilanları silebileceğini gösterdi."
        )
        glass_story(
            "Model seçimi",
            "Linear Regression, Ridge, Lasso, ElasticNet, Decision Tree, Gradient Boosting ve Random Forest karşılaştırıldı."
        )

    with c2:
        glass_story(
            "EDA",
            "Fiyat dağılımı belirgin biçimde sağa çarpıktı. Fiyatla en güçlü pozitif Spearman ilişkileri accommodates, beds, bedrooms ve bathrooms değişkenlerinde görüldü."
        )
        glass_story(
            "Overfitting",
            "İlk kontrolsüz Decision Tree train verisini neredeyse kusursuz öğrenirken test performansı düştü. Model karmaşıklığı sınırlandırıldı; Random Forest 5-fold GridSearchCV ile ayarlandı."
        )
        glass_story(
            "Final sonuç",
            "Random Forest: Train R²=0,7562, Test R²=0,6324, RMSE=81,71 €, MAE=58,06 €. Daha az veri kullanmak overfitting'i çözmedi; daha fazla eğitim verisi test başarısını artırdı."
        )

    st.stop()

# =========================================================
# 1. PROBLEM & HYPOTHESIS
# =========================================================
section_header(
    "01",
    "Problem, Motivasyon ve Hipotez",
    "Projeyi bir model seçme egzersizi olarak değil, fiyat yapısını anlamaya ve genelleme problemiyle baş etmeye odaklanan uçtan uca bir çalışma olarak kurguladım."
)

st.markdown(
    f"""
    <div class="insight">
        <b>Temel problem:</b> Paris'te aynı şehir içinde Airbnb fiyatları; konum, oda tipi,
        kapasite, yatak odası ve banyo sayısı, minimum konaklama süresi, yorum geçmişi ve
        müsaitlik gibi birçok faktöre göre değişiyor. Bu nedenle problem tek değişkenli basit
        bir yapı değil, <b>çok değişkenli bir regresyon problemi</b>.
    </div>
    """,
    unsafe_allow_html=True
)

c1, c2 = st.columns(2)
with c1:
    glass_story(
        "Temel hipotez",
        "Gecelik fiyatın özellikle accommodates, bedrooms, bathrooms, beds, room_type ve konum değişkenlerinin birlikte etkisiyle açıklanabileceğini varsaydım."
    )
with c2:
    glass_story(
        "Model hipotezi",
        "Fiyat yapısında doğrusal olmayan ilişkiler bulunduğu için ağaç tabanlı modellerin doğrusal regresyon yaklaşımlarından daha güçlü test performansı gösterebileceğini öngördüm."
    )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================================================
# 2. DATASET
# =========================================================
section_header(
    "02",
    "Veri Kaynağı ve Kullanılan Değişkenler",
    "Analiz, Inside Airbnb tarafından yayımlanan 16 Haziran 2026 tarihli Paris detailed listings veri setine dayanıyor."
)

d1, d2, d3 = st.columns(3)
with d1:
    metric_card("Ham gözlem", "77.679", "İlan")
with d2:
    metric_card("Ham değişken", "90", "Sütun")
with d3:
    metric_card("Temiz fiyat sonrası", "48.402", "Analiz edilebilir ilan")

st.dataframe(variables_df, use_container_width=True, hide_index=True)

st.markdown(
    '<div class="purple-note"><b>Değişken seçimi:</b> Modelde fiyatla ilişkili, yorumlanabilir ve proje kapsamına uygun değişkenler kullanıldı. Hedef değişken <code>price_eur</code> sürekli sayısal olduğu için problem regresyon olarak ele alındı.</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================================================
# 3. CLEANING
# =========================================================
section_header(
    "03",
    "Veri Temizleme ve Eksik Değerler",
    "Modelleme öncesi temel amaç, hedef fiyatı kullanılabilir hale getirmek ve eksik değerleri test verisinden bilgi sızdırmadan yönetmekti."
)

c1, c2, c3 = st.columns(3)
with c1:
    glass_story("Fiyat temizliği", "Price alanı sayısal forma dönüştürüldü; fiyatı eksik veya sıfırdan küçük/eşit kayıtlar çıkarıldı.")
with c2:
    glass_story("Sayısal eksikler", "Modelleme aşamasında sayısal eksikler eğitim verisinden öğrenilen medyan ile tamamlandı.")
with c3:
    glass_story("Kategorik eksikler", "Kategorik değişkenlerde eğitim verisinden öğrenilen en sık değer kullanıldı.")

st.markdown(
    '<div class="insight"><b>Neden train verisinden?</b> Eksik değer doldurma gibi preprocessing kararlarını tüm veri üzerinden öğrenmek, test bilgisinin dolaylı biçimde modele sızmasına yol açabilir. Bu nedenle bu adımlar train/test ayrımından sonra uygulandı.</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================================================
# 4. OUTLIERS
# =========================================================
section_header(
    "04",
    "Aykırı Değer Analizi",
    "IQR yöntemi önce tanısal amaçla uygulandı; fakat 'istatistiksel olarak uç' ile 'veri hatası' aynı kabul edilmedi."
)

left, right = st.columns([1.1, 1])
with left:
    fig = px.bar(
        outlier_df.sort_values("IQR Outlier (%)"),
        x="IQR Outlier (%)",
        y="Değişken",
        orientation="h",
        text="IQR Outlier (%)",
        color="IQR Outlier (%)",
        color_continuous_scale=[CREAM, SAGE_SOFT, SAGE_DARK],
        title="IQR kuralına göre aykırı gözlem oranları"
    )
    fig.update_layout(
        coloraxis_showscale=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,.55)",
        height=470
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.dataframe(outlier_df, use_container_width=True, hide_index=True)
    st.markdown(
        '<div class="warning"><b>Kritik örnek:</b> <code>bathrooms</code> değişkeninde Q1=Q3=1 olduğu için IQR=0. Bu durumda 1’den farklı çok sayıda gerçek ilan outlier olarak işaretleniyor. Bu nedenle otomatik IQR silme veri yapısını bozabilirdi.</div>',
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class="story-card">
        <b>Uygulanan karar</b><br/>
        Hedef <code>price_eur</code> için model kapsamı yalnızca eğitim verisinden öğrenilen IQR sınırlarına göre belirlendi.
        Açıklayıcı değişkenlerde ise körlemesine satır silmek yerine sadece aşırı uç değerlerin etkisi
        eğitim verisinin <b>%99 üst yüzdelik sınırı</b> ile kontrol edildi.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================================================
# 5. EDA
# =========================================================
section_header(
    "05",
    "Keşifsel Veri Analizi (EDA)",
    "Model kurmadan önce fiyatın dağılımı, oda tipleri ve sayısal değişkenler arasındaki ilişkiler incelendi."
)

e1, e2, e3 = st.columns(3)
with e1:
    metric_card("Medyan fiyat", "205,50 €", "Analiz verisi")
with e2:
    metric_card("Ortalama fiyat", "321,23 €", "Sağ kuyruktan etkileniyor")
with e3:
    metric_card("Dağılım", "Sağa çarpık", "Yüksek fiyatlı az sayıdaki ilan")

st.image("images/price_distribution.png", use_container_width=True)

st.markdown(
    '<div class="insight">Ortalamanın medyandan belirgin yüksek olması, az sayıdaki yüksek fiyatlı ilanın sağ kuyruğu uzattığını gösteriyor. Bu nedenle fiyatı yalnızca ortalama üzerinden yorumlamak yanıltıcı olabilir.</div>',
    unsafe_allow_html=True
)

st.markdown("### Oda tipleri")
st.markdown(
    """
    <div class="story-card">
        <b>Bulgular:</b> Hotel room en yüksek medyan fiyata sahip; entire home/apartment ikinci sırada.
        Private room ve shared room kategorilerinde medyan fiyat daha düşük.
        Bu durum oda tipinin fiyat için önemli bir kategorik ayırıcı olduğunu destekledi.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("### Spearman korelasyonu")
st.image("images/correlation_matrix.png", use_container_width=True)

corr_cards = st.columns(5)
corr_vals = [
    ("accommodates", "ρ ≈ 0,60"),
    ("beds", "ρ ≈ 0,54"),
    ("bedrooms", "ρ ≈ 0,53"),
    ("bathrooms", "ρ ≈ 0,43"),
    ("minimum_nights", "ρ ≈ -0,33"),
]
for col, (name, value) in zip(corr_cards, corr_vals):
    with col:
        metric_card(name, value, "Fiyat ile Spearman ilişkisi")

st.markdown(
    '<div class="purple-note">Kapasite değişkenleri kendi aralarında da yüksek korelasyon gösterebildiği için sonuçlar tek bir değişkene bakılarak değil, model içindeki ortak etkilerle birlikte yorumlandı.</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================================================
# 6. STATISTICAL TESTS
# =========================================================
section_header(
    "06",
    "İstatistiksel Testler",
    "Dağılım yapısına göre parametrik olmayan yöntemler tercih edildi."
)

t1, t2, t3 = st.columns(3)
with t1:
    glass_story("Shapiro-Wilk", "Fiyatın normal dağılıma uygunluğu 5.000 gözlemlik örneklemde kontrol edildi; normal dağılım varsayımı desteklenmedi.")
with t2:
    glass_story("Spearman", "Sayısal değişkenlerle fiyat arasındaki ilişkiler doğrusal varsayıma daha az bağımlı Spearman katsayısıyla incelendi.")
with t3:
    glass_story("Kruskal-Wallis", "Oda tipi ve mahalle gibi kategorik gruplar arasındaki fiyat farklılıkları parametrik olmayan Kruskal-Wallis testiyle değerlendirildi.")

st.markdown(
    '<div class="warning"><b>Yorum ilkesi:</b> Büyük örneklemde çok küçük farklar bile istatistiksel olarak anlamlı olabilir. Bu nedenle p-değerleri tek başına değil; grafikler ve ilişki büyüklükleriyle birlikte yorumlandı.</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================================================
# 7. TRAIN TEST
# =========================================================
section_header(
    "07",
    "Train/Test Ayrımı ve Data Leakage Kontrolü",
    "Model performansını tarafsız ölçebilmek için veri önce %80 eğitim ve %20 test olarak ayrıldı."
)

p1, p2 = st.columns(2)
with p1:
    metric_card("Eğitim seti", "%80", "Modelin öğrendiği bölüm")
with p2:
    metric_card("Test seti", "%20", "Model seçiminden bağımsız değerlendirme")

st.markdown(
    """
    <div class="timeline">
        <div class="timeline-item"><b>1 · Train/Test ayrımı</b><br/>Önce veri ayrıldı.</div>
        <div class="timeline-item"><b>2 · Eksik değer doldurma</b><br/>Medyan ve mod yalnızca eğitim verisinden öğrenildi.</div>
        <div class="timeline-item"><b>3 · Outlier eşikleri</b><br/>Capping ve hedef fiyat sınırları yalnızca eğitim verisinden öğrenildi.</div>
        <div class="timeline-item"><b>4 · Encoding</b><br/>Kategorik değişkenler one-hot encoding ile dönüştürüldü.</div>
        <div class="timeline-item"><b>5 · Scaling</b><br/>Doğrusal modellerde sayısal değişkenler standardize edildi; ağaç tabanlı modeller ölçekleme olmadan eğitildi.</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="insight"><b>Amaç:</b> Test verisinin preprocessing kararlarına sızmasını önlemek ve final performans ölçümünü daha güvenilir hale getirmek.</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================================================
# 8. MODELS
# =========================================================
section_header(
    "08",
    "Modelleme ve Değerlendirme Metrikleri",
    "Doğrusal ve ağaç tabanlı yedi farklı regresyon yaklaşımı aynı test çerçevesinde karşılaştırıldı."
)

st.markdown(
    """
    <span class="mini-chip">Linear Regression</span>
    <span class="mini-chip">Ridge</span>
    <span class="mini-chip">Lasso</span>
    <span class="mini-chip">ElasticNet</span>
    <span class="mini-chip">Decision Tree</span>
    <span class="mini-chip">Gradient Boosting</span>
    <span class="mini-chip">Random Forest</span>
    """,
    unsafe_allow_html=True
)

r1, r2, r3 = st.columns(3)
with r1:
    glass_story("R²", "Hedef değişkendeki varyansın model tarafından ne kadarının açıklandığını gösterir.")
with r2:
    glass_story("MAE", "Tahminlerin gerçek fiyatlardan ortalama mutlak sapmasını gösterir.")
with r3:
    glass_story("RMSE", "Büyük tahmin hatalarını MAE'ye göre daha güçlü cezalandırır.")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================================================
# 9. OVERFITTING
# =========================================================
section_header(
    "09",
    "Overfitting Analizi",
    "İlk Decision Tree modelinde çok yüksek train başarısı, test verisine aynı ölçüde taşınmadı."
)

st.markdown(
    '<div class="warning"><b>İlk uyarı:</b> Kontrolsüz Decision Tree eğitim verisinde R² değerini neredeyse 1,00 seviyesine taşıdı; test performansı belirgin biçimde daha düşük kaldı. Bu, başarı değil <b>overfitting</b> göstergesiydi.</div>',
    unsafe_allow_html=True
)

o1, o2, o3 = st.columns(3)
with o1:
    glass_story("Sorun", "Ağaç eğitim verisinin ayrıntılarını ve gürültüsünü fazla öğreniyordu.")
with o2:
    glass_story("Müdahale", "max_depth, min_samples_split ve min_samples_leaf gibi karmaşıklık parametreleri sınırlandırıldı.")
with o3:
    glass_story("Hedef", "Train skorunu maksimum yapmak değil, test başarısını korurken train-test farkını azaltmak.")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================================================
# 10. DATA SIZE EXPERIMENT
# =========================================================
section_header(
    "10",
    "Eğitim Verisi Miktarı Deneyi",
    "Hocanın 'veriyi küçültüp tekrar dene' önerisi deneysel olarak test edildi; test seti sabit tutularak aynı Random Forest farklı eğitim oranlarıyla yeniden eğitildi."
)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=size_df["Kullanılan oran"], y=size_df["Train R²"],
    mode="lines+markers", name="Train R²",
    line=dict(color=SAGE_DARK, width=4),
    marker=dict(size=9)
))
fig.add_trace(go.Scatter(
    x=size_df["Kullanılan oran"], y=size_df["Test R²"],
    mode="lines+markers", name="Test R²",
    line=dict(color=LILAC_DARK, width=4),
    marker=dict(size=9)
))
fig.update_layout(
    title="Eğitim verisi miktarının model performansına etkisi",
    xaxis_title="Kullanılan eğitim verisi (%)",
    yaxis_title="R²",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,.55)",
    height=480,
    legend=dict(orientation="h", y=1.12)
)
st.plotly_chart(fig, use_container_width=True)

st.dataframe(size_df[["Eğitim verisi", "Train R²", "Test R²", "Gap"]], use_container_width=True, hide_index=True)

st.markdown(
    '<div class="insight"><b>Sonuç:</b> Test R² yaklaşık 0,584’ten 0,631’e yükseldi. Daha az eğitim verisi overfitting’i çözmedi; aksine daha fazla veri modelin genelleme başarısına katkı sağladı.</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================================================
# 11. RF TUNING
# =========================================================
section_header(
    "11",
    "Random Forest Modelinin İyileştirilmesi",
    "Final model, yalnızca eğitim verisi üzerinden yapılan 5-fold GridSearchCV ile ayarlandı."
)

g1, g2 = st.columns([1, 1.25])
with g1:
    st.dataframe(rf_params, use_container_width=True, hide_index=True)
with g2:
    glass_story(
        "Tuning stratejisi",
        "Hesaplama maliyetini yönetmek için hiperparametre araması yalnızca eğitim setinden seçilen 10.000 gözlemlik sabit bir alt kümede yapıldı. Test seti hiperparametre seçiminde kullanılmadı."
    )
    glass_story(
        "Final eğitim",
        "Seçilen hiperparametreler belirlendikten sonra final Random Forest modeli tüm eğitim verisi üzerinde yeniden eğitildi."
    )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================================================
# 12. MODEL COMPARISON
# =========================================================
section_header(
    "12",
    "Final Model Karşılaştırması",
    "Model seçimi yalnızca train skoruna değil; Test R², RMSE, MAE ve train-test farkına birlikte bakılarak yapıldı."
)

st.image("images/model_comparison.png", use_container_width=True)

styled = model_df.copy()
st.dataframe(
    styled.style.format({
        "Train R²": "{:.4f}",
        "Test R²": "{:.4f}",
        "RMSE (€)": "{:.2f}",
        "MAE (€)": "{:.2f}",
        "Gap": "{:.4f}",
    }),
    use_container_width=True,
    hide_index=True
)

f1, f2, f3, f4 = st.columns(4)
with f1:
    metric_card("Final model", "Random Forest", "En dengeli genel sonuç")
with f2:
    metric_card("Train R²", "0,7562", "Final model")
with f3:
    metric_card("Test R²", "0,6324", "En yüksek test skoru")
with f4:
    metric_card("MAE", "58,06 €", "Ortalama mutlak hata")

st.markdown(
    '<div class="purple-note"><b>Yorum:</b> Doğrusal modeller yaklaşık 0,55 Test R² seviyesinde birbirine çok yakın kaldı. Gradient Boosting ve Random Forest daha yüksek test başarısı verdi; bu da fiyat yapısında doğrusal olmayan ilişkiler ve değişken etkileşimlerinin önemli olduğuna işaret ediyor.</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================================================
# 13. FEATURE IMPORTANCE
# =========================================================
section_header(
    "13",
    "Random Forest Özellik Önemleri",
    "Final modelin fiyat tahmininde hangi değişkenleri daha yoğun kullandığı incelendi."
)

st.image("images/feature_importance.png", use_container_width=True)

fi1, fi2, fi3 = st.columns(3)
with fi1:
    glass_story("1 · accommodates", "Konaklama kapasitesi hem korelasyonda hem model öneminde öne çıktı.")
with fi2:
    glass_story("2 · minimum_nights", "Basit korelasyonda negatif ilişki göstermesine rağmen model içinde yüksek önem aldı.")
with fi3:
    glass_story("3 · bedrooms", "Yatak odası sayısı fiyat yapısında güçlü bir fiziksel özellik olarak öne çıktı.")

st.markdown(
    '<div class="warning"><b>Önemli yorum:</b> Feature importance nedensellik kanıtı değildir. Bir değişkenin model için faydalı olması, fiyatı tek başına “neden” olarak belirlediği anlamına gelmez.</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================================================
# 14. CONCLUSION
# =========================================================
section_header(
    "14",
    "Sonuç, Kısıtlar ve Gelecek Çalışmalar",
    "Projenin ana çıktısı yalnızca en yüksek skoru bulmak değil; veri hazırlama ve model karmaşıklığı kararlarının genelleme performansını nasıl etkilediğini göstermekti."
)

st.markdown(
    f"""
    <div class="insight">
        <b>Ana sonuç:</b> Random Forest en dengeli ve en başarılı model oldu.
        Final model <b>Test R²=0,6324</b>, <b>RMSE=81,71 €</b> ve <b>MAE=58,06 €</b>
        değerlerine ulaştı. Başlangıçtaki overfitting azaltıldı; daha az veri kullanmanın çözüm olmadığı görüldü.
    </div>
    """,
    unsafe_allow_html=True
)

lim1, lim2 = st.columns(2)
with lim1:
    st.markdown("### Kısıtlar")
    st.markdown(
        """
        - Veri yalnızca Paris ve 16 Haziran 2026 tarihli tek kesiti temsil ediyor.
        - Sezon, tatil, etkinlik, hafta içi/hafta sonu ve rezervasyon tarihi dinamikleri doğrudan modele girmiyor.
        - Çok yüksek fiyatlı bazı gözlemler gerçek lüks ilanlar olabilir.
        - Final Random Forest'ta train-test farkı tamamen sıfırlanmış değil.
        """
    )

with lim2:
    st.markdown("### Gelecek çalışmalar")
    st.markdown(
        """
        - Louvre, Eyfel Kulesi, metro istasyonları ve merkeze uzaklık gibi mekânsal feature'lar eklenebilir.
        - İlan açıklaması, amenities, yorum metinleri, fotoğraf kalitesi ve host özellikleri kullanılabilir.
        - XGBoost, CatBoost ve LightGBM karşılaştırılabilir.
        - Nested cross-validation ve farklı tarih/şehirlerde dış doğrulama yapılabilir.
        """
    )

st.markdown(
    """
    <div class="hero" style="margin-top:2rem; padding:1.7rem 2rem;">
        <div class="eyebrow">Final mesaj</div>
        <h2 style="margin:0;">Daha fazla train skoru ≠ daha iyi model</h2>
        <p style="margin-top:.55rem;">
            Bu projede en önemli öğrenim, modeli eğitim verisinde mümkün olduğunca yüksek skora taşımak yerine;
            veri sızıntısını önlemek, aykırı değerleri kontrollü yönetmek ve genelleme performansını korumak oldu.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
