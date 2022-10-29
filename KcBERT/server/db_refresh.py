from pymongo import MongoClient

import os, torch, time, datetime, json, re
import numpy as np
import traceback
import app_kcbert

def get_stat(host, port, C, percentage):
    try:
        hate = ['woman/family', 'man', 'minority', 'race/nationality', 'age', 'region', 'religion', 'extra', 'curse']
        li = []
        client = MongoClient(host=host, port=port) # 추후 서버 띄우면 아이피 및 포트 변경
        db = client["community_database"]
        collection = db[C]

        # DB에서 모든 document 꺼내오기
        post_list = list(collection.find({}))
        for asdf, item in enumerate(post_list):
            print(asdf)
            pid = item['_id']
            
            if len(item['comments']) == 0:
                continue

            total = len(item['comments'])
            num = 0
            
            for item2 in item['comments']:
                if item2['message'] == "[삭제된 댓글입니다.]": # 삭제된 것은 넘어가기
                    continue
                
                if item2['result'] in hate:
                    num += 1

            li.append(num/total)
        
        return li

    except Exception as e:
        print(traceback.format_exc())
    finally:
        client.close()
        print('DB connection closed')

def refresh_db(host, port, C):
    ''' DB 데이터 유효성 확인 후 포맷에 맞게 변경하는 함수이다.
    Args:
        host: 서버 호스트
        port: 서버 포트
        C: 커뮤니티의 이름(문자열), 해당 DB 접속 위함
    
    Returns:
        None        
    '''
    start = time.time()
    hate = ['woman/family', 'man', 'minority', 'race/nationality', 'age', 'region', 'religion', 'extra', 'curse']
    # 모델 로드
    try:
        base_dir = os.getcwd()
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
        for asdf, item in enumerate(post_list):
            print(asdf)
            pid = item['_id']
            
            # 태그가 달려있다면 수정할 필요 없음!
            if "tags" in item:
                continue
            
            # 태그가 없다면 수정 필요!
            # 댓글이 하나도 없다면, 게시글 content로 tag 판단
            if len(item['comments']) == 0:
                content_info = app_kcbert.testModel(model, item['content'])
                content_result = content_info["maxClass"]
                if content_result == 'clean':
                    item['tags'] = 0
                else:
                    item['tags'] = 1
            
            else:
                total = len(item['comments'])
                num = 0
                # 댓글들 있다면 분류 결과 및 신뢰도 등록! 분류 결과는 해당 게시글에서 혐오+악플이 20%넘어가면 분쟁글!
                for item2 in item['comments']:
                    if item2['message'] == "[삭제된 댓글입니다.]": # 삭제된 것은 넘어가기
                        continue
                    
                    # result, precision 채워 넣기
                    if "result" not in item2:
                        S = item2['message']
                        res = app_kcbert.testModel(model, S)
                        result = res["maxClass"]
                        precision = res["reliability"]

                        if result in hate:
                            num += 1

                        item2['result'] = result
                        item2['precision'] = precision

                if num/total >= 0.2:
                    item['tags'] = 1
                else:
                    item['tags'] = 0
            
            # DB에 반영
            collection.replace_one({'_id':pid}, item)

    except Exception as e:
        print(traceback.format_exc())
    finally:
        client.close()
        end = time.time()
        print(f"{end - start:.5f} sec")
        print('DB connection closed')


if __name__=="__main__":
    # Start DB refresh
    community_list = ["fmkorea"]
    for item in community_list:
        refresh_db('localhost', 27017, item)

    # res = get_stat('localhost', 27017, 'fmkorea', 15)
    # print(res)
    # print(sum(res)/len(res))