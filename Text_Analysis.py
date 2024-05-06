import requests
import pandas as pd
import nltk
import re
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup 

df=pd.read_excel('Input.xlsx')

for index, row in df.iterrows():
    url = row['URL']
    url_id = row['URL_ID']
    
# make a request to url
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }  # giving user access
    try:
        response = requests.get(url,headers=header)
        response.raise_for_status()
    except:
        print("can't get response of {}".format(url_id))

    #create a beautifulsoup object
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
    except:
        print("can't get page of {}".format(url_id))
    #find title
    try:
        title = soup.find('h1').get_text()
    except:
        print("can't get title of {}".format(url_id))
        continue
  #find text
    article = ""
    try:
        for p in soup.find_all('p'):
            article += p.get_text()
    except:
        print("can't get text of {}".format(url_id))

    #write title and text to the file
 
    file_name = 'C:/Users/hp/Downloads/New folder (10)/text/' + str(url_id) + '.txt'
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(title + '\n' + article)


# Directories
textdir = 'C:/Users/hp/Downloads/New folder (10)/text'
stopwordsdir = 'C:/Users/hp/Downloads/New folder (10)/StopWords'
sentimentdir = 'C:/Users/hp/Downloads/New folder (10)/MasterDictionary'

# Load all stop words from the stopwords directory and store in the set variable
stop_words = set()
for files in os.listdir(stopwordsdir):
    with open(os.path.join(stopwordsdir, files), 'r', encoding='latin-1') as f:
        stop_words.update(set(f.read().splitlines()))

# Load all text files from the directory and store in a list(docs)
docs = []
for text_file in os.listdir(textdir):
    file_path = os.path.join(textdir, text_file)
    # Clean up file name by removing invalid characters
    cleaned_file_name = re.sub(r'[^\w\s.-]', '', text_file)  # Remove characters that are not letters, numbers, whitespace, dots, or dashes
    try:
        with open(file_path, 'r', encoding='latin-1') as f:
            text = f.read()
            # Tokenize the given text file
            words = word_tokenize(text)
            # Remove the stop words from the tokens
            filtered_text = [word for word in words if word.lower() not in stop_words]
            # Add each filtered tokens of each file into a list
            docs.append(filtered_text)
    except Exception as e:
        print(f"Error processing file {cleaned_file_name}: {e}")

# Store positive and negative words from the directory
pos = set()
neg = set()

for files in os.listdir(sentimentdir):
    if files == 'positive-words.txt':
        with open(os.path.join(sentimentdir, files), 'r', encoding='latin-1') as f:
            pos.update(f.read().splitlines())
    else:
        with open(os.path.join(sentimentdir, files), 'r', encoding='latin-1') as f:
            neg.update(f.read().splitlines())

# Now collect the positive and negative words from each file
# Calculate the scores from the positive and negative words
positive_words = []
negative_words = []
positive_score = []
negative_score = []
polarity_score = []
subjectivity_score = []

# Iterate through the list of docs
for i in range(len(docs)):
    positive_words.append([word for word in docs[i] if word.lower() in pos])
    negative_words.append([word for word in docs[i] if word.lower() in neg])
    positive_score.append(len(positive_words[i]))
    negative_score.append(len(negative_words[i]))
    polarity_score.append((positive_score[i] - negative_score[i]) / ((positive_score[i] + negative_score[i]) + 0.000001))
    subjectivity_score.append((positive_score[i] + negative_score[i]) / ((len(docs[i])) + 0.000001))


# Average Sentence Length = the number of words / the number of sentences
# Percentage of Complex words = the number of complex words / the number of words 
# Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)

avg_sentence_length = []
Percentage_of_Complex_words = []
Fog_Index = []
complex_word_count = []
avg_syllable_word_count = []
pp_count = []

nltk_stopwords_set = set(stopwords.words('english'))

