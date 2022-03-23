import argparse
import timeit
import os
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from ir_system import IRSystem

# docs = ['hello i m a machine learning engineer', 
#         'hello bad world machine engineering people', 
#         'the world is a bad place',
#         'engineering a great machine that learns',"world is so great",'','']
docs=[]
for i in range(1,50):
    docs.append(' ')

#these are just a list of preliminary stop words listed by us but all the other stop words are take care using nltk library
stop_words = ['is', 'a', 'for', 'the', 'of','this','was','it','that','.',',',';',':','-','_']


documentID = 0
path = r"C:\Users\Rohan\OneDrive\Desktop\ir\Wildcard-Query-Search-Engine\proj\dataset"

ps = PorterStemmer()
tokens={}
filename={}
for root, dirs, files in os.walk(path):
    for file in files:
        filename[documentID+1]=file
        with open(os.path.join(path, file), encoding="utf-8",errors="ignore") as f:
                documentID += 1
                line_tokens = []
                print(documentID)
               
                for line in f:
                    print(line)
                    line_tokens = line.split()
                    for each in line_tokens:
                        if each not in stop_words:
                            curr_word=""
                            for x in each:
                                if x.isalnum():
                                    curr_word+=x
                            docs[documentID]+=' '+curr_word   

                            if curr_word not in tokens:
                                tokens[curr_word] = [documentID]
                            else:
                                tokens[curr_word].append(documentID)
def rotate(str, n):
    return str[n:] + str[:n]

keys = tokens.keys()
for key in sorted(keys):
    dkey = key + "$"
    for i in range(len(dkey),0,-1):
        out = rotate(dkey,i)

class TrieNode:
     
    # Trie node class
    def __init__(self):
        self.children = [None]*26
 
        # isEndOfWord is True if node represent the end of the word
        self.isEndOfWord = False
 
class Trie:
     
    # Trie data structure class
    def __init__(self):
        self.root = self.getNode()
 
    def getNode(self):
     
        # Returns new trie node (initialized to NULLs)
        return TrieNode()
 
    def _charToIndex(self,ch):
         
        # private helper function
        # Converts key current character into index
        # use only 'a' through 'z' and lower case
         
        return ord(ch)-ord('a')

    def insert(self,key):
         
        # If not present, inserts key into trie
        # If the key is prefix of trie node,
        # just marks leaf node
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
 
            # if current character is not present
            if not pCrawl.children[index]:
                pCrawl.children[index] = self.getNode()
            pCrawl = pCrawl.children[index]
 
        # mark last node as leaf
        pCrawl.isEndOfWord = True
 
    def search(self, key):
         
        # Search key in the trie
        # Returns true if key presents
        # in trie, else false
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            if not pCrawl.children[index]:
                return False
            pCrawl = pCrawl.children[index]
 
        return pCrawl.isEndOfWord
def parse_args():
    parser = argparse.ArgumentParser(description='Information Retrieval System Configuration')
    return parser.parse_args()

def hashFunc(s):
    ans= hash(s)
    ans=ans%1003#1003 is some primenumber
    # print(ans)
    return ans
hm={}#hashmap for preprocessing
def preprocessHash():
    for x in tokens:
        if hashFunc(x) not in hm:
            hm[hashFunc(x)]=[x]
        else:
            hm[hashFunc(x)].append(x)
        
def main():
    args = parse_args()
    ir = IRSystem(docs, stop_words=stop_words)
    preprocessHash()
    while True:
        query = input('Enter boolean query: ')
        for x in query:
            if(x=='*'):
                wildcard(query)
        start = timeit.default_timer()
        nquery=editDistQuery(query)
        print(query)
        print(nquery)
        query=input('ENTER THE CORRECTED INPUT: ')
        results = ir.process_query(query)
    
        stop = timeit.default_timer()

        if results is not None:
            print ('Processing time: {:.5} secs'.format(stop - start))
            print('\nDoc IDS: ')
            li=[]
            for x in results:
                # print(type(x))
                filename.get(x-1)
                li.append(x)
            print(li) 
            # print(filename)   
      
def editDistQuery(query):
    finalQuery=""
    words=query.split()
    
    
    # for word in words:
    #     if hm.get(hashFunc(x)) is not None:
    #         for k in hm.get(hashFunc(x)):
    #             value=editDistDP(k,word,len(k),len(word))
    #             if(value<ans_val):
    #                 ans_val=value
    #                 finalWord=k
    #     finalQuery+=' '+finalWord
    # return finalQuery   
    for word in words:
        ans_val=100000000000000
        finalWord=""
        if(word=="AND" or word=="OR" or word=="NOT" or tokens.get(word) is not None):
            finalQuery=finalQuery+word+" "
            continue
        for k in tokens.keys():
            if(k==word):
                print("hellow")
            value=editDistDP(k,word,len(k),len(word))
            if(value<ans_val):
                ans_val=value
                finalWord=k
        finalQuery=finalQuery+finalWord+" "
    # finalQuery.strip()
    
    return finalQuery   
 
def editDistDP(str1, str2, m, n):
    # Create a table to store results of subproblems
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]
 
    # Fill d[][] in bottom up manner
    for i in range(m + 1):
        for j in range(n + 1):
 
            # If first string is empty, only option is to
            # insert all characters of second string
            if i == 0:
                dp[i][j] = j    # Min. operations = j
 
            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i    # Min. operations = i
 
            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
 
            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                   dp[i-1][j],        # Remove
                                   dp[i-1][j-1])    # Replace
 
    return dp[m][n]
 
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print('EXIT')


