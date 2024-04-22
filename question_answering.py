from underthesea import ner
from neo4j import GraphDatabase
from transformers import pipeline


class QuestionAnswering:
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        self.qa_pipeline = pipeline(
            "question-answering",
            model="mrm8488/bert-multi-cased-finetuned-xquadv1",
            tokenizer="mrm8488/bert-multi-cased-finetuned-xquadv1",
        )

    def close(self):
        self.driver.close()

    def get_entities(self, result):
        include_tag1 = ["N", "Np", "A"]
        include_tag2 = ["B-NP", "B-AP"]
        core_words = []
        current_core_word = ""
        for i, (word, tag1, tag2, _) in enumerate(result):
            if tag1 not in include_tag1 or tag2 not in include_tag2:
                continue
            current_core_word += word
            if i + 1 < len(result) and (
                result[i + 1][1] in include_tag1 and result[i + 1][2] in include_tag2
            ):
                current_core_word += " " + result[i + 1][0]
            core_words.append(current_core_word)
            current_core_word = ""
        return core_words

    # def query_neo4j(self, entities):
    #     passages = {}
    #     with self.driver.session() as session:
    #         for entity in entities:
    #             query = f"match (s)-[r]->(o) WHERE s.name contains '{entity}' return s, r, o limit 20"
    #             print(query)
    #             result = session.run(query)
    #             if result.peek() is None:
    #                 continue
    #             for record in result:
    #                 s, r, o = record["s"], record["r"], record["o"]
    #                 s_name = dict(s)["name"]
    #                 o_name = dict(o)["name"]
    #                 r_type = r.type
    #                 # if s_name not in passages:
    #                 #     passages[s_name] = {}
    #                 # if r_type not in passages[s_name]:
    #                 #     passages[s_name][r_type] = []
    #                 # passages[s_name][r_type].append(o_name)
    #                 passages += f"{s_name} {r_type} {o_name}"
    #     # formatted_passages = ""
    #     # for s, r_os in passages.items():
    #     #     for r, os in r_os.items():
    #     #         formatted_passages += f"{s} {r} {', '.join(os)}. "
    #     # return formatted_passages
    #     return passages

    def query_neo4j(self, entities):
        passages = ""
        with self.driver.session() as session:
            for entity in entities:
                query = f"match (s)-[r]->(o) WHERE s.name contains '{entity}' return s, r, o limit 20"
                print(query)
                result = session.run(query)
                if result.peek() is None:
                    continue
                for record in result:
                    s, r, o = record["s"], record["r"], record["o"]
                    s_name = dict(s)["name"]
                    o_name = dict(o)["name"]
                    r_type = r.type
                    passages += f"{s_name} {r_type} {o_name}. "
        return passages

    def answer_question(self, question):
        result = ner(question)
        print(result)
        entities = self.get_entities(result)
        print(entities)
        passage = self.query_neo4j(entities)
        passage = passage.replace("_", " ")
        print(passage)
        if len(passage) == 0:
            return "Xin lỗi! Tôi không hiểu câu hỏi của bạn."
        else:
            result = self.qa_pipeline({"context": passage, "question": question})
            return result["answer"]
