import pandas as pd,numpy as np,lightgbm as lgb
from sklearn.metrics import r2_score
d=pd.read_pickle('all.pkl')
d['hour']=d.ts.dt.hour; d['dow']=d.ts.dt.day_of_week; d['stc']=d.st.astype('category')
d['yr']=d.ts.dt.year
F=['stc','hour','dow','wind_speed_10m','wd_s','wd_c','boundary_layer_height','precipitation','temperature_2m','relative_humidity_2m','ws6','ws24','ws48','blh6','blh24','blhmax24','pr24','pr72','pr240','wd6s','wd6c','wd24s','wd24c','land24','rh24','t24']
y=np.log1p(d.pm25); d['exp']=np.nan
for yr in sorted(d.yr.unique()):
    tr=d.yr!=yr
    m=lgb.LGBMRegressor(objective='huber',alpha=0.4,n_estimators=800,learning_rate=0.03,num_leaves=63,min_child_samples=100,subsample=0.7,subsample_freq=1,colsample_bytree=0.7,verbose=-1)
    m.fit(d.loc[tr,F],y[tr]); d.loc[~tr,'exp']=np.expm1(m.predict(d.loc[~tr,F]))
d['date']=d.ts.dt.date
day=d.groupby(['src','st','date']).agg(actual=('pm25','mean'),expected=('exp','mean'),n=('pm25','size')).reset_index()
day=day[day.n>=18]
city=day.groupby('date').agg(actual=('actual','mean'),expected=('expected','mean'),k=('st','size')).reset_index()
city=city[city.k>=3]; city['extra']=city.actual-city.expected
print('daily st R2',r2_score(day.actual,day.expected),'city R2',r2_score(city.actual,city.expected))
for y_ in [2018,2019,2024,2025,2026]:
    c=city[pd.to_datetime(city.date).dt.year==y_]; 
    if len(c): print(y_,'R2',round(r2_score(c.actual,c.expected),2),'n',len(c))
city['m']=pd.to_datetime(city.date).dt.to_period('M')
print(city.groupby('m')[['actual','expected','extra']].mean().round(1).to_string())
print(city.sort_values('extra',ascending=False).head(30).to_string())
d[['ts','src','st','pm25','exp']].to_pickle('hourly2.pkl'); day.to_csv('daily2.csv',index=False); city.to_csv('city2.csv',index=False)
