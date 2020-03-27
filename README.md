# IRS-SearchEngine
A simple search engine developed as part of SRI course at the University of Jaén, Spain.

Class SearchEngine in the searchengine.py module can be used to initialize or load an index and then process queries on that index.
The script itself takes 3 command line arguments. First, the path to the config file. Second, the path to the query txt file. Third, how many top matches to return.
The config file should can contain two lines. 
  - structures=folder path to the structures folder from which index can be loaded, and saved at the end of the script. 
  - collection=folder path from which the html files can be scrubed and added to the index if it exists, or create a new index from those files
