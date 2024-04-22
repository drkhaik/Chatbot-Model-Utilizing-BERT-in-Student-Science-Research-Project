from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from scraper import get_content, clean_content
from file_utils import read_data_from_file
from db_connect import Database
from question_answering import QuestionAnswering
from dotenv import load_dotenv
import os

load_dotenv()

url_frontend = os.getenv("URL_FRONTEND")

app = Flask(__name__)
# CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
@app.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = url_frontend
    header["Access-Control-Allow-Headers"] = (
        "Origin, X-Requested-With, Content-Type, Accept, Authorization"
    )
    header["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST, PUT, DELETE"
    header["Access-Control-Allow-Credentials"] = "true"
    return response


db_url = os.getenv("DB_URL")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

url = "https://www.uef.edu.vn/vdtqt/song-nganh/nganh-dao-tao-8381"
soup = get_content(url)
cleaned_content = clean_content(soup)

with open("response_sbsn.txt", "wb") as file:
    file.write(cleaned_content.encode("utf-8"))

file_path = "./response_with_clear_data.txt"
data = read_data_from_file(file_path)


db = Database(
    db_url,
    db_user,
    db_password,
)

# records, summary = db.execute_query("MATCH (n) RETURN n")
# print(f"Query executed on server: {summary.server.address}")
# print(f"Number of records returned: {len(records)}")


# question = "Song bằng song ngành UEF có bao nhiêu ngành đào tạo?"


# question = "Địa chỉ cơ sở B nằm ở đâu?"


# question = "Điểm trung bình tích luỹ như nào là bằng giỏi?"
# 3.20->3.59

# question = "Chuẩn đầu ra Tiếng Anh của UEF gồm những gì?"
# đạt được điểm IELTS 5.5 trở lên

# question = "Đăng kí song bằng song ngành UEF ở đâu?"
# Answer 2: Trung tâm hỗ trợ học vụ - Tầng 2 - Cơ sở A

# question = "Điều kiện để học song bằng song ngành UEF là gì"
# Answer: Sinh viên học hết HKI năm nhất của ngành thứ 1

qa = QuestionAnswering(
    db_url,
    db_user,
    db_password,
)

# question = "Chuẩn đầu ra Tiếng Anh của UEF gồm những gì?"
# correct response but not enough
# question = "Xếp hạng bằng tốt nghiệp có yêu cầu gì không?"
# fail
# question = "Chuẩn đầu ra Tin học khoá 2021 gồm những gì?"
# Tin học ứng dụng CNTT cơ bản và Tin học ứng dụng.
# question = "Tôi có thể đăng ký khoá học Tin học ở đâu?"
# fail
# question = "Liệt kê tên một số ngành đào tạo song bằng song ngành?"
# fail
# question = "Hoàn thành chương trình Song ngành sẽ nhận được gì?"
# Answer: Bằng Tốt nghiệp ngành thứ 1 và Giấy chứng nhận
# question = "Về học phần thực tập của Song bằng thì sao?"
# answer = Chỉ cần đạt 1 lần ở ngành thứ 1
# question = "Về chương trình đào tạo của Song bằng thì sao?"
# fail
# answer = qa.answer_question(question)
# print("Answer:", answer)

# @app.route("/api/test", methods=["POST"])
# def test_endpoint():
#     data = request.get_json()
#     test123 = data.get("test123")  # use the get method to avoid KeyError
#     if test123 is not None:
#         print(test123)
#     else:
#         print("test123 not in data")
#     return "Success!", 200


@app.route("/api/v1/chatbot-answer", methods=["POST"])
# @cross_origin()
def handle_question_and_answer():
    data = request.get_json()
    print("Data:", data)
    question = data.get("question")
    print("Question:", question)
    answer = qa.answer_question(question)
    # Process the message with your BERT model
    return {"answer": answer}


qa.close()


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/test', methods=['GET'])
# cross_origin(origins='*')
def test():
    if request.method == "POST":
        # Handle the POST request here
        return jsonify(message="POST request returned"), 201
    else:
        # Handle the GET request here
        return jsonify(message="GET request returned")


@app.route("/api/test", methods=["POST"])
def test_endpoint():
    data = request.get_json()
    test123 = data.get("test123")  # use the get method to avoid KeyError
    if test123 is not None:
        print(test123)
    else:
        print("test123 not in data")
    return "Success!", 200


if __name__ == "__main__":
    app.run(port=5005, debug=True)
