import streamlit as st
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import tempfile

st.title("FITS 이미지 스펙트럼 플롯 및 온도 계산 앱")

uploaded_file = st.file_uploader("FITS 또는 FITS.FZ 이미지 파일 업로드", type=["fits", "fz"])

def planck_law(wavelength_m, temperature_k):
    """흑체복사 법칙 단순 계산 (단위 변환 필요)"""
    h = 6.626e-34  # 플랑크 상수
    c = 3.0e8      # 빛 속도
    k = 1.38e-23   # 볼츠만 상수
    wl5 = wavelength_m ** 5
    exponent = np.exp(h * c / (wavelength_m * k * temperature_k)) - 1.0
    intensity = (2.0 * h * c ** 2) / (wl5 * exponent)
    return intensity

if uploaded_file is not None:
    suffix = ".fits" if uploaded_file.name.endswith(".fits") else ".fits.fz"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_filename = tmp_file.name

    try:
        hdul = fits.open(temp_filename)
        data = hdul[0].data
        hdul.close()

        if data is None:
            st.error("이미지 데이터가 없습니다.")
        else:
            st.write(f"이미지 데이터 차원: {data.shape}")

            # 다채널(RGB) 분리 (있으면)
            if data.ndim == 3:
                st.write("RGB 채널 분리")
                fig, axs = plt.subplots(1, 3, figsize=(15,5))
                colors = ['Red', 'Green', 'Blue']
                for i in range(3):
                    axs[i].imshow(data[i], cmap='gray', origin='lower')
                    axs[i].set_title(f"{colors[i]} 채널")
                    axs[i].axis('off')
                st.pyplot(fig)

                # 채널 중 하나 선택해 스펙트럼처럼 플롯 가능 (예: 중앙 행 픽셀 밝기)
                channel = st.selectbox("채널 선택", options=colors)
                ch_idx = colors.index(channel)
                spectrum = data[ch_idx][data.shape[1]//2, :]
                wl = np.linspace(400, 700, spectrum.size)  # nm 단위 가정 (가상)
                fig2, ax2 = plt.subplots()
                ax2.plot(wl, spectrum)
                ax2.set_xlabel("파장 (nm)")
                ax2.set_ylabel("강도")
                ax2.set_title(f"{channel} 채널 스펙트럼 (중앙 행)")
                st.pyplot(fig2)

                # 가장 강한 파장 위치 찾기
                peak_idx = np.argmax(spectrum)
                peak_wl_nm = wl[peak_idx]
                st.write(f"가장 강한 파장: {peak_wl_nm:.1f} nm")

                # Wien 변위 법칙으로 온도 추정 (λ_peak * T = 2.898e6 nm*K)
                temperature = 2.898e6 / peak_wl_nm
                st.write(f"추정된 온도: {temperature:.0f} K")

            elif data.ndim == 2:
                st.write("단일 채널 이미지")

                # 중앙 행 밝기 스펙트럼 플롯
                spectrum = data[data.shape[0]//2, :]
                wl = np.linspace(400, 700, spectrum.size)  # nm 단위 가정
                fig, ax = plt.subplots()
                ax.plot(wl, spectrum)
                ax.set_xlabel("파장 (nm)")
                ax.set_ylabel("강도")
                ax.set_title("중앙 행 스펙트럼 플롯")
                st.pyplot(fig)

                peak_idx = np.argmax(spectrum)
                peak_wl_nm = wl[peak_idx]
                st.write(f"가장 강한 파장: {peak_wl_nm:.1f} nm")
                temperature = 2.898e6 / peak_wl_nm
                st.write(f"추정된 온도: {temperature:.0f} K")

            else:
                st.warning("지원하지 않는 데이터 차원입니다.")

    except Exception as e:
        st.error(f"파일 처리 중 오류: {e}")
