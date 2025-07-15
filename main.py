
n = 200
x0 = np.random.uniform(-1, 1, n)
y0 = np.random.uniform(-1, 1, n)
z0 = np.random.uniform(-1, 1, n)

# 팽창 비율
scale = 1 + H0 * time / 1000
x1 = x0 * scale
y1 = y0 * scale
z1 = z0 * scale

# 3D 시각화
fig = go.Figure()

# 팽창 전 (gray)
fig.add_trace(go.Scatter3d(
    x=x0, y=y0, z=z0,
    mode='markers',
    marker=dict(size=3, color='lightgray'),
    name='팽창 전'
))

# 팽창 후 (orange)
fig.add_trace(go.Scatter3d(
    x=x1, y=y1, z=z1,
    mode='markers',
    marker=dict(size=4, color='orange'),
    name='팽창 후'
))

fig.update_layout(
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
        aspectmode='cube'
    ),
    title=f'우주 팽창: H₀={H0}, 시간={time}',
    legend=dict(x=0.02, y=0.98)
)

st.plotly_chart(fig)

