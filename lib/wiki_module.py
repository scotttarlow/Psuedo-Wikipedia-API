import requests
from urllib import quote
from unidecode import unidecode
from collections import OrderedDict
from bs4 import BeautifulSoup


#helper functions
def param_query(params):
    """
    
    Takes wikipedia parameters, converts, and returns it into appropriate query     format. 
    
    """
    param_list = [key+'='+str(value) for key,value in params.items()] 
    return '?'+'&'.join(param_list)

def cat_param_id(category):
    """
    
    Takes category name, formats, and adds it to wikipedia endpoint dictionary to extract category info.    
    
    """
    params = { 'action':'query',
               'format':'json',              
               'prop':'extracts',
               'exlimit':'maxl',
               'titles':'Category:'+quote(category)}
    return params

def cat_param_pages(category):
    """
    
    Takes category name, formats, and adds it to wikipedia endpoint dictionary to get a list of pages associated with that category.  
    
    """
    params = { 'action':'query',
               'format':'json',              
               'list':'categorymembers',
               'cmlimit':'max',
               'cmtype':'page',
               'cmtitle':'Category:'+quote(category)}
    return params

def page_params(pageid):
    """    
    
    Takes pageid and adds it to wikipedia endpoint dictionary to extract the content of the page.      
    
    """
    params = { 'action':'query',
               'format':'json',              
               'prop':'extracts',
               'exlimit':'maxl',
               'pageids':quote(pageid)}
    return params

def text_cleaner(text):
    """    
    
    Takes wikipedia page content and cleans their formatting to return plain text.  
    
    """
    text = " ".join(text.split()).replace("\'","").replace("/"," ").replace(r"[...]","")
    return text

def get_summary(text):
    """
    
    Takes plain text and returns the first 2 sentences as summary.  
    
    """
    summary = '.'.join(text.split('.')[:2])
    return summary 


#actual functions
def query_category(category):
    """
    
    Takes category name and returns a dictionary with category id and a list of pages (page id and title) associated with that category.
    
    """
    base_url = "https://en.wikipedia.org/w/api.php"
    
    param_one = cat_param_id(category)
    query_one = param_query(param_one)
    response_one = requests.get(base_url+query_one)
    categoryid = response_one.json()['query']['pages'].keys()[0]
    
    param_two = cat_param_pages(category)
    query_two = param_query(param_two)
    response_two = requests.get(base_url+query_two)
    pages = response_two.json()['query']['categorymembers']
    
    return {'categoryid':categoryid,'pages':[{'pageid':page['pageid'],'title':(unidecode(
                        page['title']))} for page in pages]}


def query_page(pageid,title):
    """
    
    Takes page id and title to return a dictionary with page id, summary, plain text and original html that was extracted from wikipedia.
    
    """
    base_url = "https://en.wikipedia.org/w/api.php"    
    
    query = param_query(page_params(pageid))
    response = requests.get(base_url+query)
    html = response.json()['query']['pages'][pageid]['extract']

    cleantext = BeautifulSoup(html,'lxml').text
    cleantext = text_cleaner(cleantext)
    summary = get_summary(cleantext)
    
    return OrderedDict([('pageid',int(pageid)),('title',title),('summary',summary),('text',cleantext),('html',html)])


