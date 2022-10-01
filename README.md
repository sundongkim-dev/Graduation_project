# Final-Project
 졸업 프로젝트


## 설정, 코드 작성 중에 겪었던 오류 및 유의사항들

0. conda 환경에서 python 3.7 버전을 사용, KoBERT의 requirements.txt를 다음과 같이 변경해야 설치 가능
    - boto3 == 1.15.18
    - gluonnlp == 0.10.0
    - mxnet == 1.7.0.post2
    - onnxruntime == 0.5.0
    - sentencepiece == 0.1.96
    - torch == 1.10.1
    - transformers == 3.0.2

1. 파일 인코딩 설정 UTF-8로 설정해야 함(EUC-KR X)

2. Illegal byte sequence Error #42
    - 설치 파일 경로에 한글이 있으면 발생

3. GPU에서 저장한 모델을 cpu에서 로드하려면 map_location 인자 설정해야줘야 정상적으로 로드 가능
    - ```dict_model = torch.load('model.pth', map_location=torch.device('cpu'))```

4. KoBERT model에서 return_dict 값 설정
    - ```_, pooler = self.bert(input_ids = token_ids, token_type_ids = segment_ids.long(), attention_mask = attention_mask.float().to(token_ids.device), return_dict=False)```

5. History
    - 2022/09/27: [1.KoBERT_training.ipynb]에서 얻은 binary classification 모델을 flask에 넘겨준 것이 prototype


## TO-DO list

- 웹사이트 꾸미기 (javascript, css 등)
- 정보 시각화
- 더 복잡한 모델 주어지면 파싱하기
- 추가 예정...

### 디렉터리 구조

![directory structure](https://user-images.githubusercontent.com/44566164/192562725-b22a8a3d-b30b-4929-b84b-95da2b887597.png)
