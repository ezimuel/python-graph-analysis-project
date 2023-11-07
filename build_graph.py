import json
import csv
import os
import igraph as ig

# Intersection of two lists using set()
def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

with open("./data/repositories.json","r") as file:
    repositories = json.load(file)

g = ig.Graph()

repos = []
for r in repositories:
    reponame = "%s/%s" % (r["repo"]["owner"]["login"], r["repo"]["name"])
    repofile = "./data/%s+%s.csv" % (r["repo"]["owner"]["login"], r["repo"]["name"])
    if (not os.path.isfile(repofile)):
        continue

    f = open(repofile,"r")
    contributors = [c for c in csv.reader(f)]
    f.close()
    
    try:
        language = r["repo"]["primaryLanguage"]["name"]
    except TypeError:
        language = None

    repos.append({
        "name": reponame,
        "stars": r["repo"]["stargazerCount"],
        "primaryLanguage": language,
        "contributors": contributors
    })
    # Add vertex in the graph
    g.add_vertex(name=reponame, language=language, stars=r["repo"]["stargazerCount"])
   
# Add edges
for start in range(0,len(repos)-1):
    for i in range(start+1,len(repos)):
        common = intersection(repos[start]["contributors"][0], repos[i]["contributors"][0])
        if len(common) > 0:
            # add an edge with a weight equal to the number of common contributors
            g.add_edge(repos[start]["name"], repos[i]["name"], weight=len(common))

g.write_graphml("network.graphml")
