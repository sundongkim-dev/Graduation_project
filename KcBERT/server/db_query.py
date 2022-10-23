from pymongo import MongoClient
from bson.son import SON

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

# 1번 쿼리
def getDailyComment(yy, mm, dd):
    res = []
    _date = ".*" + str(yy) + "/" + str(mm).zfill(2) + "/" + str(dd).zfill(2) + ".*"
    
    # 전체 댓글 수 
    first_condition = [
        { 
            "$unwind": {
                "path": "$comments",
            }
        },
        {
            "$match" : {
                "comments.time": {"$regex": _date},
            },
        },
        {
            "$group": {
                '_id': 'null',
                "count": {"$sum": 1},
            }
        },
    ]
    first_condition_result = collection.aggregate(first_condition)
    for i in first_condition_result:
        res.append(i['count'])
    
    # 혐오, 악플 댓글 수
    first_specific_condition = [
        { 
            "$unwind": {
                "path": "$comments",
            }
        },
        {
            "$match" : {
                "comments.time": {"$regex": _date},
            },
        },
        {
            "$group": {
                '_id': '$comments.result',
                "count": {"$sum": 1},
            }
        },
    ]
    first_specific_condition_result = collection.aggregate(first_specific_condition)

    hate_dict = {'woman/family' : 0, 'man': 0, 'minority': 0, 'race/nationality': 0, 'age': 0, 'region': 0, 'religion': 0, 'extra': 0, 'curse': 0, 'clean': 0 }
    for i in first_specific_condition_result:
        hate_dict[i['_id']] = i['count']

    return res, hate_dict

# 2번 쿼리
def getHourlyComment(yy, mm, dd):
    res = []
    _date = ".*" + str(yy) + "/" + str(mm).zfill(2) + "/" + str(dd).zfill(2)
    # 전체 게시글 수
    first_condition = {"date": {'$regex': _date + ".*"}}
    first_condition_result = collection.count_documents(first_condition)
    res.append(first_condition_result)

    # 혐오 조장 게시글 수
    second_condition = [{"date": {'$regex': _date + ".*"}}, {"tags": 1}]
    second_condition_result = collection.count_documents({'$and': second_condition})
    res.append(second_condition_result)

    # 각 시간에 대한 수
    for hm in hhmm:
        second_specific_condition = [{"date": {'$regex': _date + " " + hm + ".*"}}, {"tags": 1}]
        second_specific_condition_result = collection.count_documents({'$and': second_specific_condition})   
        res.append(second_specific_condition_result)
    
    return res

# 3번 쿼리
def getMonthlyComment(yy, mm):
    # 특정 월 한 달 동안에 대한 전체 댓글/혐오 댓글/악플 댓글/전체 게시글/혐오 조장글 개수
    res = []
    _date = ".*" + str(yy) + "/" + str(mm).zfill(2) + ".*"
    # 전체 게시글
    zero_condition =  {"date": {'$regex': _date + ".*"}}
    zero_condition_result = collection.count_documents(zero_condition)
    res.append(zero_condition_result)

    # 전체 댓글
    first_condition = [
        { 
            "$unwind": {
                "path": "$comments",
            }
        },
        {
            "$match" : {
                "comments.time": {"$regex": _date},
            },
        },
        {
            "$group": {
                '_id': 'null',
                "count": {"$sum": 1},
            }
        },
    ]
    first_condition_result = collection.aggregate(first_condition)
    for i in first_condition_result:
        res.append(i['count'])
    
    # 혐오 댓글, 악플 댓글
    first_specific_condition = [
        { 
            "$unwind": {
                "path": "$comments",
            }
        },
        {
            "$match" : {
                "comments.time": {"$regex": _date},
            },
        },
        {
            "$group": {
                '_id': '$comments.result',
                "count": {"$sum": 1},
            }
        },
    ]
    first_specific_condition_result = collection.aggregate(first_specific_condition)
    hate_dict = {'woman/family' : 0, 'man': 0, 'minority': 0, 'race/nationality': 0, 'age': 0, 'region': 0, 'religion': 0, 'extra': 0, 'curse': 0, 'clean': 0 }
    for i in first_specific_condition_result:
        hate_dict[i['_id']] = i['count']
    
    # 혐오 조장글 개수
    second_condition = [{"date": {'$regex': _date + ".*"}}, {"tags": 1}]
    second_condition_result = collection.count_documents({'$and': second_condition})
    res.append(second_condition_result)

    return res, hate_dict

first_query_ans, first_query_hate_dict = getDailyComment(22, 10, 20)
second_query_ans = getHourlyComment(22, 10,20)
third_query_ans, third_query_hate_dict = getMonthlyComment(22, 10)

print(first_query_ans, first_query_hate_dict, second_query_ans)
print(third_query_ans, third_query_hate_dict)