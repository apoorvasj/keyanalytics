from github import Github
import pandas as pd
import datetime

#function to get first_x_pulls
def get_x_pulls(count,reponame,access_key):  
    
    access_key="your access key"
    g=Github(access_key,retry=10,timeout=15)
    repo=g.get_repo(f"{reponame}")
    pulls=repo.get_pulls(state='all')    
    
    latest_x_pulls=[]
  
    if(pulls):
        for i in range(count):
            print(pulls[i])
            latest_x_pulls.append(pulls[i])
        return latest_x_pulls

#function to get details of the PR

def get_pull_details(pulls,reponame):
    prtime=None
    reviewtime=None
    ttfr=None
    details=[]
    dt=datetime.datetime.now()
    
    #print("Length of pulls is", len(pulls))
    
    for pr in pulls:
        print(pr.title)
        try:
            #if PR has been reviewed             
            comments=pr.get_review_comments()
            prtime=pr.created_at
            reviewtime=comments[0].created_at
            ttfr= reviewtime-prtime
            details.append([reponame,pr.title,pr.number,prtime,reviewtime,str(ttfr)])
            

        except IndexError:
            #PR has not been reviewed 
            print(f"No review comments in PR {pr.title} #{pr.number}")
            continue            
               
    return details      
        
    
#function to write the details to a csv file

def datatocsv(details,path_name):
    #each list represents a row in the dataframe
    
    df=pd.DataFrame(details,columns=["Repository Name","PR Title","PR Number","Created at","First Review at","TTFR"])
    df.to_csv(f"{path_name}")

if __name__=='__main__':
    
    reponame="apache/beam" #change repo name here
    count=20 #change count according to number of Pull Requests you want to extract
    access_key="your access key" #enter your API key here

    latest_x=get_x_pulls(count, reponame, access_key)    
    details=get_pull_details(latest_x,reponame)  

    datatocsv(details,r"enter file path here") #Ex: C:\Users\My PC\Downloads\githubwrite2.csv
