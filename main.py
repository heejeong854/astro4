import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("주계열성별 시간에 따른 생명가능지대 시뮬레이션 (원 + 수직선)")

# 주계열성 선택
spectral_type = st.selectbox("별 분광형 선택", ["M형", "K형", "G형 (태양형)", "F형"])

# 행성 궤도 입력
planet_orbit = st.slider("행성 궤도 반경 (AU)", 0.1, 5.0, 1.0, step=0.01)

# 시간 슬라이더 (억 년 단위)
time_max = {"M형": 300, "K형": 200, "G형 (태양형)": 100, "F형": 50}
max_age = time_max[spectral_type]
time = st.slider("시간 (억 년)", 0, max_age, 0)

# 광도 진화 파라미터 (초기광도, 증가율)
params = {
    "M형": (0.08, 0.01),
    "K형": (0.4, 0.05),
    "G형 (태양형)": (1.0, 0.10),
    "F형": (2.0, 0.15)
}
L0, rate = params[spectral_type]

# 기본 HZ 거리 (태양 대비 거리 기준)
hz_base = {
    "M형": (0.1, 0.3),
    "K형": (0.4, 0.8),
    "G형 (태양형)": (0.95, 1.67),
    "F형": (1.5, 2.2)
}
hz_inner_base, hz_outer_base = hz_base[spectral_type]

# 현재 시간 광도 계산 (지수 증가 근사, 음수 방지)
luminosity = max(L0 * np.exp(rate * time), 0.01)  # 최소 0.01로 제한

# 현재 HZ 거리 계산
hz_inner = np.sqrt(luminosity) * hz_inner_base
hz_outer = np.sqrt(luminosity) * hz_outer_base

# 행성 생명가능 여부
habitable = hz_inner <= planet_orbit <= hz_outer

# --- 2D 평면 시각화 (별 + HZ 원 + 행성 수직선) ---
fig, ax = plt.subplots(figsize=(6, 6))

# 별 (중앙 노란 원)
star = plt.Circle((0, 0), 0.1, color='yellow')
ax.add_artist(star)

# HZ 외부 원 (연한 초록, 투명)
hz_outer_circle = plt.Circle((0, 0), hz_outer, color='green', alpha=0.2)
ax.add_artist(hz_outer_circle)

# HZ 내부 경계 (초록 점선)
hz_inner_circle = plt.Circle((0, 0), hz_inner, edgecolor='green', facecolor='none', linewidth=2, linestyle='--')
ax.add_artist(hz_inner_circle)

# 행성 위치 수직선 (파란색, y 범위 ±1.3 * hz_outer)
line_ymin = -hz_outer * 1.3
line_ymax = hz_outer * 1.3
ax.vlines(planet_orbit, line_ymin, line_ymax, color='blue', linewidth=3, label='행성 궤도')

# 행성 생명가능 여부 텍스트 표시 (위쪽, 겹침 방지)
color_text = "green" if habitable else "red"
status_text = "🌿 생명가능지대 내" if habitable else "⚠️ 생명가능지대 밖"
ax.text(planet_orbit, line_ymax * 1.05, status_text, color=color_text,
        fontsize=12, fontweight='bold', ha='center', va='bottom')

# 축 설정 및 비율 조정
ax.set_xlim(-hz_outer * 1.5, hz_outer * 1.5)
ax.set_ylim(line_ymin * 1.1, line_ymax * 1.2)
ax.set_aspect('equal')
ax.axis('off')
ax.legend(loc='upper right', fontsize=10)

# Streamlit에 그래프 출력
st.pyplot(fig)

# 추가 정보 표시
st.write(f"**현재 광도**: {luminosity:.2f} L☉")
st.write(f"**HZ 내경계**: {hz_inner:.2f} AU, **외경계**: {hz_outer:.2f} AU")
st.write(f"**행성 궤도**: {planet_orbit:.2f} AU")
