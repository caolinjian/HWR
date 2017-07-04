# all the imports
from flask import Flask, jsonify, request, redirect, url_for, render_template, flash
from numpy import *
import operator
from os import listdir

# configuration
DEBUG = True
SECRET_KEY = 'development key'

# create our little application :)
app = Flask(__name__,static_folder='dist/static',template_folder='dist')
app.config.from_object(__name__)

def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j]=int(lineStr[j])
    return returnVect

hwLabels = []
trainingFileList = listdir('trainingDigits')
m = len(trainingFileList)
trainingMat = zeros((m,1024))
for i in range(m):
    fileNameStr = trainingFileList[i]
    fileStr = fileNameStr.split('.')[0]     #take off .txt
    classNumStr = int(fileStr.split('_')[0])
    hwLabels.append(classNumStr)
    trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)

app.config['hwLabels'] = hwLabels
app.config['trainingMat'] = trainingMat

def classify0(inX,dataSet,labels,k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX,(dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0)+1
    # print classCount
    sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    print sortedClassCount
    return sortedClassCount[0][0]



@app.route('/recognition',methods=['POST'])
def recognition():
    data = request.get_json()['data']
    testData =  zeros((1,1024))
    for i in range(32):
        lineArr = data[i]
        for j in range(32):
            testData[0,32*i+j]=lineArr[j]

    return jsonify({'test': classify0(testData, app.config['trainingMat'], app.config['hwLabels'], 5)})

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run()
