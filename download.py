#!/Users/Scott/anaconda/bin/python
import lib.database_module as db
import lib.wiki_module as wiki
import yaml
import sys

args = sys.argv
sys.argv.pop(0)

# checks to see if argument is a yml, if not, makes args a list
if '.yml' in args[0]:
    with open(args[0], 'r') as stream:
        try:
            a =(yaml.load(stream))
        except yaml.YAMLError as exc:
            print(exc)
    category = a['categories'].split(',')
else:
    category = args
    
#gets all pages_ids for a given category 
subject_pages = []
for c in category:
    subject_pages.append(wiki.query_category(str(c)))    

#adds all categorys to database
for c,i_d in zip(category,subject_pages):
	db.create_or_update_category_in_database(str(c),i_d['categoryid'])

print '**********',"uploaded categories",category,'**********'


# pages are in list then dictionary
pages = []
for c in subject_pages:
    for p in c:
        for i in c[p]:
            try:
                pages.append((wiki.query_page(str(i['pageid']),i['title']),c['categoryid']))
            except:
                pass
                

#this loads pages into data base
for p in pages:
    db.create_or_update_page_in_database(category_id=p[1],
                                     page_id=p[0]['pageid'],
                                     page_text=p[0]['text'],
                                     page_title=p[0]['title'])

print '**************' ,'uploaded all pages' ,'*************'