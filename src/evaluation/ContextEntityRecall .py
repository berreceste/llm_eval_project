import pandas as pd
import os
from dotenv import load_dotenv
from ragas import EvaluationDataset, evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import ContextEntityRecall
from langchain_openai import ChatOpenAI
import ast
from langfuse.callback import CallbackHandler
from langchain.callbacks.manager import CallbackManagerForLLMRun
import json

# Ortam değişkenlerini yükle
load_dotenv()

# Langfuse callback ayarı
callback_handler = CallbackHandler()
callback_manager = CallbackManagerForLLMRun(
    run_id="test_run",
    handlers=[callback_handler],
    inheritable_handlers=[]
)

# LLM tanımı (Langfuse entegre)
llm_wrapped = ChatOpenAI(model="gpt-4o", callbacks=[callback_handler])
llm = LangchainLLMWrapper(llm_wrapped)

# Veri yükle
csv_path = "data/ragas_ready_dataset_v4.csv"
df = pd.read_csv(csv_path)

# retrieved_contexts temizle ve dönüştür
cleaned_rows = []
for _, row in df.iterrows():
    raw_context = row["retrieved_contexts"]
    context_list = []

    try:
        # Tek tırnakları çift tırnağa çevir
        raw_context = raw_context.replace("'", '"')
        # Fazla \n karakterlerini temizle
        raw_context = raw_context.replace("\\n", " ")
        # Önce ast.literal_eval dene
        try:
            items = ast.literal_eval(raw_context)
        except:
            # Eğer ast.literal_eval başarısız olursa, json.loads dene
            items = json.loads(raw_context)
        for item in items:
            line = item.strip()
            if line:
                context_list.append(line)
    except Exception as e:
        print(f"Hata: {e} - Satır atlanıyor.")
        context_list = []

    cleaned_rows.append({
        "user_input": row["user_input"],
        "response": row["response"],
        "reference": row["reference"],
        "retrieved_contexts": context_list
    })

# Temizlenmiş veriyi yeni CSV'ye kaydet
cleaned_df = pd.DataFrame(cleaned_rows)
cleaned_df.to_csv("data/ragas_ready_dataset_v6.csv", index=False)
print("Temizlenmiş veri 'data/ragas_ready_dataset_v6.csv' dosyasına kaydedildi.")

# Dataset formatına çevir
dataset = EvaluationDataset.from_list(cleaned_rows)

# Metriği tanımla
metric = ContextEntityRecall(llm=llm)

# Değerlendirme
results = evaluate(dataset, metrics=[metric], llm=llm)

# Sonuçları göster
results_df = results.to_pandas()
print("\nENTITY RECALL SONUÇLARI:\n", results_df)

# CSV'ye kaydet
results_df.to_csv("context_entity_recall_results.csv", index=False)
print("Sonuçlar 'context_entity_recall_results.csv' dosyasına kaydedildi.")
