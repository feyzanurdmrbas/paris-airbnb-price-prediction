import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Paris Airbnb | Gecelik Fiyat Tahmini", page_icon="🏠", layout="wide", initial_sidebar_state="expanded")

INK="#26332B"; MUTED="#647168"; SAGE_DARK="#506D59"; SAGE="#789781"; SAGE_SOFT="#B9CCBE"; CREAM="#F8F3E9"; BEIGE="#E9DDCB"; LILAC="#DCCFE6"; LILAC_DARK="#9D89B4"; GOLD="#C8A86B"

st.markdown(f"""
<style>
html, body, [class*="css"] {{font-family:"Segoe UI",Arial,sans-serif;}}
.stApp {{background:radial-gradient(circle at 10% 8%,rgba(220,207,230,.70) 0%,rgba(220,207,230,0) 25%),radial-gradient(circle at 92% 12%,rgba(185,204,190,.72) 0%,rgba(185,204,190,0) 30%),radial-gradient(circle at 82% 86%,rgba(233,221,203,.78) 0%,rgba(233,221,203,0) 31%),linear-gradient(135deg,#FCFBF8 0%,#F2F6F2 45%,#F8F1E9 100%);color:{INK};}}
.block-container {{max-width:1380px;padding-top:1.8rem;padding-bottom:4rem;}}
[data-testid="stSidebar"] {{background:linear-gradient(180deg,rgba(75,104,85,.99) 0%,rgba(57,81,67,.99) 62%,rgba(72,65,79,.99) 100%);border-right:1px solid rgba(255,255,255,.10);}}
[data-testid="stSidebar"] * {{color:#FAFCFA !important;}}
[data-testid="stSidebar"] [role="radiogroup"] label {{background:rgba(255,255,255,.055);border-radius:12px;padding:.28rem .42rem;margin-bottom:.18rem;}}
h1,h2,h3 {{color:{INK};letter-spacing:-.025em;}}
.hero {{background:linear-gradient(125deg,rgba(255,255,255,.86) 0%,rgba(235,244,237,.82) 38%,rgba(243,236,247,.78) 69%,rgba(249,241,228,.82) 100%);border:1px solid rgba(120,151,129,.22);border-radius:28px;padding:2.2rem 2.4rem;box-shadow:0 18px 46px rgba(51,74,60,.09);backdrop-filter:blur(10px);margin-bottom:1.45rem;}}
.hero .eyebrow {{display:inline-block;padding:.38rem .72rem;border-radius:999px;background:rgba(80,109,89,.10);color:{SAGE_DARK};font-weight:800;font-size:.78rem;letter-spacing:.07em;text-transform:uppercase;margin-bottom:.85rem;}}
.hero h1 {{font-size:2.38rem;line-height:1.10;margin:0;color:{INK};}}
.hero p {{color:{MUTED};font-size:1.02rem;max-width:930px;margin-top:.78rem;line-height:1.72;}}
.glass-card {{background:rgba(255,255,255,.80);border:1px solid rgba(120,151,129,.17);border-radius:19px;padding:1.12rem 1.18rem;box-shadow:0 8px 24px rgba(51,74,60,.055);min-height:128px;}}
.card-label {{color:{MUTED};font-size:.77rem;font-weight:850;text-transform:uppercase;letter-spacing:.07em;}}
.card-value {{color:{SAGE_DARK};font-size:1.72rem;font-weight:850;margin-top:.30rem;}}
.card-note {{color:{MUTED};font-size:.83rem;line-height:1.45;margin-top:.25rem;}}
.explain-card {{background:linear-gradient(135deg,rgba(255,255,255,.86),rgba(248,244,238,.80));border:1px solid rgba(120,151,129,.16);border-radius:18px;padding:1rem 1.12rem;margin-bottom:.75rem;box-shadow:0 7px 20px rgba(51,74,60,.048);}}
.explain-card .q {{color:{SAGE_DARK};font-weight:850;font-size:.92rem;margin-bottom:.32rem;}}
.explain-card .a {{color:{INK};line-height:1.62;font-size:.95rem;}}
.insight {{background:linear-gradient(135deg,rgba(226,238,229,.96),rgba(243,237,248,.93));border-left:5px solid {SAGE};border-radius:13px;padding:.94rem 1.05rem;margin:.65rem 0 1rem;line-height:1.62;color:{INK};}}
.warning {{background:linear-gradient(135deg,rgba(252,246,232,.97),rgba(247,240,226,.94));border-left:5px solid {GOLD};border-radius:13px;padding:.94rem 1.05rem;margin:.65rem 0 1rem;line-height:1.62;color:{INK};}}
.purple-note {{background:linear-gradient(135deg,rgba(242,236,247,.96),rgba(236,244,239,.95));border-left:5px solid {LILAC_DARK};border-radius:13px;padding:.94rem 1.05rem;margin:.65rem 0 1rem;line-height:1.62;color:{INK};}}
.result-box {{background:linear-gradient(135deg,rgba(225,238,229,.98),rgba(248,241,229,.95));border:1px solid rgba(120,151,129,.24);border-radius:19px;padding:1.15rem 1.25rem;margin:.7rem 0 1rem;box-shadow:0 8px 22px rgba(51,74,60,.05);}}
.hypothesis {{background:rgba(255,255,255,.80);border:1px solid rgba(120,151,129,.17);border-radius:18px;padding:1.05rem 1.18rem;margin-bottom:.78rem;box-shadow:0 6px 18px rgba(51,74,60,.045);}}
.h-title {{color:{INK};font-weight:850;margin-bottom:.42rem;}}
.supported {{display:inline-block;background:rgba(120,151,129,.13);color:{SAGE_DARK};font-weight:850;padding:.26rem .55rem;border-radius:999px;margin-bottom:.46rem;}}
.chip {{display:inline-block;background:rgba(80,109,89,.09);color:{SAGE_DARK};font-size:.77rem;font-weight:750;padding:.34rem .60rem;border-radius:999px;margin:.11rem .17rem .11rem 0;}}
</style>
""", unsafe_allow_html=True)

