import datacollection1
from datacollection1 import access, getDetails, datatocsv
import unittest
from unittest.mock import MagicMock, patch
import datetime


@patch("datacollection1.Github")
class TestDataCollection(unittest.TestCase):
    
    #function to construct mock pull requests
    
    def construct_mockPRs(self, mock_Github, multiple_prs=False, comments=False):

        mock_github_object = MagicMock()
        mock_Github.return_value = mock_github_object
          
        #mock PRs
        
        PR1 = MagicMock(
            title="Test PR 1",
            number=1,
            created_at=datetime.datetime(2024, 6, 14, 11, 29, 15),
        )

        PR2 = MagicMock(
            title="Test PR 2",
            number=2,
            created_at=datetime.datetime(2024, 6, 14, 13, 29, 15),
        )

        mock_pulls = [PR1, PR2]
        mock_github_object.get_repo().get_pulls.return_value = mock_pulls
        
        #Get the first x number of pulls
        pulls_list = access(2)
        
        #mock comments for pull requests

        comments_PR1 = [
            MagicMock(
                body="PR1 c1", created_at=datetime.datetime(2024, 6, 14, 12, 29, 15)
            ),
            MagicMock(
                body="PR1 c2", created_at=datetime.datetime(2024, 6, 14, 13, 29, 15)
            ),
        ]
        comments_PR2 = [
            MagicMock(
                body="PR2 c1", created_at=datetime.datetime(2024, 6, 14, 13, 29, 15)
            ),
            MagicMock(
                body="PR2 c2", created_at=datetime.datetime(2024, 6, 14, 13, 29, 15)
            ),
        ]

        PR1.get_review_comments.return_value = comments_PR1
        PR2.get_review_comments.return_value = comments_PR2
        
        #return values based on number of PRs and comments
        
        #Multiple PRs with review comments
        
        if (comments) and (multiple_prs):
            return pulls_list, PR1, PR2, comments_PR1, comments_PR2
        
        #Single PR with review comments

        elif (comments) and (not multiple_prs):
            pulls_list.remove(pulls_list[-1])
            return pulls_list, PR1, comments_PR1
        
        #Multiple PRs with no review comments

        elif (not comments) and multiple_prs:
            PR1.get_review_comments.return_value = []
            PR2.get_review_comments.return_value = []
            return pulls_list
        
        #Single PR with no comments
        else:
            PR1.get_review_comments.return_value = []
            pulls_list.remove(pulls_list[-1])

            return pulls_list


    #test for Single PR with comments
    
    def test_single_pr(self, mock_Github):
        
        pulls_list, PR1, comments_PR1 = self.construct_mockPRs(
            mock_Github, multiple_prs=False, comments=True
        )

        x = PR1.created_at
        y = comments_PR1[0].created_at
        pull_details = getDetails(pulls_list, "Mock Repo")
        self.assertEqual(pull_details, [["Mock Repo", "Test PR 1", 1, x, y, y - x]])

        datatocsv(pull_details, r"C:\Users\My PC\Downloads\singlepr.csv")
        
        
    #test for Single PR with no comments
    
    def test_single_pr_nocomments(self, mock_Github):

        pulls_list = self.construct_mockPRs(
            mock_Github, multiple_prs=False, comments=False
        )
        pull_details = getDetails(pulls_list, "Mock Repo")

        # Empty List if no comments
        self.assertEqual(pull_details, [])


    #test for multiple PRs with comments
    
    def test_multiple_prs(self, mock_Github):

        pulls_list, PR1, PR2, comments_PR1, comments_PR2 = self.construct_mockPRs(
            mock_Github, multiple_prs=True, comments=True
        )
        x1 = PR1.created_at
        y1 = comments_PR1[0].created_at
        x2 = PR2.created_at
        y2 = comments_PR2[0].created_at

        pull_details = getDetails(pulls_list, "Mock Repo")
        self.assertEqual(
            pull_details,
            [
                ["Mock Repo", "Test PR 1", 1, x1, y1, y1 - x1],
                ["Mock Repo", "Test PR 2", 2, x2, y2, y2 - x2],
            ],
        )

        datatocsv(pull_details, r"C:\Users\My PC\Downloads\multipr.csv")
        
    #test for multiple PRs with no comments
    

    def test_multiple_prs_nocomments(self, mock_Github):
        pulls_list = self.construct_mockPRs(
            mock_Github, multiple_prs=True, comments=False
        )
        pull_details = getDetails(pulls_list, "Mock Repo")

        # Empty List if no comments
        self.assertEqual(pull_details, [])


if __name__ == "__main__":
    unittest.main()
