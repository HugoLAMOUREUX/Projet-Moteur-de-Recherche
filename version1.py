# -*- coding: utf-8 -*-
"""
Created on Wed May  4 16:29:21 2022

@author: xinra
"""
import spacy
import nltk
import re
nltk.download('stopwords')
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from tqdm import tqdm
import math


 #Enleve les stopword, tokenize, stemming, lowerKey
 #Retourne une liste de lemma
def preprosseingDoc(doc, isRequest):
    stopset = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    final = []
    #Detecte le titre
    if isRequest:
        title = re.search(".T\n(.*)\n", doc)
        if title != None:
            print(title.group())
        pass
    else:
        doc_split=re.split("\s\s+",doc)
        if len(doc_split) > 1:
            title = doc_split[0]
            tokens = wordpunct_tokenize(title) # split text on whitespace and punctuation
            clean = [token.lower() for token in tokens if token.lower() not in stopset and len(token) > 2]
            final += ['title_'+stemmer.stem(word) for word in clean]
    #tokenize etc
    #Rajoute les balises
    tokens = wordpunct_tokenize(doc) # split text on whitespace and punctuation
    clean = [token.lower() for token in tokens if token.lower() not in stopset and len(token) > 2]
    final += [stemmer.stem(word) for word in clean]
    return final

def calculate_tf(tokens):
    tf_score = {}
    for token in tokens:
        tf_score[token] = tokens.count(token)
    return tf_score

def matrice_doc(doc,dictionary):
    res = {}
    for word in doc:
        if word in dictionary:
            res[word] = doc.count(word)/len(doc)
    return res
def calcul_tfidf(description):
    for doc in description.keys():
        description[doc] = description[doc]* math.log10(1460/len(description))
        
            
    

if __name__ == "__main__":
      
      file = open('CISI.ALLnettoye')
      read = file.read()
      
      file = open('CISI.QRY')
      read += file.read()
      doc_list=re.split(".I\s\d+",read)
     
      dictionary = {}
      real_doc = []
      vectorList = []
      
      invertedFile = {}
      for doc in tqdm(doc_list) : 
          res = preprosseingDoc(doc, doc_list.index(doc) >= 1461)
          real_doc.append(res)
          if doc_list.index(doc) < 1461:
              for word in res :
                  if(not word in dictionary) :
                      dictionary[word] = 1
          vectorList.append(matrice_doc(res, dictionary))
          
      for word in tqdm(dictionary):
          description = {}
          for i in range(len(vectorList)):
              if(word in vectorList[i].keys()):
                  if i < 1461:
                      description["D"+str(i)] = vectorList[i][word]
                  else:
                      description["R"+str(i-1460)] = vectorList[i][word]
          calcul_tfidf(description)
          invertedFile[word] = description
      import json
      with open('data.json', 'w') as f:
          json.dump(invertedFile, f)         
      
      