model_df=pd.DataFrame({"Model":["Linear Regression","Ridge","Lasso","ElasticNet","Decision Tree","Gradient Boosting","Random Forest"],"Train R²":[0.5590,0.5590,0.5586,0.5586,0.5899,0.6372,0.7562],"Test R²":[0.5507,0.5507,0.5503,0.5504,0.5468,0.6179,0.6324],"RMSE (€)":[90.33,90.33,90.36,90.36,90.72,83.30,81.71],"MAE (€)":[66.31,66.31,66.30,66.32,64.98,59.78,58.06]})
model_df["Train-Test Farkı"]=model_df["Train R²"]-model_df["Test R²"]
size_df=pd.DataFrame({"Eğitim verisi":["%10","%25","%50","%75","%100"],"Kullanılan oran":[10,25,50,75,100],"Train R²":[0.7617,0.7656,0.7633,0.7586,0.7553],"Test R²":[0.5835,0.6052,0.6179,0.6267,0.6313]})
size_df["Train-Test Farkı"]=size_df["Train R²"]-size_df["Test R²"]
outlier_df=pd.DataFrame({"Değişken":["Gecelik fiyat","Maksimum misafir kapasitesi","Yatak odası sayısı","Banyo sayısı","Yatak sayısı","Toplam yorum sayısı","Aylık yorum sayısı","Minimum konaklama süresi","Yıllık müsait gün"],"Teknik sütun":["price_eur","accommodates","bedrooms","bathrooms","beds","number_of_reviews","reviews_per_month","minimum_nights","availability_365"],"IQR Outlier (%)":[7.85,3.76,3.02,22.32,9.31,9.00,5.64,15.17,0.00],"Gözlenen maksimum":["97.003,05 €","16","33","42","32","4.589","55,49","365","365"]})
variables_df=pd.DataFrame({"Sunumda kullandığım ad":["Gecelik fiyat","Mahalle / bölge","Enlem ve boylam","Oda tipi","Maksimum misafir kapasitesi","Yatak odası / banyo / yatak","Toplam yorum sayısı","Aylık ortalama yorum","Değerlendirme puanı","Minimum konaklama süresi","Yıllık müsaitlik"],"Veri setindeki sütun":["price_eur","neighbourhood_cleansed","latitude / longitude","room_type","accommodates","bedrooms / bathrooms / beds","number_of_reviews","reviews_per_month","review_scores_rating","minimum_nights","availability_365"],"Rolü":["Hedef değişken","Konum","Konum","Konaklama türü","Kapasite","Fiziksel özellikler","Yorum geçmişi","Yorum sıklığı","Değerlendirme","Konaklama kuralı","Müsaitlik"]})
rf_params=pd.DataFrame({"Parametre":["Ağaç sayısı","Maksimum derinlik","Minimum bölünme örneği","Minimum yaprak örneği","Kullanılan özellik oranı"],"Teknik adı":["n_estimators","max_depth","min_samples_split","min_samples_leaf","max_features"],"Final değer":["80","15","12","6","0,7"]})

def hero(phase,title,text):
    st.markdown(f'<div class="hero"><div class="eyebrow">{phase}</div><h1>{title}</h1><p>{text}</p></div>',unsafe_allow_html=True)

def metric_card(label,value,note):
    st.markdown(f'<div class="glass-card"><div class="card-label">{label}</div><div class="card-value">{value}</div><div class="card-note">{note}</div></div>',unsafe_allow_html=True)

def explain(q,a):
    st.markdown(f'<div class="explain-card"><div class="q">{q}</div><div class="a">{a}</div></div>',unsafe_allow_html=True)

