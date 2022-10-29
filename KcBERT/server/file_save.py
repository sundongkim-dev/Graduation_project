def fileToArray(fileName):
    '''
    인자로 받은 파일이름을 배열로 리턴
    ex. fileToArray("sample.txt") => [12, 34, 56]
    '''
    with open(fileName, "r", encoding="UTF-8") as f:
        lines = f.readlines()
        result = []
        for line in lines:
            result.append(line.strip())
    return result

def arrayToFile(fileName, arr):
    '''
    인자로 받은 배열을 파일로 추가
    ex. fileToArray("sample.txt", [12, 34, 56])
    '''
    with open(fileName, "a", encoding="UTF-8") as f:
        for e in arr:
            f.write(str(e))
            f.write("\n")
            
    
if __name__ == "__main__":
    # 테스트 코드
    arrayToFile("sample.txt", [12, 34, {"name": 65, "files": [12, 34, 56]}])
    print(fileToArray("sample.txt"))