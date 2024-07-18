import argparse
import time

from src.archicad import ArchicadWrapper
from src.speckle import SpeckleWrapper

ts = time.time()

cmd = argparse.ArgumentParser()
cmd.add_argument('-p', '--port', required=False, help='archicad port')
arg = cmd.parse_args()

# ac = ArchicadWrapper(arg.port)

# export issues into the bcfzip

# read them

spk = SpeckleWrapper()

stream = spk.client.stream.search('aeb487f0e6')[0]
comment = spk.create_comment()


print(f'\n{round(time.time() - ts, 2)} sec')
