import imageio.v2 as imageio
import os

images = []
for i in range(1600):
    filename = f"frames2/frame_{i:04d}.png"
    if not os.path.exists(filename):
        continue
    images.append(imageio.imread(filename))

imageio.mimsave("bhahaha_tri.mp4", images, fps=24)
