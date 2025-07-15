import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

st.title("조석력과 타원형 해수면 높이 시뮬레이션")
st.write("현재 시간: 2025년 7월 15일 오후 8:09 KST")

# 상수
G = 6.67430e-11  # 만유인력 상수 (m³ kg⁻¹ s⁻²)
M_earth = 5.972e24  # 지구 질량 (kg)
M_moon = 7.342e22  # 달 질량 (kg)
earth_radius = 6371e3  # 지구 반지름 (m)

# 사용자 입력
days = st.slider("시간 (일)", 0, 27, 0)  # 약 27.3일 공전 주기
distance_variation = 363300 + 46600 * np.cos(2 * np.pi * days / 27.3)  # 근지점-원지점 변화 (km)
distance = distance_variation * 1000  # m 단위

# 조석력 계산 (r³에 비례)
tidal_force = G * M_earth * M_moon / (distance ** 3)
tidal_amplitude = tidal_force * earth_radius / 1e12  # 간단한 조석 진폭 모델

# 달의 각도 (시간에 따른 위치)
moon_angle = 2 * np.pi * days / 27.3  # 0~2π 라디안

# 지구와 타원형 조석 시각화
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal')
ax.set_xlim(-earth_radius * 1.5 / 1000, earth_radius * 1.5 / 1000)
ax.set_ylim(-earth_radius * 1.5 / 1000, earth_radius * 1.5 / 1000)
ax.set_xlabel("거리 (km)")
ax.set_ylabel("거리 (km)")

# 지구 모형
earth = plt.Circle((0, 0), earth_radius / 1000, color='blue', label='지구')
ax.add_artist(earth)

# 타원형 조석 (달 방향으로 늘어난 타원)
ellipse = Ellipse((0, 0), 
                  width=(earth_radius + tidal_amplitude * 2) / 1000,  # 장축
                  height=(earth_radius + tidal_amplitude * 0.5) / 1000,  # 단축
                  angle=np.degrees(moon_angle),  # 달의 각도에 따른 회전
                  edgecolor='green', 
                  facecolor='none', 
                  linewidth=2, 
                  label='조석 타원')
ax.add_artist(ellipse)

# 달 위치 (간략 표시)
moon_x = distance / 1000 * np.cos(moon_angle)
moon_y = distance / 1000 * np.sin(moon_angle)
ax.plot(moon_x, moon_y, 'yo', label='달')

ax.legend()
ax.axis('off')  # 축 숨기기 (심플한 모형용)

st.pyplot(fig)

# 추가 정보
st.write(f"현재 거리: {distance_variation:.0f} km")
st.write(f"조석력: {tidal_force:.2e} N/m³")
st.write(f"조석 진폭: {tidal_amplitude:.2f} m")
