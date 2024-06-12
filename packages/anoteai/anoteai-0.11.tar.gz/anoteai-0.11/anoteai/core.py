# import requests
# import json
# # import time

# class Anote:
#     def __init__(self, api_key):
#         self.API_BASE_URL = 'http://localhost:5000'
#         # self.API_BASE_URL = 'https://api.anote.ai'
#         self.headers = {
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer {api_key}'
#         }

#     def create_dataset(self, task_type, name):
#         url = f"{self.API_BASE_URL}/public/createDataset"
#         data = json.dumps({
#             "taskType": task_type,
#             "name": name
#         })
#         response = requests.post(url, data=data, headers=self.headers)

#         return response.json()

#     def upload(self, file_path, dataset_id, decomposition_type):
#         url = f"{self.API_BASE_URL}/public/upload"
#         form_data = {
#             'decompositionType': decomposition_type,
#             'datasetId': dataset_id
#         }
#         files = {
#             'files[]': (file_path, open(file_path, 'rb'))
#         }
#         response = requests.post(url, headers=self.headers, data=form_data, files=files)
#         return response.json()

#     def customize(self, name, dataset_id, parent_category_id=None, prompt_text=None, is_structured_prompt=None):
#         url = f"{self.API_BASE_URL}/public/customize"
#         data = json.dumps({
#             "name": name,
#             "datasetId": dataset_id,
#             "parentCategoryId": parent_category_id,
#             "promptText": prompt_text,
#             "isStructuredPrompt": is_structured_prompt
#         })
#         response = requests.post(url, data=data, headers=self.headers)
#         return response.json()

#     def get_next_text_block(self, dataset_id):
#         url = f"{self.API_BASE_URL}/public/getNextTextBlock"
#         params = {'datasetId': dataset_id}
#         response = requests.get(url, params=params, headers=self.headers)

#         if response.status_code != 200:
#             return {"error": response.text}, response.status_code

#         return response.json()

#     def annotate(self, id, specified_entities, category_ids, is_delete):
#         url = f"{self.API_BASE_URL}/public/annotate"
#         data = json.dumps({
#             "id": id,
#             "specifiedEntities": specified_entities,
#             "categoryIds": category_ids,
#             "isDelete": is_delete
#         })
#         response = requests.post(url, data=data, headers=self.headers)
#         return response.json()

#     def train(self, dataset_id):
#         url = f"{self.API_BASE_URL}/public/train"
#         data = json.dumps({
#             "id": dataset_id
#         })
#         response = requests.post(url, data=data, headers=self.headers)
#         return response.json()

#     def predict(self, dataset_id, text):
#         url = f"{self.API_BASE_URL}/public/predict"
#         data = json.dumps({
#             "id": dataset_id,
#             "text": text
#         })
#         response = requests.post(url, data=data, headers=self.headers)
#         return response.json()

#     def download(self, id):
#         url = f"{self.API_BASE_URL}/public/download"
#         params = {'id': id}
#         response = requests.get(url, params=params, headers=self.headers)
#         return response.text

#     def evaluate(self, dataset_id):
#         """
#         Evaluate predictions on one or multiple documents/text.
#         :param dataset_id: The ID of the dataset that has had predictions made on it.
#         """
#         if not dataset_id:
#             return {"error": "Dataset ID is not set. Please create a dataset first."}

#         url = f"{self.API_BASE_URL}/public/evaluate"
#         # For file uploads, requests can handle files directly in the 'files' parameter

#         data = {'datasetId': dataset_id} #'task_type': task_type}  # Infer task type for now
#         response = requests.post(url, json=data, headers=self.headers)
#         return response.json()

import requests
import json
import os
import re

import csv
# from handlers.public_handlers import *
# from handlers.private_handlers import *

# class ModelType(IntEnum):
#     FTGPT = 0
#     LLAMA3 = 1
#     MLM = 2

def _open_files(document_files):
    files = []
    if document_files is None:
        return files
    else:
        for file_path in document_files:
            file_name = os.path.basename(file_path)
            files.append(('files[]', (file_name, open(file_path, 'rb'), 'text/plain')))
        return files

