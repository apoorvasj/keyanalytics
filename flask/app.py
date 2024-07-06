from flask import Flask, request, render_template, redirect
from datacollection import get_x_pulls, get_pull_details, datatocsv
from stats import collectstats
from boxplot import plot
#from stats import visualiseboxplot


app=Flask(__name__)
filename=r"C:\Users\My PC\Downloads\github_stats.csv" #enter any filename here

@app.route('/')
def index():
    return redirect('/collect')

@app.route('/collect', methods=['POST','GET'])
def my_form_page():
    if request.method=='POST':
        
        reponame=request.form['name']
        print(reponame)
        count=int(request.form['count'])
        access_key='your access key' #enter your API access key here    
        pulls=get_x_pulls(count,reponame,access_key)
        res=get_pull_details(pulls,reponame)
        datatocsv(res,filename)
        
        return redirect('/result')
    return render_template('page.html')

@app.route('/result', methods=['POST','GET'])
def results():
    
    plotted_img=plot(filename,'Week','TTFR (hours)','TTFR trend')
    avg=collectstats(filename)
    return render_template('drawgraphs.html',plot=plotted_img,average=avg)
    
if __name__=='__main__':
    app.run(debug=True)

