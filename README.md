# AIR2022
Advanced Information Retrieval 2022 Group Project

Reddit Content Analysis of r/conspiracy

## Project layout

### Root Folder
The root folder contains python files mostly used for data retrival via the PRAW API:

#### main.py
The main.py requires 3 positional arguments which are:
- reddit_client_id
- reddit_client_secret
- openAi_api_key

The reddit client_id and client_secret can be obtained by creating a reddit application in your reddit account. The application type has to be 'script'.
The OpenAI API Key can be generated with your OpenAI Account.

### dataframes Folder
This folder contains multiple datasets which were already crawled in order to have reproducable results.

### notebooks Folder
This folder contains different notebooks for different topics of this work and their results

__Attention:__  
For 'content_analysis.ipynb' the OpenAI API Key needs to be specified before the call to OpenAiWrapper:
```python
Utils.openAi_api_key = 'your API Key'
```
Alternatively you can paste a csv file called embeddings_hot.csv which contains all embeddings of the already crawled dataset 'praw_hot_submissions.csv'.
You can download this file here: https://drive.google.com/file/d/1d9dBYjTuzCVufF4gY8g1dtWSuKroUBx0/view?usp=sharing
