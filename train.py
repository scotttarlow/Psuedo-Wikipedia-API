#!/Users/Scott/anaconda/bin/python
from sklearn.externals import joblib
import lib.database_module as db

cat_vectors = db.select_all_category_vectors()
page_vectors = db.select_all_page_vectors()
joblib.dump(cat_vectors,'category_vectors.plk')
joblib.dump(page_vectors,'page_vectors.plk')

print "pickles made"