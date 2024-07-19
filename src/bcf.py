import os
import zipfile
import xml.etree.ElementTree as xet

class BCFWrapper():

	def __init__(self, filepath):

		try:
			os.path.isfile(filepath)
			self.filepath = filepath
			print (f'BCF file found: {self}')
		except Exception as e:
			raise e

	@staticmethod
	def parse_markup(xml):
		root = xet.fromstring(xml)
		topic = root.find('Topic')

		markup = {
			'TopicStatus': topic.get('TopicStatus'),
			'TopicType': topic.get('TopicType'),
			'CreationDate': topic.find('CreationDate').text,
			'CreationAuthor': topic.find('CreationAuthor').text,
			'Title': topic.find('Title').text,
			'Priority': topic.find('Priority').text,
			'Labels': topic.find('Labels').text
		}
		return markup if markup else None

	@staticmethod
	def parse_viewpoint(xml):
		root = xet.fromstring(xml)
		selectedIds = []
		for component in root.findall('.//Component[@Selected="true"]'):
		    elemId = component.find('AuthoringToolId').text
		    selectedIds.append(elemId)

		camera_viewpoint = root.find('.//CameraViewPoint')
		camera_direction = root.find('.//CameraDirection')

		viewpoint = {
			'selected': selectedIds,
			'camera_viewpoint': {
				'x': camera_viewpoint.find('X').text,
				'y': camera_viewpoint.find('Y').text,
				'z': camera_viewpoint.find('Z').text
			},
			'camera_direction': {
				'x': camera_direction.find('X').text,
				'y': camera_direction.find('Y').text,
				'z': camera_direction.find('Z').text
			}
		}
		return viewpoint if viewpoint else None

	def read(self):
		issues = []
		with zipfile.ZipFile(self.filepath, 'r') as zipped:
			for item in zipped.namelist():
				path = item.split('/')
				if len(path)>1 and path[1] in ['markup.bcf', 'viewpoint.bcfv']:
					issueId = path[0]

					propSet = path[1].split('.')[0]
					parser = getattr(BCFWrapper, 'parse_' + propSet)
					with zipped.open(item) as xml:
						data = parser(xml.read())

					if issues and issues[-1].get('guid') == issueId:
						issues[-1][propSet] = data
					else:
						issues.append({'guid': issueId, **{propSet: data}})

		return issues