def _open_training_data(x_train_csv, y_train_csv):
    with open(x_train_csv, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        x_train = [row[0] for row in csv_reader]

    with open(y_train_csv, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        y_train = [row[0] for row in csv_reader]

    return x_train, y_train

def _close_files(files):
    # Close files that were opened for document paths
    for _, file_tuple in files:
        file_obj = file_tuple[1]  # Closing the file object
        file_obj.close()

class Anote:
    def __init__(self, api_key, is_private):
        # self.API_BASE_URL = 'http://localhost:5000'
        self.API_BASE_URL = 'https://api.anote.ai'
        self.is_private = is_private
        self.model_id = "model_id"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

    def upload(self, task_type, model_type, ticker=None, file_paths=None):
        """Upload documents or specify a ticker for data retrieval and Q&A. This method supports various tasks, such as uploading documents or querying the government's EDGAR database.

        Args:
            task_type (str): Specifies the type of task to perform. This can be document-based interaction (e.g., "documents") or financial data analysis ("edgar").
            model_type (str): Determines the AI model to use for processing the request. Different model types available are "gpt" for GPT-4 and "claude" for Claude.
            ticker (str, optional): The ticker symbol for financial data analysis tasks. Required if the task_type is 'edgar'. Example: 'AAPL' for Apple Inc.
            file_paths (list[str], optional): A list of file paths to documents for document-based tasks. Required if task_type is 'documents'. Example: ['path/to/file1.pdf', 'path/to/file2.pdf'].

        Returns:
            response (dict): A JSON response from the API, including the `chat_id` for interactions based on the uploaded content or specified ticker.
        """

        if task_type is None:
            return {"error": "Task type is not set. Please enter a task type"}

        if model_type is None:
            return {"error": "Model type is not set. Please enter a model type"}

        if ticker is None and file_paths is None:
             return {"error": "You must enter at least one of the following: ticker or file_paths"}
        print("model_type")
        print(model_type)
        if self.is_private == False:
            if model_type != "gpt" and model_type != "claude":
                return {"error": "Model type is not valid. Please enter a valid model type"}
            return upload_public(self.API_BASE_URL, self.headers, task_type, model_type, ticker, file_paths)
        else:
            if model_type != "llama" and model_type != "mistral":
                return {"error": "Model type is not valid. Please enter a valid model type"}
            return upload_private(task_type, model_type, ticker, file_paths)

    def train(self, model_name, fine_tuning_type, x_train_csv, y_train_csv, document_files, model_type = 0, is_private=False):
        """
        Train or Fine Tune a model via supervised or unsupervised fine tuning

        Args:
            model_name (str): The name of the model - which is referenced in the model_ids table alongside the model_id.
            model_type (str): Model that is used to do the fine tuning - could be "FT-GPT", "Llama3" for supervised, "MLM" for unsupervised.
            fine_tuning_type (str): The type of fine tuning - could be "supervised" or "unsupervised"
            x_train_csv (string of csv file path): training data for fine tuning - for each row could contain question or context entries
            y_train_csv (string of csv file path): training labels for fine tuning - for each row could contain answer entries
            document_files (list[str], optional): A list of file paths to documents for document-based tasks for training. Example: ['path/to/file1.pdf', 'path/to/file2.pdf'].
            is_private: The user can designate if they want to train a private model - will default to "Llama3" but can choose "Mistral"

        Returns:
            response (dict): A JSON response from the API, including the `model_id` of the trained model.
        """
        url = f"{self.API_BASE_URL}/public/train"
        if fine_tuning_type == "supervised":
            x_train, y_train = _open_training_data(x_train_csv, y_train_csv)

            # Prepare the data for form submission, including both files and values
            data = {
                "modelName": model_name,
                "modelType": model_type,
                "x_train": json.dumps(x_train),
                "y_train": json.dumps(y_train),
            }

            files = _open_files(document_files)

            # Note: `data` is used for non-file form fields, `files` is used for file uploads
            response = requests.post(url, data=data, headers=self.headers, files=files)

            _close_files(files)

            if response.status_code == 200:
                try:
                    response_data = response.json()
                    self.model_id = response_data.get('modelId')
                    return response_data
                except requests.exceptions.JSONDecodeError:
                    print("Failed to decode JSON response for Train Supervised")
            else:
                print(f"Supervised fine tuning request failed with status code {response.status_code}")
            return {}

        elif fine_tuning_type == "unsupervised":
            # Prepare the data for form submission, including both files and values
            data = {
                "modelName": model_name,
                "modelType": model_type,
            }

            files = _open_files(document_files)
            # Note: `data` is used for non-file form fields, `files` is used for file uploads
            response = requests.post(url, data=data, headers=self.headers, files=files)

            _close_files(files)

            if response.status_code == 200:
                try:
                    response_data = response.json()
                    self.model_id = response_data.get('modelId')
                    return response_data
                except requests.exceptions.JSONDecodeError:
                    print("Failed to decode JSON response for Train Unsupervised")
            else:
                print(f"Unsupervised fine tuning request failed with status code {response.status_code}")
            return {}

    def predict(self, model_name, model_id, question_text, context_text=None, question_csv=None, document_files = None, model_type = 0):
        """Make predictions based on a dataset uploaded.

        Args:
            model_name (str): The name of the model - which is referenced in the model_ids table alongside the model_id.
            model_id (str): The model id that is the output of the train API call - enables fine tuned models to be called.
            question_text (str): A string that contains the question.
            context_text (str): A string that contains additional text that can be concatenated to the question, if needed.
            document_files (list[str], optional): A list of file paths to documents for document-based tasks for predictions. Example: ['path/to/file1.pdf', 'path/to/file2.pdf'].

        Returns:
            response (dict): A JSON response from the API, including the `results` of the predictions.
        """
        url = f"{self.API_BASE_URL}/public/predict"
        # Handle document files
        files = _open_files(document_files)
        # Prepare the data for form submission, including both files and values
        data = {
            "modelId": model_id,
            "modelName": model_name,
            "modelType": model_type,
            "questionText": question_text,
            "additionalText": context_text,
            "questionCSV": question_csv
        }
        response = requests.post(url, files=files, data=data, headers=self.headers)

        _close_files(files)

        if response.status_code == 200:
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                print("Failed to decode JSON response for Predict")
        else:
            print(f"Predict request failed with status code {response.status_code}")
            return {}

    def chat(self, chat_id, message, finetuned_model_key=None):
        """Send a message to the chatbot based on documents previously uploaded.

        Args:
            chat_id (int): The ID of the chat that has had documents uploaded.
            message (str): The message to send to the chatbot.
            finetuned_model_key (str, optional): An optional custom model OpenAI key. If provided, the chatbot uses this finetuned model for the response.

        Returns:
            response (dict): The JSON response from the API containing `answer`, `message_id` and `sources` (which contains the document name and the relevant chunk).
        """

        if not chat_id:
            return {"error": "Chat ID is not set. Please upload documents first and enter the chat ID."}

        if not message:
            return {"error": "Message is not set. Please enter a message to send."}

        if self.is_private == False:
            url = f"{self.API_BASE_URL}/public/chat"
            data = {
                "chat_id": chat_id,
                "message": message,
                "model_key": finetuned_model_key
            }
            response = requests.post(url, json=data, headers=self.headers)
            return response.json()
        else:
            return chat_private(chat_id, message, finetuned_model_key)


    def evaluate(self, message_id, evaluation_data):
        """Evaluate predictions on one or multiple documents/text.

        Args:
            message_id (str): The ID of the message associated with the uploaded documents. This ID is used to identify which set of documents/text predictions should be evaluated.

        Returns:
            response (dict): A JSON response from the API, containing the evaluation results, `answer_relevancy`, `faithfulness` of the predictions on the specified message's documents or text. If the message ID is not provided or invalid, the function returns an error message indicating that a valid message ID is required for the operation.
        """

        if not message_id:
            return {"error": "Dataset ID is not set. Please create a dataset first."}

        if self.is_private == False:
            url = f"{self.API_BASE_URL}/public/evaluate"
            data = {'message_id': message_id, 'evaluation_data': evaluation_data}
            response = requests.post(url, json=data, headers=self.headers)
            return response.json()
        else:
            return evaluate_private(message_id)

def upload_public(API_url, headers, task_type, model_type, ticker=None, file_paths=None):
    if task_type == "documents": #Question-answering
        if file_paths is None:
            return {"error": "You are attempting to do question-answering. There are no files uploaded. Please upload at least one file."}
        else:
            url = f"{API_url}/public/upload"

            data = {
                "task_type": task_type,
                "model_type": model_type
            }

            files = []
            opened_files = []
            html_paths = []
            for path in file_paths:
                result = is_file_or_isHtml(path)
                if result == "file":
                    try:
                        file = open(path, 'rb')
                        opened_files.append(file)
                        files.append(("files[]", (path.split('/')[-1], file, "application/octet-stream")))
                    except Exception as e:
                        return {"error": f"Error opening file {path}: {e}"}
                elif result == "html":
                    html_paths.append(path)
                else:
                    return {"error": f"This file path {path} is not valid. Please enter a valid file path or URL."}

            data['html_paths'] = html_paths

            headers = {key: val for key, val in headers.items() if key.lower() != 'content-type'}

            try:
                response = requests.post(url, data=data, files=files, headers=headers)
                print("response")
                print(response)
                return response.json()
            except requests.exceptions.JSONDecodeError as e:
                return {"error": f"Failed to decode JSON response {e}"}
            finally:
                for file in opened_files:
                    file.close()
    elif task_type == "edgar":
        if not ticker:
            return {"error": "You are attempting to use EDGAR. There is no ticker uploaded. Please enter a ticker."}
        else:
            url = f"{API_url}/public/upload"

            data = {
                "task_type": task_type,
                "model_type": model_type,
                "ticker": ticker
            }

            headers = {key: val for key, val in headers.items() if key.lower() != 'content-type'}

            try:
                response = requests.post(url, data=data, headers=headers)
                return response.json()
            except requests.exceptions.JSONDecodeError as e:
                return {"error": "Failed to decode JSON response"}
    else:
        return {"error": "Task type is not recognized. Please enter a valid task type."}

def is_file_or_isHtml(path):
    if os.path.isfile(path):
        return "file"
    if re.match(r'(https?://|www\.)', path):
        return "html"
    else:
        return "unknown"

import os
import sqlite3
import ollama
import json
import requests
import ray
from tika import parser as p
from datasets import Dataset
import ragas
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)


# from handlers.private_db import *
# from handlers.public_handlers import is_file_or_isHtml

USER_SDK_EMAIL = "api@example.com"

def upload_private(task_type, model_type, ticker, file_paths):
    user_id = create_db_file()

    conn, cursor = get_db_connection()


    task_type_mapping = {"documents": 0, "edgar": 1}
    task_type_number = task_type_mapping.get(task_type, task_type)

    model_type_mapping = {"llama": 0, "mistral": 1}
    model_type_number = model_type_mapping.get(model_type, model_type)

    cursor.execute('INSERT INTO chats (user_id, model_type, associated_task) VALUES (?, ?, ?)', (user_id, model_type_number, task_type_number))
    chat_id = cursor.lastrowid

    conn.commit()
    conn.close()

    files = []
    paths = []

    if task_type == "documents":
        if file_paths is None:
            return {"error": "No files uploaded. Please upload at least one file."}
        for path in file_paths:
            if is_file_or_isHtml(path) == "file":
                files.append(path)
            elif is_file_or_isHtml(path) == "html":
                #text = get_text_from_url(path) #from chatbot_endpoints
                paths.append(path)
            else:
                return {"error": f"Invalid file path or URL: {path}"}
        process_files(task_type, files, paths, USER_SDK_EMAIL, model_type, chat_id)
    return {'id': chat_id}

def chat_private(chat_id, message, finetuned_model_key=None):
    conn, cursor = get_db_connection()

    model_type, task_type = get_chat_info(chat_id)

    add_message_to_db(message, chat_id, 1)

    #Get most relevant section from the document
    sources = get_relevant_chunks(2, message, chat_id)
    sources_str = " ".join([", ".join(str(elem) for elem in source) for source in sources])
    sources_swapped = [[str(elem) for elem in source[::-1]] for source in sources]


    if (model_type == 0):
        response = ollama.chat(model='llama2', messages=[
            {
            'role': 'user',
            'content': f'You are a factual chatbot that answers questions about uploaded documents. You only answer with answers you find in the text, no outside information. These are the sources from the text:{sources_str} And this is the question:{message}.',

            },
        ])
        answer = response['message']['content']
    else:
        response = ollama.chat(model='mistral', messages=[
            {
            'role': 'user',
            'content': f'You are a factual chatbot that answers questions about uploaded documents. You only answer with answers you find in the text, no outside information. These are the sources from the text:{sources_str} And this is the question:{message}.',

            },
        ])
        answer = response['message']['content']

    #This adds bot message
    message_id = add_message_to_db(answer, chat_id, 0)

    try:
        add_sources_to_db(message_id, sources)
    except:
        print("error adding sources to db or no sources")

    response_dict = {
        "message_id": message_id,
        "answer": answer,
        "sources": sources_swapped
    }

    return response_dict


def evaluate_private(message_id):
    question_json, answer_json = get_message_info(message_id)

    question = question_json['message_text']
    answer = answer_json['message_text']
    context = answer_json['relevant_chunks']

    #get it in the corret data format to put in ragas
    if not isinstance(context, list):
        context = [context]

    contexts = [context]

    data = {
        "question": [question],
        "answer": [answer],
        "contexts": contexts
    }

    dataset = Dataset.from_dict(data)

    result = ragas.evaluate(
        dataset = dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
        ],
    )

    return result


