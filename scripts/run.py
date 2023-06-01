import argparse
import os
import time

import mandybrot_gpu as mandy

OUTPUT_DIR = "output"

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("real", type=float)
parser.add_argument("imag", type=float)
parser.add_argument("width", type=int)
parser.add_argument("height", type=int)
parser.add_argument("scale", type=float)
parser.add_argument("max_iters", type=int)
parser.add_argument("cmap", nargs="+", type=str)
args = parser.parse_args()

if not os.path.exists(OUTPUT_DIR):
	os.makedirs(OUTPUT_DIR)

t0 = time.time()

# Build the colour map
cmap = mandy.colour.build_colour_map(args.cmap, 256)

data = mandy.sample.area(
	args.real, args.imag, args.width, args.height, args.scale, args.max_iters
)

# Convert to an image
img = mandy.colour.image(data, args.max_iters, cmap)
mandy.colour.encode(img).save(os.path.join(OUTPUT_DIR, "mandybrot.png"))

t1 = time.time()


print(f"Calculation time: {t1-t0} seconds.")