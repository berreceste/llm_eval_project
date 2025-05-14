import pandas as pd
import os
from dotenv import load_dotenv
from ragas import EvaluationDataset, evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import LLMContextPrecisionWithReference, LLMContextPrecisionWithoutReference
from langchain_openai import ChatOpenAI
import ast

# Ortam değişkenlerini yükle
load_dotenv()

# LLM tanımı
llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))

# Veri yükle
csv_path = "data/ragas_ready_dataset_v2.csv"
df = pd.read_csv(csv_path)

# Dataset formatına çevir
samples = []
for idx, row in df.iterrows():
    try:
        # retrieved_contexts string'ini listeye çevir
        contexts = ast.literal_eval(row["retrieved_contexts"])
        
        samples.append({
            "user_input": row["user_input"],
            "retrieved_contexts": contexts,
            "response": row["response"],
            "reference": row["reference"]
        })
    except Exception as e:
        print(f"Hata satır {idx}: {e}")
        continue

print(f"Toplam {len(samples)} örnek oluşturuldu.")

if len(samples) > 0:
    dataset = EvaluationDataset.from_list(samples)

    # Metrikler
    metrics = [
        LLMContextPrecisionWithReference(llm=llm),
        LLMContextPrecisionWithoutReference(llm=llm)
    ]

    # Değerlendirme
    results = evaluate(dataset, metrics=metrics, llm=llm)

    # Sonuçları göster
    results_df = results.to_pandas()
    print(results_df)

    # CSV'ye kaydet
    results_df.to_csv("context_precision_results.csv", index=False)
    print("Sonuçlar 'context_precision_results.csv' dosyasına kaydedildi.")
else:
    print("Hiç örnek oluşturulamadı. CSV dosyasını kontrol edin.")
