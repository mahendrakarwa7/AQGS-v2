textinput=""
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pymysql
from textblob import TextBlob
from my_functions import custom_ner
from module_2  import   ready_rules , passed_text

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import spacy

final2=[]
final = []
final3=[]

app = Flask(__name__)



def parse(string):
    try:
        final.clear()
        final1.clear()
        final2.clear()
        txt = TextBlob(string)
        for sentence in txt.sentences:
            genQuestion(sentence)
            quest(sentence)       
    except Exception as e:
        raise e
    
# mahendraa text-preprocessing
def preprocess_text(text):
    # Tokenize
    sentences = sent_tokenize(text)

    # Tokenize into words and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for sentence in sentences for word in word_tokenize(sentence) if word.isalnum() and word.lower() not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

    return lemmatized_words

# mahendraa text-preprocessing

nlp = spacy.load('en_core_web_sm')
def pos_and_ner(text):
    doc = nlp(text)
    pos_tags = [(token.text, token.pos_) for token in doc]
    named_entities = [(ent.text, ent.label_) for ent in doc.ents]

    return pos_tags, named_entities

# mahendraa text-preprocessing

def dependency_parsing_and_srl(text):
    doc = nlp(text)
    dependency_tree = [(token.text, token.dep_, token.head.text) for token in doc]
    semantic_roles = [(token.text, token.dep_, token.head.text, [child.text for child in token.children]) for token in doc]
    return dependency_tree, semantic_roles








def quest(text):
    if type(text) is str:    
        text = TextBlob(text) 

    bucket1 = {}  
    
    for i,j in enumerate(text.tags): 
        if j[1] not in bucket1:
            bucket1[j[1]] = i
            
            question1 = ' '
    b1=['NN','VBZ']
    b2=['NNP','VBZ']
    
    if all(key in  bucket1 for key in b1): 
        final1.append('Define' + ' ' + text.words[bucket1['NN']] +' '+ '.')
       
        
    elif all(key in  bucket1 for key in b2): 
        final1.append('Define' + ' ' + text.words[bucket1['NNP']] +' '+ '.')
        
    if 'VBZ' in bucket1 and text.words[bucket1['VBZ']] == "’":
        final1.append(final1.replace(" ’ ","'s "))
        
    

def genQuestion(line):
    if type(line) is str:    
        line = TextBlob(line) 

    bucket = {}  
    
    for i,j in enumerate(line.tags):  
        if j[1] not in bucket:
            bucket[j[1]] = i
            
           
            
    l1 = ['NNP', 'VBG', 'VBZ', 'IN']
    l2 = ['NNP', 'VBG', 'VBZ']
    l3 = ['PRP', 'VBG', 'VBZ', 'IN']
    l4 = ['PRP', 'VBG', 'VBZ']
    l5 = ['PRP', 'VBG', 'VBD']
    l6 = ['NNP', 'VBG', 'VBD']
    l7 = ['NN', 'VBG', 'VBZ']

    l8 = ['NNP', 'VBZ', 'JJ']
    l9 = ['NNP', 'VBZ', 'NN']

    l10 = ['NNP', 'VBZ']
    l11 = ['PRP', 'VBZ']
    l12 = ['NNP', 'NN', 'IN']
    l13 = ['NN', 'VBZ']
    
    if all(key in  bucket for key in l1): #'NNP', 'VBG', 'VBZ', 'IN' in sentence.
        final.append('What' + ' ' + line.words[bucket['VBZ']] +' '+ line.words[bucket['NNP']]+ ' '+ line.words[bucket['VBG']] + '?')

    
    elif all(key in  bucket for key in l2): #'NNP', 'VBG', 'VBZ' in sentence.
        final.append('What' + ' ' + line.words[bucket['VBZ']] +' '+ line.words[bucket['NNP']] +' '+ line.words[bucket['VBG']] + '?')

    
    elif all(key in  bucket for key in l3): #'PRP', 'VBG', 'VBZ', 'IN' in sentence.
        final.append('What' + ' ' + line.words[bucket['VBZ']] +' '+ line.words[bucket['PRP']]+ ' '+ line.words[bucket['VBG']] + '?')

    
    elif all(key in  bucket for key in l4): #'PRP', 'VBG', 'VBZ' in sentence.
       final.append('What ' + line.words[bucket['PRP']] +' '+  ' does ' + line.words[bucket['VBG']]+ ' '+  line.words[bucket['VBG']] + '?')

    elif all(key in  bucket for key in l7): #'NN', 'VBG', 'VBZ' in sentence.
        final.append('What' + ' ' + line.words[bucket['VBZ']] +' '+ line.words[bucket['NN']] +' '+ line.words[bucket['VBG']] + '?')

    elif all(key in bucket for key in l8): #'NNP', 'VBZ', 'JJ' in sentence.
        final.append('What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[bucket['NNP']] + '?')

    elif all(key in bucket for key in l9): #'NNP', 'VBZ', 'NN' in sentence
        final.append('What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[bucket['NNP']] + '?')

    elif all(key in bucket for key in l11): #'PRP', 'VBZ' in sentence.
        if line.words[bucket['PRP']] in ['she','he']:
           final.append('What' + ' does ' + line.words[bucket['PRP']].lower() + ' ' + line.words[bucket['VBZ']].singularize() + '?')

    elif all(key in bucket for key in l10): #'NNP', 'VBZ' in sentence.
        final.append('What' + ' does ' + line.words[bucket['NNP']] + ' ' + line.words[bucket['VBZ']].singularize() + '?')

    elif all(key in bucket for key in l13): #'NN', 'VBZ' in sentence.
        final.append('What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[bucket['NN']] + '?')

    
    if 'VBZ' in bucket and line.words[bucket['VBZ']] == "’":
        final.append(final.replace(" ’ ","'s "))

    # Print the genetated questions as output.
    #if question != '':
    #print('\n', 'Question: ' + question )
        
  
        

app = Flask(__name__)


app.secret_key = 'sanket'

connection = pymysql.connect(
    host='sql6.freesqldatabase.com',    # db hostname according to localhost 
    user='sql6689373',              # username  of free sql db
    password='TZ5Dk8InrJ',            # pwd  of free sql db
    database='sql6689373',              #db name of free sql db
)

mysql = MySQL(app)

@app.route('/pythonlogin/home')
def home():

    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))

        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('xyz.html', msg=msg)

@app.route('/pythonlogin/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)', (username, password, email,))
            connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/pythonlogin/profile',methods=["POST"])
def profile():
    # Check if user is loggedin
    questions=[]
    textinput=request.form.get("name")
    #parse(textinput)
    #preprocessed_text = preprocess_text(textinput)
    #print(preprocessed_text)
    #pos_tags, named_entities = pos_and_ner(textinput)
    #print("POS Tags:", pos_tags)
    #print("Named Entities:", named_entities)
    #dependency_tree, semantic_roles = dependency_parsing_and_srl(textinput)
    #print("Dependency Tree:", dependency_tree)
    #print("Semantic Roles:", semantic_roles)
    #final2=final1+final
    #final2 = custom_ner(textinput)
    final3 = ready_rules()
    lst =[]
    passed_text(textinput)
    """for que in final3:
        lst.append(que[1])"""

    final =  final3
    questions=[]
    for val in final:
        if val!=' ' and val not in questions: 
            questions.append(val) 
         
    return render_template("profile.html", questions=questions)
    
@app.route('/')
def start():
    return render_template("index.html")

def index():
    name = ready_rules()
    #print(name)

    


# if __name__ == '__main__':
#     app.run()
