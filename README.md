This is the Readme for Project 6, a pseudo API for Wikipedia.

See Example_Commandline_Output jupyter notebook for example outputs from the command line. 

Current Corpus: 20 Categories, 2296 Pages

The scope of this project involves 4 pipelines:

1. Download

	To download all the pages of a Wikipedia category, either type the categories as a string using command line:
	
		./download '<category1>','<category2>', .....
		
		or 
		
	input the file path, as a string, of a .yml file:	
	
		./download 'filepath/category.yml'
	
	This pipeline will download all the pages in the category, and upload them to the project 6 database.

2. Search

	 To search the database, input string in the command line:
	 
	 	./search.py '<search term>'
	 
	 This pipeline will return the names and summaries of the top 5 most related articles to 
	 the search term.
	 
	 The method for searching is Latent Semantic Analysis. This functionality can be seen in lib/encoding_module.
	 Using Latent Semantic Analysis(LSA), all the pages are encoded and uploaded to the data base. There is a
	 Jupyter Notebook, Page_vectors_to_db which downloads all the wikipedia pages in project 6's database, encodes them
	 into vectors, and then uploads them to the data base.
	 
	 The search term is encoded to a vector using the same LSA transformer that was used to encode the pages.
	 The search term vector is then compared using cosine similarities with each page vector. The top 5 highest 
	 scoring page vectors are then returned, and outputted  in the format described in the previous paragraph.

3. Train

	To train the "page" to "category" predictor, use the command line:
		
		./train.py
	
	which will select all the category vectors from the data base and then
	pickle them for later use.
	
	The category vectors made by combining all the text from every article, and then running
	the LSA algorithm to project that category in the same euclidean space as each page.
	
	This method can be further updated with a Machline Learning algorithm using the page
	vectors as features and the category_id of each page as the target. 
	
	This pipeline will also load all the page vectors and save them in a pickle.
	
	
4. Predict
	
	Predict uses the cosine similarity to predict which category a page is in. The inputs
	for the command line are as follows:
	
		./predict.py '<page id>' '<page name>'
	
	The page entered in the command line is encoded to a vector and then compared to
	the category vectors made in Train. The output is a similarity score of the highest 
	category, the category name, the difference between the highest similarity score
	and the second highest similarity score, and the name of the second highest category. 
	
	
These were the methods created separate from the rest of the class:
	encoding_module.py
	select_all_categories in database_module.py
	
	
	
	