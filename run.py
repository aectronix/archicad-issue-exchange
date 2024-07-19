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

# ac = ArchicadWrapper(arg.port)

# export issues into the bcfzip

# read them

spk = SpeckleWrapper()
commit = spk.retrieve('aeb487f0e6', '784ad6fdb5')


bcf = BCFWrapper('C:\\Users\\i.yurasov\\Desktop\\dev\\_tmp\\issues.bcfzip')
issues = bcf.read()
# # print (issues)
# print(json.dumps(issues, indent = 4))
for issue in issues:
	print (issue)

# stream = spk.client.stream.search('aeb487f0e6')[0]
# comment = spk.create_comment(
# 	projectId='aeb487f0e6',
# 	title = 'New Thread with VP',
# 	modelId = '0425408de2',
# 	cameraPosition = [
# 		7.58733,
# 		-33.643906,
# 		2.632540
# 	],
# 	cameraTarget = [
# 		0.892799,
# 		32.236394,
# 		0.133442
# 	]
# )


print(f'\n{round(time.time() - ts, 2)} sec')