def transparent(fig,height=470):
    fig.update_layout(height=height,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(255,255,255,.52)",font=dict(color=INK),margin=dict(l=25,r=25,t=65,b=35))
    return fig

with st.sidebar:
    st.markdown("## 🏠 Paris Airbnb")
    st.markdown("### Gecelik Fiyat Tahmini")
    st.caption("Bireysel Veri Analitiği Bitirme Projesi")
    st.markdown("---")
    page=st.radio("Sunum Bölümü",["1 · Projeye Giriş","2 · Veri Setini Tanıma","3 · Veri Temizleme","4 · Aykırı Değer Analizi","5 · Keşifsel Veri Analizi","6 · İstatistiksel Analiz","7 · Modelleme İçin Veri Hazırlama","8 · Modeller ve Değerlendirme","9 · Overfitting Analizi","10 · Eğitim Verisi Miktarı","11 · Random Forest Optimizasyonu","12 · Final Model ve Bulgular","13 · Sonuç ve Hipotezler"],label_visibility="collapsed")
    st.markdown("---")
    st.caption("FAZ 1 · Veriyi Anlama · 1–6")
    st.caption("FAZ 2 · Model Geliştirme · 7–12")
    st.caption("FAZ 3 · Sonuç · 13")
    st.markdown("---")
    st.caption("Feyza Nur Demirbaş · 2026")

if page=="1 · Projeye Giriş":
    hero("FAZ 1 · VERİYİ ANLAMA","Paris Airbnb İlanlarında Gecelik Fiyat Tahmini","Bu projede amacım yalnızca en yüksek model skorunu bulmak değildi. Paris Airbnb fiyatlarının hangi özelliklerle ilişkili olduğunu anlamak, aykırı değerleri kontrollü biçimde ele almak ve modelin eğitim verisini ezberlemesini önleyecek savunulabilir bir süreç kurmak istedim.")
    c1,c2,c3=st.columns(3)
    with c1: metric_card("Problem türü","Regresyon","Hedef değişken gecelik fiyat (€)")
    with c2: metric_card("Veri kaynağı","Inside Airbnb","Paris detailed listings")
    with c3: metric_card("Ana odak","Genelleme","Outlier + overfitting kontrolü")
    st.markdown("### Problem ve başlangıç beklentilerim")
    explain("Neyi tahmin etmeye çalışıyorum?","Paris'teki bir Airbnb ilanının gecelik fiyatını tahmin etmeye çalışıyorum. Fiyat sürekli sayısal bir değişken olduğu için problem regresyon olarak ele alındı.")
    explain("Neden tek bir değişken yeterli değil?","Aynı şehirdeki iki ilan; konum, oda tipi, maksimum misafir kapasitesi, yatak odası ve banyo sayısı, minimum konaklama süresi, yorum geçmişi ve müsaitlik gibi birçok özellik nedeniyle farklı fiyatlanabilir. Bu yüzden fiyatı tek bir değişkene bağlamak yerine değişkenleri birlikte değerlendirdim.")
    st.markdown('''<div class="hypothesis"><div class="h-title">Hipotez 1 · Kapasite ve fiziksel özellikler</div>Maksimum misafir kapasitesi, yatak odası, banyo ve yatak sayısı arttıkça gecelik fiyatın genel olarak yükselmesini bekledim.</div><div class="hypothesis"><div class="h-title">Hipotez 2 · Doğrusal olmayan yapı</div>Airbnb fiyatlarının yalnızca doğrusal ilişkilerle açıklanamayacağını; bu nedenle ağaç tabanlı modellerin doğrusal modellerden daha yüksek test başarısı gösterebileceğini düşündüm.</div><div class="hypothesis"><div class="h-title">Hipotez 3 · Overfitting kontrolü</div>Model karmaşıklığını sınırlandırıp çapraz doğrulama kullandığımda eğitim ve test performansı arasındaki farkın azaltılabileceğini öngördüm.</div>''',unsafe_allow_html=True)
    st.markdown('<div class="purple-note"><b>Burada sonucu söylemiyorum.</b> Bunlar analize başlamadan önceki beklentilerim. Son bölümde bulgulara dönüp hangilerinin desteklendiğini değerlendireceğim.</div>',unsafe_allow_html=True)

elif page=="2 · Veri Setini Tanıma":
    hero("FAZ 1 · VERİYİ ANLAMA","Veri Setini Tanıma","Model kurmadan önce verinin büyüklüğünü, hedef değişkeni ve hangi ilan özelliklerini kullanabileceğimi anlamaya odaklandım.")
    c1,c2,c3=st.columns(3)
    with c1: metric_card("Ham gözlem","77.679","Paris Airbnb ilanı")
    with c2: metric_card("Ham değişken","90","Veri setindeki sütun sayısı")
    with c3: metric_card("Fiyat temizliği sonrası","48.402","Analize alınan ilan")
    explain("Veri seti nereden geliyor?","Inside Airbnb tarafından yayımlanan Paris detailed listings veri setini kullandım. Ham veri 77.679 ilan ve 90 değişkenden oluşuyordu.")
    explain("Neden tüm 90 değişkeni doğrudan modele vermedim?","Projenin kapsamına uygun, yorumlanabilir ve fiyatla ilişkili olmasını beklediğim değişkenleri seçtim. Böylece hem modeli daha anlaşılır tuttum hem de gereksiz karmaşıklığı azalttım.")
    st.markdown("### Kullandığım temel değişkenler")
    st.dataframe(variables_df,use_container_width=True,hide_index=True)
    st.markdown('<div class="insight"><b>Sunum dili:</b> Önce Türkçe anlamını söylüyorum; gerekirse parantez içinde teknik sütun adını gösteriyorum. Örneğin “maksimum misafir kapasitesi (<code>accommodates</code>)”.</div>',unsafe_allow_html=True)

elif page=="3 · Veri Temizleme":
    hero("FAZ 1 · VERİYİ ANLAMA","Veri Temizleme ve Eksik Değerler","Ham veriyi doğrudan modele vermek yerine önce hedef fiyatı kullanılabilir hale getirdim ve eksik değerlerin nerede yoğunlaştığını inceledim.")
    explain("Fiyat alanında ne yaptım?","Fiyat alanındaki para birimi işaretlerini temizleyip sayısal formata dönüştürdüm. Fiyatı eksik veya sıfırdan küçük/eşit olan kayıtlar hedef değişken açısından anlamlı olmadığı için analiz dışında kaldı.")
    explain("Eksik değerleri neden hemen doldurmadım?","Eksik değerleri tüm veri seti üzerinden doldurmak test verisindeki bilgiyi eğitim sürecine taşıyabilir. Bu nedenle önce eksikliği inceledim; gerçek doldurma işlemini modelleme aşamasında yalnızca eğitim verisinden öğrenilen değerlerle yaptım.")
    c1,c2,c3=st.columns(3)
    with c1: metric_card("Aylık yorum sıklığı","≈ %17 eksik","reviews_per_month")
    with c2: metric_card("Yatak odası","≈ %16 eksik","bedrooms")
    with c3: metric_card("Banyo sayısı","≈ %12 eksik","bathrooms")
    st.markdown('<div class="result-box"><b>Kararım:</b><br/>Sayısal eksikleri eğitim verisinden öğrenilen <b>medyan</b> ile, kategorik eksikleri ise eğitim verisinden öğrenilen <b>en sık görülen değer</b> ile doldurdum. Bu kararı train/test ayrımından sonra uyguladım.</div>',unsafe_allow_html=True)

elif page=="4 · Aykırı Değer Analizi":
    hero("FAZ 1 · VERİYİ ANLAMA","Aykırı Değer Analizi","Bu bölüm projenin en kritik kararlarından biri. Amacım uç değerleri otomatik olarak silmek değil; hangi değerlerin gerçekten model için problem yaratabileceğini anlamaktı.")
    explain("Neden aykırı değerleri inceledim?","Fiyat dağılımında ve bazı sayısal özelliklerde çok yüksek değerler vardı. Bu gözlemler regresyon modelini güçlü biçimde etkileyebileceği için önce hangi değişkenlerde uç değerlerin yoğun olduğunu görmek istedim.")
    explain("Neden IQR?","IQR, verinin ortadaki %50'lik bölümüne dayanır ve uç gözlemleri sistematik biçimde belirlemek için kolay yorumlanan bir yöntemdir. Alt sınırı Q1−1,5×IQR; üst sınırı Q3+1,5×IQR olarak hesapladım.")
    fig=px.bar(outlier_df.sort_values("IQR Outlier (%)"),x="IQR Outlier (%)",y="Değişken",orientation="h",text="IQR Outlier (%)",color="IQR Outlier (%)",color_continuous_scale=[CREAM,SAGE_SOFT,SAGE_DARK],title="IQR kuralına göre aykırı gözlem oranları")
    fig.update_layout(coloraxis_showscale=False); fig.update_traces(texttemplate="%{text:.2f}%")
    st.plotly_chart(transparent(fig,500),use_container_width=True)
    st.markdown('<div class="warning"><b>Neden IQR’ın bulduğu her şeyi silmedim?</b><br/>Airbnb pazarı doğal olarak heterojen. Çok lüks, yüksek kapasiteli veya çok banyolu gerçek ilanlar dağılımın uçlarında olabilir. Bu yüzden “istatistiksel olarak aykırı” olmak otomatik olarak “veri hatası” anlamına gelmiyor.</div>',unsafe_allow_html=True)
    explain("Bathrooms değişkeninde ne fark ettim?","Banyo sayısında Q1 ve Q3 değerlerinin ikisi de 1 olduğu için IQR=0 çıktı. Böyle olunca 1 banyodan farklı çok sayıda geçerli ilan otomatik olarak aykırı işaretleniyordu. Bu, mekanik IQR temizliğinin veri yapısını bozabileceğini gösterdi.")
    explain("Son kararı nasıl verdim?","IQR'ı uç değerleri tanımak için kullandım; ancak açıklayıcı değişkenlerde her outlier'ı silmedim. Hedef fiyat için eğitim verisinden öğrenilen IQR kapsamını kullandım. Açıklayıcı değişkenlerde yalnızca aşırı üst değerlerin etkisini eğitim verisinin %99 yüzdelik sınırıyla kontrol ettim.")
    st.markdown('<div class="insight"><b>Ana mesaj:</b> Outlier tespiti ile outlier müdahalesini birbirinden ayırdım. Önce “uç değer var mı?” dedim; sonra “bu değer gerçekten silinmeli mi?” sorusunu veri yapısına göre ayrıca değerlendirdim.</div>',unsafe_allow_html=True)

elif page=="5 · Keşifsel Veri Analizi":
    hero("FAZ 1 · VERİYİ ANLAMA","Keşifsel Veri Analizi (EDA)","Aykırı değer yapısını gördükten sonra fiyat dağılımını, oda tiplerini ve sayısal değişkenlerin fiyatla ilişkisini ayrıntılı olarak inceledim.")
    st.markdown("### 1 · Fiyat dağılımı")
    st.image("images/price_distribution.png",use_container_width=True)
    c1,c2,c3=st.columns(3)
    with c1: metric_card("Medyan fiyat","205,50 €","Dağılımın orta noktası")
    with c2: metric_card("Ortalama fiyat","321,23 €","Yüksek fiyatlardan daha fazla etkileniyor")
    with c3: metric_card("Dağılım","Sağa çarpık","Uzun sağ kuyruk")
    st.markdown('<div class="insight"><b>Grafik yorumu:</b><br/>İlanların büyük kısmı düşük ve orta fiyat aralıklarında toplanıyor; fiyat yükseldikçe ilan sayısı hızla azalıyor. Sağ tarafta uzayan kuyruk az sayıdaki çok pahalı ilandan kaynaklanıyor. Medyanın 205,50 €, ortalamanın 321,23 € olması da yüksek fiyatlı ilanların ortalamayı yukarı çektiğini gösteriyor. Bu bulgu hem outlier kontrolünü hem de normal dağılım varsayımını sorgulamam gerektiğini gösterdi.</div>',unsafe_allow_html=True)
    st.markdown("### 2 · Oda tipine göre fiyat")
    explain("Oda tiplerinde ne gördüm?","Hotel room en yüksek medyan fiyata sahipti; entire home/apartment ikinci sıradaydı. Private room ve shared room kategorilerinde medyan fiyat daha düşüktü. Bu nedenle oda tipinin fiyatı ayıran anlamlı bir kategorik özellik olduğunu düşündüm.")
    st.markdown("### 3 · Spearman korelasyon matrisi")
    st.image("images/correlation_matrix.png",use_container_width=True)
    c1,c2,c3,c4,c5=st.columns(5)
    vals=[("Misafir kapasitesi","ρ≈0,60","En güçlü pozitif"),("Yatak sayısı","ρ≈0,54","Pozitif"),("Yatak odası","ρ≈0,53","Pozitif"),("Banyo sayısı","ρ≈0,43","Pozitif"),("Minimum gece","ρ≈-0,33","Negatif")]
    for col,(a,b,c) in zip([c1,c2,c3,c4,c5],vals):
        with col: metric_card(a,b,c)
    st.markdown('<div class="purple-note"><b>Korelasyon yorumu:</b><br/>Fiyatla en güçlü pozitif ilişki maksimum misafir kapasitesinde. Yatak ve yatak odası sayıları da benzer biçimde pozitif ilişki gösteriyor; yani ilan fiziksel olarak büyüdükçe fiyat genel olarak yükseliyor. Minimum konaklama süresi ise fiyatla orta düzeyde negatif ilişkili. Ancak korelasyon nedensellik göstermediği için bu ilişkileri daha sonra model sonuçları ve özellik önemleriyle birlikte değerlendirdim.</div>',unsafe_allow_html=True)

elif page=="6 · İstatistiksel Analiz":
    hero("FAZ 1 · VERİYİ ANLAMA","İstatistiksel Analiz","EDA'da gördüğüm ilişkileri yalnızca grafiklere bırakmak istemedim. Dağılım yapısına uygun testlerle sayısal ve kategorik ilişkileri ayrıca değerlendirdim.")
    explain("Neden önce normal dağılımı kontrol ettim?","Kullanacağım istatistiksel yöntemin verinin dağılım yapısına uygun olmasını istedim. Fiyat değişkenini 5.000 gözlemlik örneklem üzerinde Shapiro-Wilk testiyle kontrol ettim ve normal dağılım varsayımı desteklenmedi.")
    explain("Neden Pearson yerine Spearman kullandım?","Fiyat dağılımı sağa çarpık ve uç değerler içeriyordu. Spearman sıralamalara dayandığı ve doğrusal ilişki varsayımına Pearson kadar bağımlı olmadığı için sayısal ilişkilerde Spearman'ı kullandım.")
    explain("Kategorik gruplarda ne kullandım?","Oda tipi ve mahalle grupları arasındaki fiyat farklarını Kruskal-Wallis testiyle değerlendirdim. Normal dağılım varsayımı desteklenmediği için parametrik olmayan bu yöntemi tercih ettim.")
    st.markdown('<div class="warning"><b>Yorum ilkesi:</b> Veri seti büyük olduğu için çok küçük farklar bile küçük p-değerleri üretebilir. Bu nedenle istatistiksel anlamlılığı tek başına yeterli görmedim; ilişki büyüklüğünü ve grafiksel bulguları da birlikte yorumladım.</div>',unsafe_allow_html=True)
    st.markdown('<div class="result-box"><b>FAZ 1 sonunda:</b><br/>Fiyat dağılımının sağa çarpık olduğunu, kapasite ve fiziksel büyüklük değişkenlerinin fiyatla güçlü pozitif ilişkiler gösterdiğini, oda tipi grupları arasında fiyat farkları bulunduğunu ve mekanik outlier silmenin veri yapısını bozabileceğini biliyorum. Artık model geliştirme aşamasına daha kontrollü geçebilirim.</div>',unsafe_allow_html=True)

elif page=="7 · Modelleme İçin Veri Hazırlama":
    hero("FAZ 2 · MODEL GELİŞTİRME","Train/Test Ayrımı ve Preprocessing","Veriyi anladıktan sonra model geliştirme aşamasına geçtim. Buradaki en önemli hedefim, test verisinin eğitim kararlarına sızmasını engellemekti.")
    c1,c2=st.columns(2)
    with c1: metric_card("Eğitim seti","%80","Modelin öğrendiği bölüm")
    with c2: metric_card("Test seti","%20","Final genelleme değerlendirmesi")
    explain("Neden önce train/test ayırdım?","Eksik değer doldurma, outlier sınırı belirleme, kategorik kodlama ve ölçekleme gibi adımların test setine bakılarak öğrenilmesini istemedim. Bu nedenle önce %80 eğitim ve %20 test ayrımı yaptım.")
    explain("Data leakage'i nasıl önledim?","Medyan/mod değerlerini, capping sınırlarını, one-hot encoding dönüşümünü ve gerekli ölçekleme parametrelerini yalnızca eğitim verisinden öğrendim; test setine aynı dönüşümleri sonradan uyguladım.")
    explain("Neden one-hot encoding?","Oda tipi ve mahalle gibi kategorik alanları modellerin kullanabileceği sayısal forma dönüştürmek için kullandım.")
    explain("Scaling neden her modelde aynı değil?","Ridge, Lasso ve ElasticNet gibi doğrusal regularization modelleri ölçeğe duyarlı olduğu için sayısal değişkenleri standardize ettim. Decision Tree ve Random Forest gibi ağaç tabanlı modeller eşiklere göre bölündüğü için scaling'e ihtiyaç duymadı.")
    st.markdown('<div class="insight"><b>Amaç:</b> Test setini model geliştirme kararları için kullanmamak ve final performans ölçümünü mümkün olduğunca tarafsız tutmak.</div>',unsafe_allow_html=True)

elif page=="8 · Modeller ve Değerlendirme":
    hero("FAZ 2 · MODEL GELİŞTİRME","Model Seçimi ve Değerlendirme Metrikleri","Tek bir algoritmanın sonucuna güvenmek yerine farklı model ailelerini aynı veri üzerinde karşılaştırdım. Böylece daha karmaşık modeller gerçekten test performansına katkı sağlıyor mu görebildim.")
    st.markdown('<span class="chip">Linear Regression</span><span class="chip">Ridge</span><span class="chip">Lasso</span><span class="chip">ElasticNet</span><span class="chip">Decision Tree</span><span class="chip">Gradient Boosting</span><span class="chip">Random Forest</span>',unsafe_allow_html=True)
    st.markdown("### Neden bu modeller?")
    explain("Linear Regression","Basit ve yorumlanabilir bir baseline oluşturdum. Daha karmaşık modeller gerçekten değer katıyor mu bunu görmek istedim.")
    explain("Ridge, Lasso, ElasticNet","Regularization'ın doğrusal model performansını ve genellemeyi iyileştirip iyileştirmediğini test ettim.")
    explain("Decision Tree","Doğrusal olmayan ilişkileri ve değişken etkileşimlerini yakalamak istedim; aynı zamanda overfitting riskini gözlemledim.")
    explain("Gradient Boosting ve Random Forest","Birden fazla ağacı bir araya getiren ensemble yaklaşımlarının tek ağaçtan ve doğrusal modellerden daha güçlü genelleme sağlayıp sağlamadığını karşılaştırdım.")
    st.markdown("### Hangi metriklerle değerlendirdim?")
    c1,c2,c3=st.columns(3)
    with c1: explain("R²","Gecelik fiyat değişkenindeki varyansın model tarafından ne kadarının açıklandığını gösteriyor.")
    with c2: explain("MAE","Tahminlerin gerçek fiyatlardan ortalama mutlak olarak kaç euro saptığını gösteriyor; iş açısından kolay yorumlanıyor.")
    with c3: explain("RMSE","Büyük tahmin hatalarını daha güçlü cezalandırıyor; modelin ciddi hata üretme eğilimini görmemi sağlıyor.")
    st.markdown('<div class="purple-note"><b>Model seçim kuralım:</b> Tek başına en yüksek R²’ye bakmadım. Test R²’nin yüksek, MAE ve RMSE’nin düşük olmasını; aynı zamanda train-test farkının gereksiz biçimde büyümemesini istedim.</div>',unsafe_allow_html=True)

elif page=="9 · Overfitting Analizi":
    hero("FAZ 2 · MODEL GELİŞTİRME","Overfitting Analizi","Model geliştirme sırasında en önemli sorunlardan biri, eğitim verisinde çok başarılı görünen bir modelin yeni veride aynı başarıyı gösterememesiydi.")
    explain("Overfitting'i nasıl fark ettim?","İlk kontrolsüz Decision Tree eğitim verisinde R² değerini neredeyse 1,00 seviyesine taşıdı; fakat test performansı belirgin biçimde daha düşük kaldı. Bu yüzden yüksek train skorunu başarı olarak yorumlamadım.")
    explain("Decision Tree neden buna yatkın?","Ağaç çok derinleştiğinde eğitim verisini çok ayrıntılı bölerek gürültüyü bile öğrenebilir. Bu da train performansını yükseltirken genelleme gücünü düşürebilir.")
    explain("Ne yaptım?","max_depth, min_samples_split ve min_samples_leaf gibi karmaşıklık parametrelerini sınırlandırdım. Böylece modelin her küçük ayrıntıyı ayrı bir dala dönüştürmesini engellemeye çalıştım.")
    st.markdown('<div class="insight"><b>Hedefim train-test farkını sıfırlamak değildi.</b> Amaç, test başarısını korurken model varyansını kabul edilebilir düzeyde tutmaktı. Daha düşük train skoru, eğer test performansı daha dengeli hale geliyorsa başarısızlık değildir.</div>',unsafe_allow_html=True)

elif page=="10 · Eğitim Verisi Miktarı":
    hero("FAZ 2 · MODEL GELİŞTİRME","Eğitim Verisi Miktarının Etkisi","Overfitting'in yalnızca veri miktarından kaynaklanıp kaynaklanmadığını anlamak için test setini sabit tuttum ve aynı Random Forest yaklaşımını farklı büyüklükte eğitim verileriyle tekrar çalıştırdım.")
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=size_df["Kullanılan oran"],y=size_df["Train R²"],mode="lines+markers",name="Train R²",line=dict(color=SAGE_DARK,width=4),marker=dict(size=10)))
    fig.add_trace(go.Scatter(x=size_df["Kullanılan oran"],y=size_df["Test R²"],mode="lines+markers",name="Test R²",line=dict(color=LILAC_DARK,width=4),marker=dict(size=10)))
    fig.update_layout(title="Eğitim verisi büyüdükçe Train/Test performansı",xaxis_title="Kullanılan eğitim verisi (%)",yaxis_title="R²",legend=dict(orientation="h",y=1.13))
    st.plotly_chart(transparent(fig,500),use_container_width=True)
    st.dataframe(size_df[["Eğitim verisi","Train R²","Test R²","Train-Test Farkı"]].style.format({"Train R²":"{:.4f}","Test R²":"{:.4f}","Train-Test Farkı":"{:.4f}"}),use_container_width=True,hide_index=True)
    st.markdown('<div class="insight"><b>Grafik yorumu:</b><br/>Eğitim verisinin yalnızca %10’unu kullandığımda Test R² yaklaşık 0,584’tü. Veri miktarını artırdıkça Test R² düzenli biçimde yükseldi ve %100 eğitim verisinde yaklaşık 0,631’e ulaştı. Train R² ise büyük ölçüde benzer seviyede kaldı. Bu nedenle daha az veri kullanmanın overfitting’i çözmediği; aksine daha fazla gözlemin genelleme performansına katkı sağladığı sonucuna vardım.</div>',unsafe_allow_html=True)

