import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.title("위도별 조석력 시뮬레이션 with 반일주기 및 월광 주기 반영")
st.write("기준 날짜: 2025년 7월 15일 오후 8:11 KST")

# 상수
G = 6.67430e-11  # 만유인력 상수
M_earth = 5.972e24
M_moon = 7.342e22
earth_radius = 6371e3

# 기준 날짜
base_date = datetime(2025, 7, 15, 20, 11)

# 사용자 입력
days_offset = st.slider("날짜 선택 (일)", 0, 30, 0)
latitude = st.slider("관측 위도 (°)", -90.0, 90.0, 37.5, 0.1)  # 우리나라 위도 대략 37.5도
current_date = base_date + timedelta(days=days_offset)

# 월광 주기 기반 달 위치 (각도)
days = days_offset % 29.5
moon_angle = 2 * np.pi * days / 29.5

# 달-지구 거리 (km) 근사
initial_distance = 384400
distance_variation = initial_distance + 46600 * np.cos(moon_angle)
distance = distance_variation * 1000  # m

# 조석 진폭 계산 (단순화)
tidal_force = G * M_earth * M_moon / (distance ** 3)
tidal_amplitude = tidal_force * earth_radius  # m/s² 단위 조석 가속도(간단화)

# 시간축: 하루 24시간, 100포인트
time_hours = np.linspace(0, 24.84, 100)  # 반일주기 포함

# 하루 주기 각속도
omega_day = 2 * np.pi / 24.84  # 약 24시간 50분

# 월광 주기 각속도
omega_moon = 2 * np.pi / 29.5

# 위도에 따른 위상, cos 위도로 조석 진폭 보정 (최대는 적도)
latitude_rad = np.radians(latitude)
lat_factor = np.cos(latitude_rad)

# 조석가속도 시계열 (시간, 하루 주기 반영 + 월광 주기)
tidal_acceleration = tidal_amplitude * lat_factor * np.cos(omega_day * time_hours - moon_angle)

# 그래프 그리기
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(time_hours, tidal_acceleration * 1e7)  # 1e7 배 스케일 조절 (눈으로 보기 편하게)
ax.set_title(f"위도 {latitude}°에서의 하루 조석력 변화 (단위: 10⁻⁷ m/s²)")
ax.set_xlabel("시간 (시간)")
ax.set_ylabel("조석 가속도 (×10⁻⁷ m/s²)")
ax.grid(True)

st.pyplot(fig)

# 추가 정보
st.write(f"현재 날짜: {current_date.strftime('%Y년 %m월 %d일 %H:%M KST')}")
st.write(f"달-지구 거리: {distance_variation:.0f} km")
st.write(f"조석 진폭 (기준 적도): {tidal_amplitude:.2e} m/s²")
st.write(f"조석 진폭 보정 계수 (위도 {latitude}°): {lat_factor:.2f}")
st.write(f"월광 주기 각도 (radian): {moon_angle:.2f}")
