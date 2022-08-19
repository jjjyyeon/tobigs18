source("TS-library.R")
library(stats)

library(dplyr)

library(itsmr)

install.packages("forecast")
dat=read.csv("Electric_Production.csv")
data<-dat$IPG2211A2N
data
data=ts(data,start=1985,end=2018,freq=12)

plot.ts(data)

#log 취해보기
data_log<-log(data)
plot.ts(data_log)

#큰 차이 없음

n=length(data);
x=seq(from=1 , to=n, by=1);
out.lm =lm(data ~1 +x);
summary(out.lm)
plot.ts(data);
title("electric production")

lines(out.lm$fitted.values, col="red")

# 증가하는 trend 와 계절성을 보임
# stationary 하지 않음

par(mfrow=c(1,2))
acf(data,lag=150);
pacf(data)
# 상관관계가 강하다, 점차 감소함 (by acf)

 

# 차분을 통해 seasonality 와 trend 없애보자.

# differencing
par(mfrow=c(2,2))
d1=diff(data)
plot.ts(d1); title("1st order diff");
d2=diff(d1)
plot.ts(d2); title("2nd order diff");
d3=diff(d2)
plot.ts(d3); title("3rd order diff");
d4=diff(d3)
plot.ts(d4); title("4th order diff")

# 1,2,3,4 차 차분이 그래프가 크게 다르지 않음
# 1차 차분으로 진행하겠다.
acf(d1,lag=150)
pacf(d1,lag=50)

#acf 그래프 에서 주기 12 로 보임

# 따라서  sarima(p.d,q)*(P,D,Q) 모형에서 d를 1로 생각하고,
# 계절성에 대한 차분도 한번더 생각하여 D 를 1로 생각한다
# 또한 pacf의 그래프에 의해 P를 1로 생각해본다
# p 는 0,1,2  경우를 시도해 본다.

# sarima(0,1,0)*(1,1,0)
fit.1 = arima(data, order = c(0,1,0), seasonal=list(order=c(1,1,0), period=12))
fit.1 # aic = 1953.95

# sarima(1,1,0)*(1,1,0)

fit.2 = arima(data, order = c(1,1,0), seasonal=list(order=c(1,1,0), period=12))
fit.2 # aic = 1940.1

# sarima(2,1,0)*(1,1,0)
fit.3 = arima(data, order = c(2,1,0), seasonal=list(order=c(1,1,0), period=12))
fit.3 # aic = 1908.35

#auto arima

library(forecast)
dat.ff = ts(data, frequency=12);
auto.arima(dat.ff) #ARIMA(2,1,1)(0,1,1)[12] 
#aic : 1786.11

#auto arima의 aic 가 가장 낮다.

#최종 모형
fit.4=arima(data, order = c(2,1,1), seasonal=list(order=c(0,1,1), period=12))
fit.4

#2018년 예측
plot(forecast(fit.4, h=12))
forecast(fit.1, h=12)

