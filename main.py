import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 빛의 속도 (km/s)
c = 3e5

st.title("허블 상수 조절로 우주 팽창 시각화")

# 배경 지식 텍스트
st.markdown("""
---
**간단한 배경 지식**  
- 후퇴속도 \(v\)는 허블 상수 \(H_0\)와 거리 \(d\)의 곱으로 계산됩니다:  
\[
v = H_0 \times d
\]  
(\(v\): km/s, \(H_0\): km/s/Mpc, \(d\): Mpc)  
- 적색편이 \(z\)는 후퇴속도를 빛의 속도로 나눈 값입니다:  
\[
z = \frac{v}{c}
\]  
(\(c\)는 빛의 속도, 약 \(3 \times 10^5\) km/s)  
---
""")

# 허블 상수 조절 슬라이더 (50~100 km/s/Mpc)
H0 = st.slider("허블 상수 H₀ (km/s/Mpc)", min_value=50, max_value=100, value=70)

# 거리 범위 입력 (Mpc 단위)
max_distance = st.number_input("최대 거리 (Mpc)", min_value=10, max_value=1000, value=500, step=10)

# 거리 배열 생성
distances = np.linspace(0, max_distance, 500)

# 후퇴속도 계산
velocities = H0 * distances  # km/s

# 적색편이 계산 (v/c)
redshifts = velocities / c

# 그래프 그리기
fig, ax1 = plt.subplots(figsize=(10,5))

color_v = 'tab:blue'
ax1.set_xlabel('거리 (Mpc)')
ax1.set_ylabel('후퇴속도 (km/s)', color=color_v)
ax1.plot(distances, velocities, color=color_v, label='후퇴속도 v')
ax1.tick_params(axis='y', labelcolor=color_v)
ax1.grid(True)

ax2 = ax1.twinx()
color_z = 'tab:red'
ax2.set_ylabel('적색편이 z', color=color_z)
ax2.plot(distances, redshifts, color=color_z, label='적색편이 z')
ax2.tick_params(axis='y', labelcolor=color_z)

plt.title(f'허블 상수 H₀ = {H0} km/s/Mpc 일 때 우주 팽창')
fig.tight_layout()

st.pyplot(fig)

# 주요 값 출력
st.write(f"최대 거리 {max_distance} Mpc 에서의 후퇴속도: {velocities[-1]:.1f} km/s")
st.write(f"최대 거리 {max_distance} Mpc 에서의 적색편이: {redshifts[-1]:.5f}")
