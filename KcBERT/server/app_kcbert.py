from flask import Flask, jsonify, render_template, request, url_for, redirect, make_response
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler # pip install APScheduler
import atexit

import os, torch, time, datetime, json
import numpy as np

import db_query
import fmkorea_crawling
import db_insert
import db_refresh

# 작업 디렉터리 설정
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

@sched.scheduled_job('interval', seconds=300, id='db')
def macro():
    os.chdir('server')
    print(f'매크로 시작 : {time.strftime("%H:%M:%S")}')
    res = fmkorea_crawling.crawling()
    print('Crawling 종료'); print('-----------')

    db_insert.insertDocuments('localhost', 27017, 'fmkorea', res)
    print('DB insert 종료'); print('-----------')

    os.chdir('..')
    db_refresh.refresh_db('localhost', 27017, 'fmkorea')

    print('DB refresh 종료'); print('-----------')
    print(f'매크로 종료 : {time.strftime("%H:%M:%S")}')

sched.start()                             # 스케쥴러 시작
atexit.register(lambda: sched.shutdown()) # 서버 종료시 스케쥴러 내리기

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
    max_len = 256
    seq = seq[:max_len]
    # 'individual' excluded
    classes = np.array(['woman/family', 'man', 'minority', 'race/nationality', 'age', 'region', 'religion', 'extra', 'curse', 'clean'])
    # classes = np.array(["여성/가족","남성","성소수자","인종/국적","연령","지역","종교","기타 혐오","악플/욕설","clean"])

    inputs = tokenizer(seq, return_tensors='pt')
    outputs = model(**inputs)
    scores = torch.sigmoid(outputs['logits']).squeeze()
    idx = scores.argmax() # probability(sigmoid) of each class

    return {"scores": scores.tolist(), "classes": classes.tolist(), "maxClass": classes[idx], "reliability": "{:2f}".format(scores[idx])}

@app.route('/statistics')
def statistics():
    community = request.args.get('community')
    if not community:
        community = "fmkorea"
    return jsonify({"data": db_query.getNPosts(community)})


if __name__ == "__main__":
    app.run()