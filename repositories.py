import json
import os
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

github_token= os.environ.get("GITHUB_TOKEN")

if github_token is None:
    print("Error: you need to create the GITHUB_TOKEN environment variable")
    exit()

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers={'Authorization': 'token ' + github_token})

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query = gql(
    """
    query getRepo($afterCursor: String){
        search(
            type:REPOSITORY, 
            query: "is:public stars:>5000 language:python",
            first: 100,
            after: $afterCursor
        ) {
        pageInfo {
            startCursor
            hasNextPage
            endCursor
        }
        repos: edges {
            repo: node {
                ... on Repository {
                url
                languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
                    edges {
                        size
                        node {
                            name
                        }
                    }
                }
                primaryLanguage {
                    name
                }
                stargazerCount
                id
                owner {
                    login
                }
                name
                }
            }
        }
    }
}
"""
)

repos = []
params = {"afterCursor" : None}

# Execute the query on the transport
for i in range (0,10):
    result = client.execute(query, variable_values=params)
    print("Fetched " + str((i+1)*100) + " repositories");
    repos += result["search"]["repos"]
    if not result["search"]["pageInfo"]["hasNextPage"]:
        break
    params = {"afterCursor" : result["search"]["pageInfo"]["endCursor"]}
exit()
# Write to disk
json_file = open("./data/repositories.json", "w")
n = json_file.write(json.dumps(repos))
json_file.close()

