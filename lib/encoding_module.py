from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline

def build_vectorizer(clean_pages):
    '''
    this function takes a list of clean pages. It returns a fit svd transformer
    '''
    vectorizer = TfidfVectorizer(stop_words='english',use_idf=True,smooth_idf=True)
    svd = TruncatedSVD(n_components=500,algorithm='randomized',n_iter=10,random_state=42)
    svd_trans = Pipeline([('tfidf', vectorizer), 
                            ('svd', svd)])
    return svd_trans.fit(clean_pages)

def get_page_vector(transformer,clean_pages,page_ids):
    '''
    this function takes a trained svd transformer and returns a dictionary with string
    page_id's (input as a list in same order as clean_pages) as keys and page vectors
    as values.
    '''
    page_vecs = {}
    for page_id,page in zip(page_ids,clean_pages):
        page_vecs[page_id] = transformer.transform([page])
        
    return page_vecs

def get_searchterm_vector(transformer,searchterm):
    '''
    this function takes a trained svd transformer and a single string search
    term. It returns the vectorized search term with the searchterm as its key.
    '''
    search_vec = {}
    search_vec[searchterm] = transformer.transform([searchterm])
    return search_vec

def get_cat_vector(transformer,clean_pages_in_cat,cat):
    '''
    this function takes a trained svd transformer, a category, and all the pages in a cateogry(list)(cleaned),
    combines the pages into one "document" and transforms that document into a vector. 
    '''
    category_doc_string = ''
    for doc in clean_pages_in_cat:
        category_doc_string += doc
    return {cat:transformer.transform([category_doc_string])}





