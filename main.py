import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("주계열성별 진화 속도 반영 생명가능지대 시뮬레이션")

# 주계열성 종류 선택
spectral_type = st.selectbox("별 분광형 선택", ["M형", "K형", "G형 (태양형)", "F형"])

# 행성 궤도 반경 입력
planet_orbit = st.slider("행성 궤도 반경 (AU)", 0.1, 5.0, 1.0, step=0.01)

# 광도 진화 파라미터 (초기광도, 증가율, 최대수명)
params = {
    "M형": (0.08, 0.01, 300),
    "K형": (0.4, 0.05, 200),
    "G형 (태양형)": (1.0, 0.10, 100),
    "F형": (2.0, 0.15, 50)
}

L0, rate, max_age = params[spectral_type]

# 시간 축 (0 ~ 최대 수명, 1000포인트)
time = np.linspace(0, max_age, 1000)

# 광도 변화 모델: 지수 증가 (근사)
luminosity = L0 * np.exp(rate * time)

# 분광형별 기본 생명가능지대 기준값 (태양 대비 거리)
hz_base = {
    "M형": (0.1, 0.3),
    "K형": (0.4, 0.8),
    "G형 (태양형)": (0.95, 1.67),
    "F형": (1.5, 2.2)
}

hz_inner_base, hz_outer_base = hz_base[spectral_type]

# 시간에 따른 HZ 거리 변화
hz_inner = np.sqrt(luminosity) * hz_inner_base
hz_outer = np.sqrt(luminosity) * hz_outer_base

# 행성 궤도와 HZ 비교 - 생명가능 여부 배열 (1: 가능, 0: 불가)
habitable = (planet_orbit >= hz_inner) & (planet_orbit <= hz_outer)

# 시각화

fig, ax = plt.subplots(figsize=(10,5))
ax.plot(time, hz_inner, label='HZ 내부 경계')
ax.plot(time, hz_outer, label='HZ 외부 경계')
ax.hlines(planet_orbit, 0, max_age, colors='blue', linestyles='dashed', label='행성 궤도')

# 생명가능 구간 색칠
ax.fill_between(time, 0, planet_orbit + 1, where=habitable, color='green', alpha=0.3, label='생명가능 구간')

ax.set_xlabel("시간 (억 년)")
ax.set_ylabel("거리 (AU)")
ax.set_title(f"{spectral_type} 주계열성 생명가능지대 진화 시뮬레이션")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# 생명가능 기간 출력
habitable_duration = time[habitable].size * (max_age / 1000)
st.write(f"행성의 생명가능 기간: 약 {habitable_duration:.1f} 억 년")
