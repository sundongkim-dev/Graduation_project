from flask import Flask, jsonify, render_template, request, url_for, redirect, make_response
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler # pip install APScheduler
import atexit

import os, torch, time, datetime, json
import numpy as np

import db_query

os.chdir('..')
base_dir = os.getcwd()

# load kcbert model
model_path = base_dir + '/model/kcbert-model.pth'
model = torch.load(model_path, map_location=torch.device('cpu'))
model.eval()

# load kcbert tokenizer
tokenizer_path = base_dir + '/model/kcbert-tokenizer.pth' 
tokenizer = torch.load(tokenizer_path)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

sched = BackgroundScheduler()

@sched.scheduled_job('interval', seconds=300, id='test_1')
def macro():
    def doCrawl():
        print('Crawling 종료'); print('-----------')
        pass
    def doInsert():
        print('DB insert 종료'); print('-----------')
        pass
    def doRefresh():
        print('DB refresh 종료'); print('-----------')
        pass
    print(f'매크로 시작 : {time.strftime("%H:%M:%S")}')
    docrawl()
    doInsert()
    doRefresh()
    print(f'매크로 종료 : {time.strftime("%H:%M:%S")}')

print('sched before~')
sched.start()
print('sched after~')
atexit.register(lambda: sched.shutdown())


@app.route('/')
def index():
    return redirect(url_for('introduce'))

@app.route('/introduce') 
def introduce(string=None):
    return render_template('introduce.html', string=string)

@app.route('/demo') 
def demo(string=None):
    return render_template('demo.html', string=string)

@app.route('/stat')
def stat(string=None):
    return render_template('statistics.html', string=string)

@app.route('/analysis')
def analysis(string=None):
    return render_template('analysis.html', string=string)

@app.route('/predict/<sentence>', methods=['POST', 'GET'])
def predict(sentence):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        print(testModel(model, sentence))
        return jsonify(testModel(model, sentence))

@app.route('/graphdata/<community>/<type>')
def graphdata(community, type):
    yy = request.args.get('yy')
    mm = request.args.get('mm')
    dd = request.args.get('dd')
    
    if type == 'dailypost':
        return jsonify(db_query.getMonthlyOrDailyPosts(community, yy, mm, dd))
    elif type == 'dailycomment':
        return jsonify(db_query.getMonthlyOrDailyComments(community, yy, mm, dd))
    elif type == 'dailyhourlystat':
        return jsonify(db_query.getDailyOrHourlyHatePostsNComments(community, yy, mm, dd))
    elif type == 'monthlypost':
        return jsonify(db_query.getMonthlyOrDailyPosts(community, yy, mm))
    elif type == 'monthlycomment':
        return jsonify(db_query.getMonthlyOrDailyComments(community, yy, mm))
    elif type == 'monthlydailystat':
        return jsonify(db_query.getDailyOrHourlyHatePostsNComments(community, yy, mm))
    else:
        return jsonify({'data':[]})

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

    # print("문장의 카테고리는:", classes[idx])
    # print("신뢰도는:", "{:2f}%".format(scores[idx]))
    # print("Time elapsed:", time.time()-test_start)

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