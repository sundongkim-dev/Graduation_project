from flask import Flask, jsonify, render_template, request, url_for

from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model

from MyModel import *

import gluonnlp as nlp
import torch
import numpy as np


tokenizer = get_tokenizer()
bertmodel, vocab = get_pytorch_kobert_model()
model = BERTClassifier(bertmodel, dr_rate=0.5)
dict_model = torch.load('model.pth', map_location=torch.device('cpu'))
model.load_state_dict(dict_model['model'], strict=False)
device = torch.device('cpu')

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
    max_len = 64
    classes = ["not clean", "clean"]
    tmp = [seq]

    tokenizer = get_tokenizer()
    tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)
    transform = nlp.data.BERTSentenceTransform(tok, max_len, pad=True, pair=False)
    tokenized = transform(tmp)

    model.eval()
    result = model(torch.tensor([tokenized[0]]).to(device), [tokenized[1]], torch.tensor(tokenized[2]).to(device))
    idx = result.argmax().cpu().item()
    print("문장의 카테고리는:", classes[idx])
    print("신뢰도는:", "{:2f}%".format(softmax(result, idx)))

