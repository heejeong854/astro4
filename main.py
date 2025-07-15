
import streamlit as st
from astropy.io import fits
import tempfile

st.title("FITS.FZ 파일 업로드 및 열기")

uploaded_file = st.file_uploader("FITS 또는 FITS.FZ 파일을 업로드하세요", type=["fits", "fz"])

if uploaded_file is not None:
    # 임시파일로 저장 (suffix는 확장자 맞게)
    suffix = ".fits" if uploaded_file.name.endswith(".fits") else ".fits.fz"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_filename = tmp_file.name

    try:
        hdul = fits.open(temp_filename)
        st.success("✅ FITS 파일 열기 성공!")
        st.write(hdul.info())
        hdul.close()
    except Exception as e:
        st.error(f"❌ FITS 파일 열기 실패: {e}")

from astropy.wcs import WCS
import matplotlib.pyplot as plt

st.title("🪐 FITS 이미지 업로드 및 WCS 정보 확인 앱")

# 파일 업로드
uploaded_file = st.file_uploader("FITS 이미지 파일을 업로드하세요", type=["fits"])

if uploaded_file is not None:
    try:
        # FITS 파일 열기
        st.title("FITS.FZ 파일 업로드 및 열기")

        uploaded_file = st.file_uploader("FITS 또는 FITS.FZ 파일을 업로드하세요", type=["fits", "fz"])


        st.success("✅ FITS 파일 열기 성공!")
        
        # HDU 정보 출력
        st.write("### 📄 헤더 정보 (Header):")
        header = hdul[0].header
        st.text(repr(header))

        # WCS 시도
        try:
            wcs = WCS(header)
            st.write("### 🌌 WCS 좌표계 정보:")
            st.text(wcs)

            # 이미지 표시
            st.write("### 🖼️ 이미지 보기:")
            data = hdul[0].data

            if data is not None and data.ndim >= 2:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection=wcs)
                ax.imshow(data, cmap='gray', origin='lower')
                ax.set_xlabel('RA')
                ax.set_ylabel('Dec')
                st.pyplot(fig)
            else:
                st.warning("⚠️ 이미지 데이터가 없거나 차원이 부족합니다.")

        except Exception as e:
            st.error(f"❌ WCS 정보 없음: {e}")
        
        hdul.close()

    except Exception as e:
        st.error(f"❌ FITS 파일 열기에 실패했습니다: {e}")