def measure(file):
    with open(os.path.join(textdir, file), 'r',encoding='ISO-8859-1') as f:
        text = f.read()
        
        # remove punctuations
        text = re.sub(r'[^\w\s.]', '', text)
        
        # split the given text file into sentences
        sentences = text.split('.')
        
        # total number of sentences in a file
        num_sentences = len(sentences)
        if num_sentences == 0:  # Handle division by zero
            num_sentences = 1  # Assigning 1 to prevent division by zero
        
        # total words in the file
        words = [word for word in text.split() if word.lower() not in nltk_stopwords_set]
        num_words = len(words)
        if num_words == 0:  # Handle division by zero
            num_words = 1  # Assigning 1 to prevent division by zero
        
        # complex words having syllable count is greater than 2
        complex_words = [word for word in words if len(re.findall(r'[aeiouAEIOU]{3,}', word)) > 2]
        
        # Syllable Count Per Word
        syllable_count = sum(len(re.findall(r'[aeiouAEIOU]+', word)) for word in words)
        avg_syllable_word_count = syllable_count / num_words
        
        # Calculate metrics
        avg_sentence_len = num_words / num_sentences
        Percent_Complex_words = len(complex_words) / num_words
        Fog_Index = 0.4 * (avg_sentence_len + Percent_Complex_words)
        #count_personal_pronouns
        personal_pronouns = ["I", "we", "my", "ours", "us"]
        count = 0
        for pronoun in personal_pronouns:
            count += len(re.findall(r"\b" + pronoun + r"\b", text))  # \b is used to match word boundaries
        
        return avg_sentence_len, Percent_Complex_words, Fog_Index, len(complex_words), avg_syllable_word_count,count

# iterate through each file or doc
for file in os.listdir(textdir):
    x, y, z, a, b,c = measure(file)
    avg_sentence_length.append(x)
    Percentage_of_Complex_words.append(y)
    Fog_Index.append(z)
    complex_word_count.append(a)
    avg_syllable_word_count.append(b)
    pp_count.append(c)


# Word Count and Average Word Length Sum of the total number of characters in each word/Total number of words
# We count the total cleaned words present in the text by 
# removing the stop words (using stopwords class of nltk package).
# removing any punctuations like ? ! , . from the word before counting.
# Initialize stopwords for English language
stopwords = set(stopwords.words('english'))

def cleaned_words(file):
    with open(os.path.join(textdir, file), 'r',encoding='ISO-8859-1') as f:
        text = f.read()
        text = re.sub(r'[^\w\s]', '', text)
        words = [word for word in text.split() if word.lower() not in stopwords]
        length = sum(len(word) for word in words)
        average_word_length = length / len(words)
    return len(words), average_word_length

word_count = []
average_word_length = []
for file in os.listdir(textdir):
    x, y = cleaned_words(file)
    word_count.append(x)
    average_word_length.append(y)


data = {
    'POSITIVE SCORE': positive_score,
    'NEGATIVE SCORE': negative_score,
    'POLARITY SCORE': polarity_score,
    'SUBJECTIVITY SCORE': subjectivity_score,
    'AVG SENTENCE LENGTH': avg_sentence_length,
    'PERCENTAGE OF COMPLEX WORDS': Percentage_of_Complex_words,
    'FOG INDEX': Fog_Index,
    'AVG NUMBER OF WORDS PER SENTENCE':avg_sentence_length,
    'COMPLEX WORD COUNT': complex_word_count,
    'WORD COUNT': word_count,
    'SYLLABLE PER WORD': avg_syllable_word_count,
    'PERSONAL PRONOUNS': pp_count,
    'AVG WORD LENGTH': average_word_length
}

# Find the length of the longest list
max_length = max(len(lst) for lst in data.values())

# Ensure all lists have the same length by padding shorter lists with NaN values
for key, value in data.items():
    data[key] = value + [float('nan')] * (max_length - len(value))

# Create DataFrame
output = pd.DataFrame(data)

# Rename columns
output.columns = [
    
    'POSITIVE SCORE','NEGATIVE SCORE','POLARITY SCORE',
    'SUBJECTIVITY SCORE','AVG SENTENCE LENGTH',
    'PERCENTAGE OF COMPLEX WORDS','FOG INDEX',
    'AVG NUMBER OF WORDS PER SENTENCE','COMPLEX WORD COUNT',
    'WORD COUNT','SYLLABLE PER WORD','PERSONAL PRONOUNS',
    'AVG WORD LENGTH'
]



import pandas as pd

# Load the original input file
input_df = pd.read_excel('Output Data Structure.xlsx')

# Retain only the two columns from the original dataframe
input_df = input_df[['URL_ID', 'URL']]

# Concatenate the input DataFrame with the output DataFrame
result_df = pd.concat([input_df, output], axis=1)

# Save the result to the input file without deleting existing columns
result_df.to_excel('Output Data Structure.xlsx', index=False)

    
