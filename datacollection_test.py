import datacollection
from datacollection import get_x_pulls, get_pull_details, datatocsv
import unittest
from unittest.mock import MagicMock, patch
import datetime

@patch('datacollection.Github')
class TestDataCollection(unittest.TestCase):
    
    #function to construct a mock PR
    def construct_mockPR(self,mock_Github):
        
        mock_github_object=MagicMock()
        mock_Github.return_value= mock_github_object
        
        PR1=MagicMock(title="Test PR",
                      number=1,
                      created_at=datetime.datetime(2024,6,14,11,29,15))
    
        #mocking the paginated list that is returned by get_pulls function
        mock_pulls=[PR1,PR1]
        mock_github_object.get_repo().get_pulls.return_value=mock_pulls
        
        return PR1
    
    
    #function to construct a mock review comment
    def construct_mock_comment(self, PR):
        comments_PR1=[MagicMock(body="PR1 c1",
                                           created_at=datetime.datetime(2024,6,14,12,29,15)),

                                 MagicMock(body="PR1 c2",
                                           created_at=datetime.datetime(2024,6,14,13,29,15)) ]
        
        PR.get_review_comments.return_value= comments_PR1
        
        return comments_PR1       
            
            
    #test for Single PR with comments
    def test_single_pr(self,mock_Github):
        
        PR1= self.construct_mockPR(mock_Github)
        
        comments_PR1=self.construct_mock_comment(PR1)
        x=PR1.created_at
        y=comments_PR1[0].created_at
        
        mock_pulls=get_x_pulls(1,"Mock Repo","")
        pull_details=get_pull_details(mock_pulls, "Mock Repo")
        
        self.assertEqual(pull_details, 
                         [["Mock Repo","Test PR",1,x,y,str(y-x)]])
        
        datatocsv(pull_details,r"C:\Users\My PC\Downloads\singlepr.csv")
        
        
    #test for Single PR with no comments
    def test_single_pr_nocomments(self,mock_Github):

        PR1= self.construct_mockPR(mock_Github)
        
        #empty list signifies there are no comments in this PR 
        PR1.get_review_comments.return_value= []
        
        mock_pulls=get_x_pulls(1,"Mock Repo","")
        pull_details=get_pull_details(mock_pulls, "Mock Repo")

        #Empty List if no comments        
        self.assertEqual(pull_details,[])
    
    
    #test for multiple PRs with comments
    def test_multiple_prs(self,mock_Github):
        
        PR1= self.construct_mockPR(mock_Github)
        PR2= self.construct_mockPR(mock_Github)
        
        comments_PR1= self.construct_mock_comment(PR1)
        comments_PR2= self.construct_mock_comment(PR2)
        
        
        x1=PR1.created_at
        y1=comments_PR1[0].created_at
        x2=PR2.created_at
        y2=comments_PR2[0].created_at
        
        mock_pulls=get_x_pulls(2,"Mock Repo","")
        pull_details=get_pull_details(mock_pulls, "Mock Repo")
        
        self.assertEqual(pull_details, 
                         [["Mock Repo","Test PR",1,x1,y1,str(y1-x1) ],
                          ["Mock Repo","Test PR",1,x2,y2,str(y2-x2) ]
                          ])
        
        datatocsv(pull_details,r"C:\Users\My PC\Downloads\multipr.csv")
    
    
    #test for multiple PRs with no comments   
    def test_multiple_prs_nocomments(self,mock_Github):
        
        PR1= self.construct_mockPR(mock_Github)
        PR2= self.construct_mockPR(mock_Github)
        
        #empty list signifies there are no comments in this PR 
        PR1.get_review_comments.return_value= []
        PR2.get_review_comments.return_value= []
        
        mock_pulls=get_x_pulls(2,"Mock Repo","")
        pull_details=get_pull_details(mock_pulls, "Mock Repo")

        #Empty List if no comments        
        self.assertEqual(pull_details,[])

     
if __name__=='__main__':
    unittest.main()
    