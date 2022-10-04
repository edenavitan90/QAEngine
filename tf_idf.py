import math
import json
import os


def compute_idf(N, nt):
    # N - Numbers of docs
    # nt - Number of docs containing the term
    return math.log(N/nt) if nt != 0 else 0


def compute_tf(query_dict, doc):
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
    print("running")
    split_term = term.split(' ')
    split_term = [elem for elem in split_term if elem.strip()]
    query_dict = dict.fromkeys(split_term, 0)

    questions_dict = {}
    for document in documents:
        questions_dict[document["qa_id"]] = {"terms": query_dict, "document": document}

    N = len(documents)
    results = run_tf_idf(questions_dict, N, split_term)

    return results[:10]


# if __name__ == "__main__":
#
#     term_arg = "a year"
#     with open("db_data_copy.json", "r") as f:
#         documents_arg = json.load(f)
#         for idx, document_x in enumerate(documents_arg):
#             document_x["qa_id"] = idx+1
#         results = run(term=term_arg, documents=documents_arg)
#
