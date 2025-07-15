import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("조석력 주기와 해수면 높이 시뮬레이션")
st.write("현재 시간: 2025년 7월 15일 오후 8:07 KST")

# 상수
G = 6.67430e-11  # 만유인력 상수 (m³ kg⁻¹ s⁻²)
M_earth = 5.972e24  # 지구 질량 (kg)
M_moon = 7.342e22  # 달 질량 (kg)
ocean_depth = 3800  # 평균 해수 깊이 (m), 단순화용

# 사용자 입력
days = st.slider("시간 (일)", 0, 27, 0)  # 약 27.3일 공전 주기
distance_variation = 363300 + 46600 * np.cos(2 * np.pi * days / 27.3)  # 근지점(363300km)에서 원지점(410000km)까지 변화
distance = distance_variation * 1000  # m 단위

# 조석력 계산 (F = G * m1 * m2 / r², r의 세제곱에 비례)
tidal_force = G * M_earth * M_moon / (distance ** 3)  # 조석력은 r³에 반비례
sea_level_change = tidal_force * ocean_depth / 1e12  # 간단한 해수면 높이 모델 (상수 조정)

# 시각화
fig, ax1 = plt.subplots(figsize=(8, 5))

# 조석력 (왼쪽 y축)
ax1.plot(range(28), [G * M_earth * M_moon / ((363300 + 46600 * np.cos(2 * np.pi * d / 27.3) * 1000) ** 3) for d in range(28)], 
         color='blue', label='조석력 (상대값)')
ax1.set_xlabel("일수 (일)")
ax1.set_ylabel("조석력 (상대값)", color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# 해수면 높이 (오른쪽 y축)
ax2 = ax1.twinx()
ax2.bar(range(28), [G * M_earth * M_moon / ((363300 + 46600 * np.cos(2 * np.pi * d / 27.3) * 1000) ** 3) * ocean_depth / 1e12 for d in range(28)], 
        color='green', alpha=0.3, label='해수면 높이 (m)')
ax2.set_ylabel("해수면 높이 변화 (m)", color='green')
ax2.tick_params(axis='y', labelcolor='green')

# 레이아웃 조정
fig.tight_layout()
fig.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2)
st.pyplot(fig)

# 추가 정보
st.write(f"현재 거리: {distance_variation:.0f} km")
st.write(f"조석력: {tidal_force:.2e} N/m³")
st.write(f"해수면 높이 변화: {sea_level_change:.2f} m")
