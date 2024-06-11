from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
def script_valid(file_base: str, df_name: str, column_name: str, file_new: str, function: str | None, model_name: str | None, prompt: str | None) -> None:
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
    if function:
        df[df_name] = df[column_name].apply(function)
    else:
        if model_name is None or prompt is None:
            raise ValueError("model_name and prompt are required if function is not provided")
        df[df_name] = df[column_name].apply(lambda x: generate_validation(x, model_name,prompt))
    df.to_csv(file_new, index=False)


def calculate_metrics(csv_file: str, column_one: str | int, column_two: str | int):
    """
    A function for calculating Accuracy and F1 Score metrics. We use the Schlern library for calculations. Column one and Column two can be both the name of the column and its number
    """
    df = pd.read_csv(csv_file)
    if isinstance(column_one, str):
        true_urls = df[column_one].tolist()
        predicted_urls = df[column_two].tolist()
    else:
        true_urls = df.iloc[:, (column_one-1)].tolist()
        predicted_urls = df.iloc[:, (column_two-1)].tolist()
    accuracy = accuracy_score(true_urls, predicted_urls)
    f1 = f1_score(true_urls, predicted_urls, average='weighted')

    return accuracy, f1,true_urls,predicted_urls