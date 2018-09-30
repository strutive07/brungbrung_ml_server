# 2018년 서울시 앱 공모전 출품작(어서와)

### 어서와 프로젝트 머신러닝 서버
### 사용 모델 명
Multinomial Naive Bayes Classification
---

데이터로써 트위터의 글을 수집했다. 본 프로젝트의 성격과 알맞은 콘서트, 세미나, 해커톤 등의 키워드를 대상으로 노이즈가 덜 끼어있고 트윗이 많은 것들을 수집했다.
 그 후 Konlpy를 사용하여 데이터를 Tokenizing한다. 트위터의경우 노이즈와 단일 자모 단어 등 Tokenizer에서 Out of Vocabulary인 단어가 많다. 조사나 부사는 자주 등장하지만 의미의 중요도는 떨어진다. 그렇기 때문에 명사만 추출한다.
 통계 기반 학습 Naive Bayesian Classification, Linear Support vector Classification, Multinomial Naive Bayes Classification 등을 사용하여 그중 가장 높은 정확률을 보이는 모델을 사용했다.

 각 Class에 대해 조건부 확률로 작동한다. N개의 독립변수가 있을 때, 각 인스턴스들은 N차원 벡터로 표현되고 K개의 분류에 대해 가능한 확률을 다음과 같은 조건부 확률로 구하여 학습한다.


 러닝시킨 확률 모델로부터 아래와 같은 수식을 통하여 Input으로 들어온 데이터를 분류한다.


 그러나 특정 이벤트의 빈도와 단어의 출현 빈도 등을 통하여 분류하는 모델이 필요했다. 위와 같은 Naive Bayes 모델에 이러한 컨셉을 적용한 다항분포 Naive Bayes 모델을 사용하니 성능이 향상했다. 아래와 같이 특성 벡터에서 단어의 유무를 가지고 있는 데이터를 기반으로 학습하였다.


 다음과 같은 수식으로 클래스를 판별한다.


 SVM의 경우 2가지의 분류로 학습을 해봤지만 Linear SVM의 경우 분류를 2가지로만 분류하여 최종적으로 Multinomial Naive Bayes Classification 을 사용했다.

 이렇게 나온 모델을 기존 애플리케이션의 게시글의 데이터를 모아서 분류하고 분석하는 일에 사용한다.
