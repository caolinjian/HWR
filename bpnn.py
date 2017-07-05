import math
import random
import os
from flask import Flask, jsonify, request, redirect, url_for, render_template, flash
import json

def img2vector(filename):
    returnVect = []
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect.append(int(lineStr[j]))
    return returnVect

def num2vector(number, max):
    returnVect = []
    for i in range(max):
        if i == number:
            returnVect.append(1)
        else :
            returnVect.append(0)
    return returnVect

def vector2num(vec):
    max = 0.0
    maxi = 0
    for i in range(len(vec)):
        if vec[i] > max:
            max = vec[i]
            maxi = i
    return maxi

random.seed(0)


def rand(a, b):
    return (b - a) * random.random() + a


def make_matrix(m, n, fill=0.0):
    mat = []
    for i in range(m):
        mat.append([fill] * n)
    return mat


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


class BPNeuralNetwork:
    def __init__(self):
        self.input_n = 0
        self.hidden_n = 0
        self.output_n = 0
        self.input_cells = []
        self.hidden_cells = []
        self.output_cells = []
        self.input_weights = []
        self.output_weights = []
        self.input_correction = []
        self.output_correction = []

    def save(self, filename):
        data = {
            "input_n": self.input_n,
            "hidden_n": self.hidden_n,
            "output_n": self.output_n,
            "input_weights": self.input_weights,
            "output_weights": self.output_weights,
            "input_correction": self.input_correction,
            "output_correction": self.output_correction
        }
        with open(filename, 'w') as json_file:
            json_file.write(json.dumps(data))
        return
        
    def load(self, filename):
        with open(filename) as json_file:
            data = json.load(json_file)
            ni = data["input_n"] - 1
            nh = data["hidden_n"]
            no = data["output_n"]
            self.setup(ni, nh, no)
            self.input_weights = data["input_weights"]
            self.output_weights = data["output_weights"]
            self.input_correction = data["input_correction"]
            self.output_correction = data["output_correction"]
        return

    def setup(self, ni, nh, no):
        self.input_n = ni + 1
        self.hidden_n = nh
        self.output_n = no
        # init cells
        self.input_cells = [1.0] * self.input_n
        self.hidden_cells = [1.0] * self.hidden_n
        self.output_cells = [1.0] * self.output_n
        # init weights
        self.input_weights = make_matrix(self.input_n, self.hidden_n)
        self.output_weights = make_matrix(self.hidden_n, self.output_n)
        # random activate
        for i in range(self.input_n):
            for h in range(self.hidden_n):
                self.input_weights[i][h] = rand(-0.2, 0.2)
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                self.output_weights[h][o] = rand(-2.0, 2.0)
        # init correction matrix
        self.input_correction = make_matrix(self.input_n, self.hidden_n)
        self.output_correction = make_matrix(self.hidden_n, self.output_n)

    def predict(self, inputs):
        # activate input layer
        for i in range(self.input_n - 1):
            self.input_cells[i] = inputs[i]
        # activate hidden layer
        for j in range(self.hidden_n):
            total = 0.0
            for i in range(self.input_n):
                total += self.input_cells[i] * self.input_weights[i][j]
            self.hidden_cells[j] = sigmoid(total)
        # activate output layer
        for k in range(self.output_n):
            total = 0.0
            for j in range(self.hidden_n):
                total += self.hidden_cells[j] * self.output_weights[j][k]
            self.output_cells[k] = sigmoid(total)
        return self.output_cells[:]

    def back_propagate(self, case, label, learn, correct):
        # feed forward
        self.predict(case)
        # get output layer error
        output_deltas = [0.0] * self.output_n
        for o in range(self.output_n):
            error = label[o] - self.output_cells[o]
            output_deltas[o] = sigmoid_derivative(self.output_cells[o]) * error
        # get hidden layer error
        hidden_deltas = [0.0] * self.hidden_n
        for h in range(self.hidden_n):
            error = 0.0
            for o in range(self.output_n):
                error += output_deltas[o] * self.output_weights[h][o]
            hidden_deltas[h] = sigmoid_derivative(self.hidden_cells[h]) * error
        # update output weights
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                change = output_deltas[o] * self.hidden_cells[h]
                self.output_weights[h][o] += learn * change + correct * self.output_correction[h][o]
                self.output_correction[h][o] = change
        # update input weights
        for i in range(self.input_n):
            for h in range(self.hidden_n):
                change = hidden_deltas[h] * self.input_cells[i]
                self.input_weights[i][h] += learn * change + correct * self.input_correction[i][h]
                self.input_correction[i][h] = change
        # get global error
        error = 0.0
        for o in range(len(label)):
            error += 0.5 * (label[o] - self.output_cells[o]) ** 2
        return error

    def train(self, cases, labels, limit=10000, learn=0.05, correct=0.1):
        for j in range(limit):
            print(j)
            error = 0.0
            for i in range(len(cases)):
                label = labels[i]
                case = cases[i]
                error += self.back_propagate(case, label, learn, correct)

    def test(self):
        savefile = "bpnn10000.json"
        if os.path.exists(savefile) == False:
            cases = []
            labels = []
            trainingFileList = os.listdir('trainingDigits')
            m = len(trainingFileList)
            for i in range(m):
                fileNameStr = trainingFileList[i]
                fileStr = fileNameStr.split('.')[0]     #take off .txt
                classNumStr = int(fileStr.split('_')[0])
                labels.append(num2vector(int(classNumStr), 10))
                cases.append(img2vector('trainingDigits/%s' % fileNameStr))

            self.setup(1023, 5, 10)
            self.train(cases, labels, 10000, 0.05, 0.1)
            for case in cases:
                print(self.predict(case))
            self.save(savefile)
        else :
            self.load(savefile)

nn = BPNeuralNetwork()
nn.test()

app = Flask(__name__,static_folder='dist/static',template_folder='dist')
app.config.from_object(__name__)
@app.route('/recognition',methods=['POST'])
def recognition():
    data = request.get_json()['data']
    testData =  []
    for i in range(32):
        lineArr = data[i]
        for j in range(32):
            testData.append(lineArr[j])

    vec = nn.predict(testData)
    print vec
    return jsonify({'test': vector2num(vec)})

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()