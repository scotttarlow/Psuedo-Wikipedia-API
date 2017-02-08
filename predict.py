#!/Users/Scott/anaconda/bin/python
import lib.database_module as db
import lib.encoding_module as en
import lib.wiki_module as wiki
import pandas as pd
import numpy as np
import sys
from sklearn.externals import joblib
from sklearn.metrics.pairwise import cosine_similarity

args = sys.argv
sys.argv.pop(0)


pageid = int(args[0])
title =  args[1]
page = wiki.query_page(pageid=str(pageid),title=title)

cat_vectors = joblib.load('cateogry_vectors.plk')
transformer = joblib.load('Vectorizer.pkl')

page_vec = en.get_page_vector(transformer=transformer,page_ids=[pageid],clean_pages=[page['text']])
similarties = [cosine_similarity(page_vec[pageid][0].reshape(1,-1),np.array(c[1]).reshape(1,-1)) for c in cat_vectors]

cat_dict = {}
for cat_id, sim in zip(cat_vectors,similarties):
    cat_dict[cat_id[0]] = sim

df = pd.Series(cat_dict,index=cat_dict.keys())
df.sort_values(inplace=True,ascending=False)
top_2 = df.head(2)
top_2 = zip(top_2.index,top_2.values)
categories = db.select_all_categories()

top_cat= []
for t in top_2:
    for c in categories:
        if int(t[0]) == c[0]:
            top_cat.append((c[1],t[1][0][0]))
            
print "The predicted category is:",top_cat[0][0],'with similarity score:',top_cat[0][1]*100,"percent."
print "This is",(top_cat[0][1]-top_cat[1][1])*100, 'precent higher than the next closest category:',top_cat[1][0],'.'