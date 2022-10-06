import math
import re


def compute_idf(N, nt):
    # N - Numbers of docs
    # nt - Number of docs containing the term
    return math.log(N / nt) if nt != 0 else 0


def compute_tf(query_dict, doc):
    doc = re.sub("[$@&,?!'\"/#%^*(){}+=|.-]", "", doc)
    tf_dict = {}
    doc_count = doc.count(' ') + 1
    for term in query_dict.keys():
        term_count = doc.lower().split(' ').count(term)
        # term_count = doc.count(term)
        tf_dict[term] = term_count / float(doc_count)
    return tf_dict


def run_tf_idf(questions_dict, N, terms):
    # TF Part
    for qa_id, dict_values in questions_dict.items():
        terms_tf_dict = dict_values["terms"]
        document = dict_values["document"]["Question"]
        questions_dict[qa_id]["terms"] = compute_tf(terms_tf_dict, document)

    # IDF Part
    nt = 0
    terms_idf_dict = {}  # Holds the idf result for each term.
    for term in terms:
        for qa_id, dict_values in questions_dict.items():
            terms_dict = dict_values["terms"]
            if terms_dict.get(term, 0) > 0:
                nt += 1
        idf_res = compute_idf(N=N, nt=nt)
        terms_idf_dict[term] = idf_res
        nt = 0

    # # Calculate TF-IDF
    result = []
    res = 0
    for qa_id, dict_values in questions_dict.items():
        terms_dict = dict_values["terms"]
        document = dict_values["document"]
        for term in terms:
            res += terms_dict[term] * terms_idf_dict[term]
        result.append((document, res))
        res = 0
    result.sort(reverse=True, key=lambda y: y[1])

    return result


def run(term, documents):
    term = re.sub("[$@&,?!'\"/#%^*(){}+=|.-]", "", term).lower()
    split_term = term.split(' ')
    split_term = [elem for elem in split_term if elem.strip()]
    query_dict = dict.fromkeys(split_term, 0)

    questions_dict = {}
    for document in documents:
        questions_dict[document["qa_id"]] = {"terms": query_dict, "document": document}

    N = len(documents)
    results = run_tf_idf(questions_dict, N, split_term)

    return results[:10]

'''
term = "pasta?"
documents = [({'Question': 'how to make pasta?', 'Answers': [{'Answer': 'go to italy', 'Likes': 8, 'Dislikes': 3}, {'Answer': 'call wolt', 'Likes': 3, 'Dislikes': 2}, {'Answer': 'learn in the internet', 'Likes': 9, 'Dislikes': 5}], 'qa_id': 2}, 0.0), ({'Question': 'what is java update scheduler?', 'Answers': [{'Answer': 'Java Update scheduler will check for newer Java updates and notify you at the scheduled frequency.', 'Likes': 3, 'Dislikes': 0}, {'Answer': 'answer 2', 'Likes': 6, 'Dislikes': 1}], 'qa_id': 1}, 0.0), ({'Question': 'From which countries did the Norse originate?', 'Answers': [{'Answer': 'Denmark, Iceland and Norway', 'Likes': 2, 'Dislikes': 0}], 'qa_id': 5}, 0.0), ({'Question': 'When were the Normans in Normandy?', 'Answers': [{'Answer': '10th and 11th centuries', 'Likes': 9, 'Dislikes': 1}, {'Answer': 'in the 10th and 11th centuries', 'Likes': 5, 'Dislikes': 5}], 'qa_id': 4}, 0.0), ({'Question': 'What century did the Normans first gain their separate identity?', 'Answers': [{'Answer': '10th century', 'Likes': 8, 'Dislikes': 0}, {'Answer': '10th', 'Likes': 0, 'Dislikes': 0}, {'Answer': 'the first half of the 10th century', 'Likes': 9, 'Dislikes': 5}], 'qa_id': 7}, 0.0), ({'Question': 'What religion were the Normans', 'Answers': [{'Answer': 'Catholic orthodoxy', 'Likes': 7, 'Dislikes': 5}, {'Answer': 'Catholic', 'Likes': 0, 'Dislikes': 4}], 'qa_id': 10}, 0.0), ({'Question': 'Who ruled the duchy of Normandy', 'Answers': [{'Answer': 'Richard I', 'Likes': 6, 'Dislikes': 4}], 'qa_id': 9}, 0.0), ({'Question': 'Who upon arriving gave the original viking settlers a common identity?', 'Answers': [{'Answer': 'Rollo', 'Likes': 7, 'Dislikes': 1}], 'qa_id': 16}, 0.0), ({'Question': 'Who did Rollo sign the treaty of Saint-Clair-sur-Epte with?', 'Answers': [{'Answer': 'King Charles III', 'Likes': 6, 'Dislikes': 5}], 'qa_id': 14}, 0.0), ({'Question': 'What part of France were the Normans located?', 'Answers': [{'Answer': 'the north', 'Likes': 2, 'Dislikes': 0}, {'Answer': 'north', 'Likes': 5, 'Dislikes': 1}], 'qa_id': 18}, 0.0)]
print(documents)
run(term, documents)
'''

