### PILLOW
from PIL import Image
import random

# Load image
im = Image.open("../horse.png")
print("loaded hordes image")
im_w, im_h = im.size

## Scale jittering
scale_jitter_lo = 0.5
scale_jitter_up = 1.25 
n = 5
img_sizes = []

#Generate N random scales
for i in range(n):
	scaling_factor = random.uniform(scale_jitter_lo,scale_jitter_up)
	img_sizes.append((int(im_w*scaling_factor),int(im_h*scaling_factor)))

#Get max w and max h among the list
max_w = max([y[0] for y in image_sizes])
max_h = max([y[1] for y in image_sizes])

#Resize images with padding
for i in img_sizes:
	pad_w = max_w - i[0]
	pad_h = max_h - i[1]
	out = im.resize(())
	out.show()

#get largest dimension and pad others
## Rotations
#out = im.rotate(45) # degrees counter-clockwise








