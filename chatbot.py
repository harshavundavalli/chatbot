import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import nltk
import os
import re
import string
import json
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.stem import WordNetLemmatizer

# Load knowledge base from pickle file
with open('knowledge_base.pickle', 'rb') as f:
    knowledge_base = pickle.load(f)

db_file = 'data_base.json'

if not os.path.exists(db_file):
    with open(db_file, 'w') as f:
        json.dump({}, f)


# Load the database
with open(db_file, 'r') as f:
    db = json.load(f)


combined_text=''

for file_name in os.listdir('scraped_texts_NTR'):
        if file_name.endswith('.txt'):
            with open(os.path.join('scraped_texts_NTR', file_name), 'r', encoding='utf-8') as f:
                text = f.read().lower()  # Read the text from the file and convert to lowercase
                # Tokenize the text
                combined_text+=text
combined_text = re.sub(r'\[[0-9]*\]', ' ', combined_text)
combined_text = re.sub(r'\s+', ' ', combined_text)
lemmer = WordNetLemmatizer()

sentence_tokens=sent_tokenize(combined_text)
word_tokens=word_tokenize(combined_text)



greet_in = ('hey', 'hi', 'hello', 'namastay')
greet_out = ['hey', 'hello', 'hi there', 'hi', 'heya', 'howdy', 'greetings',  'namastay']
def greeting(sent):
    for word in sent.split():
        if word.lower() in greet_in:
            return random.choice(greet_out)
      


welcome_msgs = {
'how are you': 'I am fine. Thankyou for asking ',
'how are you doing': 'I am fine. Thankyou for asking ',
'how do you do': 'I am great. Thanks for asking ',
'how are you holding up': 'I am fine. Thankyou for asking ',
'how is it going': 'It is going great. Thankyou for asking ',
'goodmorning': 'Good Morning ',
'goodafternoon': 'Good Afternoon ',
'goodevening': 'Good Evening ',
'good day': 'Good day to you too ',
'whats up': 'The sky ',
'thanks': 'Dont mention it. You are welcome ',
'thankyou': 'Dont mention it. You are welcome ',
'thank you': 'Dont mention it. You are welcome ',
}


welcome_val = welcome_msgs.values()
welcome_val = [str (item) for item in welcome_val]

#function for checking cosine similarity between the query and welcome_msgs
def cosine_welcome_msgs(doc, query):
    query = [query]
    tf = TfidfVectorizer(use_idf=True, sublinear_tf=True)
    tf_doc = tf.fit_transform(doc)
    tf_query = tf.transform(query)
    cosineSimilarities = cosine_similarity(tf_doc,tf_query).flatten()
    related_docs_indices = cosineSimilarities.argsort()[:-2:-1]
    if (cosineSimilarities[related_docs_indices] > 0.7):
        ans = [welcome_val[i] for i in related_docs_indices[:1]]
        return ans[0]
   

   
def respond(user_response):
    response=''
    
    tfidfvec=TfidfVectorizer(stop_words='english')
    tfidf=tfidfvec.fit_transform(sentence_tokens)
    #checking cosine similarity between query and all other sentences
    vals=cosine_similarity(tfidf[-1],tfidf)
    idx=vals.argsort()[0][-2]
    flat=vals.flatten()
    flat.sort()
    req_tfidf=flat[-2]
    
    if(req_tfidf==0):
        response="I am sorry.i can't help you with that now"
        return response
    else:
        response=response+sentence_tokens[idx]
        return response    

def create_user_model(user):
    #check whether the user in database
    if user not in db:
        db[user] = {'queries': [],'likes':[],'dislikes':[]}
        print(f'User model created for {user}.')
    else:
        print(f'welcome back {user}.')

def add_query(user, query):
    #append the query to user queries
    if user in db:
        db[user]['queries'].append(query)
        
    else:
        print(f'User {user} not found in the database.')

def add_dislike(user, query):
    #append the query to user queries
    if user in db:
        db[user]['dislike'].append(query)
        
    else:
        print(f'User {user} not found in the database.')

def add_like(user, query):
    #append the query to user queries
    if user in db:
        db[user]['like'].append(query)
        
    else:
        print(f'User {user} not found in the database.')

def update_database():
    #save the updated data to database
    with open(db_file, 'w') as f:
        json.dump(db, f, indent=4)
    


stop=True
while(stop==True):
   name = input('\nHello, my name is Loki,the chatbot designed to provide the information about jr.ntr . What is your name? : ')
   name = name.lower()
   #create user model and initialize it
   create_user_model(name)
   update_database()
   stop1=True
   print('Loki: Hi '+(name)+', what do you want to know about ntr?. If you want to exit, type Bye. :')
   while(stop1==True):
        
        query=input('You:')
        
        query = query.lower()
        query = query.strip("!@#$%^&*()<>,;?")
        if(query=='bye'):
            stop1=False
            print('Loki: This is Loki signing off. Bye, take care '+(name))
      
        else:
            #if query is in greetings
            if(greeting(query)!=None):
                print('\nLoki: '+greeting(query)+' '+(name))

            #if query related to smalltalk
            elif(cosine_welcome_msgs(welcome_msgs, query)!=None):
                x = cosine_welcome_msgs(welcome_msgs, query)
                print('\nLoki: '+x)

            
            else:
                #adding query to database
                add_query(name,query)
                update_database()
                sentence_tokens.append(query)
                word_tokens+=word_tokenize(query)
                final_words=list(set(word_tokens))
                print('Loki: ',respond(query))
                sentence_tokens.remove(query)
        stop=False
