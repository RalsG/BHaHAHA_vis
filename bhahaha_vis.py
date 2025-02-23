import numpy as np
from mayavi import mlab
import os
import glob

# Define the folder where the .gp files are stored
folder_path = r"C:\Users\ralst\Downloads\two_blackholes_collide"

# Get all .gp files in sorted order
file_list = sorted(glob.glob(f"{folder_path}/*.gp"))



# Function that can handle potential blank lines or irregularities in the file
def parse_gp_file_safe(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith("#") and line.strip():  # Skip header and blank lines
                try:
                    # Attempt to parse the line into floats
                    data.append(list(map(float, line.split())))
                except ValueError:
                    # Ignore lines that cannot be parsed
                    continue
    return np.array(data)


# Output directory for frames
output_dir = "frames"
os.makedirs(output_dir, exist_ok=True)

# Set visualization parameters
mlab.figure(size=(800, 800), bgcolor=(1, 1, 1))  # White background
mlab.view(azimuth=65, elevation=95)

for i, file in enumerate(file_list):
	# adjust speed through visualization without wasting time on frames that won't be used
	ff_message = False
	if (i<40):
		pass
	elif (i<100):
		if (i%3!=0):
			continue
		ff_text = "3x speed"
		ff_message = True
	elif (i<1400):
		if (i%100!=0):
			continue  
		ff_text = "100x speed"
		ff_message = True
	elif (i<1460):
		if (i%3!=0):
			continue
		ff_text = "3x speed"
		ff_message = True
	elif (i==1539):
		ff_text = "End state/failure mode"
		ff_message = True



	horizon_data = parse_gp_file_safe(file)

	# Load x, y, z data from your horizon file
	x, y, z = horizon_data[:, 0], horizon_data[:, 1], horizon_data[:, 2]
	vertices = np.column_stack((x, y, z))

	N, M = 80, 161  # BHaHAHA data so far has used 80x161 theta-phi grid
	x_grid = x.reshape((N, M))
	y_grid = y.reshape((N, M))
	z_grid = z.reshape((N, M))

	# Clear last frame
	mlab.clf()

	# Now use mlab.mesh for a structured surface
	mlab.mesh(x_grid, y_grid, z_grid, color=(0, 0, 1), opacity=0.8)
	iteration_title = "Iteration " + str(i+1) + "e+03"
	mlab.text(0.35, 0.9, iteration_title, width=0.5, color=(0, 0, 0))
	if ff_message:
		mlab.text(0.6, 0.8, ff_text, width=0.25, color=(0, 0, 0))

	# Save the frame
	frame_filename = f"{output_dir}/frame_{i:04d}.png"
	mlab.savefig(frame_filename)
	print(f"Saved: {frame_filename}")

# Save some duplicate end frames so it lingers
for i in range(1540, 1600):
	frame_filename = f"{output_dir}/frame_{i:04d}.png"
	mlab.savefig(frame_filename)
	print(f"Saved: {frame_filename}")

# Close mlab figure
mlab.close()
