import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("3D 우주 팽창 시각화 (허블법칙 기반)")

st.markdown(r"""
---
**📘 허블법칙과 3D 팽창 모델**

- **허블법칙:**  
\[
v = H_0 \cdot d
\]

- 은하들은 중심으로부터 일정 비율로 멀어집니다:  
\[
\vec{r}(t) = \vec{r}_0 \cdot \left(1 + \frac{H_0 \cdot t}{k} \right)
\]

- \(H_0\): 허블 상수 (km/s/Mpc),  
  \(t\): 시간 (임의 단위),  
  \(k\): 비례 상수 (스케일 조정용)
---
""")

# 슬라이더
H0 = st.slider("허블 상수 H₀ (km/s/Mpc)", 10, 100, 50, step=5)
time = st.slider("시간 (임의 단위)", 0, 100, 20)
scale = 1 + H0 * time / 1000

# 은하 생성 (3D 랜덤 위치)
np.random.seed(1)
n_galaxies = 200
x0 = np.random.uniform(-1, 1, n_galaxies)
y0 = np.random.uniform(-1, 1, n_galaxies)
z0 = np.random.uniform(-1, 1, n_galaxies)

# 팽창 반영
x = x0 * scale
y = y0 * scale
z = z0 * scale

# 3D 그래프
fig = go.Figure(data=go.Scatter3d(
    x=x, y=y, z=z,
    mode='markers',
    marker=dict(size=3, color=z, colorscale='Viridis', opacity=0.8)
))

fig.update_layout(
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
        aspectmode='cube'
    ),
    title=f'3D 은하 팽창 시뮬레이션 (H₀={H0}, 시간={time})'
)

st.plotly_chart(fig)
