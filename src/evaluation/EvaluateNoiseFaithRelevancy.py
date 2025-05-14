import pandas as pd
import os
import ast
from dotenv import load_dotenv
from ragas import EvaluationDataset, evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import NoiseSensitivity, ResponseRelevancy, Faithfulness
from langchain_openai import ChatOpenAI
from langfuse.callback import CallbackHandler
from langchain.callbacks.manager import CallbackManagerForLLMRun

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

# CSV yükleme
csv_path = "data/ragas_ready_dataset_v2.csv"
df = pd.read_csv(csv_path)

# retrieved_contexts format düzeltmesi
data = []
for _, row in df.iterrows():
    try:
        raw = row["retrieved_contexts"].replace("'", '"')
        parsed = ast.literal_eval(raw)
        cleaned = []
        for chunk in parsed:
            for part in chunk.split("\\n"):
                line = part.strip()
                if line:
                    cleaned.append(line)
    except:
        cleaned = []

    data.append({
        "user_input": row["user_input"],
        "response": row["response"],
        "retrieved_contexts": cleaned,
        "reference": row["reference"]
    })

# EvaluationDataset'e dönüştür
dataset = EvaluationDataset.from_list(data)

# Metrikleri tanımla
metrics = [
    NoiseSensitivity(llm=llm),
    ResponseRelevancy(llm=llm),
    Faithfulness(llm=llm)
]

# Değerlendirme yap
results = evaluate(dataset=dataset, metrics=metrics, llm=llm)
results_df = results.to_pandas()
print("\nNOISE - RELEVANCY - FAITHFULNESS SONUÇLARI:\n", results_df)

# CSV'ye aktar
results_df.to_csv("noise_relevancy_faithfulness_results.csv", index=False)
print("Sonuçlar 'noise_relevancy_faithfulness_results.csv' olarak kaydedildi.")
