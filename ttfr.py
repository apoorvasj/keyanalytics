from github import Github, RateLimitExceededException
import time
from datetime import timedelta

access_token = "your token" #your GITHUB access token
g = Github(access_token,retry=10,timeout=15)
request_delay=1

#time to first review for a specific PR
def time_to_first_review(reponame, prnumber):


    #time between when the PR was submitted to the time of first comment from reviewer

    while True:
        try:
    
            repo=reponame
            pr=repo.get_pull(prnumber)
            
            pr_time= pr.created_at
            comments=list(pr.get_review_comments())

            
            if(pr.get_review_comments().totalCount>0):
                commentsdict={}
                for comment in comments:
                    commentsdict[comment.id]=[comment.body,comment.created_at]
                
                #first review comment created at
                review_time=comments[0].created_at 
                
                #ttfr- time to first review
                ttfr= review_time-pr_time
                
                print(f"Time to first review for PR: {pr.title} is:" ,review_time-pr_time)
                return ttfr
            
            else:
                print(f"This PR: {pr.title} has not been reviewed yet.")
                return None
        
        except RateLimitExceededException as e:
             print(e.status)
             print('rate limit exceeded')
             time.sleep(300)
             continue
        finally:
             time.sleep(request_delay)
             
        

def average_ttfr(reponame):
    repo=reponame
    prs=repo.get_pulls(state='all')
    ttfrlist=[]
    prtitle=[]

    try:
        for pr in prs:
            
                if(pr.get_review_comments().totalCount>0):
                    time=time_to_first_review(repo, pr.number)
                    ttfrlist.append(time)
                    prtitle.append(pr.title)

    except RateLimitExceededException as e:
                print(e.status)
                print('Rate limit exceeded')
                time.sleep(300)
                    

    avg=sum(ttfrlist,timedelta())/len(ttfrlist)
            
    print("The fastest PR review was:",prtitle[ttfrlist.index(min(ttfrlist))], "which took:",min(ttfrlist))
    print("The PR review which took the most time was:",prtitle[ttfrlist.index(max(ttfrlist))], "which took:",max(ttfrlist))
    print("The total size of pull requests is:", prs.totalCount)
    print("The average time to first review is:", avg)


reponame="enter a repo name here" #Ex:"vipulgupta2048/vanilla"
prnumber=50 #enter your own prnumber here
reponame=g.get_repo(reponame)
time_to_first_review(reponame,prnumber)
average_ttfr(reponame)




