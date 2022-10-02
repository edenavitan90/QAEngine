import math
import os


def compute_idf(N, nt):
    # N - Numbers of docs
    # nt - Number of docs containing the term
    return math.log(N/nt) if nt != 0 else 0


def compute_tf(query_dict, doc):
    tf_dict = {}
    doc_count = doc.count(' ') + 1
    for term in query_dict.keys():
        term_count = doc.count(term)
        tf_dict[term] = term_count/float(doc_count)
    return tf_dict


def run_tf_idf(books_dict, N, terms):
    # TF Part
    for book, book_term in books_dict.items():
        path = os.getcwd() + os.sep + "books" + os.sep + book
        with open(path, 'r', encoding='utf-8') as f:
            book_doc = f.read().lower()
        books_dict[book] = compute_tf(book_term, book_doc)

    # IDF Part
    print()
    nt = 0
    terms_idf_dict = {}  # Holds the idf result for each term.
    for term in terms:
        for book, book_terms in books_dict.items():
            if book_terms.get(term, 0) > 0:
                nt += 1
        idf_res = compute_idf(N=N, nt=nt)
        terms_idf_dict[term] = idf_res
        nt = 0

    # Calculate TF-IDF
    result = []
    res = 0
    for book, book_term in books_dict.items():
        for term in terms:
            res += book_term[term] * terms_idf_dict[term]
        result.append((book, res))
        res = 0
    result.sort(reverse=True, key=lambda y: y[1])
    return result


def get_books():
    working_dir = os.getcwd()
    path = working_dir + os.sep + "books"
    books_list = []
    for (root, dirs, file) in os.walk(path):
        for f in file:
            if '.txt' in f:
                books_list.append(f)
    return books_list

'''
if __name__ == "__main__":
    query_string = input("Please insert a query string:\n")
    splitted_query = query_string.split(' ')
    splitted_query = [elem for elem in splitted_query if elem.strip()]
    query_dict = dict.fromkeys(splitted_query, 0)
    books_list = get_books()
    books_dict = dict.fromkeys(books_list, query_dict)
    N = len(books_list)
    results = run_tf_idf(books_dict, N, splitted_query)

    print("Book in descending order using TF-IDF Algorithm:")
    for result in results:
        print(f"Book Title: {result[0].replace('.txt','')}  |   Book Score: {result[1]:.6f}")
'''
def run(term, documents):
    pass