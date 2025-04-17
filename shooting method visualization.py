import numpy as np
from mayavi import mlab

def generate_sample_trajectories(num_trajectories=5, num_points=100):
    # Generates sample curved trajectories.
    # Note: equations for the trajectories would work too
    all_trajectories = []
    observer_z = 20
    screen_z = -10
    z_range = observer_z - screen_z



    for i in range(num_trajectories):
        # Set starting points. If I understand correctly they should all originate from exactly at the observer? Otherwise add some random x-y shift.
        start_x = 0
        start_y = 0

        # Simulate ending points (could be points on the red screen)
        end_x = np.random.uniform(-2.0, 2.0)
        end_y = np.random.uniform(-4.0, 4.0)

        # Parameter 't' from 0 (observer) to 1 (screen)
        t = np.linspace(0, 1, num_points)

        # Z coordinate goes linearly from observer to screen. Technically approximation but they're fake trajectories anyway.
        # Change if using equations for real trajectories
        z = observer_z - z_range * t

        # X and Y coordinates with a curve bending around z=0 (t=20/30 = 2/3)
        bend_factor = 5 * (i / (num_trajectories -1 + 1e-6) - 0.5) # Spread the bends
        x = start_x * (1 - t) + end_x * t + bend_factor * 4 * t * (1 - t) # Parabolic term for bending
        y = start_y * (1 - t) + end_y * t - bend_factor * 2 * 4 * t * (1 - t) # Different bend for y

        # Format as list of lists: [[x0,y0,z0], [x1,y1,z1], ...]
        trajectory = np.vstack([x, y, z]).T.tolist()
        all_trajectories.append(trajectory)

    return all_trajectories


# Create figure
mlab.figure(bgcolor=(1, 1, 1), size=(1000, 800))

# Create central black sphere
mlab.points3d(0, 0, 0, scale_factor=2, color=(0, 0, 0), resolution=50)

# Create red screen (5x10 rectangle at z = -10; resolution determined by # in front of j - shouldn't need to be >2)
x_red, y_red = np.mgrid[-2.5:2.5:2j, -5:5:2j]  # 5 units wide (x), 10 units tall (y)
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

my_photon_trajectories = generate_sample_trajectories(num_trajectories=10, num_points=50)

# --- Plot the Trajectories ---
trajectory_color = (0, 0.8, 0) # Bright Green
trajectory_radius = 0.03       # Adjust for desired thickness (or None for simple line)
tube_sides = 6                # Smoothness of the tube


for trajectory in my_photon_trajectories:
    if not trajectory: # Skip if a trajectory list is empty
        continue

    # Convert list of lists to a NumPy array for easier slicing
    # Shape will be (num_points, 3)
    traj_array = np.array(trajectory)

    if traj_array.shape[0] < 2 or traj_array.shape[1] != 3: # Need at least 2 points and exactly 3 coordinates
        continue

    # Extract x, y, z coordinates
    x_coords = traj_array[:, 0]
    y_coords = traj_array[:, 1]
    z_coords = traj_array[:, 2]

    # Plot the trajectory as a 3D line (optionally as a tube)
    mlab.plot3d(x_coords, y_coords, z_coords,
                color=trajectory_color,
                tube_radius=trajectory_radius,
                tube_sides=tube_sides)



# Configure view
mlab.view(azimuth=45, elevation=45, distance=35)
mlab.show()