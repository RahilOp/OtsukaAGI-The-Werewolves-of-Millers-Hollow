import os
import openai
import pinecone
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import math
import faiss
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers import TimeWeightedVectorStoreRetriever
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
import csv
from datetime import datetime, timedelta
from datetime import date
from IPython.display import display, HTML
import streamlit as st


os.environ['OPENAI_API_KEY'] = '97ce304ef1a84eddb8e7598eb47479c3'
openai.api_type = "azure"
openai.api_base = "https://openaifor-intershipteamb.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

PINECONE_API_KEY = os.getenv("8cfca7f3-504b-4137-ac53-e71c60611988")
PINECONE_API_ENV = os.getenv("us-west4-gcp-free")

pinecone.init(api_key=PINECONE_API_KEY,environment=PINECONE_API_ENV)


USER_NAME = "God" # The name you want to use when interviewing the agent.
LLM = ChatOpenAI(max_tokens=1200, openai_api_key=os.getenv("OPENAI_API_KEY"), model_name = 'gpt-3.5-turbo', model_kwargs = {'engine': 'gpt-35-turbo'})


def generate_embedding(text):
  text= text.replace("\n"," ")
  res = openai.Embedding.create(
  deployment_id="text-embedding-ada-002",
  input=text,
  MODEL="text-embedding-ada-002")

  final_res = res['data'][0]['embedding']

  return final_res

def relevance_score(text1,text2):
  vector1 = np.array(generate_embedding(text1))
  vector2 = np.array(generate_embedding(text2))
  return cosine_similarity(vector1.reshape(1,-1),vector2.reshape(1,-1))[0][0]

def retrieval_score():
  pass

# Function to interact and ask questions to LLM
def _generate_dialogue_response():
   pass

def generate_response(prompt):
  default_str = "Setup a context for yourself and whenever you are asked something, Imagine you are a character in a captivating role-playing game, and your objective is to engage players by embodying a believable persona. Answer questions as a human character, drawing upon your extensive memory, distinct traits, ongoing plans, and unique profile to provide immersive and realistic responses. Bring your character to life with depth and authenticity. In the conversation, please respond as if you were a person, without explicitly mentioning that you are an AI language model."
  prompt = default_str + prompt
  result = openai.ChatCompletion.create(engine = "gpt-35-turbo",
                                                   messages = [ {"role": "system", "content": prompt} ],
                                                   temperature=0.7,
                                                   max_tokens=128,
                                                   top_p=0.95,
                                                   frequency_penalty=0,
                                                   presence_penalty=0,
                                                   stop=None)

  filter = ''.join([chr(i) for i in range(1, 32)])
  final_response = result["choices"][0]["message"]["content"].translate(str.maketrans('', '', filter))

  detail_heads = ["Date","Query","Tokens_Used","Response"]
  response_details = [date.today(),prompt, result["usage"]["total_tokens"], final_response]
  print(response_details[0])

  with open('tokens_history.csv','a') as tokens:
    writer = csv.writer(tokens)
    writer.writerow(response_details)

  return final_response

def relevance_score_fn(score: float) -> float:
    """Return a similarity score on a scale [0, 1]."""
    # This will differ depending on a few things:
    # - the distance / similarity metric used by the VectorStore
    # - the scale of your embeddings (OpenAI's are unit norm. Many others are not!)
    # This function converts the euclidean norm of normalized embeddings
    # (0 is most similar, sqrt(2) most dissimilar)
    # to a similarity function (0 to 1)
    return 1.0 - score / math.sqrt(2)

def create_new_memory_retriever():
    """Create a new vector store retriever unique to the agent."""
    # Define your embedding model
    embeddings_model = OpenAIEmbeddings(model='"text-embedding-ada-002"', openai_api_key=os.getenv("OPENAI_API_KEY"))
    # Initialize the vectorstore as empty
    embedding_size = 1536
    index = faiss.IndexFlatL2(embedding_size)
    vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {}, relevance_score_fn=relevance_score_fn)
    return TimeWeightedVectorStoreRetriever(vectorstore=vectorstore, other_score_keys=["importance"], k=15)

def print_colored(text,color):
    
    color_code = {
        'black': '#000000',
        'red': '#FF0000',
        'green': '#00FF00',
        'yellow': '#FFFF00',
        'blue': '#0000FF',
        'magenta': '#FF00FF',
        'cyan': '#00FFFF',
        'white': '#FFFFFF',
        'light blue': '#ADD8E6',
        'sky blue': "#87CEEB"
    }
    
    text_color = color_code[color]
    text = f'<span style="color: {text_color};">{text}</span>'
    st.markdown(text, unsafe_allow_html=True)
    


   


