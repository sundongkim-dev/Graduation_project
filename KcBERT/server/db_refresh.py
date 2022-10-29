from pymongo import MongoClient

import os, torch, time, datetime, json, re
import numpy as np
import traceback
import app_kcbert

def refresh_db(host, port, C):
    ''' DB 데이터 유효성 확인 후 포맷에 맞게 변경하는 함수이다.
    Args:
        host: 서버 호스트
        port: 서버 포트
        C: 커뮤니티의 이름(문자열), 해당 DB 접속 위함
    
    Returns:
        None        
    '''
    # 모델 로드
    try:
        base_dir = os.getcwd()
        #load kcbert model & tokenizer - 서버에서 먼저 실행해야 현재 작업 디렉터리 올바르게 됨, 서버 먼저 실행안하면 오류 발생!
        model_path = base_dir + '/model/kcbert-model.pth'
        model = torch.load(model_path, map_location=torch.device('cpu'))
        model.eval()
        tokenizer_path = base_dir + '/model/kcbert-tokenizer.pth' 
        tokenizer = torch.load(tokenizer_path)
    except Exception as e:
        print(traceback.format_exc())
    finally:
        print('db_refresh: model loaded')

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
            
            # 댓글들 포맷팅
            for item2 in item['comments']:
                if item2['message'] == "[삭제된 댓글입니다.]": # 삭제된 것은 넘어가기
                    continue
                
                # result, precision 채워 넣기
                if "result" not in item2:
                    S = item2['message']
                    res = app_kcbert.testModel(model, S)
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
    community_list = ["fmkorea"]
    for item in community_list:
        refresh_db('localhost', 27017, item)