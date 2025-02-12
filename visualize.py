import numpy as np
import plotly.graph_objects as go

# Load trajectory data
try:
    trajectories = np.load("trajectories.npy")
except FileNotFoundError:
    print("Error: trajectories.npy not found! Run the MD simulation first.")
    exit()

num_steps, num_particles, _ = trajectories.shape

# Create initial 3D scatter plot
fig = go.Figure()

# Add particle traces (empty at first)
particle_traces = []
for i in range(num_particles):
    trace = go.Scatter3d(
        x=[], y=[], z=[], mode='markers',
        marker=dict(size=6, color='blue'),
        name=f'Particle {i+1}'
    )
    particle_traces.append(trace)
    fig.add_trace(trace)

# Animation frames (update positions dynamically)
frames = []
for step in range(num_steps):
    frame_data = []
    for i in range(num_particles):
        frame_data.append(go.Scatter3d(
            x=[trajectories[step, i, 0]], 
            y=[trajectories[step, i, 1]], 
            z=[trajectories[step, i, 2]],
            mode='markers',
            marker=dict(size=6, color='blue')
        ))
    frames.append(go.Frame(data=frame_data, name=str(step)))

# Add frames to figure
fig.update(frames=frames)

# Set animation settings
fig.update_layout(
    title="3D Molecular Dynamics Simulation",
    updatemenus=[{
        "buttons": [
            {"args": [None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True}],
             "label": "Play",
             "method": "animate"},
            {"args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}],
             "label": "Pause",
             "method": "animate"}
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }]
)

# Save as an interactive HTML file
fig.write_html("md_simulation_animated.html")

# Show the interactive animation
fig.show()