import os
import pandas as pd
from ragas import evaluate
from ragas.metrics import AspectCritic
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langfuse.callback import CallbackHandler
from datasets import Dataset

# Ortam değişkenlerini yükle
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Langfuse + OpenAI LLM ayarları
callback_handler = CallbackHandler()
llm_raw = ChatOpenAI(model="gpt-4o", callbacks=[callback_handler])
evaluator_llm = LangchainLLMWrapper(llm_raw)

# AspectCritic metriğini tanımla
metric = AspectCritic(
    name="priority_accuracy",
    llm=evaluator_llm,
    definition="""
There are three priority levels for test cases:
- P1: High Priority — Critical tests covering core business logic.
- P2: Medium Priority — Important, but not breaking flows.
- P3: Low Priority — Minor issues, UI polish, or edge cases.

Evaluate whether the assigned priority (P1/P2/P3) is appropriate for each test case.
"""
)

# Temizlenmiş veri setini yükle
df = pd.read_csv("data/raw/test_cases_cleaned.csv")

# 3 farklı model çıktısı için değerlendirme yap
response_types = {
    "normal_response": "priority_eval_normal.csv",
    "no_execution_time_response": "priority_eval_noexec.csv",
    "no_severity_response": "priority_eval_noseverity.csv"
}

for column, output_file in response_types.items():
    samples = [
        {"user_input": row["user_input"], "response": row[column]}
        for _, row in df.iterrows()
    ]
    eval_dataset = Dataset.from_dict({
        "user_input": [s["user_input"] for s in samples],
        "response": [s["response"] for s in samples]
    })
    results = evaluate(eval_dataset, metrics=[metric])
    results_df = results.to_pandas()
    results_df.to_csv(output_file, index=False)
    print(f"✅ {column} değerlendirmesi tamamlandı → {output_file}")
