import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import os


class consumo:
	def __init__(self,path,maximum=200):
		c=pd.read_csv(path,sep=';',parse_dates=True,index_col=0)
		s=c.reindex(pd.date_range(c.index[0],c.index[-1],freq='H'))
		self.df=s.apply(lambda x: (x['maximum']-x['minimum']) if (x['minimum']>0 and x['maximum']>0 and ((x['maximum']-x['minimum'])<maximum)) else np.NaN,axis=1)
		

	def forfullday(self,start_hour=3):
		s=self.df.groupby(lambda x: (x-pd.DateOffset(hours=start_hour)).date()).apply(lambda x: [e for e in x]) #agrupar por dia
		s.reset_index()
		#s.index=pd.to_datetime(s.index)
		s=s.reindex(pd.date_range(s.index[0],s.index[-1],freq='D'))
		return s.iloc[1:-2]

class day24HTS:
		# 24 hour value in vector/array type form indexs by day
		def __init__(self,df):
			self.df=df
			self.distance=self._fdtw_
		#choise the distance	
		def setdistance(self,namedistance):
			distances={'ftdw':self._fdtw_, 'euclidean':self._euclidean_, 'deform':self._deform_}
			if namedistance in distances.keys():
				self.distance=distances[namedistance]
				
		# distace Fast Dynamic Time Warping
		def _fdtw_ (self,a,b):
			x = np.array(a)
			y = np.array(b)
			return fastdtw(x, y, dist=euclidean)[0]
		# euclidean distance	
		def _euclidean_(self,a,b):
			return np.sqrt(np.sum((np.array(a)-np.array(b))**2))
			
		def _deform_ (self,a,b):
			dk=fastdtw(a, b, dist=euclidean)[1]
			return len([(i,j) for (i,j) in dk if i!=j ])
			
		def idist(self,i,j):
			return self.distance(self.df.iloc[i],self.df.iloc[j])
		def ddist(self,day1,day2):
			c=self.df.index()
			if (day1 in c) and (day2 in c):
				return self.distance(self.df[day1],self.df[day2])
			else:
				return None,None
		def idistOther(self,i,other_list):
			return self.distance(self.df.iloc[i],other_list)
		def daydistOther(self,day1,other_list):
			c=self.df.index()
			if (day1 in c) :
				return self.distance(self.df[day1],other_list)
			else:
				return None,None

		def toDataframe(self):
			#Expand dataframe from columns with list element.
			return self.df.apply(lambda x: pd.Series(x))

		def describe(self):
			return self.toDataframe().describe()
			
		def mean(self):
			return self.df.apply(lambda x:np.array(x).mean())
		
		def std(self):
			return self.df.apply(lambda x:np.array(x).mean())

		def sum(self):
			return self.df.apply(lambda x:np.sum(np.array(x)))
        
		def norm(self):
			return self.df.apply(lambda x: ((np.array(x)-np.array(x).mean())/np.array(x).std()).tolist())
			
			



class amanecer:
	def __init__(self,path):
		c=pd.read_csv(path,sep=';',parse_dates=True,index_col=0)
		self.df=c.reindex(pd.date_range(c.index[0],c.index[-1],freq='D'))
		
class tiempo:
	def __init__(self,path):
		c=pd.read_csv(path,sep=';',parse_dates=True,index_col=1)
		s=c.reindex(pd.date_range(c.index[0],c.index[-1],freq='D'))
		self.df=s.loc[:,'Tmax':'Prec4']
	
		

def StructOfData(path,serie,dbg=1):
	#Get All files of every campus
	h={} # Campus is the key
	for r,d,f in os.walk(path):
		if len(d)<1: #Haven't any dir
			(head,tail)=os.path.split(r)
			h[tail]={}
			for fl in f:
				(head,tailf)=os.path.split(fl)
				tailf.split('.')[0]
				if dbg:
					print r+'/'+fl
				try:
					h[tail][tailf.split('.')[0]]=serie(r+'/'+fl) # For every campus all building-meter
				except Exception as inst:
					print type(inst)
	return h
	
def LoadAllConsumer(folder='consumos',hstart=5):
    h=StructOfData(folder,consumo,0)
    hdaysAll={}
    for campus in h.keys():
        hdaysAll[campus]={}
        for building in h[campus].keys():
            hdaysAll[campus][building]=h[campus][building].forfullday(hstart)
    return hdaysAll

def WorkWeekendDay (ts,factor=1.20):
    hd=ts[ts.index.dayofweek>=5] #get weekend days
    cut_work=day24HTS(hd).mean().mean()*factor #minimum energy for work day
    wdays=day24HTS(ts) # work days
    workdays=wdays.df[wdays.mean()>=cut_work] # work days are not holidays
    holidays=wdays.df[wdays.mean()<cut_work]
    return workdays,holidays
    
def compact(l): #Compact deformation list from DTW
	lo=len(l)
	s=[]
	s.append(l[0])
	s=l[1:]
	while len(l):
		if l[0][0]==s[-1][0]:
			if type(s[-1][1])!=list:
				s[-1]=(l[0][0],[s[-1][1],l[0][1]])
			else:
				s[-1]=(l[0][0],s[-1][1]+[l[0][1]])
			l=l[1:]
			continue
		if l[0][1]==s[-1][1]:
			if type(s[-1][0])!=list:
				s[-1]=([s[-1][0],l[0][0]],l[0][1])
			else:
				s[-1]=(s[-1][0]+[l[0][0]],l[0][1])
			l=l[1:]
			continue
		s.append(l[0])
		l=l[1:]
	return s[lo-1:]
