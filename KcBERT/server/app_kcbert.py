from flask import Flask, jsonify, render_template, request, url_for, make_response
from pymongo import MongoClient

import os, torch, time, datetime, json
import numpy as np

os.chdir('..')
base_dir = os.getcwd()

# load kcbert model
model_path = base_dir + '/model/kcbert-model.pth'
model = torch.load(model_path, map_location=torch.device('cpu'))
model.eval()

# load kcbert tokenizer
tokenizer_path = base_dir + '/model/kcbert-tokenizer.pth' 
tokenizer = torch.load(tokenizer_path)

# DB 연결
client = MongoClient('127.0.0.1', 27017) # 127.0.0.1: localhost IP / 27017: 포트 번호 
db = client.everytime_database           # 연결하고자 하는 데이터베이스
collection = db.post_collection          # 연결하고자 하는 컬렉션 이름
print(collection)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
@app.route('/') 
def index(string=None):
    return render_template('demo.html', string=string)

@app.route('/stat')
def stat(string=None):
    return render_template('statistics.html', string=string)

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

@app.route('/statistics', methods=['POST', 'GET'])
def statistics():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        post_list = list(collection.find({}, {'_id':False}))
        return jsonify({'data': post_list})

if __name__ == "__main__":
    app.run()