from github import Github

# for os enviorment 
import os

# setting up your github token to access github
# used instaed of login id password
token = os.environ.get("Github_Token")

# passing the token for accessing
g = Github(token)

# kind of like accessing the content of a list using from
# gives us a list of repos in the account
# for repo in g.get_user().get_repos():
    # print(repo.full_name)

problem1 = "acmjec/CompetitiveCoding_Hacktoberfest2024/blob/main/JP%20Morgan/problem11.md"
pronlem2 = "acmjec/CompetitiveCoding_Hacktoberfest2024/blob/main/JP%20Morgan/problem9.md"
problem3 = "acmjec/CompetitiveCoding_Hacktoberfest2024/blob/main/JP%20Morgan/problem8.md"
problem4 = "acmjec/CompetitiveCoding_Hacktoberfest2024/blob/main/JP%20Morgan/problem7.md"
problem5 = "acmjec/CompetitiveCoding_Hacktoberfest2024/blob/main/JP%20Morgan/problem10.md"

# initializing the repo
repo = g.get_repo("acmjec/CompetitiveCoding_Hacktoberfest2024")

# getting content of the repo
content = repo.get_contents("")
for content_file in content:
    print(content_file)