import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("생명가능지대 (Habitable Zone) 시뮬레이션 및 시각화")

# 별 광도 입력 (태양광도 대비)
luminosity = st.slider("별의 광도 (태양 대비)", 0.1, 10.0, 1.0, step=0.1)

# 행성 궤도 반경 입력 (AU 단위)
planet_orbit = st.slider("행성 궤도 반경 (AU)", 0.1, 5.0, 1.0, step=0.01)

# 생명가능지대 계산
hz_inner = np.sqrt(luminosity) * 0.95
hz_outer = np.sqrt(luminosity) * 1.67

# 생명가능지대 내 여부 판단
if hz_inner <= planet_orbit <= hz_outer:
    habitability = "🌿 생명가능지대 내에 있습니다!"
else:
    habitability = "⚠️ 생명가능지대 밖에 있습니다."

# 결과 출력
st.write(f"별의 생명가능지대: {hz_inner:.2f} AU ~ {hz_outer:.2f} AU")
st.write(f"행성 궤도 반경: {planet_orbit:.2f} AU")
st.write(habitability)

# --- 1. 2D 평면 시각화 ---

fig1, ax1 = plt.subplots(figsize=(6,6))

# 별 (중앙 노란 원)
star = plt.Circle((0,0), 0.1, color='yellow', label='별')
ax1.add_artist(star)

# 생명가능지대 외곽 (연한 초록 투명 원)
hz_ring_outer = plt.Circle((0,0), hz_outer, color='green', alpha=0.2)
ax1.add_artist(hz_ring_outer)

# 생명가능지대 내부 경계 (초록 점선 테두리만)
hz_ring_inner = plt.Circle((0,0), hz_inner, edgecolor='green', facecolor='none', linewidth=2, linestyle='--')
ax1.add_artist(hz_ring_inner)

# 행성 위치 (파란 원)
planet = plt.Circle((planet_orbit, 0), 0.05, color='blue', label='행성')
ax1.add_artist(planet)

ax1.set_xlim(-2*hz_outer, 2*hz_outer)
ax1.set_ylim(-2*hz_outer, 2*hz_outer)
ax1.set_aspect('equal')
ax1.set_title("생명가능지대 시각화 (2D 평면)")
ax1.axis('off')

# --- 2. 거리 축 그래프 ---

fig2, ax2 = plt.subplots(figsize=(8, 2))

# 생명가능지대 범위 회색 배경
ax2.axvspan(hz_inner, hz_outer, color='gray', alpha=0.3, label='생명가능지대')

# 행성 궤도 위치 수직선
ax2.axvline(planet_orbit, color='blue', linewidth=3, label='행성 궤도')

ax2.set_xlim(0, max(5, hz_outer + 0.5))
ax2.set_ylim(0, 1)
ax2.set_yticks([])
ax2.set_xlabel("거리 (AU)")
ax2.set_title("생명가능지대 범위와 행성 궤도 위치")

ax2.legend(loc='upper right')

# Streamlit에 두 그래프 함께 표시
col1, col2 = st.columns(2)

with col1:
    st.pyplot(fig1)

with col2:
    st.pyplot(fig2)
