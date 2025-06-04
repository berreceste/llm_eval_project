import os
import pandas as pd
import ast
import time
from dotenv import load_dotenv
from ragas import EvaluationDataset, evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import LLMContextPrecisionWithReference, LLMContextPrecisionWithoutReference
from langchain_openai import ChatOpenAI
from langfuse import Langfuse
from langfuse.callback import CallbackHandler

# Ortam değişkenlerini yükle
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Langfuse başlatma
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
)

# Langfuse callback handler
langfuse_handler = CallbackHandler(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
)

# LLM tanımı - gpt-3.5-turbo kullanıyoruz
llm = LangchainLLMWrapper(ChatOpenAI(
    model="gpt-3.5-turbo",
    callbacks=[langfuse_handler]
))

# CSV yolu
csv_path = "data/raw/ragas_ready_dataset_with_responses_UPDATED.csv"
df = pd.read_csv(csv_path)

# Değerlendirilecek 3 response türü
response_columns = {
    "response_normal": "context_precision_normal.csv",
    "response_no_exec": "context_precision_noexec.csv",
    "response_no_severity": "context_precision_noseverity.csv"
}

# Ortak metrikler
metrics = [
    LLMContextPrecisionWithReference(llm=llm),
    LLMContextPrecisionWithoutReference(llm=llm)
]

# Batch size ve bekleme süresi
BATCH_SIZE = 5
WAIT_TIME = 2  # saniye

# Her model cevabı için döngü
for response_col, output_file in response_columns.items():
    samples = []
    for idx, row in df.iterrows():
        try:
            # Boş response değerlerini kontrol et
            if pd.isna(row[response_col]):
                print(f"⚠️ Satır {idx}: Boş response değeri atlandı.")
                continue
                
            contexts = ast.literal_eval(row["retrieved_contexts"])
            samples.append({
                "user_input": row["user_input"],
                "retrieved_contexts": contexts,
                "response": row[response_col],
                "reference": row["reference"]
            })
            
            # Batch size kontrolü
            if len(samples) >= BATCH_SIZE:
                print(f"🔍 {response_col} için {len(samples)} örnek değerlendiriliyor...")
                dataset = EvaluationDataset.from_list(samples)
                results = evaluate(dataset, metrics=metrics, llm=llm)
                results_df = results.to_pandas()
                results_df.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
                print(f"✅ Batch değerlendirmesi tamamlandı → {output_file}")
                samples = []  # Batch'i temizle
                time.sleep(WAIT_TIME)  # Rate limit için bekle
                
        except Exception as e:
            print(f"⚠️ Hata satır {idx}: {e}")
            continue

    # Kalan örnekleri değerlendir
    if samples:
        print(f"🔍 {response_col} için kalan {len(samples)} örnek değerlendiriliyor...")
        dataset = EvaluationDataset.from_list(samples)
        results = evaluate(dataset, metrics=metrics, llm=llm)
        results_df = results.to_pandas()
        results_df.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
        print(f"✅ Son batch değerlendirmesi tamamlandı → {output_file}")

# Langfuse'u kapat
langfuse.flush()
