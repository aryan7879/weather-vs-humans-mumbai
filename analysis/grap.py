import pandas as pd,numpy as np
h=pd.read_pickle('hourly2.pkl'); h['date']=h.ts.dt.normalize()
day=h.groupby(['src','st','date']).agg(actual=('pm25','mean'),exp=('exp','mean'),n=('pm25','size')).reset_index(); day=day[day.n>=18]; day['res']=day.actual-day.exp
city=day.groupby('date').agg(actual=('actual','mean'),exp=('exp','mean'),res=('res','mean'),k=('st','size'))
city=city[city.k>=3].asfreq('D')
def diff(t,L=12):
    b=city.loc[t-pd.Timedelta(days=L):t-pd.Timedelta(days=1)]; a=city.loc[t+pd.Timedelta(days=1):t+pd.Timedelta(days=L)]
    if b.res.count()<8 or a.res.count()<8: return None
    return dict(act=a.actual.mean()-b.actual.mean(), exp=a.exp.mean()-b.exp.mean(), res=a.res.mean()-b.res.mean(),
                b_act=b.actual.mean(),a_act=a.actual.mean(),b_exp=b.exp.mean(),a_exp=a.exp.mean())
g=diff(pd.Timestamp('2025-11-27')); print({k:round(v,1) for k,v in g.items()})
pl=[]
for t in city.index:
    if t.month in (10,11,12,1,2) and abs((t-pd.Timestamp('2025-11-27')).days)>30:
        r=diff(t)
        if r: pl.append(r['res'])
pl=np.array(pl); print('placebo n',len(pl),'share <= grap',(pl<=g['res']).mean(),'pctiles',np.percentile(pl,[1,5,50,95]).round(1))
print(city.loc['2025-11-10':'2025-12-20',['actual','exp','res']].round(1).to_string())
