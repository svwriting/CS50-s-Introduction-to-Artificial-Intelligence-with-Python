import nltk
import sys
import os
import math
import string

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))
    #query = set(tokenize("What are the types of supervised learning?")) 
    #query = set(tokenize("When was Python 3.0 released?")) 
    #query = set(tokenize("How do neurons connect in a neural network?")) 

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dic_={}
    for str_ in os.listdir(directory):
        with open(os.path.join(directory,str_),mode='r') as txt_:
            dic_[str_]=txt_.read()
    return dic_
    raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tok_=[ str_ for str_ in nltk.word_tokenize(document.lower()) \
        if ((str_ not in string.punctuation) and ( str_ not in nltk.corpus.stopwords.words('english')))
    ]
    return tok_
    raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    dic_={}
    for txt_ in documents:
        for word_ in set(documents[txt_]):
            if word_ in dic_:
                dic_[word_]+=1
            else:
                dic_[word_]=1
    dn=len(documents)
    for word_ in dic_:
        dic_[word_]=math.log(dn/dic_[word_])
    return dic_
    raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    dic_=[]
    for file_ in files:
        tfidf_=0
        for word_ in query:
            tfidf_+=idfs[word_]*files[file_].count(word_)
        dic_.append((file_,tfidf_))
    dic_.sort(key=lambda x:x[1],reverse=True)
    dic_=[ x[0] for x in dic_ ]
    return dic_[:n]
    raise NotImplementedError

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    dic_=[]
    for sentence_ in sentences:
        sumidf=0
        count_=0
        for word_ in query:
            if word_ in sentences[sentence_]:
                count_+=1
                sumidf+=idfs[word_]
        density_=float(count_)/len(sentences[sentence_])
        dic_.append((sentence_,sumidf,density_))
    dic_.sort(key=lambda x:(x[1],x[2]) ,reverse=True)
    dic_=[ x[0] for x in dic_ ]
    dic_=dic_[:n]
    return dic_
    raise NotImplementedError


if __name__ == "__main__":
    main()
