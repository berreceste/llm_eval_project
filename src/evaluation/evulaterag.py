import pandas as pd
import os
from dotenv import load_dotenv
from ragas import EvaluationDataset, evaluate
from ragas.metrics import AspectCritic, LLMContextRecall, Faithfulness, FactualCorrectness
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI
from langfuse.callback import CallbackHandler

# Ortam değişkenlerini yükle (API key için)
load_dotenv()

# ChatOpenAI modelini sarmala
llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o", callbacks=[CallbackHandler()]))

# CSV'den veriyi yükle
csv_path = "data/ragas_ready_dataset_v2.csv"
df = pd.read_csv(csv_path)

# Dataset formatına çevir
samples = []
for _, row in df.iterrows():
    samples.append({
        "user_input": row["user_input"],
        "retrieved_contexts": eval(row["retrieved_contexts"]),  # liste formatı için
        "response": row["response"],
        "reference": row["reference"]
    })

dataset = EvaluationDataset.from_list(samples)

# Değerlendirme metrikleri
metrics = [
    AspectCritic(
        name="priority_accuracy",
        llm=llm,
        definition="""
There are three priority levels for test cases:
- P1: High Priority — Critical tests covering core business logic.
- P2: Medium Priority — Important, but not breaking flows.
- P3: Low Priority — Minor issues, UI polish, or edge cases.

Evaluate whether the assigned priority (P1/P2/P3) is appropriate for each test case.
"""
    ),
    LLMContextRecall(),
    Faithfulness(),
    FactualCorrectness()
]

# Değerlendirme yap
results = evaluate(dataset, metrics=metrics)

# Sonuçları yazdır
results_df = results.to_pandas()
print(results_df)

# CSV olarak dışa aktar
results_df.to_csv("evaluation_results.csv", index=False)
print("Sonuçlar 'evaluation_results.csv' dosyasına kaydedildi.")


