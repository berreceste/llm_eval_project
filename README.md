# RAG Değerlendirme Projesi

Bu proje, Retrieval Augmented Generation (RAG) sistemlerinin ve dil modeli yanıtlarının kalitesini çeşitli metrikler aracılığıyla değerlendirmek için tasarlanmıştır. Proje, `ragas` kütüphanesini temel alarak farklı değerlendirme metriklerini uygulayan Python script'lerinden oluşmaktadır. Her bir script, belirli bir veri setini kullanarak bir veya daha fazla metriği hesaplar ve sonuçları genellikle bir CSV dosyasına kaydeder.

## Proje Yapısı

```
.
├── data/
│   ├── raw/                     # Ham veri setleri
│   │   ├── ragas_ready_dataset_v2.csv # Değerlendirme için kullanılan ana veri setlerinden biri
│   │   ├── ragas_ready_dataset_v4.csv # Değerlendirme için kullanılan ana veri setlerinden biri
│   │   └── test_cases.csv           # evaulate.py tarafından kullanılan test case'leri
│   └── processed/               # Script'ler tarafından üretilen sonuç CSV dosyaları ve işlenmiş veri setleri
│       ├── ragas_ready_dataset_v6.csv       # ContextEntityRecall.py tarafından üretilen işlenmiş veri
│       ├── noise_relevancy_faithfulness_results.csv # EvaluateNoiseFaithRelevancy.py sonuçları
│       ├── context_entity_recall_results.csv      # ContextEntityRecall .py sonuçları
│       ├── context_recall_results.csv             # evaulatecontextrecall.py sonuçları
│       ├── context_precision_results.csv          # evaulatecontextprecision.py sonuçları
│       └── evaluation_results.csv                 # evulaterag.py sonuçları
├── src/
│   └── evaluation/
│       ├── EvaluateNoiseFaithRelevancy.py
│       ├── ContextEntityRecall .py
│       ├── evaulatecontextrecall.py
│       ├── evaulatecontextprecision.py
│       ├── evulaterag.py
│       └── evaulate.py
├── .gitignore
```

## Proje Akış Şeması

Aşağıda projenin genel veri ve işlem akışını gösteren bir diyagram bulunmaktadır:

