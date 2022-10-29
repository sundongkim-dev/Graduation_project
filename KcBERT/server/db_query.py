from pymongo import MongoClient

import traceback
 
host = 'localhost'
port = 27017

''' 구현해야할 쿼리 목록
C 커뮤니티의 
1. yy년 mm월의 cleanPost(정상 게시글), hatePost(혐오 게시글)의 수
2. yy년 mm월의 cleanComment(정상 댓글), curseComment(악플), hateComment(혐오 댓글)의 수
3. yy년 mm월의 날짜별 hatePost(혐오 게시글), hateComment(혐오+악플)의 수
4. yy년 mm월 DD일의 cleanPost(정상 게시글), hatePost(분쟁글)의 수
5. yy년 mm월 DD일의 cleanComment(정상 댓글), curseComment(악플), hateComment(혐오 댓글)의 수
6. yy년 mm월 DD일의 시간별 hatePost(혐오 게시글), hateComment(혐오+악플)의 수
'''

hhmm = [str(x) if x > 9 else "0" + str(x) for x in range(24)]
hate = ['woman/family', 'man', 'minority', 'race/nationality', 'age', 'region', 'religion', 'extra']

# 1번 쿼리, 4번 쿼리
def getMonthlyOrDailyPosts(C, yy, mm, dd=0):
    '''     
    Args:
        C: 커뮤니티의 이름(문자열), DB 접속 위함
        yy: 년 (정수형)
        mm: 월 (정수형)
        dd: 일 (정수형) if 0, monthly else daily로 조회
    
    Returns:
        C 커뮤니티의 yy년 mm월 (optional:dd일)의 cleanPost(정상 게시글, index=0), hatePost(혐오 게시글, index=1)의 수를 딕셔너리로 반환
    '''
    # DB 연결
    try:
        client = MongoClient(host=host, port=port) # 추후 서버 띄우면 아이피 및 포트 변경
        db = client["community_database"]
        collection = db[C]

        res = {}
        if dd == 0: # montly로 조회
            _date = ".*" + str(yy).zfill(2) + "/" + str(mm).zfill(2) + ".*"
        else:       # daily로 조회
            _date = ".*" + str(yy).zfill(2) + "/" + str(mm).zfill(2) + "/" + str(dd).zfill(2) + ".*"

        # 정상 게시글의 수 - tag == 0
        first_condition = [{"date": {'$regex': _date}}, {"tags": 0}]
        first_condition_result = collection.count_documents({'$and': first_condition})
        res["cleanPost"] = first_condition_result

        # 분쟁 게시글의 수 - tag == 1
        second_condition = [{"date": {'$regex': _date}}, {"tags": 1}]
        second_condition_result = collection.count_documents({'$and': second_condition})
        res["hatePost"] = second_condition_result

        return res

    except Exception as e:
        print(traceback.format_exc())
    finally:
        client.close()
        print('DB connection closed')