def process_files(chat_type, files, paths, user_email, model_type, chat_id):
    if chat_type == "documents": #question-answering
        #Ingest pdf
        MAX_CHUNK_SIZE = 1000

        for file in files:

            result = p.from_file(file)
            text = result["content"].strip()

            filename = file

            doc_id, doesExist = add_document_to_db(text, filename, chat_id=chat_id)

            if not doesExist:
                result_id = chunk_document.remote(text, MAX_CHUNK_SIZE, doc_id)
                result = ray.get(result_id)
        for path in paths:
            text = get_text_from_url(path)

            doc_id, doesExist = add_document_to_db(text, path, chat_id=chat_id)

            if not doesExist:
                result_id = chunk_document.remote(text, MAX_CHUNK_SIZE, doc_id)
                result = ray.get(result_id)
    elif chat_type == "edgar": #edgar

        if ticker:
            MAX_CHUNK_SIZE = 1000

            reset_uploaded_docs(chat_id, user_email)


            url, ticker = download_10K_url_ticker(ticker)
            filename = download_filing_as_pdf(url, ticker)

            text = get_text_from_single_file(filename)

            doc_id, doesExist = add_document_to_db(text, filename, chat_id)

            if not doesExist:
                result_id = chunk_document.remote(text, MAX_CHUNK_SIZE, doc_id)
                result = ray.get(result_id)
    else:
        return {"id": "Please enter a valid task type"}

    return {"id": chat_id}

