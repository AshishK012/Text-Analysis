import pandas as pd
import nltk
import re
import string
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.corpus import opinion_lexicon
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from nltk.corpus import cmudict



def positive_negative_score(tokens,words,text):
    positive_wds = set(opinion_lexicon.positive())
    negative_wds = set(opinion_lexicon.negative())
    p=[]
    n=[]
    for e in tokens:
        if e in positive_wds:
            p.append(e)
    pos=len(p)
    for e in tokens:
        if e in negative_wds:
            n.append(e)
    neg=len(n)
    
    
    print(f"Positive {pos}, negative {neg}")
    Polarity_Score(pos,neg,tokens,words,text)
    
def avg_sentence_length(tokens,text):
    sentences = nltk.sent_tokenize(text)
    total_words = sum(len(tokens) for sentence in sentences)
    print("avg_sentence_length: ",total_words / len(sentences) )
    percentage_complex_words(tokens,text)
    #calculate_fog_index(tokens,text)
    

def calculate_avg_per_sentence(tokens,text):
    sentence=sent_tokenize(text)
    try:
        average=len(tokens)/len(sentence)
        print("calculate_avg_per_sentence: ",average)
    except ZeroDivisionError:
        print("calculate_avg_per_sentence: ",0)
    avg_sentence_length(tokens,text)
    
    
def subjectivity_score(x,y,tokens,words,text):
    subjectivity=(x + y)/ (len(words) + 0.000001)
    print("subjectivity_score: ",subjectivity)
    
    calculate_avg_per_sentence(tokens,text)

   
def Polarity_Score(x,y,tokens,words,text):
    Polarity= (x - y)/ ((x + y) + 0.000001)
    print("Polarity_Score: ",Polarity)
    subjectivity_score(x,y,tokens,words,text)
   


def percentage_complex_words(tokens,text):
    syllable = 0
    complex_word_count = 0
    cmudict_dict = cmudict.dict()
    for word in tokens:
        syllable = syllable + syllable_counter(word, cmudict_dict)[0]
        if syllable_counter(word, cmudict_dict)[0] >= 2:
            complex_word_count += 1
    try:
        complex_word=(complex_word_count / len(tokens))
        print("percentage_complex_words: ",complex_word)
    except ZeroDivisionError:
        print("percentage_complex_words: ",0)
    calculate_word_count(tokens)
                    

def syllable_counter(word, cmudict_dict):
    try:
        return [len(list(y for y in x if y[-1].isdigit())) for x in cmudict_dict[word.lower()]]
    except KeyError:
        return [1]


def syllables_per_word(tokens):
    syllable_count = 0
    cmudict_dict = cmudict.dict()
    for word in tokens:
        syllable_count=syllable_count + syllable_counter(word, cmudict_dict)[0]
    try:
        syllables_perword=(syllable_count / len(tokens))
        print("syllables_per_word: ",syllables_perword)
    except ZeroDivisionError:
        print("syllables_per_word: ",0)
        
    calculate_personal_pronouns(tokens)

 
def calculate_personal_pronouns(tokens):
    personal_pronoun_count = 0
    for word in tokens:
        if word.lower() in ['i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours']:
            personal_pronoun_count += 1

    print("calculate_personal_pronouns: ",personal_pronoun_count)
    
    avg_word_length(tokens)


def avg_word_length(tokens):
    total_chars = sum(len(tokens) for word in tokens)
    print("avg_word_length: ",total_chars / len(tokens))
    


def calculate_word_count(tokens):
    print("calculate_word_count: ",len(tokens))
    syllables_per_word(tokens)
    
   
def clean_text(text,url_id):
    f=open(url_id+".txt","r",encoding='utf-8')
    text=f.read()
    all_reviews=list()
    text=text.lower()
    pattern=re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F]))+')
    text=pattern.sub('',text)
    text=re.sub(r"{,.\"!@#$%^&*(){}?/;~:<>*=-}","",text)
    #print(text)
    tokens= word_tokenize(text)
    #print(tokens)
    table=str.maketrans('','',string.punctuation)
    stripped=[w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]
    stop_words=set(stopwords.words("english"))
    words = [w for w in words if not w in stop_words]
    #print(words)
    positive_negative_score(tokens,words,text)
    f.close()
    



def writeFile(Text,url_id):
    f=open(url_id+".txt","w+",encoding='utf-8')
    for paragraph in Text:
            f.write(paragraph)
    f.close()
    clean_text(Text,url_id)
    



    
def articles():
    dataset=pd.read_csv("Input.csv")
    url=0
    for i in range(0,len(dataset)):
                url=i
                page=requests.get(dataset.iloc[url][1])
                htmlcontent=page.content
                soup=BeautifulSoup(htmlcontent,'html.parser')

                divContent=soup.find_all('div',attrs={'class':['td-post-content tagdiv-type'
                                                               ,'tdb-block-inner td-fix-index',
                                                               'mdc-o-content-body mck-u-dropcap']})
                paragraphs = []
                try:
                    paragraphs.append(soup.find("h1").get_text()+"\n")
                except:
                    return
                print("Title: ",paragraphs[0])
                for x in divContent:
                    paragraph_tags=x.find_all(['p','li'])
                    for p in paragraph_tags:
                        paragraphs.append(p.text.strip())
                x=str(dataset.iloc[i][0]
                writeFile(paragraphs,x) 

articles()