elif page=="11 · Random Forest Optimizasyonu":
    hero("FAZ 2 · MODEL GELİŞTİRME","Random Forest Optimizasyonu","Random Forest en güçlü adaylardan biri olduktan sonra hiperparametrelerini test setine bakmadan, çapraz doğrulama üzerinden daha kontrollü biçimde seçtim.")
    explain("Neden GridSearchCV?","Tek bir hiperparametre kombinasyonunu rastgele seçmek yerine belirlediğim seçenekleri 5-fold cross-validation ile karşılaştırdım. Böylece kararımı tek bir train/test bölünmesine daha az bağımlı hale getirdim.")
    explain("Neden 10.000 eğitim gözlemi?","Tüm eğitim verisinde geniş 5-fold arama hesaplama açısından daha maliyetliydi. Bu nedenle yalnızca eğitim setinden sabit bir 10.000 gözlemlik alt küme seçtim. Test verisini hiperparametre aramasına dahil etmedim.")
    explain("Sonra ne yaptım?","Seçtiğim parametrelerle final Random Forest modelini yeniden tüm eğitim verisi üzerinde eğittim. Böylece tuning yönetilebilir kaldı fakat final model mevcut eğitim verisinin tamamından yararlandı.")
    st.markdown("### Final Random Forest parametreleri")
    st.dataframe(rf_params,use_container_width=True,hide_index=True)
    st.markdown('<div class="purple-note"><b>Seçim ilkesi:</b> Hiperparametrelerde yalnızca en yüksek train skorunu değil, cross-validation performansını ve train-validation farkını da dikkate aldım. Amaç daha karmaşık değil, daha iyi genelleyen modeli seçmekti.</div>',unsafe_allow_html=True)

