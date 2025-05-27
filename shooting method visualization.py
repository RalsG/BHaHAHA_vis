import numpy as np
from mayavi import mlab


photon_trajectories = np.load("<photon trajectory file name>") # enter file name for photons paths here


# Create figure
mlab.figure(bgcolor=(1, 1, 1), size=(1000, 800))

# Create central black sphere
mlab.points3d(0, 0, 0, scale_factor=2, color=(0, 0, 0), resolution=50)

# Create red screen (20x20 rectangle at z = -10; resolution determined by # in front of j - shouldn't need to be >2)
x_red, y_red = np.mgrid[-10:10:2j, -10:10:2j]  # 5 units wide (x), 10 units tall (y)
mlab.mesh(x_red, y_red, np.full_like(x_red, -10), color=(1, 0, 0), opacity=0.6)

# Create blue screen (1x2 rectangle at z = +19; resolution same as above)
x_blue, y_blue = np.mgrid[-0.5:0.5:2j, -1:1:2j]  # 1 unit wide (x), 2 units tall (y)
mlab.mesh(x_blue, y_blue, np.full_like(x_blue, 19), color=(0, 0, 1), opacity=0.6)

# Create grey observer sphere (radius 0.25 at z = +20)
mlab.points3d(0, 0, 20, scale_factor=0.5, color=(0.8, 0.8, 0.8), resolution=50)

# Trajectory lines testing
mlab.plot3d([0, 10], [0, 0], [0, 0], color=(0, 1, 1),)
mlab.plot3d([0, 0], [0, 15], [0, 0], color=(1, 1, 0),)
mlab.plot3d([0, 0], [0, 0], [0, 15], color=(1, 0, 1),)


# --- Plot the Trajectories ---
trajectory_color = (0, 0.8, 0) # Bright Green
trajectory_radius = 0.03       # Adjust for desired thickness (or None for simple line)
num_sides = 6                # Smoothness of the tube




def color_spectrum(width):
    spectrum = np.zeros((width, 3))
    for i in range(width):
        if i < width / 3:
            r = (i / (width / 3))
            g = (1 - i / (width / 3))
            b = 0
        elif i < 2 * width / 3:
            r = (1 - (i - width / 3) / (width / 3) )
            g = 0
            b = ((i - width / 3) / (width / 3))
        else:
            r = 0
            g = ((i - 2 * width / 3) / (width / 3))
            b = (1 - (i - 2 * width / 3) / (width / 3))
        spectrum[i, :] = [r, g, b]
    return spectrum

trajectory_colors = color_spectrum(len(photon_trajectories))

i = 0
for trajectory in photon_trajectories:
    
    print(i, len(trajectory), len(trajectory[0]))

    # Convert list of lists to a NumPy array for easier slicing
    # Shape will be (num_points, 3)
    traj_array = np.array(trajectory)

    if traj_array.shape[0] < 2 or traj_array.shape[1] != 3: # Need at least 2 points and exactly 3 coordinates
        print("Trajectory " + str(i) + "deleted.")
        continue

    # Extract x, y, z coordinates
    x_coords = traj_array[:, 2]
    y_coords = traj_array[:, 1]
    z_coords = traj_array[:, 0]

    # Plot the trajectory as a 3D line (optionally as a tube)
    mlab.plot3d(x_coords, y_coords, z_coords,
                color=tuple(trajectory_colors[i]),
                tube_radius=trajectory_radius,
                tube_sides=num_sides)
    i += 1


# Configure view
mlab.view(azimuth=45, elevation=45, distance=35)
mlab.show()