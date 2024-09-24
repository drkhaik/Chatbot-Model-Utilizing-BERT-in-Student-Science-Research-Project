# Chatbot Overview

The Chatbot backend is built using Python with the Flask framework and developed as an API for flexibility in integration across multiple platforms. The data collection process utilizes the `requests` module to fetch content from web pages, storing the returned content in an object. The `BeautifulSoup` library is then employed to remove HTML tags and extract necessary data.

A crucial step in the chatbot system is the keyword recognition of user input (questions). Incorrect keyword recognition can lead to erroneous data queries, resulting in inaccurate input for the BERT model. For this, the team uses Named Entity Recognition (NER) from the Underthesea NLP Toolkit, an open-source Python module for processing NLP tasks in Vietnamese. Developed by Vu Anh and collaborators, Underthesea provides APIs for applying pre-trained models on Vietnamese text for tasks like word segmentation, POS tagging, and NER. It is based on popular deep learning libraries like PyTorch, facilitating the training of deep learning models.

Once the user’s question is identified, the team moves on to analyze and apply the BERT algorithm. The `bert-multi-cased-finetuned-xquadv1` model by Manuel Romero is utilized for predicting answers in the Chatbot. This model, developed by Google, has been fine-tuned on the SQuAD v1.1 dataset for question-answering tasks in multiple languages, including Vietnamese. The "question-answering" Pipeline from the Transformers library is also used, which combines the fine-tuned BERT model with the corresponding tokenizer.

Using the "question-answering" Pipeline, the system predicts answers based on the context of the user’s question and the query results from the database. The output is an object containing the answer, its position in the text, and the confidence score.

After integrating the Chatbot into the project, it operates via API to receive user questions and provide answers.
