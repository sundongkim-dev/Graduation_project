# Graduation-Project

졸업 프로젝트(2022.05~2022.10) 수행


## 설정, 코드 작성 중에 겪었던 오류 및 유의사항들

0. History
    - 2022/09/27: [1.KoBERT_training.ipynb]에서 얻은 binary classification 모델을 flask에 넘겨준 것이 prototype
    - 2022/10/02: KcBERT가 성능이 더 뛰어난 이유로 KcBERT로 웹 서빙 결정
    - 2022/10/03: 모델 output 용량 이슈로 온전히 업로드 되지 않았음 -> .gitignore에 추가하고 구글 드라이브로 공유
    - 2022/10/04: 디렉터리 구조 리팩터링

### KoBERT 관련
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

### KcBERT 관련
0. conda 환경에서 python 3.7.13 버전을 사용, 서버 작동을 위해 사용한 패키지 버전은 다음과 같다.
    - numpy==1.21.5
    - transformers==4.18.0
    - datasets==1.17.0
    - torch==1.12.0
    - Flask==2.2.2


## TO-DO list

- 웹사이트 꾸미기 (javascript, css 등)
- 정보 시각화
- 웹 디자인
- 보고서 작성

### 디렉터리 구조

![directory structure](https://user-images.githubusercontent.com/44566164/193811585-e63e5f3e-669a-45bb-a1fe-e1fbbba8ad2c.png)

## 모델 학습 환경 및 지표

**서버 환경**: linux

**가상환경**: anaconda 4.14.0(python 3.8.13)

**모델 학습**

1. 데이터셋: 기존 unsmile dataset을 cleaning(약 120개 데이터 re-labeling)한 데이터셋
2. 사용 모델: KoBERT, KcBERT(KoBERT를 네이버 댓글 데이터를 사용해서 처음부터 학습한 모델)
    
    
**카테고리별 성능**(f1-score)

||여성/가족|남성|성소수자|인종/국적|연령|지역|종교|기타 혐오|악플/욕설|clean|
|---|---|---|---|---|---|---|---|---|---|---|
|KoBERT|0.74|0.79|0.81|0.77|0.25|0.84|0.87|0.00|0.59|0.70|
|KcBERT|0.80|0.87|0.83|0.83|0.86|0.91|0.88|0.47|0.67|0.76|
|Baseline|0.76|0.85|0.83|0.82|0.83|0.88|0.87|0.30|0.67|0.77|
* Baseline은 스마일 게이트에서 제공한 수치
* KoBERT, KcBERT 모두 15 epoch으로 학습


**Data cleaning 전후 성능(f1-score) 비교**

||여성/가족|남성|성소수자|인종/국적|연령|지역|종교|기타 혐오|악플/욕설|clean|micro avg|macro avg|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|cleaning 전|0.79|0.84|0.83|0.80|0.82|0.86|0.88|0.00|0.67|0.75|0.76|0.72|
|cleaning 후|0.79|0.83|0.83|0.80|0.84|0.88|0.88|0.00|0.68|0.75|0.77|0.73|
* data cleaning이 성능에 영향을 미치는지 파악하기 위해 KcBERT 모델을 사용하여 5 epoch씩 학습시킨 결과
* f1-score 평균 1% 향상


**Epoch 당 loss 변화 추이**

* 그래프로 보여주자