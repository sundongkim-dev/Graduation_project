# Graduation-Project

졸업 프로젝트(2022.09~2022.10) 수행


## 설정, 코드 작성 중에 겪었던 오류 및 유의사항들

0. History
    - 2022/09/27: [1.KoBERT_training.ipynb]에서 얻은 binary classification 모델을 flask에 넘겨준 것이 prototype
    - 2022/10/02: KcBERT가 성능이 더 뛰어난 이유로 KcBERT로 웹 서빙 결정
    - 2022/10/03: 모델 output 용량 이슈로 온전히 업로드 되지 않았음 -> .gitignore에 추가하고 구글 드라이브로 공유
    - 2022/10/04: 디렉터리 구조 리팩터링
    - 2022/10/13: MongoDB 선정, 프로토타입 최소 요건 정리, 통계 탭 디자인, 모델 사이즈 명시
    - 2022/10/17: 통계 탭 기능 구현, 경로 오류 수정
    - 2022/10/18: DB data insert 및 refresh 기능 구현
    - 2022/10/19: 사이트 현황 탭 게시글/댓글 표 출력 기능 구현
    - 2022/10/20: 통계 탭 그래프 페이지 구현
    - 2022/10/21: 통계에 필요한 쿼리들 구현 -> 미스커뮤니케이션으로 인한 잘못된 설계 추후 업데이트
    - 2022/10/22: DB와 그래프 연동 구현
    - 2022/10/27: 쿼리 업데이트, 모델 지표 페이지, 네비게이션 바 항목 및 콜랩스 추가
    - 2022/10/28: 크롤링 모듈 구현, db에 약 20개의 데이터 삽입 및 refresh 자동화 구현
    - 2022/10/29: 표본 데이터 DB 삽입, 로그 출력 20개 제한

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
0. conda 환경에서 python 3.7.13 버전을 사용, 모델 구성 및 서버 구성을 위한 패키지 버전은 다음과 같다.
    - numpy==1.21.5
    - transformers==4.18.0
    - datasets==1.17.0
    - torch==1.12.0
    - Flask==2.2.2
    - APScheduler==3.9.1
    - beautifulsoup4==4.11.1
    - lxml==4.9.1
    - pymongo==4.2.0
    - selenium==4.5.0
    - torch==1.12.0
    - webdriver-manager==3.8.4

1. KcBERT가 KoBERT보다 성능이 뛰어난 관계로 KcBERT 모델로 웹 서비스

### 디렉터리 구조

![directory structure](https://user-images.githubusercontent.com/44566164/193811585-e63e5f3e-669a-45bb-a1fe-e1fbbba8ad2c.png)

## 모델 학습 환경 및 지표

**-서버 환경**: Linux

**-가상환경**: Anaconda 4.14.0(python 3.8.13)

**2. 데이터셋**

Smilegate사에서 제공한 unsmile dataset을 cleaning한 데이터셋.
데이터셋을 분석하던 중 일부 데이터 레이블링이 잘못되어 있음을 확인했다. 모든 데이터셋을 수기로 확인하기엔 무리가 있어 모델 기반 방식으로 약 120개(전체 데이터 중 약 1%) 데이터의 레이블을 고치는 작업을 진행했다.

**3. 모델**

BERT는 대량의 영어 말뭉치 데이터를 사용하여 multi-layer transformer encoder 모델을 MLM(Masked Language Modeling)과 NSP(Next Sentence Prediction) training objective로 학습한 모델이다. transformer encoder 내부의 self-attention layer는 BERT 모델이 입력 문장의 문맥을 고려한 좋은 representation을 만들도록 해준다. 본 프로젝트에서는 한국어 감정분석 문제를 풀기위한 sentence encoder로써 KoBERT와 KcBERT를 사용한다.   

1. KoBERT: 한국어 위키, 뉴스 기사, 책 등 잘 정제된 데이터를 사용하여 BERT를 추가학습한 모델
2. KcBERT: 네이버 뉴스의 댓글과 대댓글을 수집해 토크나이저와 BERT모델을 처음부터 사전학습한 모델

||vocabulary size|number of parameters|model size(model.bin)|
|---|---|---|---|
|KoBERT|8002|92194570|368.85MB|
|KcBERT|30000|108926218|435.77MB|


**4. 학습**

KoBERT, KcBERT 모델 내의 파라미터는 변경하지 않고 최종적인 부류를 위한 가장 마지막 신경망 층의 파라미터만 학습하는 방식으로 학습했다.

epoch별 loss 변화 추이 그래프

![loss_per_epochs](/KcBERT/model/result/img/loss_per_epochs.png)

**5. 카테고리별 성능**(f1-score)
1. 데이터셋: 기존 unsmile dataset을 cleaning(약 120개 데이터 re-labeling)한 데이터셋
2. 사용 모델: KoBERT, KcBERT(KoBERT를 네이버 댓글 데이터를 사용해서 처음부터 학습한 모델)

**6. 최종 사용 모델 크기**
1. kcbert-model.pth: 425,599KB
2. kcbert-tokenizer.pth: 665KB

**7. 카테고리별 성능**(f1-score)

||여성/가족|남성|성소수자|인종/국적|연령|지역|종교|기타 혐오|악플/욕설|clean|
|---|---|---|---|---|---|---|---|---|---|---|
|KoBERT|0.74|0.79|0.81|0.77|0.25|0.84|0.87|0.00|0.59|0.70|
|KcBERT|0.80|0.87|0.83|0.83|0.86|0.91|0.88|0.47|0.67|0.76|
|Baseline|0.76|0.85|0.83|0.82|0.83|0.88|0.87|0.30|0.67|0.77|
* Baseline은 스마일 게이트에서 제공한 수치

**8. Data cleaning 전후 성능(f1-score) 비교**

||여성/가족|남성|성소수자|인종/국적|연령|지역|종교|기타 혐오|악플/욕설|clean|micro avg|macro avg|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|cleaning 전|0.79|0.84|0.83|0.80|0.82|0.86|0.88|0.00|0.67|0.75|0.76|0.72|
|cleaning 후|0.79|0.83|0.83|0.80|0.84|0.88|0.88|0.00|0.68|0.75|0.77|0.73|