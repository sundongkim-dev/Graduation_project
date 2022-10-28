'''
1. 크롤링한 결과의 mongoDB에 저장하는 코드 -> 추후 서버에서 자동화(insert 및 refresh) 예정
2. 크롤링 직후의 JSON object 양식
3. 모델에 돌리고 난 후 refresh된 JSON object 양식
'''
from pymongo import MongoClient
import datetime, traceback

def insertDocuments(host, port, C, objectList):
    try:
        client = MongoClient(host=host, port=port) # 추후 서버 띄우면 아이피 및 포트 변경
        db = client["community_database"]
        collection = db[C]
        collection.insert_many(objectList)
    except Exception as e:
        print(traceback.format_exc())
    finally:
        client.close()
        print('DB connection closed')

''' 
크롤링 직후의 JSON object 양식
document1 = {
    _id: POST_ID, # '_id'는 db에 insert할 때 자동 생성
    board: POST_BOARD,
    title: POST_TITLE,
    content: POST_CONTENT,
    username: POST_WRITER,
    date: POST_DATE,
    comments: [
        { 
            username: COMMENT_WRITER,
            message: COMMENT_MESSAGE,
            time: COMMENT_DATE,
        },
        { 
            username: COMMENT_WRITER,
            mesage: COMMENT_MESSAGE,
            time: COMMENT_TIME
        },
    ]
}

모델에 돌리고 난 후 refresh된 JSON object 양식
document1 = {
    _id: POST_ID, 
    board: POST_BOARD,
    title: POST_TITLE,
    content: POST_CONTENT,
    username: POST_WRITER,
    date: POST_DATE,
    comments: [
        { 
            username: COMMENT_WRITER,
            message: COMMENT_MESSAGE,
            time: COMMENT_DATE,
            result: COMMENT_RESULT,
            precision: RESULT_PRECISION
        },
    ]
    tags: POST_TAGS
}
'''