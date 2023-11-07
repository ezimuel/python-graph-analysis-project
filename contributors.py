import json
import csv
import os
import requests

github_token= os.environ.get("GITHUB_TOKEN")

if github_token is None:
    print("Error: you need to create the GITHUB_TOKEN environment variable")
    exit()

# Using an access token for github API
headers = {
    "Authorization": "Bearer " + github_token,
    "X-GitHub-Api-Version": "2022-11-28"
}

# Get all the contributors of popular projects (>5k stars)
with open("./data/repositories.json","r") as file:
    repositories = json.load(file)

for repo in repositories:
    reponame = "%s/%s" % (repo["repo"]["owner"]["login"], repo["repo"]["name"])
    repofile = "./data/%s+%s.csv" % (repo["repo"]["owner"]["login"], repo["repo"]["name"])
    
    if (os.path.isfile(repofile)):
        continue
    
    list_contributors = []
    print("Contributors of %s ... " % (reponame), end="")
    for page in range(1,4):
        response = requests.get("https://api.github.com/repos/%s/contributors?per_page=100&page=%d" % (reponame, page), headers=headers)
        if (response.status_code == 403):
            print ("Error too many contributors")
            break    
        contributors = response.json()
        list_contributors += [c["login"] for c in contributors]

    if (response.status_code == 403):
        continue

    f = open(repofile,"w")
    writer = csv.writer(f)
    writer.writerow(list_contributors)
    f.close()
    print("done")

