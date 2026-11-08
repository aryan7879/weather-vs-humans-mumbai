import pandas as pd,numpy as np,json
h=pd.read_pickle('hourly2.pkl'); h['res']=h.pm25-h.exp; h['date']=h.ts.dt.normalize()
day=h.groupby(['src','st','date']).agg(actual=('pm25','mean'),exp=('exp','mean'),n=('pm25','size')).reset_index(); day=day[day.n>=18]; day['res']=day.actual-day.exp
city=day.groupby('date').agg(actual=('actual','mean'),exp=('exp','mean'),res=('res','mean'),k=('st','size')).reset_index(); city=city[city.k>=3].set_index('date').asfreq('D')
# local baseline: median residual of days -21..-8 and +8..+21
def local(dt,w=2):
    dt=pd.Timestamp(dt); win=city.loc[dt-pd.Timedelta(days=w):dt+pd.Timedelta(days=w)]
    base=pd.concat([city.loc[dt-pd.Timedelta(days=21):dt-pd.Timedelta(days=8)],city.loc[dt+pd.Timedelta(days=8):dt+pd.Timedelta(days=21)]]).res.median()
    return win,base
out={}
for name,dt in {'2018':'2018-11-07','2019':'2019-10-27','2024':'2024-11-01','2025':'2025-10-21'}.items():
    win,base=local(dt); win=win.dropna()
    if len(win)==0: print(name,"no data"); continue
    extra=(win.res-base); 
    out[name]=dict(days=len(win),actual_mean=round(win.actual.mean(),1),weather_expected=round(win.exp.mean(),1),extra_mean=round(extra.mean(),1),peak_day=str(win.actual.idxmax().date()),peak=round(win.actual.max(),1),extra_sum_ugday=round(extra.clip(lower=0).sum(),1),cig=round(extra.clip(lower=0).sum()/22,1))
    print(name,out[name]); print(win[['actual','exp','res']].round(1).assign(extra=extra.round(1)).to_string())
# placebo: distribution of 5-day window extras over all non-Diwali Oct-Nov days
