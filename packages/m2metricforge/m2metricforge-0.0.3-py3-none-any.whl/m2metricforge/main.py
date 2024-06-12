from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
import json


def script_valid(file_base: str, df_name: str, column_name: str, file_new: str,
                 model_name: str | None, prompt: str | None) -> None:
    """
    A function for creating validation dataset or creating a new column, using your own model. To do this, enter in function your function, which generating answer. Otherwise select model what you need and prompt and then new CSV file would be generated
    """

    def generate_validation(text: str, model_name: str, prompt: str):
        llm = ChatOllama(model=model_name)
        chat_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=(
                        f"""{prompt}"""
                    )
                ),
                HumanMessagePromptTemplate.from_template("{text}"),
            ]
        )
        messages = chat_template.format_messages(text=text)
        response = llm(messages)
        return response

    df = pd.read_csv(file_base)
    if model_name is None or prompt is None:
        raise ValueError("Not all parametres provided")
    df[df_name] = df[column_name].apply(lambda x: generate_validation(x, model_name, prompt))
    df.to_csv(file_new, index=False)


def script_generate(csv_file: str, column_name: str, dfnew_name: str | None, model_query) -> None:
    """
    A function for applying RAG function "model_query" to the provdied dataset, to generate answers for "column_name" in your dataset. By default model_query generate answer in str format.
    """
    df = pd.read_csv(csv_file)
    result = df[column_name].apply(model_query)
    df['validated_results'] = result

    if dfnew_name is None:
        df.to_csv("result_dataset", index=False)
    else:
        df.to_csv(dfnew_name, index=False)


def script_generate_json(csv_file: str, column_name: str, dfnew_name: str | None, desired_data: str, model_query) -> None:
    """
       A function for applying RAG function "model_query" to the provdied dataset, to generate answers for "column_name" in your dataset. This function assumes your LLM generate answer in JSON view, so you need to select which name from JSON you want extract in desired_data variable
    """
    def extract_url(json_string, desired_data):
        try:
            # Convert JSON-like string to dictionary
            data = json.loads(json_string.replace('""', '"'))
            # Extract the 'data/url' value
            return data.get(desired_data, '')
        except json.JSONDecodeError:
            return ''

    df = pd.read_csv(csv_file)
    result = df[column_name].apply(model_query)
    df['validated_results'] = result
    df['extracted_url'] = df['validated_results'].apply(lambda x: extract_url(x, desired_data))

    if dfnew_name is None:
        df.to_csv("result_dataset.csv", index=False)
    else:
        df.to_csv(dfnew_name, index=False)


def calculate_metrics(csv_file: str, column_one: str | int, column_two: str | int):
    """
    A function for calculating Accuracy and F1 Score metrics in percentage. We use the Sklern library for calculations. Column one and Column two can be both the name of the column and its number.
    """
    df = pd.read_csv(csv_file)

    if isinstance(column_one, str):
        true_urls = df[column_one].tolist()
        predicted_urls = df[column_two].tolist()
    else:
        true_urls = df.iloc[:, (column_one - 1)].tolist()
        predicted_urls = df.iloc[:, (column_two - 1)].tolist()

    accuracy = accuracy_score(true_urls, predicted_urls)
    f1 = f1_score(true_urls, predicted_urls, average='weighted')

    return accuracy, f1