```mermaid
graph TD
    A[data/raw/ragas_ready_dataset_v2.csv] --> B1[EvaluateNoiseFaithRelevancy.py]
    A --> B4[evaulatecontextprecision.py]
    A --> B5[evulaterag.py]

    C[data/raw/ragas_ready_dataset_v4.csv] --> B2[ContextEntityRecall .py]
    C --> B3[evaulatecontextrecall.py]

    B2 -- İşler ve üretir --> D[data/processed/ragas_ready_dataset_v6.csv]

    E[data/raw/test_cases.csv] --> B6[evaulate.py]

    B1 --> R1[data/processed/noise_relevancy_faithfulness_results.csv]
    B2 --> R2[data/processed/context_entity_recall_results.csv]
    B3 --> R3[data/processed/context_recall_results.csv]
    B4 --> R4[data/processed/context_precision_results.csv]
    B5 --> R5[data/processed/evaluation_results.csv]
    B6 -.-> R6[Konsol Çıktısı (DataFrame)]

    subgraph "Ham Veri Setleri (data/raw)"
        A
        C
        E
    end

    subgraph "Değerlendirme Script'leri (src/evaluation)"
        B1
        B2
        B3
        B4
        B5
        B6
    end

    subgraph "Sonuç Dosyaları / Çıktılar (data/processed ve Konsol)"
        R1
        R2
        R3
        R4
        R5
        R6
    end

    style A fill:#D5F5E3,stroke:#2ECC71,stroke-width:2px
    style C fill:#D5F5E3,stroke:#2ECC71,stroke-width:2px
    style E fill:#D5F5E3,stroke:#2ECC71,stroke-width:2px
    style D fill:#EBF5FB,stroke:#3498DB,stroke-width:2px

    style B1 fill:#FCF3CF,stroke:#F1C40F,stroke-width:2px
    style B2 fill:#FCF3CF,stroke:#F1C40F,stroke-width:2px
    style B3 fill:#FCF3CF,stroke:#F1C40F,stroke-width:2px
    style B4 fill:#FCF3CF,stroke:#F1C40F,stroke-width:2px
    style B5 fill:#FCF3CF,stroke:#F1C40F,stroke-width:2px
    style B6 fill:#FCF3CF,stroke:#F1C40F,stroke-width:2px

    style R1 fill:#FDEDEC,stroke:#E74C3C,stroke-width:2px
    style R2 fill:#FDEDEC,stroke:#E74C3C,stroke-width:2px
    style R3 fill:#FDEDEC,stroke:#E74C3C,stroke-width:2px
    style R4 fill:#FDEDEC,stroke:#E74C3C,stroke-width:2px
    style R5 fill:#FDEDEC,stroke:#E74C3C,stroke-width:2px
    style R6 fill:#FDEDEC,stroke:#E74C3C,stroke-width:2px
```
**Not:** `ContextEntityRecall .py` script'i, `data/raw/ragas_ready_dataset_v4.csv`'yi işleyerek `data/processed/ragas_ready_dataset_v6.csv` adlı bir ara işlenmiş veri dosyası üretir. Script, **bu işlenmiş veriyi kullanarak** `ContextEntityRecall` metriğini değerlendirir ve sonuçlarını `data/processed/context_entity_recall_results.csv` dosyasına yazar. Şemada, `data/processed/ragas_ready_dataset_v6.csv`'nin üretimi ve `context_entity_recall_results.csv`'nin bu işlenmiş veriden (dolaylı olarak `data/raw/ragas_ready_dataset_v4.csv`'den) türetildiği gösterilmiştir.

## Kullanılan Teknolojiler

*   Python 3.x
*   Pandas: Veri işleme ve CSV yönetimi için.
*   Ragas: RAG değerlendirme metrikleri için ana kütüphane.
*   Langchain & Langchain-OpenAI: Dil modelleri (özellikle OpenAI GPT-4o) ile etkileşim için.
*   Dotenv: Ortam değişkenlerini yönetmek için (API anahtarları vb.).
*   Langfuse: LLM çağrılarının takibi için (bazı scriptlerde entegre).
*   Datasets (Hugging Face): Veri setlerini yönetmek için (evaulate.py'de).

## Değerlendirme Script'leri ve Metrikler

Aşağıda her bir Python script'inin detayları, kullandığı veri setleri, hesapladığı metrikler ve ürettiği sonuç dosyaları listelenmiştir.

---

### 1. `src/evaluation/EvaluateNoiseFaithRelevancy.py`

*   **Açıklama:** Bu script, bir RAG sisteminin gürültüye duyarlılığını, yanıt alaka düzeyini ve sadakatini değerlendirir.
*   **Veri Seti:** `data/raw/ragas_ready_dataset_v2.csv`
    *   Bu CSV dosyasının `user_input`, `response`, `retrieved_contexts` ve `reference` sütunlarını kullanır.
    *   `retrieved_contexts` sütunu özel bir temizleme ve `ast.literal_eval` ile işleme sürecinden geçer.
*   **Kullanılan Metrikler (Ragas):**
    *   `NoiseSensitivity`: Modelin alakasız veya gürültülü bağlam girdilerine ne kadar duyarlı olduğunu ölçer. Yüksek skor, gürültüden daha az etkilendiğini gösterir. (Değer Aralığı: Genellikle 0-1)
    *   `ResponseRelevancy`: Üretilen yanıtın verilen girdiye (soruya) ne kadar alakalı olduğunu ölçer. Yüksek skor, daha yüksek alaka düzeyini gösterir. (Değer Aralığı: Genellikle 0-1)
    *   `Faithfulness`: Üretilen yanıtın sağlanan bağlama ne kadar sadık kaldığını, yani bağlamdaki bilgilere dayanıp dayanmadığını ölçer. Yüksek skor, yanıtın bağlamla daha tutarlı olduğunu gösterir. (Değer Aralığı: Genellikle 0-1)
*   **Sonuç Dosyası:** `data/processed/noise_relevancy_faithfulness_results.csv`
    *   Bu dosya, her bir veri örneği için hesaplanan `noise_sensitivity`, `response_relevancy` ve `faithfulness` skorlarını içerir.
*   **Önemli Fonksiyonlar:**
    *   `pd.read_csv()`: Veri setini yükler.
    *   `ast.literal_eval()`: `retrieved_contexts` sütununu Python listelerine dönüştürür.
    *   `EvaluationDataset.from_list()`: Veriyi Ragas formatına dönüştürür.
    *   `evaluate()`: Ragas metriklerini hesaplar.
    *   `results.to_pandas()` ve `df.to_csv()`: Sonuçları CSV'ye yazar.
*   **LLM:** `gpt-4o` (LangchainLLMWrapper aracılığıyla)

---

### 2. `src/evaluation/ContextEntityRecall .py`

*   **Açıklama:** Bu script, sağlanan bağlamdaki önemli varlıkların ne kadarının üretilen yanıtta veya referansta geri çağrıldığını değerlendirir.
*   **Veri Seti:**
    *   Giriş: `data/raw/ragas_ready_dataset_v4.csv`
    *   Çıkış (işlenmiş veri): `data/processed/ragas_ready_dataset_v6.csv`
    *   `retrieved_contexts` sütunu üzerinde karmaşık bir temizleme işlemi yapar (tek tırnakları çift tırnağa çevirme, `\\n` temizleme, `ast.literal_eval` ve `json.loads` ile ayrıştırma).
*   **Kullanılan Metrikler (Ragas):**
    *   `ContextEntityRecall`: Referans yanıtta veya soruda bulunan ve aynı zamanda sağlanan bağlamda da mevcut olan varlıkların ne kadarının model tarafından üretilen yanıtta da bulunduğunu ölçer. Yüksek skor, daha fazla ilgili varlığın yakalandığını gösterir. (Değer Aralığı: Genellikle 0-1)
*   **Sonuç Dosyası:** `data/processed/context_entity_recall_results.csv`
    *   Her örnek için `context_entity_recall` skorunu içerir.
*   **Önemli Fonksiyonlar:**
    *   Veri temizleme ve dönüştürme fonksiyonları (`ast.literal_eval`, `json.loads`).
    *   `EvaluationDataset.from_list()`
    *   `evaluate()`
    *   `results.to_pandas()` ve `df.to_csv()`
*   **LLM:** `gpt-4o` (LangchainLLMWrapper aracılığıyla)

---

### 3. `src/evaluation/evaulatecontextrecall.py`

*   **Açıklama:** Bu script, referans bağlamda (ground truth) bulunan bilgilerin ne kadarının geri getirilen bağlamda (retrieved context) bulunduğunu değerlendirir. İki farklı yaklaşımla ölçüm yapar: LLM tabanlı ve LLM tabanlı olmayan.
*   **Veri Seti:** `data/raw/ragas_ready_dataset_v4.csv`
    *   `retrieved_contexts` ve `reference_contexts` sütunlarını kullanır.
*   **Kullanılan Metrikler (Ragas):**
    *   `LLMContextRecall`: LLM kullanarak, referans bağlamdaki cümlelerin anlamca ne kadarının geri getirilen bağlamda kapsandığını ölçer. (Değer Aralığı: Genellikle 0-1)
    *   `NonLLMContextRecall`: LLM kullanmadan, genellikle metin benzerliği veya örtüşme yöntemleriyle referans bağlamdaki cümlelerin ne kadarının geri getirilen bağlamda bulunduğunu ölçer. (Değer Aralığı: Genellikle 0-1)
*   **Sonuç Dosyası:** `data/processed/context_recall_results.csv`
    *   Her örnek için `llm_context_recall` ve `non_llm_context_recall` skorlarını içerir.
*   **Önemli Fonksiyonlar:**
    *   `ast.literal_eval()` ve `eval()`: Bağlam sütunlarını işler.
    *   `EvaluationDataset.from_list()`
    *   `evaluate()`
    *   `results.to_pandas()` ve `df.to_csv()`
*   **LLM (LLMContextRecall için):** `gpt-4o`

---

### 4. `src/evaluation/evaulatecontextprecision.py`

*   **Açıklama:** Bu script, geri getirilen bağlamın ne kadarının gerçekten ilgili ve soruya yanıt vermek için gerekli olduğunu değerlendirir. İki farklı yaklaşımla ölçüm yapar: referanslı ve referanssız.
*   **Veri Seti:** `data/raw/ragas_ready_dataset_v2.csv`
*   **Kullanılan Metrikler (Ragas):**
    *   `LLMContextPrecisionWithReference`: LLM kullanarak, geri getirilen bağlamdaki cümlelerin, bir referans yanıt (ground truth) verildiğinde soruya ne kadar odaklı ve gürültüsüz olduğunu ölçer. (Değer Aralığı: Genellikle 0-1)
    *   `LLMContextPrecisionWithoutReference`: LLM kullanarak, geri getirilen bağlamdaki cümlelerin, bir referans yanıt olmadan, sadece soruya göre ne kadar odaklı ve gürültüsüz olduğunu ölçer. (Değer Aralığı: Genellikle 0-1)
*   **Sonuç Dosyası:** `data/processed/context_precision_results.csv`
    *   Her örnek için `llm_context_precision_with_reference` ve `llm_context_precision_without_reference` skorlarını içerir.
*   **Önemli Fonksiyonlar:**
    *   `ast.literal_eval()`: `retrieved_contexts` sütununu işler.
    *   `EvaluationDataset.from_list()`
    *   `evaluate()`
    *   `results.to_pandas()` ve `df.to_csv()`
*   **LLM:** `gpt-4o`

---

### 5. `src/evaluation/evulaterag.py`

*   **Açıklama:** Bu script, çeşitli RAG metriklerini bir arada değerlendirir. Özellikle "priority_accuracy" adında özel bir `AspectCritic` metriği içerir.
*   **Veri Seti:** `data/raw/ragas_ready_dataset_v2.csv`
*   **Kullanılan Metrikler (Ragas):**
    *   `AspectCritic (name="priority_accuracy")`:
        *   **Tanım:** "Test caseleri için üç öncelik seviyesi vardır: P1 (Yüksek Öncelik - Kritik, temel iş mantığını kapsayan testler), P2 (Orta Öncelik - Önemli, ancak akışları kesmeyenler), P3 (Düşük Öncelik - Küçük sorunlar, UI cilası veya uç durumlar). Atanan önceliğin (P1/P2/P3) her test case'i için uygun olup olmadığını değerlendirin."
        *   **Değer Aralığı:** Muhtemelen bir uygunluk skoru (0-1) veya kategorik bir değerlendirme (örn: Uygun/Uygun Değil gibi). Sonuç CSV'sinden teyit edilmelidir.
    *   `LLMContextRecall`: (Yukarıda açıklandı)
    *   `Faithfulness`: (Yukarıda açıklandı)
    *   `FactualCorrectness`: Üretilen yanıtın, sağlanan bağlamdaki bilgilere göre olgusal olarak ne kadar doğru olduğunu ölçer. Yüksek skor, daha yüksek olgusal doğruluğu gösterir. (Değer Aralığı: Genellikle 0-1)
*   **Sonuç Dosyası:** `data/processed/evaluation_results.csv`
    *   Her örnek için `priority_accuracy`, `llm_context_recall`, `faithfulness`, ve `factual_correctness` skorlarını içerir.
*   **Önemli Fonksiyonlar:**
    *   `eval()`: `retrieved_contexts` sütununu işler.
    *   `EvaluationDataset.from_list()`
    *   `evaluate()`
    *   `results.to_pandas()` ve `df.to_csv()`
*   **LLM:** `gpt-4o`

---

### 6. `src/evaluation/evaulate.py`

*   **Açıklama:** Bu script, `data/raw/test_cases.csv` dosyasındaki test caseleri için özel tanımlı bir "priority_accuracy" metriğini (AspectCritic kullanarak) değerlendirir.
*   **Veri Seti:** `data/raw/test_cases.csv`
    *   Bu dosyanın `user_input` ve `response` sütunlarını kullanır.
*   **Kullanılan Metrikler (Ragas):**
    *   `AspectCritic (name="priority_accuracy")`:
        *   **Tanım:** (Yukarıdaki `evulaterag.py` bölümünde açıklandığı gibi) Test caselerinin öncelik seviyelerinin uygunluğunu değerlendirir.
        *   **Değer Aralığı:** (Yukarıdaki `evulaterag.py` bölümünde açıklandığı gibi)
*   **Sonuç Dosyası:** Bu script sonuçları bir CSV dosyasına **kaydetmez**, doğrudan konsola yazdırır.
*   **Önemli Fonksiyonlar:**
    *   `pd.read_csv()`: Veri setini yükler.
    *   `Dataset.from_dict()` (Hugging Face datasets): Veriyi Ragas için uygun formata dönüştürür.
    *   `evaluate()`: Metriği hesaplar.
    *   `results.to_pandas()`: Sonuçları DataFrame'e çevirir ve `print()` ile konsola basar.
*   **LLM:** `gpt-4o`

## Kurulum ve Çalıştırma

1.  **Bağımlılıkları Yükleyin:**
    ```bash
    pip install pandas ragas langchain langchain-openai python-dotenv langfuse datasets
    ```
2.  **Ortam Değişkenleri:**
    Proje kök dizininde bir `.env` dosyası oluşturun ve OpenAI API anahtarınızı ekleyin:
    ```
    OPENAI_API_KEY="sk-YOUR_API_KEY"
    LANGFUSE_PUBLIC_KEY="pk-lf-..." # Eğer Langfuse kullanılıyorsa
    LANGFUSE_SECRET_KEY="sk-lf-..." # Eğer Langfuse kullanılıyorsa
    ```
3.  **Veri Setleri:**
    *   Gerekli ham CSV dosyalarının (`ragas_ready_dataset_v2.csv`, `ragas_ready_dataset_v4.csv`, `test_cases.csv`) `data/raw/` klasöründe bulunduğundan emin olun.
    *   `ContextEntityRecall .py` script'i çalıştırıldığında `data/processed/ragas_ready_dataset_v6.csv` dosyasını üretecektir.
4.  **Script'leri Çalıştırma:**
    İlgili Python script'ini doğrudan çalıştırabilirsiniz:
    ```bash
    python src/evaluation/EvaluateNoiseFaithRelevancy.py
    python src/evaluation/ContextEntityRecall .py
    # vb. diğer scriptler için
    ```
    Sonuçlar, script'in içinde belirtilen CSV dosyalarına (veya `evaulate.py` durumunda konsola) yazdırılacaktır.

## Metriklerin Değer Aralıkları ve Anlamları

Çoğu `ragas` metriği (örneğin `Faithfulness`, `ResponseRelevancy`, `ContextRecall`, `ContextPrecision`, `FactualCorrectness`, `NoiseSensitivity`) genellikle **0 ile 1 arasında** bir skor üretir.
*   **1'e yakın skorlar** genellikle daha iyi performansı gösterir (daha yüksek sadakat, alaka düzeyi, hatırlama, kesinlik, olgusal doğruluk veya gürültüye karşı daha iyi direnç).
*   **0'a yakın skorlar** ise genellikle daha düşük performansı gösterir.

`AspectCritic` metriği (bu projede "priority_accuracy" olarak kullanılmış), tanımına bağlı olarak farklı çıktılar verebilir. LLM'in yaptığı değerlendirmeye göre bir skor (0-1 aralığında olabilir) veya kategorik bir çıktı (örneğin, P1/P2/P3 atamasının "Uygun" veya "Uygun Değil" şeklinde bir değerlendirmesi ve gerekçesi) üretebilir. Oluşan sonuç CSV dosyalarındaki değerler bu konuda daha net bilgi verecektir. Genellikle bu metrikler de 0-1 arasında bir skora normalize edilir.

## Sorun Giderme (Troubleshooting)

Aşağıda, bu projeyi kullanırken karşılaşabileceğiniz bazı yaygın sorunlar ve çözüm önerileri bulunmaktadır:

1.  **`OPENAI_API_KEY` Hatası (AuthenticationError):**
    *   **Sorun:** Script'leri çalıştırırken `AuthenticationError` veya API anahtarının geçersiz olduğuna dair bir hata alıyorsanız.
    *   **Çözüm:**
        *   Proje kök dizininde `.env` adlı bir dosya oluşturduğunuzdan ve içine `OPENAI_API_KEY="sk-YOUR_API_KEY"` şeklinde geçerli OpenAI API anahtarınızı eklediğinizden emin olun.
        *   `load_dotenv()` fonksiyonunun script'lerin başında çağrıldığını kontrol edin.
        *   API anahtarınızın OpenAI hesabınızda aktif ve yeterli krediye sahip olduğunu doğrulayın.

2.  **Kütüphane Bağımlılık Hataları (ImportError):**
    *   **Sorun:** `ImportError: No module named 'ragas'` (veya başka bir kütüphane) gibi hatalar.
    *   **Çözüm:**
        *   Gerekli tüm kütüphanelerin kurulu olduğundan emin olun. Kurulum bölümündeki `pip install ...` komutunu çalıştırın:
          ```bash
          pip install pandas ragas langchain langchain-openai python-dotenv langfuse datasets
          ```
        *   Birden fazla Python ortamınız varsa doğru ortamda olduğunuzdan emin olun. Bir sanal ortam (virtual environment) kullanmanız önerilir.

3.  **Veri Dosyası Bulunamadı Hatası (FileNotFoundError):**
    *   **Sorun:** `FileNotFoundError: [Errno 2] No such file or directory: 'data/raw/ragas_ready_dataset_v2.csv'` gibi hatalar.
    *   **Çözüm:**
        *   Script'lerin beklediği CSV dosyalarının (`ragas_ready_dataset_v2.csv`, `ragas_ready_dataset_v4.csv`, `test_cases.csv`) doğru yolda (`data/raw/` klasörü altında) bulunduğundan emin olun.
        *   Dosya adlarının script'lerde belirtilenlerle tam olarak eşleştiğini kontrol edin (büyük/küçük harf duyarlılığına dikkat edin).

4.  **Veri Formatı Hataları (örn: `ast.literal_eval` veya `json.loads` hataları):**
    *   **Sorun:** `retrieved_contexts` veya diğer sütunlar işlenirken `ValueError: malformed node or string` gibi hatalar.
    *   **Çözüm:**
        *   Giriş CSV dosyalarındaki (özellikle `retrieved_contexts`) verilerin script'lerin beklediği formatta olduğundan emin olun. Bu sütunlar genellikle string olarak temsil edilen listeler veya JSON benzeri yapılar içerir.
        *   `ContextEntityRecall .py` script'i, `retrieved_contexts` sütununu temizlemek için hem `ast.literal_eval` hem de `json.loads` kullanır; bu, formatta bazı esneklikler olabileceğini gösterir ancak yine de dikkatli olunmalıdır.
        *   Veri setinizde beklenmedik karakterler, eksik tırnak işaretleri veya bozuk yapılar olup olmadığını kontrol edin.

5.  **Langfuse Entegrasyon Sorunları:**
    *   **Sorun:** Langfuse callback'leri ile ilgili hatalar veya Langfuse'a verilerin gitmemesi.
    *   **Çözüm:**
        *   Eğer Langfuse kullanıyorsanız, `.env` dosyanızda `LANGFUSE_PUBLIC_KEY` ve `LANGFUSE_SECRET_KEY` ortam değişkenlerinin doğru şekilde ayarlandığından emin olun.
        *   Langfuse sunucusunun erişilebilir olduğunu ve ağ bağlantınızda sorun olmadığını kontrol edin.

6.  **Metrik Hesaplama Süresinin Uzun Olması:**
    *   **Sorun:** Özellikle LLM tabanlı metriklerin (örn: `Faithfulness`, `ResponseRelevancy`) hesaplanması uzun sürebilir.
    *   **Çözüm:**
        *   Bu durum normaldir, çünkü her bir örnek için LLM çağrıları yapılır.
        *   Daha küçük veri alt kümeleriyle test ederek başlayabilirsiniz.
        *   `ragas` veya `langchain` kütüphanelerinde asenkron işleme veya toplu işleme (batch processing) gibi optimizasyonlar varsa, bunları araştırmayı düşünebilirsiniz (ancak mevcut script'ler bunları doğrudan kullanmıyor olabilir).

Bu listede olmayan bir sorunla karşılaşırsanız, hatanın tam metnini ve hangi script'i çalıştırdığınızı not alarak sorunu daha detaylı inceleyebilirsiniz.

## Metriklerin Değer Aralıkları, Detaylı Yorumlama ve Örnek Çıktılar

Bu bölümde, projede kullanılan `ragas` metriklerinin ne anlama geldiği, hangi değer aralıklarında sonuçlar ürettiği ve bu sonuçların nasıl yorumlanabileceği üzerine daha detaylı bilgiler sunulmaktadır. **Not:** Aşağıdaki CSV çıktı örnekleri varsayımsaldır ve metriklerin tipik yapılarını göstermek amaçlıdır. Gerçek çıktılar, kullanılan verilere ve LLM yanıtlarına göre değişiklik gösterecektir.

Çoğu `ragas` metriği (örneğin `Faithfulness`, `ResponseRelevancy`, `ContextRecall`, `ContextPrecision`, `FactualCorrectness`, `NoiseSensitivity`, `ContextEntityRecall`) genellikle **0 ile 1 arasında** bir skor üretir.
*   **1'e yakın skorlar** genellikle daha iyi performansı gösterir (daha yüksek sadakat, alaka düzeyi, hatırlama, kesinlik, olgusal doğruluk veya gürültüye karşı daha iyi direnç).
*   **0'a yakın skorlar** ise genellikle daha düşük performansı gösterir.

### Standart Ragas Metrikleri (0-1 Skalası)

Bu metrikler genellikle aşağıdaki gibi bir CSV yapısında sunulur (örneğin, `data/processed/noise_relevancy_faithfulness_results.csv` dosyasından bir kesit):

```
user_input,response,retrieved_contexts,reference,noise_sensitivity,response_relevancy,faithfulness
"Soru 1...","Yanıt 1...","[Bağlam 1A, Bağlam 1B]","Referans Yanıt 1",0.85,0.92,0.78
"Soru 2...","Yanıt 2...","[Bağlam 2A]","Referans Yanıt 2",0.91,0.75,0.88
...
```

**Yorumlama Örnekleri:**

*   **`Faithfulness` (Sadakat):**
    *   **Skor 0.9:** Üretilen yanıtın, sağlanan bağlamdaki bilgilere büyük ölçüde sadık kaldığını ve bağlam dışı bilgi içerme olasılığının düşük olduğunu gösterir. Model, iddialarını bağlamla destekleyebilmektedir.
    *   **Skor 0.7:** Üretilen yanıtın çoğunlukla bağlama sadık olduğunu ancak bazı kısımlarının bağlam tarafından tam olarak desteklenmiyor olabileceğini veya hafifçe bağlam dışına çıkmış olabileceğini gösterir.
    *   **Skor 0.5 veya altı:** Yanıtın bağlamla önemli ölçüde tutarsız olduğu veya bağlamda bulunmayan bilgiler içerdiği anlamına gelebilir. Bu durum "halüsinasyon" olarak da adlandırılır.

*   **`ResponseRelevancy` (Yanıt Alaka Düzeyi):**
    *   **Skor 0.95:** Üretilen yanıtın, kullanıcının sorusuyla son derece alakalı olduğunu ve sorunun özünü başarılı bir şekilde ele aldığını gösterir.
    *   **Skor 0.6:** Yanıtın soruyla kısmen alakalı olduğunu ancak tam olarak odaklanmamış olabileceğini veya sorunun bazı yönlerini eksik bırakmış olabileceğini gösterir.

*   **`ContextRecall` (Bağlam Hatırlama - LLMContextRecall / NonLLMContextRecall):**
    *   **Skor 0.8:** Referans (ground truth) bağlamda bulunan önemli bilgilerin %80'inin, model tarafından geri getirilen bağlamda (retrieved context) da bulunduğunu gösterir. Yüksek skor, RAG sisteminin ilgili dokümanları bulmada başarılı olduğunu işaret eder.

*   **`ContextPrecision` (Bağlam Kesinliği - LLMContextPrecisionWithReference / LLMContextPrecisionWithoutReference):**
    *   **Skor 0.85:** Geri getirilen bağlamın %85'inin gerçekten soruya yanıt vermek için alakalı ve gerekli olduğunu, gereksiz veya gürültülü bilgi oranının düşük olduğunu gösterir. Yüksek skor, RAG sisteminin sadece ilgili parçaları getirdiğini gösterir.

*   **`ContextEntityRecall` (Bağlam Varlık Hatırlama):**
    *   **Skor 0.75:** Referans yanıtta veya soruda bulunan ve aynı zamanda sağlanan bağlamda da mevcut olan önemli varlıkların %75'inin, model tarafından üretilen yanıtta da yakalandığını gösterir.

*   **`FactualCorrectness` (Olgusal Doğruluk):**
    *   **Skor 0.9:** Modelin ürettiği yanıtın, sağlanan bağlamdaki bilgilere göre yüksek derecede olgusal olarak doğru olduğunu gösterir.

*   **`NoiseSensitivity` (Gürültüye Duyarlılık):**
    *   **Skor 0.2:** Modelin, bağlama eklenen alakasız bilgilere (gürültüye) karşı oldukça duyarlı olduğunu gösterir. Yani, gürültü eklendiğinde yanıt kalitesi önemli ölçüde düşmektedir. Bu metrikte daha yüksek skorlar (1'e yakın) gürültüye karşı daha az duyarlılık (daha iyi performans) anlamına gelir. Bu nedenle, 0.2 düşük bir performansı işaret eder.

### `AspectCritic` Metriği ("priority_accuracy")

Bu metrik, LLM'in belirli bir tanım (aspect) doğrultusunda değerlendirme yapmasını sağlar. Projedeki "priority_accuracy" tanımı, test caselerinin önceliklendirilmesinin (P1/P2/P3) uygunluğunu değerlendirir.

Çıktısı genellikle bir skor (Ragas bunu 0 veya 1 olarak verebilir; 1=başarılı/uygun, 0=başarısız/uygun değil) ve LLM'in bu skoru neden verdiğine dair bir gerekçe (reasoning) içerir. `data/processed/evaluation_results.csv` dosyasında şöyle görünebilir:

```
user_input,response,retrieved_contexts,reference,priority_accuracy,llm_context_recall,faithfulness,factual_correctness
"Test Case A (P1 atanmış)","Model Yanıtı A...", "[Bağlam A]", "Referans A", 1.0, 0.9, 0.95, 0.88
"Test Case B (P3 atanmış)","Model Yanıtı B...", "[Bağlam B]", "Referans B", 0.0, 0.8, 0.85, 0.92
...
```
Bazı Ragas versiyonları veya yapılandırmaları, `AspectCritic` için doğrudan bir gerekçe sütunu eklemeyebilir ve bu bilgi `evaluate` fonksiyonunun döndürdüğü `Result` nesnesinin detaylarında bulunabilir. Eğer sadece skor (0/1 veya 0-1 aralığında) varsa:

*   **`priority_accuracy` Skoru 1.0:** LLM, atanan test case önceliğinin (P1/P2/P3) verilen tanıma göre uygun olduğuna karar vermiştir.
*   **`priority_accuracy` Skoru 0.0:** LLM, atanan test case önceliğinin uygun olmadığına karar vermiştir.

**Neden Önemli?** Bu metrik, standart metriklerin ötesine geçerek, bir RAG sisteminin veya LLM'nin, belirli iş kurallarına, yönergelerine veya kalite beklentilerine ne kadar uyduğunu ölçmek için esneklik sağlar. "priority_accuracy" özelinde, test süreçlerinin etkinliğini değerlendirmede kritik olabilir.

**Not:** Gerçek sonuç CSV dosyalarındaki değerler ve sütun adları, bu genel örneklere göre farklılık gösterebilir. En doğru yorumlama için kendi sonuç dosyalarınızı incelemeniz önemlidir.

## Katkıda Bulunma

Proje ile ilgili öneri, hata bildirimi veya katkılarınız için lütfen bir issue açın veya bir pull request gönderin.

