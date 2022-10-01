import os

tsv_path = 'c:\\Users\\mok03\\졸업 프로젝트\\korean_unsmile_dataset-main'
train_data_path = os.path.join(tsv_path, 'unsmile_train_v1.0.tsv')
valid_data_path = os.path.join(tsv_path, 'unsmile_valid_v1.0.tsv')

categories = ['여성/가족', '남성', '성소수자', '인종/국적', '연령', '지역', '종교', '기타 혐오', '악플/욕설', 'clean', '개인지칭']
categories_drop_personalref = ['여성/가족', '남성', '성소수자', '인종/국적', '연령', '지역', '종교', '기타 혐오', '악플/욕설', 'clean']