import pandas as pd
from datetime import timedelta

def compute_stats(pathname):
    
    df=pd.read_csv(pathname)
    ttfr_list=[]
    prtitle=[]
    
    for i in range (len(df['TTFR'])):
        ttfr_list.append(pd.to_timedelta(df['TTFR'][i]))
        prtitle.append(df['PR Title'][i])

    average_time=sum(ttfr_list,timedelta())/len(ttfr_list)

    print("The fastest PR review was:",prtitle[ttfr_list.index(min(ttfr_list))], "which took:",min(ttfr_list))
    print("The PR review which took the most time was:",prtitle[ttfr_list.index(max(ttfr_list))], "which took:",max(ttfr_list))
    print("The total size of pull requests is:", len(prtitle))
    print("The average time to first review is:", average_time)
    
if __name__=='__main__':
    pathname=r"enter path to your file" #Ex: "C:\Users\My PC\Downloads\githubwrite.csv"
    compute_stats(pathname)
