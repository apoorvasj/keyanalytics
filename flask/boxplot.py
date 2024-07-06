import matplotlib.pyplot as plt
import pandas as pd
import math
import io

#plotting function
def plot(filename, xlabel, ylabel, title):
    
    df=pd.read_csv(filename)
    print(df.head())
    print(df.columns)

    #convert required columns to datetime and timedelta objects
    df.TTFR=pd.to_timedelta(df.TTFR)
    df['Created at']= pd.to_datetime(df['Created at'])

    #create a new dataframe containing just the data you need
    df1=pd.DataFrame({'Created_at':df['Created at'],'TTFR':df.TTFR})

    #setting new index for grouping purposes
    df1.set_index('Created_at', inplace=True)
    
    df1.TTFR= df1.TTFR.dt.total_seconds()/(3600) #hours conversion
    print(df1.TTFR)

    list_week=[]
    list_ttfr=[]
    
    #Group using week
    df2=df1.groupby([pd.Grouper(level=0,freq='168h')])
    
    #The groupby function returns an iterable object which contains the group heading and the grouped dataframe

    for duration, duration_df in df2:
        #print(duration)
        #print(duration_df)
        if not duration_df.empty:
            list_ttfr.append(duration_df.TTFR)
    
   
    #grouping to extract the week strings
    df3=df1.groupby([pd.Grouper(level=0,freq='168h')]).median()
    
    #formatting the dates to look like 06-07 - 06-14
    df3.index = df3.index.map(lambda x: f"{x.strftime('%m-%d')} - {(x + pd.DateOffset(days=7)).strftime('%m-%d')}")
    
    #appending to a list so i can use it as an xtick later on.
    count=0
    for index in df3.index:
        
        row = df3.loc[index]
        if not (math.isnan(row[count])):
            print(index)
            list_week.append(index)
    
    #preparing for subplots    
    
    fig= plt.figure(figsize=(10,7))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    bp=ax.boxplot(list_ttfr, flierprops=dict(markeredgecolor='red'))

    #change 1,2,3,4 x-ticks to custom x_tick
    plt.xticks(range(1,len(list_ttfr)+1),list_week)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()



    #the below lines were just to check if the median of the groups was correctly matching the boxplots. 
    #uncomment if you wish to verify median for each week.

    df4=df1.groupby([pd.Grouper(freq='168h')]).median()
    print(df4)
    
    img = io.StringIO()
    fig.savefig(img, format='svg')
    #clip off the xml headers from the image
    svg_img = '<svg' + img.getvalue().split('<svg')[1]
    return svg_img

if __name__=='__main__':
    pathname=r"enter path name" #Ex: "C:\Users\My PC\Downloads\githubwrite.csv"
    reponame=r"xyz"     #enter your repo name
    xlabel= 'Week'
    ylabel= 'TTFR (hours)'
    title= f'TTFR in the month of June 2024 for Repository {reponame}'
    
    plot(pathname,xlabel,ylabel,title)