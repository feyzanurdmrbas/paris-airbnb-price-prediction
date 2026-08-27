import streamlit as st

# Sayfa ayarları
st.set_page_config(
    page_title="Paris Airbnb Fiyat Tahmini",
    page_icon="🏠",
    layout="wide"
)

# -----------------------------
# Başlık
# -----------------------------
st.title("🏠 Paris Airbnb Gecelik Fiyat Tahmini")
st.write(
    """
    Bu uygulama, Paris'teki Airbnb ilanlarının gecelik fiyatlarını incelemek
    ve makine öğrenmesi modellerinin sonuçlarını etkileşimli olarak sunmak
    amacıyla hazırlanmıştır.
    """
)

st.divider()

# -----------------------------
# Temel proje bilgileri
# -----------------------------
st.subheader("📌 Proje Özeti")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Ham Veri", "77.679 ilan")

with col2:
    st.metric("Analiz Verisi", "48.402 ilan")

with col3:
    st.metric("En İyi Model", "Random Forest")

with col4:
    st.metric("Test R²", "0,6324")

st.write(
    """
    Projede Linear Regression, Ridge, Lasso, ElasticNet, Decision Tree,
    Gradient Boosting ve Random Forest modelleri karşılaştırılmıştır.
    En başarılı model Random Forest olmuştur.
    """
)

st.divider()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📊 Menü")

sayfa = st.sidebar.radio(
    "Bölüm seçiniz:",
    [
        "Genel Bakış",
        "Veri Analizi",
        "Model Karşılaştırması",
        "Özellik Önemleri",
        "Proje Süreci"
    ]
)

# -----------------------------
# GENEL BAKIŞ
# -----------------------------
if sayfa == "Genel Bakış":

    st.header("🔎 Genel Bakış")

    st.write(
        """
        Projenin amacı, Paris Airbnb ilanlarının gecelik fiyatlarını;
        konum, oda tipi, konaklama kapasitesi, yatak odası, banyo,
        minimum konaklama süresi ve değerlendirme bilgileri gibi
        özelliklerden yararlanarak tahmin etmektir.
        """
    )

    st.info(
        """
        Temel hipotez: Airbnb fiyatları yalnızca tek bir değişkene bağlı değildir.
        Özellikle kapasite ve konum değişkenlerinin birlikte etkili olduğu,
        doğrusal olmayan ilişkiler nedeniyle ağaç tabanlı modellerin daha
        başarılı olabileceği düşünülmüştür.
        """
    )

    st.subheader("Final Random Forest Sonuçları")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Train R²", "0,7562")

    with c2:
        st.metric("Test R²", "0,6324")

    with c3:
        st.metric("RMSE", "81,71 €")

    with c4:
        st.metric("MAE", "58,06 €")


# -----------------------------
# VERİ ANALİZİ
# -----------------------------
elif sayfa == "Veri Analizi":

    st.header("📈 Keşifsel Veri Analizi")

    st.subheader("Gecelik Fiyat Dağılımı")

    st.image(
        "images/price_distribution.png",
        use_container_width=True
    )

    st.write(
        """
        Fiyat dağılımı belirgin şekilde sağa çarpıktır.
        İlanların büyük bölümü düşük ve orta fiyat aralıklarında yer alırken,
        az sayıdaki yüksek fiyatlı ilan uzun bir sağ kuyruk oluşturmaktadır.
        """
    )

    st.subheader("Spearman Korelasyon Matrisi")

    st.image(
        "images/correlation_matrix.png",
        use_container_width=True
    )

    st.write(
        """
        Fiyatla en güçlü pozitif ilişkiler accommodates, beds,
        bedrooms ve bathrooms değişkenlerinde görülmüştür.
        Minimum_nights ise fiyatla negatif yönlü ilişki göstermektedir.
        """
    )


# -----------------------------
# MODEL KARŞILAŞTIRMASI
# -----------------------------
elif sayfa == "Model Karşılaştırması":

    st.header("🤖 Regresyon Modellerinin Karşılaştırılması")

    st.image(
        "images/model_comparison.png",
        use_container_width=True
    )

    st.write(
        """
        Random Forest, Test R² açısından en başarılı model olmuştur.
        Gradient Boosting ikinci sırada yer alırken doğrusal modeller
        birbirine oldukça yakın sonuçlar vermiştir.
        """
    )

    st.success(
        """
        Random Forest:
        Test R² = 0,6324  
        RMSE = 81,71 €  
        MAE = 58,06 €
        """
    )


# -----------------------------
# ÖZELLİK ÖNEMLERİ
# -----------------------------
elif sayfa == "Özellik Önemleri":

    st.header("🌿 Random Forest Özellik Önemleri")

    st.image(
        "images/feature_importance.png",
        use_container_width=True
    )

    st.write(
        """
        Final modelde özellikle accommodates, minimum_nights ve bedrooms
        öne çıkmaktadır. Latitude ve longitude değişkenlerinin de yüksek
        önem taşıması, konum bilgisinin fiyat tahminindeki rolünü göstermektedir.
        """
    )


# -----------------------------
# PROJE SÜRECİ
# -----------------------------
elif sayfa == "Proje Süreci":

    st.header("🧩 Proje Süreci")

    st.markdown(
        """
        **1. Veri Kaynağı**  
        Inside Airbnb Paris veri seti kullanıldı.

        **2. Veri Temizleme**  
        Geçersiz fiyatlar çıkarıldı ve eksik değerler incelendi.

        **3. Aykırı Değer Analizi**  
        IQR yöntemi tanısal olarak kullanıldı. Her aykırı değer otomatik
        olarak silinmedi.

        **4. Keşifsel Veri Analizi**  
        Fiyat dağılımı, oda tipleri ve Spearman korelasyonları incelendi.

        **5. Train / Test Ayrımı**  
        Veri %80 eğitim, %20 test olarak ayrıldı.

        **6. Modelleme**  
        Yedi farklı regresyon yaklaşımı karşılaştırıldı.

        **7. Overfitting Kontrolü**  
        Decision Tree ve Random Forest modellerinde eğitim-test farkları
        incelendi.

        **8. Hiperparametre Optimizasyonu**  
        Random Forest için 5-fold cross-validation ve GridSearchCV kullanıldı.

        **9. Final Model**  
        En başarılı model Random Forest olarak belirlendi.
        """
    )

    st.warning(
        """
        Projenin önemli bulgularından biri, daha az eğitim verisi kullanmanın
        overfitting sorununu çözmemesidir. Veri miktarı arttıkça test
        performansı yükselmiştir.
        """
    )