def get_text_from_url(web_url):
    response = requests.get(web_url)
    result = p.from_buffer(response.content)
    text = result["content"].strip()
    text = text.replace("\n", "").replace("\t", "")
    return text

import os
import sqlite3
import numpy as np
import openai
from sec_api import QueryApi, RenderApi
import requests
import PyPDF2
import ray
import logging

sec_api_key=os.environ.get('sec_api_key')

USER_ID = 1
## Private methods
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db_connection():
    db_path = os.environ.get('DB_PATH', './database.db') #somehow has to get the path to the .db file inside the private chatbot app

    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    return conn, cursor

def create_db_file():
    db_exists = os.path.exists('database.db')

    connection = sqlite3.connect('database.db')
    cur = connection.cursor()

    if not db_exists:
        with open('schema.sql') as f:
            connection.executescript(f.read())

        insert_sql = """
        INSERT INTO users (
            session_token,
            session_token_expiration,
            password_reset_token,
            password_reset_token_expiration,
            credits,
            credits_updated,
            chat_gpt_date,
            num_chatgpt_requests
        ) VALUES (
            'sessionToken123',
            '2023-01-01 00:00:00',
            'passwordResetToken123',
            '2023-01-01 00:00:00',
            10,
            '2023-01-01 00:00:00',
            '2023-01-01 00:00:00',
            5
        );
        """
        cur.execute(insert_sql)

    cur.execute('SELECT id FROM users')
    users = cur.fetchone()

    connection.commit()
    connection.close()

    #return users
    return users[0]

