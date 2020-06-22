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
lastWordIndex = -1
indexesG = -1  # Current index value of sorted index
group = []
prePOS = ''
result = ''    # Final Results


# If a word has multiple POS
def WordPOSTraversal(words):
  global prePOS  
  # words = word[loopIndex][indexes]
  wordMatrix = dic[words[indexesG]]
  if len(wordMatrix) == 12:
    CompMatrices(wordMatrix,words)
  else:
    for target_list in wordMatrix:
      return CompMatrices(target_list, words)

def CompMatrices(wordMatrix, words):
  global prePOS
  global result
  wordMatrix = np.array(wordMatrix)
  prePOSMatrix = np.array(rules[prePOS])
  truth = (wordMatrix == prePOSMatrix).any()
  posStr = ','.join([str(x) for x in wordMatrix])
  prePOS = POS[posStr]
  # print(lastWordIndex != indexesG)
  # print(prePOS)
  if truth:       # If POS is satisfied and the last word is not reached 
    # CompMatrices(wordMatrix, words)
    # print(indexesG)
    result = result + '\\' + words[indexesG] + prePOS

def DicTraversal(seg_index_list):
 global prePOS
 global indexesG
 global group
 for indexes in seg_index_list:
    if indexesG != indexes:
      for i in range(0,len(word)):
        indexesG = indexes        # Remove duplicate calls
        if word[i].__contains__(indexesG):
          if indexesG == 0:
            prePOS = 'START'
          WordPOSTraversal(word[i])   #////

# Split the same index into array
def group_by_element(lst):
    index = []
    for i, _ in enumerate(lst):
        if i < len(lst) - 1 and lst[i + 1] != lst[i]:
            index.append(i + 1)

    def take(lst, n):
        for i in range(n):
            yield next(lst)

    if not hasattr(lst, 'next'):
        lst = iter(lst)

    begin = 0
    for item in index:
        x = list(take(lst, item - begin ))
        begin = item
        yield x

    yield list(lst)
    
# search word in dic & sort word of sentense
def SearchDic():
  global group
  global lastWordIndex
  for i in range(0,len(keys)):
    wordIndex = sentense.find(keys[i])
    if wordIndex != -1 or wordIndex != '-1':
      seg_index_list.append(wordIndex)
      word.append({wordIndex : sentense[wordIndex : wordIndex + len(keys[i])]})
  seg_index_list.sort()# sort word index
  group = group_by_element(seg_index_list)
  lastWordIndex = seg_index_list[len(seg_index_list) - 1]
  DicTraversal(seg_index_list)
  print(result)

SearchDic()