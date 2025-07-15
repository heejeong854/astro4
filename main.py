import streamlit as st
from astropy.io import fits
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
from datetime import datetime
import numpy as np
from PIL import Image
import tempfile
import matplotlib.pyplot as plt

st.set_page_config(page_title="FITS 스펙트럼 플롯 및 온도 계산", layout="wide")
st.title("🔭 FITS 이미지 스펙트럼 플롯 및 온도 계산 앱")

uploaded_file = st.file_uploader(
    "분석할 FITS 또는 FITS.FZ 파일을 선택하세요.",
    type=['fits', 'fit', 'fz']
)

seoul_location = EarthLocation(lat=37.5665, lon=126.9780, height=50)
now_astropy = Time(datetime.utcnow())

def wien_temperature(peak_wavelength_nm):
    # Wien 변위 법칙: λ_peak * T = 2.898e6 (nm·K)
    return 2.898e6 / peak_wavelength_nm

if uploaded_file:
    suffix = ".fits" if uploaded_file.name.endswith(".fits") else ".fits.fz"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_filename = tmp_file.name

    try:
        with fits.open(temp_filename) as hdul:
            image_hdu = None
            for hdu in hdul:
                if hdu.data is not None and hdu.is_image:
                    image_hdu = hdu
                    break

            if image_hdu is None:
                st.error("파일에서 유효한 이미지 데이터를 찾을 수 없습니다.")
            else:
                header = image_hdu.header
                data = image_hdu.data
                data = np.nan_to_num(data)

                st.success(f"**'{uploaded_file.name}'** 파일을 성공적으로 처리했습니다.")

                col1, col2 = st.columns(2)

                with col1:
                    st.header("이미지 정보")
                    st.text(f"크기: {data.shape[1]} x {data.shape[0]} 픽셀")
                    if 'OBJECT' in header:
                        st.text(f"관측 대상: {header['OBJECT']}")
                    if 'EXPTIME' in header:
                        st.text(f"노출 시간: {header['EXPTIME']} 초")

                    st.header("물리량")
                    mean_brightness = np.mean(data)
                    st.metric(label="이미지 전체 평균 밝기", value=f"{mean_brightness:.2f}")

                with col2:
                    st.header("이미지 미리보기")
                    if data.max() == data.min():
                        norm_data = np.zeros(data.shape, dtype=np.uint8)
                    else:
                        scale_min = np.percentile(data, 5)
                        scale_max = np.percentile(data, 99.5)
                        data_clipped = np.clip(data, scale_min, scale_max)
                        norm_data = (255 * (data_clipped - scale_min) / (scale_max - scale_min)).astype(np.uint8)

                    img = Image.fromarray(norm_data)
                    st.image(img, caption="업로드된 FITS 이미지", use_container_width=True)

                # 스펙트럼 플롯 및 온도 계산 (중앙 행 스펙트럼 사용, 파장 가정: 400~700nm)
                st.header("스펙트럼 플롯 및 온도 계산")

                if data.ndim == 2:
                    spectrum = data[data.shape[0] // 2, :]
                    wl = np.linspace(400, 700, spectrum.size)  # 단순 가정: 400~700nm 범위

                    fig, ax = plt.subplots()
                    ax.plot(wl, spectrum, color='purple')
                    ax.set_xlabel("파장 (nm)")
                    ax.set_ylabel("강도")
                    ax.set_title("중앙 행 스펙트럼 플롯")
                    st.pyplot(fig)

                    peak_idx = np.argmax(spectrum)
                    peak_wl = wl[peak_idx]
                    st.write(f"가장 강한 파장: {peak_wl:.1f} nm")

                    temperature = wien_temperature(peak_wl)
                    st.write(f"Wien 변위 법칙에 따른 추정 온도: {temperature:.0f} K")

                elif data.ndim == 3:
                    st.write("3차원 이미지 (채널별 스펙트럼)은 추후 지원 예정입니다.")
                else:
                    st.warning("지원하지 않는 데이터 차원입니다.")

                # --- 사이드바: 현재 천체 위치 계산 ---
                st.sidebar.header("🧭 현재 천체 위치 (서울 기준)")
                if 'RA' in header and 'DEC' in header:
                    try:
                        target_coord = SkyCoord(ra=header['RA'], dec=header['DEC'], unit=('hourangle', 'deg'))
                        altaz = target_coord.transform_to(AltAz(obstime=now_astropy, location=seoul_location))
                        altitude = altaz.alt.degree
                        azimuth = altaz.az.degree

                        st.sidebar.metric("고도 (°)", f"{altitude:.2f}")
                        st.sidebar.metric("방위각 (°)", f"{azimuth:.2f}")
                    except Exception as e:
                        st.sidebar.warning(f"천체 위치 계산 실패: {e}")
                else:
                    st.sidebar.info("FITS 헤더에 RA/DEC 정보가 없습니다.")

    except Exception as e:
        st.error(f"파일 처리 중 오류가 발생했습니다: {e}")
        st.warning("파일이 손상되었거나 유효한 FITS 형식이 아닐 수 있습니다.")
else:
    st.info("시작하려면 FITS 또는 FITS.FZ 파일을 업로드해주세요.")
