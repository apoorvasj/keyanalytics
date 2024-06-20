from github import Github
import pandas as pd

#function to get first_x_pulls
def access(count):

    access_key="your access key"
    g=Github(access_key,retry=10,timeout=15)
    reponame="apache/beam" #enter any reponame here
    repo=g.get_repo(reponame)
    pulls=repo.get_pulls(state='all')
    
    
    first_x_pulls=[]
  
    if(pulls):
        for i in range(count):

            first_x_pulls.append(pulls[i])
        return first_x_pulls

#function to get details of the PR

def getDetails(pulls,reponame):
    prtime=None
    reviewtime=None
    ttfr=None
    details=[]
    
    #print("Length of pulls is", len(pulls))
    
    for pr in pulls:
            
        try:
            #if PR has been reviewed             
            comments=pr.get_review_comments()
            prtime=pr.created_at
            reviewtime=comments[0].created_at
            ttfr= reviewtime-prtime
            details.append([reponame,pr.title,pr.number,prtime,reviewtime,ttfr])
            

        except IndexError:
            #PR has not been reviewed 
            print(f"No review comments in PR #{pr.number}")
            continue            
               
    return details      
        
    
#function to write the details to a csv file

def datatocsv(details,path_name):
    #each list represents a row in the dataframe
    
    df=pd.DataFrame(details,columns=["Repository Name","PR Title","PR Number","Created at","First Review at","TTFR"])
    df.to_csv(f"{path_name}")

if __name__=='__main__':
    
    count=20 #change count according to number of Pull Requests you want    
    first_x=access(count)    
    details=getDetails(first_x,"Apache/Github")  
    datatocsv(details,r"C:\Users\My PC\Downloads\githubwrite.csv")

