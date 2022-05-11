import re
import json
from scipy import spatial




def recherche(dictionnaire,seuil):
    
    #Inversion du dictionnaire reçu
    dictionnaireInverse={}
    for word in dictionnaire:
        for doc in dictionnaire[word]:
            if doc not in dictionnaireInverse:
                dictionnaireInverse[doc]={}
            dictionnaireInverse[doc][word]=dictionnaire[word][doc]
    #print(dictionnaireInverse)
            
    #Association mot indice
    correspMots={}
    i=0
    for word in dictionnaire:
        correspMots[word]=i
        i+=1
    #print(correspMots)
    
    #On fait un vecteur par document et requete en séparant requete et document
    vecteursDocs={}
    vecteursReq={}
    for doc in dictionnaireInverse:
        if(re.match("D.*",doc) is not None):
            vecteursDocs[doc]=[0]*len(correspMots)
            for word in dictionnaireInverse[doc]:
                vecteursDocs[doc][correspMots[word]]=dictionnaire[word][doc]
        else:
            vecteursReq[doc]=[0]*len(correspMots)
            for word in dictionnaireInverse[doc]:
                vecteursReq[doc][correspMots[word]]=dictionnaire[word][doc]
    #print("\n",vecteursDocs,"\n", vecteursReq)
    
    #print(vecteursDocs)
    #print(vecteursReq)
    

    #Comparaison des vecteurs requêtes aux documents et remplissage du tableau res si la similarité entre les
    #deux est supérieur au seuil fourni
    res={}

    for req in vecteursReq:
        for doc in vecteursDocs:
            sim=1-spatial.distance.cosine(vecteursReq[req],vecteursDocs[doc])
            if(sim>0.01):
                print(sim)
                #print((vecteursReq[req],vecteursDocs[doc]))
            if sim>seuil:
                if req not in res:
                    res[req]={}
                res[req][doc]=sim
    #print(res)  

    #Affichage des résultats triés dans le fichier Res.txt
    fichier=open("Res.txt","w")
    for req in res:
        while res[req]:
            max=0
            temp=0
            for doc in res[req]:
                if(res[req][doc]>max):
                    max=res[req][doc]
                    temp=doc
            if max!=0:
                fichier.write(req+"   "+temp+"   "+str(max)+"\n")
                res[req].pop(temp)
        
    fichier.close()
    
    return



if __name__ == "__main__":
    with open('data.json') as json_file:
        dictionnaire = json.load(json_file)
    #print(dictionnaire)
    #print(dictionnaire['18']['D1'])
    recherche(dictionnaire,0.2)
    #sim=spatial.distance.cosine([0,0,0,0.024650290902159578],[0.09134649426355344, 0, 0, 0.024650290902159578])
    #print(1-spatial.distance.cosine([0,0,0,0,0,0,0,1,1,0,0,0,0,0,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]))
    #print(sim)
