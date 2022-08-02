import pandas as pd 
import numpy as np  
data=pd.read_csv('HR_Employee_Attrition.csv')
data.head()
data.info()
data.describe()
data.describe().to_csv("data_describe.csv",index=False)


#결측치 확인
data.isnull()
data.isnull().sum()

# 이상치 확인
# 1. IQR 이용
q3= data.quantile(0.75) 
q1= data.quantile(0.25)

iqr=q3-q1
iqr

# 1) age
def age_outlier(data):
    age=data['Age']
    if age>q3['Age']+1.5*iqr['Age'] or q1['Age'] -1.5*iqr['Age'] :
        return True
    else:
        return False

data['Age_이상치 여부']=data.apply(age_outlier,axis=1)
data
data_age_false=data.loc[data['Age_이상치 여부']==False]
data_age_false #empty --> age 이상치 없다

# 2) TotalWorkingYears
def TotalWorkingYears_outlier(data):
    TotalWorkingYears=data['TotalWorkingYears']
    if TotalWorkingYears>q3['TotalWorkingYears']+1.5*iqr['TotalWorkingYears'] or q1['TotalWorkingYears'] -1.5*iqr['TotalWorkingYears'] :
        return True
    else:
        return False

data['TotalWorkingYears_이상치 여부']=data.apply(TotalWorkingYears_outlier,axis=1)
data
data_TotalWorkingYears_false=data.loc[data['TotalWorkingYears_이상치 여부']==False]
data_TotalWorkingYears_false #empty -->  TotalWorkingYears 이상치 없다

#이상치 평균, 표준편차 이용
data=pd.read_csv('HR_Employee_Attrition.csv')
mean = np.mean(data)
mean
std = np.std(data)
std
data['Age']

threshold = 3

outlier = [] 

for i in data['Age']: 
    z = (i-mean)/std 
    if  (threshold<z).bool(): 
        outlier.append(i) 

print('데이터셋 내의 이상값은', outlier) 

## 잘 안됨...

## zscore 이용
from scipy import stats

data['z_scales age']=stats.zscore(data['Age'])
data.head()
data2=data.copy()
data2=data2['z_scales age'].between(-2,2)
data2.head()
data2_age_false=data2.loc[data['z_scales age']==False]
data2_age_false # empty


data['z_scales DailyRate']=stats.zscore(data['DailyRate'])
data.head()
data3=data.copy()
data3=data3['z_scales DailyRate'].between(-2,2)
data3.head()
data3_age_false=data2.loc[data['z_scales DailyRate']==False]
data3_age_false # empty

# boxplot
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


plt.rcParams['axes.unicode_minus'] = False  # matplotlib 마이너스기호 표시
plt.rc('font', family='NanumGothic')  # matplotlib 한글폰트 표시


df = pd.read_csv('HR_Employee_Attrition.csv')
df

df.boxplot(column=['DistanceFromHome'])
plt.show()

#histogram
original_df = df[['DistanceFromHome']]
original_df.hist(bins=20, figsize=(10,5))
plt.show()


# 시각화
# 1) 기본 산점도
df = pd.read_csv('HR_Employee_Attrition.csv')
plt.scatter(df['JobLevel'],df['MonthlyIncome'])
plt.show()
#업무의 수준이 높을 수록 월 소득 증가

# 2) 성별 비율 -count
import seaborn as sns
df = pd.read_csv('HR_Employee_Attrition.csv')
df 
sns.countplot(x = df['Gender'])
plt.show()
# 남자가 200명 이상 많다.

# 3) EducationField 종류별
sns.countplot(x = df['EducationField'])
plt.show()

# 4) 성별 결혼여부 에 따른 월 소득 - facet grid
sns.FacetGrid(df, col = 'MaritalStatus', row = 'Gender').map(sns.distplot, 'MonthlyIncome')
plt.show()

# 5) pair plot
sns.pairplot(df)
plt.show()

# 변수간 상관관계
df.corr()
sns.heatmap(df.corr(), annot=True, cmap="YlGnBu")
plt.show()

### 수치형 변수만 선택 가능한가???

# 파생변수

df['education gb']=np.where(df['Education']>=3, 'good','bad')
df

grade=[(mpg['cty']>=20),(mpg['cty']<20)&(mpg['cty']>=17),(mpg['cty']<17)]
choice=['a','b','c']
mpg['cty_grade']=np.select(grade,choice,default='Not Specified')

grade=[(df['YearsInCurrentRole']>=15),(df['YearsInCurrentRole']<15)&(df['YearsInCurrentRole']>=7),(df['YearsInCurrentRole']<7)]
choice=['a','b','c']
df['YearsInCurrentRole_grade']=np.select(grade,choice,default='Not Specified')
df