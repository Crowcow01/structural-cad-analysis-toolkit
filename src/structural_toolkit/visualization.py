import plotly.graph_objects as go

def plot_model(model, solver=None):
    fig=go.Figure()
    for m in model.members.values():
        a,b=model.nodes[m.start_node],model.nodes[m.end_node]
        fig.add_trace(go.Scatter3d(x=[a.x,b.x],y=[a.y,b.y],z=[a.z,b.z],mode="lines",line={"width":6},name=f"Member {m.id}"))
    fig.add_trace(go.Scatter3d(x=[n.x for n in model.nodes.values()],y=[n.y for n in model.nodes.values()],z=[n.z for n in model.nodes.values()],mode="markers+text",text=[str(n.id) for n in model.nodes.values()],textposition="top center",marker={"size":6},name="Nodes"))
    fig.update_layout(title="Structural Model",scene={"xaxis_title":"X","yaxis_title":"Y","zaxis_title":"Z"},showlegend=False)
    return fig
