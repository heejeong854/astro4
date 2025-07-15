import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("우주 팽창 시각화 (허블법칙 기반 모델)")

# 설명 텍스트 + 수식
st.markdown(r"""
---
**📘 배경 설명: 허블법칙 기반 팽창 모델**

- **허블법칙:**  
\[
v = H_0 \cdot d
\]
- 별이나 은하의 거리 \(d\)가 멀어질수록, 관측되는 후퇴 속도 \(v\)도 커진다는 법칙입니다.

- 이 팽창 모형에서는 거리의 시간에 따른 변화를 단순화하여 다음과 같이 나타냅니다:

\[
d(t) = d_0 \cdot \left(1 + \frac{H_0 \cdot t}{1000} \right)
\]

- 여기서 \(H_0\): 허블 상수 (km/s/Mpc),  
  \(t\): 시간 (임의 단위),  
  \(d_0\): 초기 거리

---
""")

# 허블 상수 슬라이더
H0 = st.slider("허블 상수 H₀ (팽창 계수, km/s/Mpc)", min_value=10, max_value=100, value=30, step=5)
time_step = st.slider("시간 (임의 단위)", min_value=0, max_value=100, value=30)

# 초기 은하 위치 생성
np.random.seed(0)
n_galaxies = 100
angles = np.random.uniform(0, 2*np.pi, n_galaxies)
radii = np.random.uniform(0.2, 1.0, n_galaxies)
x0 = radii * np.cos(angles)
y0 = radii * np.sin(angles)

# 허블법칙 기반 팽창 반영
scale = 1 + H0 * time_step / 1000
x = x0 * scale
y = y0 * scale

# 시각화
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(x, y, color='orange', s=10)
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.set_title(f"시간 {time_step}, 허블 상수 H₀ = {H0}")
ax.axis('off')

st.pyplot(fig)
