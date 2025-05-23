import random
import pandas as pd
import math

class exNode:
  def __init__(self, value):
    self.value = value
    self.size = len(value)

class inNode(exNode):
  def __init__(self, value, left, right, splitAtt, splitValue):
    super().__init__(value)
    self.left = left
    self.right = right
    self.splitAtt = splitAtt
    self.splitValue = splitValue

def iTree(data, currentHeight, heightLimit):
  if (currentHeight >= heightLimit or len(data) <= 1):
    return exNode(data)
  else:
    xleft = []
    xright = []
    splitColumn = random.randint(0, len(data[0])-1)
    splitVal = random.uniform(findMin(data, splitColumn), findMax(data, splitColumn))
    for i in range(0, len(data)):
      if(filter(data=data, column=splitColumn, row=i, splitVal=splitVal)):
        xright.append(data[i])
      else:
        xleft.append(data[i])
    return inNode(value=data, left=iTree(xleft,currentHeight+1,heightLimit), right=iTree(xright,currentHeight+1,heightLimit), splitAtt=splitColumn, splitValue=splitVal)

def iForest(data, trees, psi ):
  forest = []
  heightLimit = math.ceil(math.log(psi, 2))
  for i in range(1, trees):
    sample = subSample(data=data, psi=psi)
    forest.append(iTree(data=sample, currentHeight=0, heightLimit=heightLimit))
  return forest

def pathLength(x, tree, currentPathLength):
  if isinstance(tree, inNode):
    attr = tree.splitAtt
    if(x[attr]<tree.splitValue):
      return pathLength(x, tree.left, currentPathLength+1)
    else:
      return pathLength(x, tree.right, currentPathLength+1)
  else:
    if(tree.size>1):
      return currentPathLength + unsuccessfulBstSearch(len(tree.value))
    else:
      return currentPathLength



def unsuccessfulBstSearch(n):
  return 2 * harmonicNumber(n-1) - (2 * (n-1)/n)

def harmonicNumber(n):
  return math.log(n) + 0.5772156649
def readData(filepath):
  df = pd.read_csv(filepath)
  arr = df.to_numpy()
  return arr

def findMax(data, column):
  max = data[0][column]
  for i in range(1,len(data)):
    if(data[i][column] > max):
      max = data[i][column]
  return max

def findMin(data, column):
  min = data[0][column]
  for i in range(1,len(data)):
    if(data[i][column] < min):
      min = data[i][column]
  return min

def filter(data, column, row, splitVal):
  if (data[row][column]>=splitVal):
    #true for if it is greater than split val
    return True
  else:
    return False

def anomalyScore(e, psi):
  return 2**(-1*(e/unsuccessfulBstSearch(psi)))

def subSample(data, psi):
  max = len(data)-1
  subSample = []
  i = random.randint(0, max)
  while(len(subSample) < psi):
    if(i==max):
      i=0
    subSample.append(data[i])
    i=i+1
  return subSample

def runTree(forest,psi,row):
  path = 0
  for i in range(0, len(forest)):
    path = path + pathLength(x=row, tree=forest[i], currentPathLength=0)
  averagepath = path / 100
  return (anomalyScore(averagepath, psi))

def createStats(data, psi,trees):
  forest = iForest(data=data, trees=trees, psi=psi)
  arr =[]
  avg = 0
  count = 0
  for i in range(0, len(data)):
    row = data[i]
    e = runTree(forest, psi, row)
    if(e>.65):
      count = count + 1
    arr.append(e)
    avg = avg + e
  print("Max: ", max(arr))
  print("Min: ", min(arr))
  print("Avg: ", avg/len(data))
  print("Count: ", count)
def runIForest(data, row, psi,trees):
  forest = iForest(data=data, trees=trees, psi=psi)

  return runTree(forest, psi, row)

def generateRandomInstance(data):
  arr = []
  for i in range(0, len(data[0])):
    arr.append(random.uniform(findMin(data, i), findMax(data, i)))
  return arr

def main():
  data = readData('creditcard.csv')
  randRow = data[random.randint(0, len(data))]
  outlier = [1.26400000e+03 , 1.11407064e+01, 9.61272620e+00 , 1.23895452e+01, 6.01334629e+00 , 3.20921290e+01 , 2.13930688e+01,  3.43031769e+01, 7.52078427e+00 , 1.92573155e+00 , 2.63662207e+00 , 3.70217663e+00, 1.84305632e+00,  2.42712334e+00 , 1.65283566e+00 , 3.63504152e+00, 4.08780179e+00 , 1.65489200e+00 , 8.88406461e-01,  7.52276373e-01, 1.17486890e+01 , 4.70997725e+00 , 1.36610997e+00 , 2.92588754e+00,8.43550804e-01 , 7.46267438e-01,  8.01386919e-01,  3.85204564e+00,4.15793357e+00,  7.71243000e+03,  0.00000000e+00]
  print("Random row: ", runIForest(data, randRow, 256, 100))
  print("Generated instance: ", runIForest(data, generateRandomInstance(data), 256, 100))
  print("Outlier: ", runIForest(data, outlier, 256, 100))
  createStats(data, 256, 100)



main()

