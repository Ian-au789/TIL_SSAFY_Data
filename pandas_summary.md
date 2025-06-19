## 1.EDA

df.head(n) : 앞에서 n개의 행 출력
df.tail(n) : 뒤에서 n개의 행 출력
df.shape : 튜플 형태로 행과 열 갯수 출력 ([0] : 행, [1] : 열)
df.info() : 데이터프레임 정보 확인
df.describe() : 각 수치형 변수 분포 확인 (개수, 평균, 표준편차 등)
df.column : 전체 컬럼 리스트 출력
df.column[n] : n+1번째 컬럼명 출력

df.iloc[:, 5].dtype : 6번째 컬럼의 데이터 타입 확인
df.iloc[2, 5] : 6번째 컬럼의 3번째 값 출력

df.index : 인덱스 구성 확인

df.select_dtypes(exclude=object).columns : 수치형 변수를 가진 컬럼 출력
df.select_dtypes(include=object).columns : 범주형 변수를 가진 컬럼 출력
df.isnull().sum() : 각 컬럼의 결측치 숫자 파악

df['column'].quantile(n) : 사분위수 구하기
df.column.nunique() : 컬럼의 유일값 개수 출력
df.column.unique() : 컬럼의 유일값 전부 출력

## 2.Filtering & Sorting

.reset_index() : 인덱스 다시 구성
df[['column1', 'column2']] : 2개의 컬럼으로 구성된 새로운 데이터 프레임 정의
.str[1:] : string 인덱스 슬라이싱
.astype('int') : int 타입으로 변환
.sort_values('column', ascending=True) : 컬럼 값에 따라 오름차순 정렬
.contains('word') : 문자열에 해당 단어 포함 여부 확인
.drop_duplicates('column', keep='first') : 컬럼에서 중복 행 제거 (첫 번째 케이스만 남김)
.startswith('N') : N으로 시작하는 데이터 추출
.len() : 문자열 길이 출력
.isin(lst) : lst 리스트에 저장된 값을 가지는 컬럼값 출력


## 3.Grouping
df.groupby('column').size() : 각 컬럼값 당 빈도수를 나타내는 그룹화
.to_frame().rename(columns={0:'counts'}) : 새로 만든 컬럼의 이름 바꾸기
.sort_values('column', ascending=False) : 해당 컬럼을 기준으로 내림차순 정렬
.agg(['mean', 'var', 'max', 'min']) : 구하고자 하는 값 여러개 동시에 구하기
.column : 해당 df의 컬럼값 


## 4.Apply, Map
.map(lambda x: func(x)) : 각 행에 func 함수 적용
.apply(func) : 각 행에 func 함수 적용 
.diff() : 현재 값과 이전 값의 차이를 계산


## 5.Time Series
pd.to_datetime(df.Yr_Mo_Dy) : 판다스에서 인식할 수 있는 datetime64로 변환
.dt 뒤에 붙이는 메서드들 
.year <- 년
.month <- 월
.day <- 일
.weekday <- 요일
.hour <- 시간
.minute <- 분
.second <- 초
.date <- 날짜
.time <- 시간
.resample('W') : 데이터를 주 단위로 뽑기

## 6.Pivot
.drop('column') : 컬럼 선택해서 삭제
.pivot_table(index = '', columns = '', values = '', aggfunc='') : 행, 열, 채울 값 지정


## 7.Merge, Concat
pd.concat([df1, df2]) : 두 데이터프레임을 하나로 합침
pd.concat([df3, df4], join='inner') : 공통 열만 유지해서 하나로 합침
pd.merge([df5, df6], on='key', how='inner') : key 값을 지정하고 교집합 합치

concat : 단순 이어붙이기, merge : join