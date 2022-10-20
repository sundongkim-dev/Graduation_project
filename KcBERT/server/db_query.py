from pymongo import MongoClient

# DB 연결
client = MongoClient('127.0.0.1', 27017) # 127.0.0.1: localhost IP / 27017: 포트 번호 
db = client.everytime_database           # 연결하고자 하는 데이터베이스
collection = db.post_collection          # 연결하고자 하는 컬렉션 이름


''' 구현해야할 쿼리 목록
1. 특정 날짜(yyyy년 mm월 dd일)에 대한 전체 댓글 수/혐오 댓글 수/악플 댓글 수


2. 특정 날짜(yyyy년 mm월 dd일)에 대한 전체 게시글 수/혐오 조장 게시글 수
+ 가능하다면 특정 날짜 특정 시간(ex. 13시~13시 59분)에 대한 항목도

3. 특정 월 한 달 동안에 대한 전체 댓글/혐오 댓글/악플 댓글/전체 게시글/혐오 조장글 개수
'''
hhmm = [str(x) if x > 9 else "0" + str(x) for x in range(24)]

# 2번 쿼리
def second_query(yy, mm, dd):
    # 전체 게시글 수 / 혐오 조장 게시글 수 / 각 시간에 대한 수
    res = []
    _date = ".*" + str(yy) + "/" + str(mm) + "/" + str(dd)
    
    first_condition = {"date": {'$regex': _date + ".*"}}
    first_condition_result = collection.count_documents(first_condition)
    res.append(first_condition_result)

    second_condition = [{"date": {'$regex': _date + ".*"}}, {"tags": 1}]
    second_condition_result = collection.count_documents({'$and': second_condition})
    res.append(second_condition_result)

    for hm in hhmm:
        second_specific_condition = [{"date": {'$regex': _date + " " + hm + ".*"}}, {"tags": 1}]
        # print(second_specific_condition)
        second_specific_condition_result = collection.count_documents({'$and': second_specific_condition})   
        res.append(second_specific_condition_result)
    
    return res
query_ans = second_query(22, 10, 18)