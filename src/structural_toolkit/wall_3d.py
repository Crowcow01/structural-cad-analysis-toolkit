import plotly.graph_objects as go


def plot_wall(wall):
    """Interactive 3D preview of a wall as an extruded box."""
    x = [0, wall.width, wall.width, 0, 0]
    y = [0, 0, wall.height, wall.height, 0]
    z0 = [0] * 5
    z1 = [wall.thickness] * 5
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z0, mode="lines", name="Front face"))
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z1, mode="lines", name="Back face"))
    for i in range(4):
        fig.add_trace(go.Scatter3d(
            x=[x[i], x[i]], y=[y[i], y[i]], z=[0, wall.thickness],
            mode="lines", showlegend=False
        ))
    fig.update_layout(
        title="3D Wall Model",
        scene={"xaxis_title": "Width (m)", "yaxis_title": "Height (m)",
               "zaxis_title": "Thickness (m)"}
    )
    return fig