# 2번 쿼리, 5번 쿼리
def getMonthlyOrDailyComments(C, yy, mm, dd=0):
    '''     
    Args:
        C: 커뮤니티의 이름(문자열), DB 접속 위함
        yy: 년 (정수형)
        mm: 월 (정수형)
        dd: 일 (정수형) if 0, monthly else daily로 조회
    
    Returns:
        C 커뮤니티의 yy년 mm월 (optional:dd일)의 cleanComment(정상 댓글), curseComment(악플), hateComment(혐오 댓글)의 수를 딕셔너리로 반환
    '''
    # DB 연결
    try:
        client = MongoClient(host=host, port=port) # 추후 서버 띄우면 아이피 및 포트 변경
        db = client["community_database"]
        collection = db[C]

        res = {}
        if dd == 0: # montly로 조회
            _date = ".*" + str(yy).zfill(2) + "/" + str(mm).zfill(2) + ".*"
        else:       # daily로 조회
            _date = ".*" + str(yy).zfill(2) + "/" + str(mm).zfill(2) + "/" + str(dd).zfill(2) + ".*"

        # 각 카테고리 댓글의 수
        base_condition = [
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
        base_condition_result = collection.aggregate(base_condition)
        
        cleanComment = curseComment = hateComment = 0
        for i in base_condition_result:
            if i['_id'] in hate:
                hateComment += i['count']
            elif i['_id'] == 'curse':
                curseComment += i['count']
            elif i['_id'] == 'clean':
                cleanComment += i['count']
            else: # 예외 처리
                pass
        
        res['cleanComment'], res['curseComment'], res['hateComment'] = cleanComment, curseComment, hateComment
        
        return res
    except Exception as e:
        print(traceback.format_exc())
    finally:
        client.close()
        print('DB connection closed')
    
# 3번 쿼리, 6번 쿼리
def getDailyOrHourlyHatePostsNComments(C, yy, mm, dd=0):
    '''     
    Args:
        C: 커뮤니티의 이름(문자열), DB 접속 위함
        yy: 년 (정수형)
        mm: 월 (정수형)
        dd: 일 (정수형) if 0, daily else hourly로 조회
    
    Returns:
        C 커뮤니티의 yy년 mm월 (optional:dd일)의 날짜별 hatePost(혐오 게시글), hateComment(혐오+악플)의 수를 list에 담고 이를 value로 갖는 딕셔너리로 반환
    '''
    # DB 연결
    try:
        client = MongoClient(host=host, port=port) # 추후 서버 띄우면 아이피 및 포트 변경
        db = client["community_database"]
        collection = db[C]

        res = {}
        if dd == 0: # montly로 조회
            _date = ".*" + str(yy).zfill(2) + "/" + str(mm).zfill(2) + ".*"
            startIdx = 6
        else:       # daily로 조회
            _date = ".*" + str(yy).zfill(2) + "/" + str(mm).zfill(2) + "/" + str(dd).zfill(2) + ".*"
            startIdx = 9

        # 날짜별 혐오 게시글 수
        first_condition = [
            {
                "$match" : {
                    "date": {'$regex': _date},
                },                
            },
            {
                "$group": {
                    "_id" : { 
                        "$substr": ["$date", startIdx, 2]
                    },
                    "count": {"$sum": 1},
                }
            },
        ]
        first_condition_result = collection.aggregate(first_condition)
        
        hatePostlist = [0]*31
        for i in first_condition_result:
            hatePostlist[int(i['_id']) - 1] = i['count']
        res['hatePost'] = hatePostlist

        # 날짜별 혐오 댓글 + 악플 수
        second_condition = [
            { 
                "$unwind": {
                    "path": "$comments",
                }
            },
            {
                "$match" : { '$and': [
                    { "comments.time": {"$regex": _date} },
                    {'$or': [
                        {"comments.result": "woman/family"},
                        {"comments.result": "man"},
                        {"comments.result": "minority"},
                        {"comments.result": "race/nationality"},
                        {"comments.result": "age"},
                        {"comments.result": "region"},
                        {"comments.result": "religion"},
                        {"comments.result": "extra"},
                        {"comments.result": "curse"},
                    ]
                    },
                ]
                },
            },
            {
                "$group": {
                    "_id" : { 
                        "$substr": ["$comments.time", startIdx, 2]
                    },
                    "count": {"$sum": 1},
                }
            },
        ]

        hateCommentlist = [0]*31  
        second_condition_result = collection.aggregate(second_condition)
        for i in second_condition_result:
            hateCommentlist[int(i['_id']) - 1] = i['count']
        res['hateComment'] = hateCommentlist

        return res

    except Exception as e:
        print(traceback.format_exc())
    finally:
        client.close()
        print('DB connection closed')
        
def getNPosts(C, count=20):
    '''     
    Args:
        C: 커뮤니티의 이름(문자열), DB 접속 위함
        count: 가져올 글 개수
    
    Returns:
        C 커뮤니티의 글 20개를 뒤에서 조회해서 배열로 반환
    '''
    # DB 연결
    try:
        client = MongoClient(host=host, port=port) # 추후 서버 띄우면 아이피 및 포트 변경
        db = client["community_database"]
        collection = db[C]

        res = []
        resultList = collection.find({}, {"_id": 0}).sort("date", -1).limit(count)
        for result in resultList:
            res.append(result)

        return res

    except Exception as e:
        print(traceback.format_exc())
    finally:
        client.close()
        print('DB connection closed')

if __name__=="__main__":
    #res = getMonthlyOrDailyPosts("everytime", 22, 10, 18)
    #res = getMonthlyOrDailyComments("everytime", 22, 10, 17)
    #res = getDailyHatePostsNComments("everytime", 22, 10)
    #res = getDailyOrHourlyHatePostsNComments("everytime", 22, 10)
    res = getNPosts("everytime", count=20)
    print(res)