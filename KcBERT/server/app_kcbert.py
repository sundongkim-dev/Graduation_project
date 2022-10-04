from flask import Flask, jsonify, render_template, request, url_for

#from MyModel import *
import os

import torch
import numpy as np
import time


base_dir = os.getcwd()

# load kcbert model
model_path = base_dir + '/model_output/kcbert-model.pth'
model = torch.load(model_path)
model.to('cpu')
model.eval()

# load kcbert tokenizer
tokenizer_path = base_dir + '/model_output/kcbert-tokenizer.pth' 
tokenizer = torch.load(tokenizer_path)


app = Flask(__name__)

@app.route('/')
def index(string=None):
    return render_template('demo.html', string=string)


@app.route('/predict/<sentence>', methods=['POST', 'GET'])
def predict(sentence):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        print(testModel(model, sentence))
        return jsonify(testModel(model, sentence))

# Test model one by one
def softmax(vals, idx):
    valscpu = vals.cpu().detach().squeeze(0)
    a = 0
    for i in valscpu:
        a += np.exp(i)
    return ((np.exp(valscpu[idx]))/a).item() * 100

def testModel(model, seq):
    test_start = time.time()
    max_len = 64

    # 'individual' excluded
    classes = np.array(['woman/family', 'man', 'minority', 'race/nationality', 'age', 'region', 'religion', 'extra', 'curse', 'clean'])
    # classes = np.array(["여성/가족","남성","성소수자","인종/국적","연령","지역","종교","기타 혐오","악플/욕설","clean"])

    inputs = tokenizer(seq, return_tensors='pt')
    outputs = model(**inputs)
    scores = torch.sigmoid(outputs['logits']).squeeze()
    idx = scores.argmax() # probability(sigmoid) of each class

    print("문장의 카테고리는:", classes[idx])
    print("신뢰도는:", "{:2f}%".format(scores[idx]))
    print("Time elapsed:", time.time()-test_start)

    return {"scores": scores.tolist(), "classes": classes.tolist(), "maxClass": classes[idx], "reliability": "{:2f}".format(scores[idx])}

if __name__ == "__main__":
    app.run()