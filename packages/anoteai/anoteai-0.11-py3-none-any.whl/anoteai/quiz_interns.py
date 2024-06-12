import pandas as pd
from core import Anote

if __name__ == "__main__":
    api_key = '09c22ca372ba18ce9d35d0ed8b4a6a3e'

    # 1. Upload all documents from Anote Documentation and Dataroom to DB
    df = pd.read_csv("./pop_quiz/documentation_links.csv")
    file_paths = df["urls"].to_list()

    # Add google drive links to file_paths

    anote = Anote(api_key, is_private=False)
    # anote = anote(api_key, is_private=True)

    upload_result = anote.upload(task_type="documents", model_type="gpt", file_paths=file_paths)
    print("output from upload: ", upload_result)
    chat_id = upload_result['id']

    # 2. Ask Model Via Chat Call to Generate 10 Quiz Questions about Anote
    chat_result = anote.chat(chat_id, "Given what you know about Anote, generate 10 quiz questions")
    print("output from chat: ", chat_result)
    message_id = chat_result['message_id']

    # 3. Ask Model to Generate 10 Answers to These Quiz Questions
    questions = chat_result['answer']
    answer_prompt = f"Given these questions: {questions} answer each quiz question accurately. Output as a list of dictionaries, with keys 'question' and 'model_answer' for each question."
    chat_result = anote.chat(chat_id, answer_prompt)
    print("Output from chat (quiz answers):", chat_result)

    # 4. Assign Each Person on the Team to Answer Each of the 10 Quiz Question By Hand


    # 5. Take Human Answers and Model Answers, Format it as a list of Dict to put into Eval,
    # with a list of dict, each dict has items question, model_answer, human_answer
    evaluation_data = [
        {
            "question": "What is Anote?",
            "model_answer": "Anote is a tool for managing documents.",
            "human_answer": "Anote helps in document management."
        }
    ]
    # 6. Evaluate the Answers of Each Human to Give them a score on how much they know about Anote
    # print("output from evaluate:", anote.evaluate(message_id, evaluation_data))
