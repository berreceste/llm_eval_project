import pandas as pd
import os
from dotenv import load_dotenv
from ragas import EvaluationDataset, evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import LLMContextRecall, NonLLMContextRecall
from langchain_openai import ChatOpenAI
import ast

# Ortam değişkenlerini yükle
load_dotenv()

# LLM tanımı
llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))

# Veri yükle
csv_path = "data/ragas_ready_dataset_v4.csv"
df = pd.read_csv(csv_path)

# retrieved_contexts temizle ve dönüştür
cleaned_rows = []
for _, row in df.iterrows():
    raw_context = row["retrieved_contexts"]
    context_list = []

    try:
        raw_context = raw_context.replace("'", '"')  # tek tırnakları çift tırnağa çevir
        items = ast.literal_eval(raw_context)
        for item in items:
            for line in item.split("\\n"):
                line = line.strip()
                if line:
                    context_list.append(line)
    except Exception as e:
        context_list = []

    cleaned_rows.append({
        "user_input": row["user_input"],
        "response": row["response"],
        "reference": row["reference"],
        "retrieved_contexts": context_list,
        "reference_contexts": eval(row["reference_contexts"]) if pd.notna(row["reference_contexts"]) else []
    })

# Dataset formatına çevir
dataset = EvaluationDataset.from_list(cleaned_rows)

# Kullanılabilir metrikler
metrics = [
    LLMContextRecall(llm=llm),
    NonLLMContextRecall()
]

# Değerlendirme
results = evaluate(dataset, metrics=metrics, llm=llm)

# Sonuçları göster
results_df = results.to_pandas()
print("\nMETRİK SONUÇLARI:\n", results_df)

# CSV'ye kaydet
results_df.to_csv("context_recall_results.csv", index=False)
print("Sonuçlar 'context_recall_results.csv' dosyasına kaydedildi.")

