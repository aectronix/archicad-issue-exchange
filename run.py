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

spk = SpeckleWrapper()
stream = spk.client.stream.search('aeb487f0e6')[0]
commit = spk.retrieve('aeb487f0e6', '784ad6fdb5')

bcf = BCFWrapper('C:\\Users\\i.yurasov\\Desktop\\dev\\_tmp\\issues.bcfzip')
issues = bcf.read()
for issue in issues:
	selectedIds = []
	for selectedId in issue['viewpoint']['selected']:
		for i in range(0, len(commit['elements'])):
			for e in commit['elements'][i]['elements']:
				if e['applicationId'] == selectedId:
					selectedIds.append(e['id'])

	comment = spk.create_comment(
		projectId='aeb487f0e6',
		title = issue['markup']['Title'],
		modelId = '0425408de2',
		cameraPosition = [
			issue['viewpoint']['camera_viewpoint']['x'],
			issue['viewpoint']['camera_viewpoint']['y'],
			issue['viewpoint']['camera_viewpoint']['z']
		],
		cameraTarget = [
			issue['viewpoint']['camera_direction']['x'],
			issue['viewpoint']['camera_direction']['y'],
			issue['viewpoint']['camera_direction']['z']
		],
		selectedObjectIds = selectedIds
	)

print(f'\n{round(time.time() - ts, 2)} sec')
