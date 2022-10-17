'''
1. mongoDB에 수동으로 저장하는 코드
2. document 양식 기록
'''

from pymongo import MongoClient
import datetime

client = MongoClient('127.0.0.1', 27017) # 127.0.0.1: localhost IP / 27017: 포트 번호 
db = client.everytime_database           # 생성하고자 하는 데이터베이스
collection = db.post_collection          # 생성하고자 하는 컬렉션 이름

document1 = {
    "board": "자유게시판",
    "title": "디논설 수업 시간에 팝콘 쳐먹지 마세요",
    "content": "개념이 없나?",
    "username": "익명",
    "tags": 1,
    "date": "2022-10-17",
    "time": "15:15",
    "comments": [
        { 
            "username": "익명1",
            "message": "팝콘 튀기는 중",
            "date": "2022-10-17",
            "time": "15:16",
            "result": 9,
            "precision": 88.5
        },
        { 
            "username": "익명2",
            "message": "ㄹㅇ? 그런 사람이 있다고??",
            "date": "2022-10-17",
            "time": "15:17",
            "result": 9,
            "precision": 87.6
        },
        { 
            "username": "익명2",
            "message": "컴공은 벌레들밖엔 없노",
            "date": "2022-10-17",
            "time": "16:20",
            "result": 8,
            "precision": 54
        }
    ]
}

document2 = {
    "board": "자유게시판",
    "title": "대학생 월세 빼고 용돈 얼마가 적절함?",
    "content": "나 90 받는데\n통신비, 인터넷, 교통비, 관리비만 해도\n30임...",
    "username": "익명",
    "tags": 0,
    "date": "2022-10-17",
    "time": "17:07",
    "comments": [
        { 
            "username": "익명1",
            "message": "교통비포함 통신비제외 40",
            "date": "2022-10-17",
            "time": "17:09",
            "result": 9,
            "precision": 91.5
        },
        { 
            "username": "익명2",
            "message": "알바를하던가 해라..",
            "date": "2022-10-17",
            "time": "17:10",
            "result": 9,
            "precision": 72
        }
    ]
}

DOCUMENTS = [document1, document2]
collection.insert_many(DOCUMENTS)


''' document 포맷
document_example = {
    "_id": POST_ID,                         # 게시글 id
    "board": POST_BOARD,                    # 게시판 이름
    "title": POST_TITLE,                    # 게시글 제목
    "content": POST_CONTENT,                # 게시글 내용
    "username": POST_WRITER,                # 게시글 작성자
    "tags": POST_RESULT,                    # 혐오 조장 게시글 결과 여부: 0, 1
    "date": POST_DATE,                      # 게시글 작성 날짜
    "time": POST_TIME,                      # 게시글 작성 시간
    "comments": [
        { 
            "username": COMMENT_WRITER,     # 댓글 작성자 이름
            "message": COMMENT_MESSAGE,      # 댓글 내용
            "date": COMMENT_DATE,           # 댓글 작성 날짜
            "time": COMMENT_TIME,           # 댓글 작성 시간
            "result": COMMENT_RESULT,       # 댓글 분류 결과: 0 ~ 9
            "precision": COMMENT_PRECISION  # 댓글 분류 신뢰도
        },
        { 
            "username": COMMENT_WRITER,
            "message": COMMENT_MESSAGE,
            "date": COMMENT_DATE,
            "time": COMMENT_TIME,
            "result": COMMENT_RESULT,
            "precision": COMMENT_PRECISION
        }
    ]
}
'''