import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io


def collectstats(filename):
    df=pd.read_csv(filename)    
    df['TTFR']=pd.to_timedelta(df.TTFR)
    average=df.TTFR.sum()/len(df['TTFR'])
    return average

    #print('average is',average)
    

'''
uncomment for bar graph instead of boxplot.

def visualiseboxplot(filename):
    
    df=pd.read_csv(filename)
    df.TTFR=pd.to_timedelta(df.TTFR)
    print(df.TTFR)
    x=df.TTFR.dt.total_seconds()
    
    #use total seconds as using just seconds ignored the day in timedelta
    print(x)
    x=x/(60*60) #convert to hours
    
    fig = Figure()
    FigureCanvas(fig)
    ax=fig.add_subplot(111)
    ax.hist(x)
    ax.set_xlabel('TTFR (hours)')
    ax.set_ylabel('Count')
    #ax.set_title(f'There are data points!')
    ax.grid(True)
    #plt.hist(x)
    #plt.show()
    img = io.StringIO()
    fig.savefig(img, format='svg')
    #clip off the xml headers from the image
    svg_img = '<svg' + img.getvalue().split('<svg')[1]
    return svg_img

'''
   
    

if __name__=='__main__':
    filename=r"C:\Users\My PC\Downloads\githubwrite.csv" #enter filepath here
    collectstats(filename)
    #visualise(filename)

