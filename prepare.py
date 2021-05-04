import env
import unicodedata
import re
import json
import nltk

from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

def basic_clean(string):
    """
    Lowercases, removes non-ASCII characters, and removes non-alphanumeric (except ' or \s') from the passed in string.
    """
    
    cleaned_string = string
    
    cleaned_string = cleaned_string.lower()
    cleaned_string = unicodedata.normalize("NFKD", cleaned_string).encode("ascii", "ignore").decode("utf-8", "ignore")
    cleaned_string = re.sub(r"[^a-z0-9'\s]", "", cleaned_string)
    
    return cleaned_string

def tokenize(string):
    """
    Applies the ToktokTokenizer.tokenize() method to the passed in string.
    """
    
    tokenized_string = string
    tokenizer = nltk.tokenize.ToktokTokenizer()
    
    return tokenizer.tokenize(tokenized_string, return_str=True)

def stem(string):
    """
    Generates a list of the stem for each word in the original string and returns the joined list of stems as a single string.
    """
    
    ps = nltk.porter.PorterStemmer()
    
    stems = [ps.stem(word) for word in string.split()]
    
    return " ".join(stems)

def lemmatize(string):
    """
    Generates a list of the root word for each word in the original string and returns the joined list of root words as a single string.
    """
    
    wnl = nltk.stem.WordNetLemmatizer()
    
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    
    return " ".join(lemmas)

def remove_stopwords(string, extra_words=None, exclude_words=None):
    """
    Generates a list of stop words then adds and/or removes the specified words from that stop word list. Any words from the \
    original string that are not present in the stop word list are added to the filtered word list. Returns the joined filtered word \
    list as a single string.
    """
    
    stopword_list = stopwords.words("english")
    extras = []
    excludes = []
    
    if extra_words != None:
        extras = extra_words.copy()
        
    if exclude_words != None:
        excludes = exclude_words.copy()
    
    stopword_list = stopword_list + extras
        
    for ex_word in excludes:
        if ex_word in stopword_list:
            stopword_list.remove(ex_word)

    filtered_words = [word for word in string.split() if word not in stopword_list]

    return " ".join(filtered_words)

def prepare_webpage_data(df, content_key):
    """
    Takes in a df and the key name of the content column then generates clean, stemmed, and lemmatized columns. The clean column contains \
    the values after the basic_clean, tokenize, and remove_stopwords functions are applied to the content column. The stemmed \
    and lemmatized columns contain the values after the stemmed and lemmatized functions are applied to the clean column.
    """
    
    prepped_df = df.copy()
    
    prepped_df['clean'] = prepped_df[content_key].apply(basic_clean)
    prepped_df['clean'] = prepped_df['clean'].apply(tokenize)
    prepped_df['clean'] = prepped_df['clean'].apply(remove_stopwords)

    prepped_df['stemmed'] = prepped_df['clean'].apply(stem)

    prepped_df['lemmatized'] = prepped_df['clean'].apply(lemmatize)
    
    return prepped_df