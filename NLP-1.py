import numpy as np

sentense = 'このひとことで元気になった'

dic = {'こ':[0,0,0,0,0,0,0,0,0,0,0,1],
    'この':[0,0,0,0,0,0,1,0,0,0,0,0],
    'こと':[0,0,1,0,0,0,0,0,0,0,0,0],
    'た':[0,0,0,0,0,0,0,1,0,0,0,0],
    'で':[[0,0,0,1,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,1,0,0,0]],
    'と':[[0,0,0,0,0,0,0,0,1,0,0,0], [0,0,0,0,0,0,0,0,0,1,0,0]],
    'な':[0,0,0,0,1,0,0,0,0,0,0,0],
    'に':[0,0,0,0,0,0,0,0,1,0,0,0],
    'にな':[0,0,0,0,0,1,0,0,0,0,0,0],
    'ひ':[0,1,0,0,0,0,0,0,0,0,0,0],
    'ひと':[0,1,0,0,0,0,0,0,0,0,0,0],
    'ひとこと':[0,1,0,0,0,0,0,0,0,0,0,0],
    'っ':[0,0,0,0,0,0,0,0,0,0,1,0],
    '元気':[0,0,0,0,0,0,0,0,0,0,0,1]
   }

POS = {
       '1,0,0,0,0,0,0,0,0,0,0,0': 'END',
       '0,1,0,0,0,0,0,0,0,0,0,0': 'CN',
       '0,0,1,0,0,0,0,0,0,0,0,0': 'FN',
       '0,0,0,1,0,0,0,0,0,0,0,0': 'V-1',
       '0,0,0,0,1,0,0,0,0,0,0,0': 'V-ra',
       '0,0,0,0,0,1,0,0,0,0,0,0': 'V-wa',
       '0,0,0,0,0,0,1,0,0,0,0,0': 'AdN',
       '0,0,0,0,0,0,0,1,0,0,0,0': 'Aux-V',
       '0,0,0,0,0,0,0,0,1,0,0,0': 'Case-P',
       '0,0,0,0,0,0,0,0,0,1,0,0': 'Conj-P',
       '0,0,0,0,0,0,0,0,0,0,1,0': 'EN',
       '0,0,0,0,0,0,0,0,0,0,0,1': 'Suf'
}

rules = {'START': [-1,1,-1,1,1,1,1,-1,-1,1,-1,-1],'CN': [1,1,1,1,1,1,-1,1,1,1,-1,1],
     'FN': [1,-1,-1,1,1,1,-1,1,1,1,-1,1],'V-1': [-1,-1,-1,-1,-1,-1,-1,1,-1,1,1,-1],
     'V-ra': [-1,-1,-1,-1,-1,-1,-1,1,-1,1,1,-1],'V-wa': [-1,-1,-1,-1,-1,-1,-1,1,-1,1,1,-1],
     'AdN': [-1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1], 'Aux-V': [1,1,1,1,1,1,1,1,-1,1,1,-1],
     'Case-P': [1,1,1,1,1,1,1,-1,1,1,-1,-1],'Conj-P': [1,1,1,1,1,1,1,1,-1,1,-1,-1],
     'EN': [1,1,1,1,1,1,1,1,-1,1,-1,-1],'Suf': [1,1,1,1,1,1,-1,-1,1,1,-1,1]}

keys = list(dic.keys())
seg_index_list = []  # indexes of Sentence-separated word
word = []   # Sentence-separated word
sortedWord = []   
temp = ''    # temporary index of Sentence-separated word
prePOS = ''
result = ''    # Final Results


# If a word has multiple POS
def WordPOSTraversal(indexes, words):
  global prePOS
  print(words)
  # words = word[loopIndex][indexes]
  wordMatrix = dic[words]
  print(wordMatrix)
  if len(wordMatrix) == 12:
    CompMatrices(wordMatrix,words, indexes)
  else:
    for target_list in wordMatrix:
      return CompMatrices(target_list, words, indexes)

def CompMatrices(wordMatrix, words, indexes):
  global prePOS
  global result
  wordMatrix = np.array(wordMatrix)
  prePOSMatrix = np.array(rules[prePOS])
  truth = (wordMatrix == prePOSMatrix).any()
  posStr = ','.join([str(x) for x in wordMatrix])
  prePOS = POS[posStr]
  if truth:
    CompMatrices(wordMatrix, words, indexes)
    result = result + '\\' + words
  # print(result)
  # print(prePOS)

def DicTraversal(seg_index_list):
 global prePOS
 global temp
 for indexes in seg_index_list:
    if temp != indexes:
      for i in range(0,len(word)):
        temp = indexes        # Remove duplicate calls
        if word[i].__contains__(indexes):
          if indexes == 0:
            prePOS = 'START'
          WordPOSTraversal(indexes, word[i])   #////
        # print(i)

# search word in dic & sort word of sentense
def SearchDic():
  for i in range(0,len(keys)):
    wordIndex = sentense.find(keys[i])
    if wordIndex != -1 or wordIndex != '-1':
      seg_index_list.append(wordIndex)
      word.append({wordIndex : sentense[wordIndex : wordIndex + len(keys[i])]})
  seg_index_list.sort()# sort word index
  DicTraversal(seg_index_list)

    
SearchDic()