elif page=="12 · Final Model ve Bulgular":
    hero("FAZ 2 · MODEL GELİŞTİRME","Final Model ve Temel Bulgular","Tüm modelleri aynı test çerçevesinde karşılaştırdıktan sonra Random Forest en dengeli genel sonucu verdi.")
    st.markdown("### Model karşılaştırması")
    st.image("images/model_comparison.png",use_container_width=True)
    st.dataframe(model_df.style.format({"Train R²":"{:.4f}","Test R²":"{:.4f}","RMSE (€)":"{:.2f}","MAE (€)":"{:.2f}","Train-Test Farkı":"{:.4f}"}),use_container_width=True,hide_index=True)
    st.markdown('<div class="insight"><b>Model karşılaştırma yorumu:</b><br/>Linear Regression, Ridge, Lasso ve ElasticNet modellerinin Test R² değerleri yaklaşık 0,55 civarında ve birbirine çok yakın kaldı. Regularization doğrusal model performansını belirgin biçimde artırmadı. Gradient Boosting ile Test R² 0,6179’a, Random Forest ile 0,6324’e yükseldi. Bu sonuç, fiyat yapısında yalnızca doğrusal ilişkilerin değil, doğrusal olmayan ilişkilerin ve değişken etkileşimlerinin de önemli olduğunu düşündürüyor.</div>',unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    with c1: metric_card("Final model","Random Forest","En yüksek Test R²")
    with c2: metric_card("Train R²","0,7562","Final model")
    with c3: metric_card("Test R²","0,6324","Yaklaşık %63 açıklanan varyans")
    with c4: metric_card("MAE","58,06 €","Ortalama mutlak hata")
    st.markdown('<div class="purple-note"><b>MAE=58,06 €:</b> Final modelin tahminleri test verisindeki gerçek gecelik fiyatlardan ortalama mutlak olarak yaklaşık 58 € sapıyor. RMSE’nin 81,71 € olması ise bazı daha büyük tahmin hatalarının bulunduğunu gösteriyor.</div>',unsafe_allow_html=True)
    st.markdown("### Özellik önemleri")
    st.image("images/feature_importance.png",use_container_width=True)
    st.markdown('<div class="insight"><b>Özellik önemleri yorumu:</b><br/>Maksimum misafir kapasitesi, minimum konaklama süresi ve yatak odası sayısı final modelde en önemli değişkenler arasında. Enlem ve boylam gibi konum değişkenleri de üst sıralarda. Minimum konaklama süresinin basit korelasyonda negatif ilişki göstermesine rağmen model içinde yüksek önem alması, ilişkinin yalnızca doğrusal olmadığını ve diğer değişkenlerle etkileşim içinde değerlendirildiğini gösteriyor.</div>',unsafe_allow_html=True)
    st.markdown('<div class="warning"><b>Dikkat:</b> Random Forest feature importance nedensellik kanıtlamaz. Burada gördüğüm şey, modelin tahmin yaparken hangi değişkenlerden daha fazla yararlandığıdır.</div>',unsafe_allow_html=True)

elif page=="13 · Sonuç ve Hipotezler":
    hero("FAZ 3 · SONUÇ","Sonuç ve Hipotezlerin Değerlendirilmesi","Son adımda başlangıçta kurduğum hipotezlere geri dönüp elde ettiğim bulguların bu beklentileri ne ölçüde desteklediğini değerlendiriyorum.")
    st.markdown('''<div class="hypothesis"><div class="h-title">Hipotez 1 · Kapasite ve fiziksel özellikler fiyatla pozitif ilişkilidir.</div><div class="supported">✓ Desteklendi</div><br/>Maksimum misafir kapasitesi fiyatla yaklaşık ρ=0,60; yatak sayısı ρ=0,54; yatak odası ρ=0,53 ve banyo sayısı ρ=0,43 pozitif Spearman ilişkisi gösterdi. İlan büyüklüğü ve kapasitesinin fiyat yapısında önemli olduğu beklentim desteklendi.</div><div class="hypothesis"><div class="h-title">Hipotez 2 · Ağaç tabanlı modeller doğrusal modellerden daha başarılı olacaktır.</div><div class="supported">✓ Desteklendi</div><br/>Doğrusal modeller Test R²≈0,55 seviyesinde kalırken Gradient Boosting 0,6179 ve Random Forest 0,6324 Test R² elde etti. Bu sonuç doğrusal olmayan ilişkilerin ve değişken etkileşimlerinin önemini destekliyor.</div><div class="hypothesis"><div class="h-title">Hipotez 3 · Model karmaşıklığı kontrol edildiğinde overfitting azaltılabilir.</div><div class="supported">✓ Büyük ölçüde desteklendi</div><br/>İlk kontrolsüz Decision Tree'deki büyük train-test farkı, karmaşıklık sınırlandırıldığında ve Random Forest çapraz doğrulama ile ayarlandığında daha dengeli hale geldi. Final modelde Train R²=0,7562 ve Test R²=0,6324 arasında hâlâ fark var; yani overfitting tamamen ortadan kalkmadı, fakat belirgin biçimde azaltıldı.</div>''',unsafe_allow_html=True)
    st.markdown("### Bu projeden ne elde ettim?")
    st.markdown('<div class="result-box">Paris Airbnb fiyatlarının tek bir özellik tarafından açıklanmadığını; özellikle <b>kapasite, fiziksel özellikler, oda tipi ve konumun</b> birlikte önemli olduğunu gördüm. Doğrusal modeller temel bir referans sağladı fakat en güçlü test performansı Random Forest’tan geldi. Projenin en önemli çıktısı yalnızca “en iyi model Random Forest” demek değil; <b>aykırı değerleri körlemesine silmeden, data leakage’i önleyerek ve overfitting’i train-test/CV farklarıyla izleyerek daha savunulabilir bir modelleme süreci kurabilmek</b> oldu.</div>',unsafe_allow_html=True)
    st.markdown("### Nasıl geliştirilebilir?")
    c1,c2=st.columns(2)
    with c1:
        explain("Daha güçlü mekânsal özellikler","Louvre, Eyfel Kulesi, metro istasyonları ve şehir merkezine uzaklık gibi Paris'e özgü konum özellikleri modele eklenebilir.")
        explain("Daha zengin ilan bilgileri","İlan açıklamaları, amenities ayrıntıları, yorum metinleri, fotoğraf kalitesi ve host özellikleri tahmin gücünü artırabilir.")
    with c2:
        explain("Farklı model aileleri","XGBoost, CatBoost ve LightGBM gibi boosting modelleri Random Forest ile karşılaştırılabilir.")
        explain("Daha güçlü doğrulama","Nested cross-validation ve farklı veri kesitleri üzerinde dış doğrulama ile genelleme performansı daha kapsamlı test edilebilir.")
    st.markdown('<div class="purple-note"><b>Sunumu kapatırken:</b> “Sonuç olarak, bu projede hedefim yalnızca yüksek bir skor üretmek değil; veri yapısını anlayarak, verdiğim preprocessing ve modelleme kararlarını gerekçelendirebildiğim ve yeni veriye daha sağlıklı genellenebilen bir fiyat tahmin süreci oluşturmaktı.”</div>',unsafe_allow_html=True)
