from pymongo import MongoClient

import os, torch, time, datetime, json, re
import numpy as np
import traceback
from app_kcbert import testModel

base_dir = os.getcwd()

#load kcbert model & tokenizer - 서버에서 먼저 실행해야 현재 작업 디렉터리 올바르게 됨, 서버 먼저 실행안하면 오류 발생!
model_path = base_dir + '/model/kcbert-model.pth'
model = torch.load(model_path, map_location=torch.device('cpu'))
model.eval()
tokenizer_path = base_dir + '/model/kcbert-tokenizer.pth' 
tokenizer = torch.load(tokenizer_path)

host = 'localhost'
port = 27017

def is_valid_format_date(_date):
    regex = r'\d{2}/\d{2}/\d{2}\s\d{2}:\d{2}'
    return bool(re.match(regex, _date))

def modify_date(_date):
    # 공백
    if len(_date) == 0: # 삭제된 건 아예 크롤링 안하는 방향으로..?
        pass
    # n분 전
    elif _date[-1] == '전':
        minutes = int(_date[:-3])
        n_minutes_before = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
        n_minutes_before = n_minutes_before.strftime("%y/%m/%d %H:%M")
        _date = n_minutes_before
    # 10/17 19:39
    elif len(_date) == len("10/17 19:39"):
        _date = datetime.datetime.today().strftime("%y/%m/%d %H:%M")[:3] + _date
    else:
        pass
    return _date

# date, time 태그의 형태 예제
# 삭제로 인한 공백 / n분 전 / # 10/17 19:39 / 21/12/12 19:39 등이 있다.
# 과거 데이터에 따라 22/10/18 19:39 같은 포맷으로 변환해야 한다.
# TODAY = datetime.datetime.today().strftime("%y/%m/%d %H:%M")

def refresh_db(C):
    ''' DB 데이터 유효성 확인 후 포맷에 맞게 변경하는 함수이다.
    Args:
        C: 커뮤니티의 이름(문자열), DB 접속 위함
    
    Returns:
        None        
    '''
    try:
        client = MongoClient(host=host, port=port) # 추후 서버 띄우면 아이피 및 포트 변경
        db = client["community_database"]
        collection = db[C]

        # DB에서 모든 document 꺼내오기
        post_list = list(collection.find({}))
        for item in post_list:
            pid = item['_id']
            modified_flag = False # 수정 있었다면 반영해서 최신화
            hate_flag = False     # 혐오 표현이라면 True
            abuse_flag = False    # 욕설 표현이라면 True
            clean_flag = False    # 클린 표현이라면 True

            # 게시글 날짜 포맷팅
            if not is_valid_format_date(item['date']): # 21/12/12 19:39
                item['date'] = modify_date(item['date'])
                modified_flag = True
            
            # 댓글들 포맷팅
            for item2 in item['comments']:
                if item2['username'] == "(삭제)": # 삭제된 것은 넘어가기
                    continue
                
                # 날짜 포맷팅
                if not is_valid_format_date(item2['time']):
                    item2['time'] = modify_date(item2['time'])
                    modified_flag = True
                
                # result, precision 채워 넣기
                if "result" not in item2:
                    S = item2['message']
                    res = testModel(model, S)
                    result = res["maxClass"]
                    precision = res["reliability"]

                    if result == 'clean':
                        clean_flag = True
                    elif result == 'curse':
                        abuse_flag = True
                    else:
                        hate_flag = True
                    item2['result'] = result
                    item2['precision'] = precision
                    modified_flag = True

            if hate_flag or abuse_flag:
                item['tags'] = 1
            else:
                item['tags'] = 0
            
            # 수정 있었다면 DB에 반영
            if modified_flag:
                collection.replace_one({'_id':pid}, item)

    except Exception as e:
        print(traceback.format_exc())
    finally:
        client.close()
        print('DB connection closed')


if __name__=="__main__":
    # Start DB refresh
    community_list = ["everytime"]
    for item in community_list:
        refresh_db(item)