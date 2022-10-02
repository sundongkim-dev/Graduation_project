from flask import Flask, jsonify, render_template, request, url_for

from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model

from MyModel import *

from kobert_tokenizer import KoBERTTokenizer

import gluonnlp as nlp
import torch
import numpy as np
import time


# load fine-tuned model
base_dir = os.getcwd()
model_dir = '/model_output' # change as you want
model_location = base_dir + model_dir
model = BertForSequenceClassification.from_pretrained(model_location)
tokenizer = KoBERTTokenizer.from_pretrained(model_name)

app = Flask(__name__)

@app.route('/')
def index(string=None):
    return render_template('submit.html', string=string)


@app.route('/predict', methods=['POST', 'GET'])
def predict(string=None):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        temp = request.args.get('string')
        testModel(model, temp)
        return render_template('submit.html', string=temp)

    #return jsonify({'class_id': 'IMAGE_NET_XXX', 'class_name': 'Cat'})

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

    model.eval()
    inputs = tokenizer(seq, return_tensors='pt')
    outputs = model(**inputs)
    scores = torch.sigmoid(outputs['logits']).squeeze()
    idx = scores.argmax() # probability(sigmoid) of each class

    print("문장의 카테고리는:", classes[idx])
    print("신뢰도는:", "{:2f}%".format(scores[idx]))
    print("Time elapsed:", time.time()-test_start)