def ensure_SDK_user_exists(user_email):
    conn, cursor = get_db_connection()

    cursor.execute("SELECT id FROM users WHERE email = ?", (user_email,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        insert_query = """
        INSERT INTO users (email, person_name, profile_pic_url, credits)
        VALUES (?, 'SDK User', 'url_to_default_image', 0)
        """
        cursor.execute(insert_query, (user_email,))
        conn.commit()
        return cursor.lastrowid

def add_message_to_db(text, chat_id, isUser):
    #If isUser is 0, it is a bot message, 1 is a user message
    conn, cursor = get_db_connection()

    cursor.execute('INSERT INTO messages (message_text, chat_id, sent_from_user) VALUES (?,?,?)', (text, chat_id, isUser))
    message_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return message_id

def get_chat_info(chat_id):
    conn, cursor = get_db_connection()

    cursor.execute("SELECT model_type, associated_task FROM chats WHERE id = ?", (chat_id,))
    result = cursor.fetchone()

    if result:
        model_type = result['model_type']
        associated_task = result['associated_task']
    else:
        model_type, associated_task = None, None
    cursor.close()
    conn.close()

    return model_type, associated_task

def get_relevant_chunks(k, question, chat_id):
    conn, cursor = get_db_connection()

    query = """
    SELECT c.start_index, c.end_index, c.embedding_vector, c.document_id, c.page_number, d.document_name
    FROM chunks c
    JOIN documents d ON c.document_id = d.id
    JOIN chats ch ON d.chat_id = ch.id
    JOIN users u ON ch.user_id = u.id
    WHERE u.id = ? AND ch.id = ?
    """

    cursor.execute(query, (USER_ID, chat_id))
    rows = cursor.fetchall()

    embeddings = []
    for row in rows:
        embeddingVectorBlob = row["embedding_vector"]
        embeddingVector = np.frombuffer(embeddingVectorBlob)
        embeddings.append(embeddingVector)

    if (len(embeddings) == 0):
        res_list = []
        for i in range(k):
            res_list.append("No text found")
        return res_list

    embeddings = np.array(embeddings)

    embeddingVector = openai.embeddings.create(input=question, model="text-embedding-ada-002").data[0].embedding
    embeddingVector = np.array(embeddingVector)

    res = knn(embeddingVector, embeddings)
    num_results = min(k, len(res))

    #Get the k most relevant chunks
    source_chunks = []
    for i in range(num_results):
        source_id = res[i]['index']

        document_id = rows[source_id]['document_id']
        page_number = rows[source_id]['page_number']
        document_name = rows[source_id]['document_name']


        cursor.execute('SELECT document_text FROM documents WHERE id = ?', (document_id,))
        doc_text = cursor.fetchone()['document_text']

        source_chunk = doc_text[rows[source_id]['start_index']:rows[source_id]['end_index']]
        source_chunks.append((source_chunk, document_name))

    return source_chunks


def knn(x, y):
    x = np.expand_dims(x, axis=0)
    # Calculate cosine similarity
    similarities = np.dot(x, y.T) / (np.linalg.norm(x) * np.linalg.norm(y))
    # Convert similarities to distances
    distances = 1 - similarities.flatten()
    nearest_neighbors = np.argsort(distances)

    results = []
    for i in range(len(nearest_neighbors)):
        item = {
            "index": nearest_neighbors[i],
            "similarity_score": distances[nearest_neighbors[i]]
        }
        results.append(item)

    return results

def add_sources_to_db(message_id, sources):
    combined_sources = ""

    for source in sources:
        chunk_text, document_name = source
        combined_sources += f"Document: {document_name}: {chunk_text}\n\n"

    conn, cursor = get_db_connection()

    cursor.execute('UPDATE messages SET relevant_chunks = ? WHERE id = ?', (combined_sources, message_id))

    conn.commit()

    cursor.close()
    conn.close()


def add_document_to_db(text, document_name, chat_id):
    conn, cursor = get_db_connection()

    cursor.execute("SELECT id, document_text FROM documents WHERE document_name = ? AND chat_id = ?", (document_name, chat_id))
    existing_doc = cursor.fetchone()

    if existing_doc:
        existing_doc_id, existing_doc_text = existing_doc
        conn.close()
        return existing_doc_id, True  # Returning the ID of the existing document


    storage_key = "temp"
    cursor.execute("INSERT INTO documents (chat_id, document_name, document_text, storage_key) VALUES (?, ?, ?, ?)", (chat_id, document_name, text, storage_key))

    doc_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return doc_id, False



@ray.remote
def chunk_document(text, maxChunkSize, document_id):
    conn, cursor = get_db_connection()

    chunks = []
    startIndex = 0

    while startIndex < len(text):
        endIndex = startIndex + min(maxChunkSize, len(text))
        chunkText = text[startIndex:endIndex]
        chunkText = chunkText.replace("\n", "")

        embeddingVector = openai.embeddings.create(input=chunkText, model="text-embedding-ada-002").data[0].embedding
        embeddingVector = np.array(embeddingVector)
        blob = embeddingVector.tobytes()
        chunks.append({
            "text": chunkText,
            "start_index": startIndex,
            "end_index": endIndex,
            "embedding_vector": embeddingVector,
            "embedding_vector_blob": blob,
        })
        startIndex += maxChunkSize

    for chunk in chunks:
        cursor.execute('INSERT INTO chunks (start_index, end_index, document_id, embedding_vector) VALUES (?,?,?,?)', [chunk["start_index"], chunk["end_index"], document_id, chunk["embedding_vector_blob"]])

    conn.commit()
    conn.close()

def reset_uploaded_docs(chat_id):
    conn, cursor = get_db_connection()

    delete_chunks_query = """
    DELETE FROM chunks
    WHERE document_id IN (
        SELECT id FROM documents
        WHERE chat_id = ?
    )
    """
    cursor.execute(delete_chunks_query, (chat_id,))

    delete_documents_query = """
    DELETE FROM documents
    WHERE chat_id = ? AND EXISTS (
        SELECT 1 FROM chats
        WHERE chats.id = documents.chat_id
        AND chats.user_id = ?
    )
    """
    cursor.execute(delete_documents_query, (chat_id, USER_ID))

    conn.commit()

    conn.close()


def download_10K_url_ticker(ticker):
    year = 2023

    ticker_query = 'ticker:({})'.format(ticker)
    query_string = '{ticker_query} AND filedAt:[{year}-01-01 TO {year}-12-31] AND formType:"10-K" AND NOT formType:"10-K/A" AND NOT formType:NT'.format(ticker_query=ticker_query, year=year)

    query = {
        "query": { "query_string": {
            "query": query_string,
            "time_zone": "America/New_York"
        } },
        "from": "0",
        "size": "200",
        "sort": [{ "filedAt": { "order": "desc" } }]
      }


    response = QueryApi.get_filings(query)

    filings = response['filings']

    if filings:
       ticker=filings[0]['ticker']
       url=filings[0]['linkToFilingDetails']
    else:
       ticker = None
       url = None

    return url, ticker

def download_filing_as_pdf(url, ticker):
    API_ENDPOINT = "https://api.sec-api.io/filing-reader"

    api_url = API_ENDPOINT + "?token=" + sec_api_key + "&url=" + url + "&type=pdf"

    response = requests.get(api_url)

    file_name = f"{ticker}.pdf"

    with open(file_name, 'wb') as f:
        f.write(response.content)

    return file_name

def get_text_from_single_file(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page_num in range(len(reader.pages)):

        text += reader.pages[page_num].extract_text()

    return text

def get_message_info(answer_id):
    conn, cursor = get_db_connection()

    answer_query = "SELECT chat_id, message_text, relevant_chunks FROM messages WHERE id = ?"

    cursor.execute(answer_query, (answer_id, ))
    answer = cursor.fetchone()

    if not answer:
        print("Either the answer does not exist or it doesn't belong to the specified user.")
        return None, None

    chat_id = answer['chat_id']

    question_query = """
    SELECT m.*
    FROM messages m
    WHERE m.id < ? AND m.chat_id = ? AND m.sent_from_user = 1
    ORDER BY m.id DESC
    LIMIT 1
    """

    cursor.execute(question_query, (answer_id, chat_id))
    question = cursor.fetchone()

    cursor.close()
    return question, answer