from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.api import operations
from specklepy.transports.server import ServerTransport
from specklepy.serialization.base_object_serializer import BaseObjectSerializer

import json
import requests
from gql import gql

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


	def query(self, query, variables):
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
	    return response.json() if response.status_code == 200 else None

	def retrieve(self, streamId, commitId):

		commit = self.client.commit.get(streamId, commitId)
		transport = ServerTransport(client=self.client, stream_id=streamId)
		if transport:
			self.transport = transport
			result = operations.receive(commit.referencedObject, self.transport)

		return result

	def search(self, projectId, objectId, applicationId):
		query_str = '''
			query Object($objectId: String!, $projectId: String!, $query: [JSONObject!], $select: [String]) {
			  project(id: $projectId) {
			    object(id: $objectId) {
			      id
			      speckleType
			      children(query: $query, select: $select) {
			        objects {
			          id
			          speckleType
			          data
			        }
			      }
			    }
			  }
			}
		'''

		variables = {
		 "projectId": projectId,
		  "objectId": objectId,
		  "query": [
		    {
		      "field": "applicationId",
		      "value": None,
		      "operator": "<"
		    },
		    {
		      "field": "applicationId",
		      "value": applicationId,
		      "operator": "="
		    }
		  ],
		  "select": "applicationId",
		}

		data = self.query(query_str, variables)
		return data['data']['project']['object']['children']['objects'] if data and 'data' in data else None


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

		data = self.query(query_str, variables)
		return data["data"] if data and "data" in data else None

	def add_thread(self, projectId, title, modelId, cameraPosition=[], cameraTarget=[], selectedObjectIds=[]):
		query_str = '''
			mutation Create($input: CreateCommentInput!) {
			  commentMutations {
			    create(input: $input) {
			      id
			    }
			  }
			}
		'''

		variables = {
			  "input": {
			    "projectId": projectId,
			    "content": {
			      "doc": {
			        "type": "doc",
			        "content": [
			          {
			            "type": "paragraph",
			            "content": [
			              {
			                "type": "text",
	                    "marks": [
	                      { "type": "bold" },
	                      { "type": "underline" }
	                    ],
			                "text": title
			              }
			            ],
			          }
			        ],
			      }
			    },
			    "resourceIdString": modelId,

          "viewerState": {
              "projectId": projectId,
              "resources": {
                  "request": {
                      "resourceIdString": f"{modelId}",
                      "threadFilters": {},
                  }
              },
              "sessionId": "qwerty",
              "ui": {
                  "camera": {
                      "isOrthoProjection": False,
                      "position": cameraPosition,
                      "target": cameraTarget,
                      "zoom": 1,
                  },
                  "explodeFactor": 0,
                  "filters": {
                      "hiddenObjectIds": [],
                      "isolatedObjectIds": [],
                      "propertyFilter": {"isApplied": False, "key": None},
                      "selectedObjectIds": selectedObjectIds,
                  },
                  "lightConfig": {
                      "azimuth": 0.75,
                      "castShadow": True,
                      "color": 16777215,
                      "elevation": 1.33,
                      "enabled": True,
                      "indirectLightIntensity": 1.2,
                      "intensity": 5,
                      "radius": 0,
                      "shadowcatcher": True,
                  },
                  "sectionBox": None,
                  "selection": [],
                  "spotlightUserSessionId": None,
                  "threads": {
                      "openThread": {
                          "isTyping": False,
                          "newThreadEditor": True,
                          "threadId": None,
                      }
                  },
              },
              "viewer": {"metadata": {"filteringState": {}}},
          }

			  }
		}

		data = self.query(query_str, variables)
		return data["data"] if data and "data" in data else None

	def add_reply(self, threadId, message):
		query_str = '''
			mutation Reply($input: CreateCommentReplyInput!) {
			  commentMutations {
			    reply(input: $input) {
			      id
			    }
			  }
			}
		'''

		variables = {
		  "input": {
		    "threadId": threadId,
		    "content": {
		      "doc": {
		        "type": "doc",
		        "content": [
		          {
		            "type": "paragraph",
		            "content": [
		              {
		                "type": "text",
		                "text": message
		              }
		            ],
		          }
		        ],
		      }
		    },
		  }
		}

		data = self.query(query_str, variables)
		return data["data"] if data and "data" in data else None



		# 452603c094db077eff44f7688f66e490

