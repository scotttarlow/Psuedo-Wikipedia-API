#!/Users/Scott/anaconda/bin/python

import lib.database_module as db
import lib.encoding_module as en
import lib.wiki_module as wiki
import pandas as pd
import numpy as np
from sklearn.externals import joblib
from sklearn.metrics.pairwise import cosine_similarity
import sys

args = sys.argv
sys.argv.pop(0)

search_term = args[0]
transformer = joblib.load('vectorizer.pkl')

search_term_vector = en.get_searchterm_vector(transformer,search_term)
pages_vectors = db.select_all_page_vectors()

cosine_scores = {}
for vec in pages_vectors:
    cosine_scores[str(vec[0])] = cosine_similarity(search_term_vector[search_term][0].reshape(1,-1),np.array(vec[1]).reshape(1,-1))

cos_series = pd.Series(data=cosine_scores.values(),index=cosine_scores.keys())
cos_series.sort_values(ascending=False,inplace=True)

five_best = cos_series.head()
five_best_pages = db.select_pages(five_best.index)

five_best_summ = []
for f in five_best_pages:
    temp = wiki.query_page(pageid=str(f[0]),title=f[1])
    five_best_summ.append((temp['title'],temp['summary']))
    

for f in five_best_summ:
    print ' '
    print   f[0],':',f[1]

