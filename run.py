import argparse
import json
import time

from src.archicad import ArchicadWrapper
from src.bcf import BCFWrapper
from src.speckle import SpeckleWrapper

ts = time.time()

cmd = argparse.ArgumentParser()
cmd.add_argument('-p', '--port', required=False, help='archicad port')
arg = cmd.parse_args()

arc = ArchicadWrapper()

spk = SpeckleWrapper()
stream = spk.client.stream.search('aeb487f0e6')[0]
commit = spk.retrieve('aeb487f0e6', '784ad6fdb5')

bcf = BCFWrapper('C:\\Users\\i.yurasov\\Desktop\\dev\\_tmp\\issues.bcfzip')
issues = bcf.read()

for issue in issues:
	selectedIds = []
	for selectedId in issue['viewpoint']['selected']:

		element = spk.search('aeb487f0e6', '2dc7ca66f4beea3850e6392dd2926a76', selectedId)
		if element:
			selectedIds.append((selectedId, element[0]['id']))

	if selectedIds:
		midIndex = round(len(selectedIds)/2)
		midId = {'elementId': {'guid': selectedIds[midIndex][0]}}
		bbox = arc.commands.Get3DBoundingBoxes([midId])
		bbox_x = (bbox[0].boundingBox3D.xMax + bbox[0].boundingBox3D.xMin) / 2
		bbox_y = (bbox[0].boundingBox3D.yMax + bbox[0].boundingBox3D.yMin) / 2
		bbox_z = (bbox[0].boundingBox3D.zMax + bbox[0].boundingBox3D.zMin) / 2
		cameraTarget = [
			bbox_x,
			bbox_y,
			bbox_z
		]
	else:
		cameraTarget = [
			issue['viewpoint']['camera_direction']['x'],
			issue['viewpoint']['camera_direction']['y'],
			issue['viewpoint']['camera_direction']['z']
		]

	comment = spk.create_comment(
		projectId='aeb487f0e6',
		title = issue['markup']['Title'],
		modelId = '0425408de2',
		cameraPosition = [
			issue['viewpoint']['camera_viewpoint']['x'],
			issue['viewpoint']['camera_viewpoint']['y'],
			issue['viewpoint']['camera_viewpoint']['z']
		],
		cameraTarget = cameraTarget,
		selectedObjectIds = [s[1] for s in selectedIds]
	)

print(f'\n{round(time.time() - ts, 2)} sec')