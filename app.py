import gradio as gr
from langchain import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
import os

DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GPT_MODEL = "gpt-3.5-turbo-0125"


pg_uri = (
    f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
db = SQLDatabase.from_uri(pg_uri)
llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name=GPT_MODEL)
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True, top_k=3)


PROMPT = """ 
Given an input question, first create a syntactically correct Postgresql query without ```sql formatting in the query. 
Run the query then look at the results of the query.
Interpret th results and return an answer.  
The question: {question}
"""


def query(question):
    try:
        response = db_chain.run(PROMPT.format(question=question))
        return response
    except:
        return "Could not perform request. Try another one"


iface = gr.Interface(
    fn=query,
    inputs="text",
    outputs="text",
    examples=[["What were the total emissions for 2022 for each category?"]],
)
iface.launch()
