from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

