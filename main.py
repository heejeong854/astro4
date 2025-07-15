import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from datetime import datetime, timedelta

st.title("조석력과 타원형 해수면 높이 시뮬레이션")
st.write("기준 날짜: 2025년 7월 15일 오후 8:11 KST")

# 상수
G = 6.67430e-11  # 만유인력 상수 (m³ kg⁻¹ s⁻²)
M_earth = 5.972e24  # 지구 질량 (kg)
M_moon = 7.342e22  # 달 질량 (kg)
earth_radius = 6371e3  # 지구 반지름 (m)

# 기준 날짜
base_date = datetime(2025, 7, 15, 20, 11)  # 2025년 7월 15일 오후 8:11 KST

# 사용자 입력 (날짜 슬라이더)
days_offset = st.slider("날짜 선택 (일)", 0, 30, 0)  # 30일 범위
current_date = base_date + timedelta(days=days_offset)
days = days_offset % 29.5  # 월광 주기 29.5일로 조정

# 실제 데이터 기반 근사 (2025년 7월 15일 달 위치 근사)
initial_distance = 384400  # 7월 15일 평균 거리 (km), 실제 데이터로 대체 가능
distance_variation = initial_distance + 46600 * np.cos(2 * np.pi * days / 29.5)  # 월광 주기 기반
distance = distance_variation * 1000  # m 단위

# 조석력 계산
tidal_force = G * M_earth * M_moon / (distance ** 3)
tidal_amplitude = tidal_force * earth_radius / 1e12  # 간단한 조석 진폭 모델

# 달의 각도
moon_angle = 2 * np.pi * days / 29.5  # 월광 주기 기반

# 달 위상 판단 (29.5일 기준)
phase = ""
if 0 <= days < 7.375:  # 삭
    phase = "삭 (신월)"
elif 7.375 <= days < 14.75:  # 상현
    phase = "상현"
elif 14.75 <= days < 22.125:  # 망
    phase = "망 (만월)"
elif 22.125 <= days < 29.5:  # 하현
    phase = "하현"
else:
    phase = "위상 계산 오류"

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

# 타원형 조석
ellipse = Ellipse((0, 0), 
                  width=(earth_radius + tidal_amplitude * 2) / 1000,  # 장축
                  height=(earth_radius + tidal_amplitude * 0.5) / 1000,  # 단축
                  angle=np.degrees(moon_angle),  # 달의 각도에 따른 회전
                  edgecolor='green', 
                  facecolor='none', 
                  linewidth=2, 
                  label='조석 타원')
ax.add_artist(ellipse)

# 달 위치
moon_x = distance / 1000 * np.cos(moon_angle)
moon_y = distance / 1000 * np.sin(moon_angle)
ax.plot(moon_x, moon_y, 'yo', label='달')

ax.legend()
ax.axis('off')  # 축 숨기기

st.pyplot(fig)

# 추가 정보
st.write(f"현재 날짜: {current_date.strftime('%Y년 %m월 %d일 %H:%M KST')}")
st.write(f"현재 거리: {distance_variation:.0f} km")
st.write(f"조석력: {tidal_force:.2e} N/m³")
st.write(f"조석 진폭: {tidal_amplitude:.2f} m")
st.write(f"현재 달 위상: {phase}")
