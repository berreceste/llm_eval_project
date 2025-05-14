import os
import pandas as pd
from ragas import evaluate
from ragas.metrics import AspectCritic
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langfuse.callback import CallbackHandler
from datasets import Dataset
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# OPENAI API KEY .env'de olmalı
llm = ChatOpenAI(model="gpt-4o")  # Chat model
embeddings = OpenAIEmbeddings()   # Embedding modeli
# .env'den anahtarları al
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Langfuse callback handler
callback_handler = CallbackHandler()

# OpenAI LLM + Langfuse
llm_raw = ChatOpenAI(model="gpt-4o", callbacks=[callback_handler])
evaluator_llm = LangchainLLMWrapper(llm_raw)

# Metrik tanımı
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

# Veriyi yükle
df = pd.read_csv("data/test_cases.csv")
samples = [{"user_input": row["user_input"], "response": row["response"]} for _, row in df.iterrows()]
eval_dataset = Dataset.from_dict({"user_input": [s["user_input"] for s in samples], "response": [s["response"] for s in samples]})

# Değerlendir
results = evaluate(eval_dataset, metrics=[metric])
print(results.to_pandas())