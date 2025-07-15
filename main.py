import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("생명가능지대 (Habitable Zone) 시뮬레이션")

# 별 광도 입력 (태양광도 대비)
luminosity = st.slider("별의 광도 (태양 대비)", 0.1, 10.0, 1.0, step=0.1)

# 행성 궤도 반경 입력 (AU 단위)
planet_orbit = st.slider("행성 궤도 반경 (AU)", 0.1, 5.0, 1.0, step=0.01)

# 생명가능지대 계산 (내부 경계와 외부 경계)
hz_inner = np.sqrt(luminosity) * 0.95
hz_outer = np.sqrt(luminosity) * 1.67

# 생명가능지대 내 여부 판단
if hz_inner <= planet_orbit <= hz_outer:
    habitability = "🌿 생명가능지대 내에 있습니다!"
else:
    habitability = "⚠️ 생명가능지대 밖에 있습니다."

# 결과 출력
st.write(f"별의 생명가능지대는 약 {hz_inner:.2f} AU 에서 {hz_outer:.2f} AU 사이입니다.")
st.write(f"행성 궤도 반경: {planet_orbit:.2f} AU")
st.write(habitability)

# 시각화
fig, ax = plt.subplots(figsize=(6,6))

# 별 그리기 (중앙)
star = plt.Circle((0,0), 0.1, color='yellow', label='별')
ax.add_artist(star)

# 생명가능지대 외곽 원 (연한 초록, 투명)
hz_ring_outer = plt.Circle((0,0), hz_outer, color='green', alpha=0.2)
ax.add_artist(hz_ring_outer)

# 생명가능지대 내부 경계 (초록 점선 테두리만)
hz_ring_inner = plt.Circle((0,0), hz_inner, edgecolor='green', facecolor='none', linewidth=2, linestyle='--')
ax.add_artist(hz_ring_inner)

# 행성 위치 표시
planet = plt.Circle((planet_orbit, 0), 0.05, color='blue', label='행성')
ax.add_artist(planet)

ax.set_xlim(-2*hz_outer, 2*hz_outer)
ax.set_ylim(-2*hz_outer, 2*hz_outer)
ax.set_aspect('equal')
ax.set_title("생명가능지대 시각화 (2D 평면)")
ax.axis('off')

st.pyplot(fig)
