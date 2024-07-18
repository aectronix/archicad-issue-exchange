from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.api import operations

import json
import requests
from gql import gql

JSON_OBJ = {
  "projectId": "aeb487f0e6",
  "viewer": {
    "metadata": {
      "filteringState": None
    }
  },
  "ui": {
    "diff": {
      "mode": 1,
      "time": 0.5,
      "command": None
    },
    "camera": {
      "zoom": 1,
      "target": [
        8.875,
        6.924999833106995,
        2.8249998092651367
      ],
      "position": [
        33.53323452754469,
        31.573644656081974,
        27.49500210465433
      ],
      "isOrthoProjection": False
    },
    "filters": {
      "propertyFilter": {
        "key": None,
        "isApplied": False
      },
      "hiddenObjectIds": [],
      "isolatedObjectIds": [],
      "selectedObjectIds": [
        "23a1e73f40b01ff830dff4a3f5cd20bd"
      ]
    },
    "threads": {
      "openThread": {
        "isTyping": True,
        "threadId": None,
        "newThreadEditor": True
      }
    },
    "selection": [
      13.8943768419011,
      -2.0502114496201798,
      8.125000002980233
    ],
    "sectionBox": None,
    "lightConfig": {
      "color": 16777215,
      "radius": 0,
      "azimuth": 0.75,
      "enabled": True,
      "elevation": 1.33,
      "intensity": 5,
      "castShadow": True,
      "shadowcatcher": True,
      "indirectLightIntensity": 1.2
    },
    "measurement": {
      "enabled": False,
      "options": {
        "visible": True,
        "type": 1,
        "vertexSnap": True,
        "units": "m",
        "precision": 2
      }
    },
    "explodeFactor": 0,
    "spotlightUserSessionId": None
  }
}

class SpeckleWrapper():

	def __init__(self, host="https://app.speckle.systems"):

		self.host = host
		self.client = None
		self.transport = None
		self.token = None

		self.connect();

	def connect(self):

		try:
			client = SpeckleClient(self.host)
			account = get_default_account()
			client.authenticate_with_account(account)
			if account and client:
				self.token = account.token
				self.client = client
				print(f'Connected to Speckle: {client}')
		except Exception as e:
			raise e

	def speckle_graphql_query(self, query, variables):
	    """
	    Sends a GraphQL query to the Speckle server and returns the response.

	    Args:
	        query (str): The GraphQL query.
	        variables (dict, optional): The variables for the GraphQL query. Defaults to None.

	    Returns:
	        dict: The response data if the request is successful, None otherwise.
	    """
	    url = f"{self.host}/graphql"
	    payload = {"query": query, "variables": variables}
	    headers = {"Authorization": self.token, "Content-Type": "application/json"}

	    response = requests.post(url, json=payload, headers=headers)
	    print (response.content)
	    return response.json() if response.status_code == 200 else None

	def get_comments(self, stream):
		query = gql(
			"""{
			comments(streamId:\""""
			+ stream.id + 
			"""\", archived: true) {
				items {
				id
				rawText
				authorId
				createdAt
				data
				resources{
					resourceId
				}
				}
			}
			}"""
		)

		data = self.speckle_graphql_query(query_str, variables)
		return data["data"] if data and "data" in data else None

	def create_comment(self):
		query_str = '''
			mutation Create($input: CreateCommentInput!) {
			  commentMutations {
			    create(input: $input) {
			      rawText
			    }
			  }
			}
		'''

		variables = {
			  "input": {
			    "projectId": "aeb487f0e6",
			    "content": {
			      "doc": {
			        "type": "doc",
			        "content": [
			          {
			            "type": "paragraph",
			            "content": [
			              {
			                "type": "text",
			                "text": "Another try 4"
			              }
			            ],
			          }
			        ],
			      }
			    },
			    "resourceIdString": "2de5096922@c433d9628f",

	            "viewerState": {
	              "projectId": "aeb487f0e6",
	              "sessionId": xxxxxxxxxxxx
	              "viewer": {
	                "metadata": {
	                  "filteringState": None
	                }
	              },
	              "resources": {
	                "request": {
	                  "threadFilters": {
	                    "includeArchived": False,
	                    "loadedVersionsOnly": True
	                  },
	                  "resourceIdString": "2de5096922@c433d9628f"
	                }
	              },
	              "ui": {
	                "diff": {
	                  "mode": 1,
	                  "time": 0.5,
	                  "command": None
	                },
	                "camera": {
	                  "zoom": 1,
	                  "target": [
	                    8.875,
	                    6.924999833106995,
	                    2.8249998092651367
	                  ],
	                  "position": [
	                    33.53323452754469,
	                    31.573644656081974,
	                    27.49500210465433
	                  ],
	                  "isOrthoProjection": False
	                },
	                "filters": {
	                  "propertyFilter": {
	                    "key": None,
	                    "isApplied": False
	                  },
	                  "hiddenObjectIds": [],
	                  "isolatedObjectIds": [],
	                  "selectedObjectIds": [
	                    "23a1e73f40b01ff830dff4a3f5cd20bd"
	                  ]
	                },
	                "threads": {
	                  "openThread": {
	                    "isTyping": True,
	                    "threadId": None,
	                    "newThreadEditor": True
	                  }
	                },
	                "selection": [
	                  13.8943768419011,
	                  -2.0502114496201798,
	                  8.125000002980233
	                ],
	                "sectionBox": None,
	                "lightConfig": {
	                  "color": 16777215,
	                  "radius": 0,
	                  "azimuth": 0.75,
	                  "enabled": True,
	                  "elevation": 1.33,
	                  "intensity": 5,
	                  "castShadow": True,
	                  "shadowcatcher": True,
	                  "indirectLightIntensity": 1.2
	                },
	                "measurement": {
	                  "enabled": False,
	                  "options": {
	                    "visible": True,
	                    "type": 1,
	                    "vertexSnap": True,
	                    "units": "m",
	                    "precision": 2
	                  }
	                },
	                "explodeFactor": 0,
	                "spotlightUserSessionId": None
	              }
	            }

			  }
		}

		data = self.speckle_graphql_query(query_str, variables)
		return data["data"] if data and "data" in data else None



		# 452603c094db077eff44f7688f66e490

