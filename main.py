import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("3D 우주 팽창 시각화 (Before vs After)")

st.markdown(r"""
---
**📘 허블법칙 기반 거리 변화**

\[
d(t) = d_0 \cdot \left(1 + \frac{H_0 \cdot t}{1000} \right)
\]

- 시간에 따라 은하들이 중심에서 멀어지는 모습을  
  두 시점(팽창 전/후)으로 시각화합니다.
---
""")

# 슬라이더
H0 = st.slider("허블 상수 H₀ (km/s/Mpc)", 10, 100, 50, step=5)
time = st.slider("시간 (임의 단위)", 0, 100, 30)

# 은하 위치 생성
np.random.seed(1)
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

