import streamlit as st
from astropy.io import fits
from astropy.wcs import WCS
import tempfile
import matplotlib.pyplot as plt

st.title("🪐 FITS 및 FITS.FZ 이미지 업로드 및 WCS 정보 확인 앱")

uploaded_file = st.file_uploader("FITS 또는 FITS.FZ 파일을 업로드하세요", type=["fits", "fz"])

if uploaded_file is not None:
    # 확장자에 맞춰 임시 파일 생성
    suffix = ".fits" if uploaded_file.name.endswith(".fits") else ".fits.fz"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_filename = tmp_file.name

    try:
        # FITS 파일 열기 (압축도 astropy가 자동 해제함)
        hdul = fits.open(temp_filename)
        st.success("✅ FITS 파일 열기 성공!")

        # 헤더 정보 출력
        header = hdul[0].header
        st.write("### 📄 헤더 정보 (Header):")
        st.text(repr(header))

        # WCS 좌표계 정보 시도
        try:
            wcs = WCS(header)
            st.write("### 🌌 WCS 좌표계 정보:")
            st.text(wcs)

            # 이미지 데이터 시각화 (2차원 이상일 때만)
            data = hdul[0].data
            if data is not None and data.ndim >= 2:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection=wcs)
                ax.imshow(data, cmap='gray', origin='lower')
                ax.set_xlabel('RA')
                ax.set_ylabel('Dec')
                st.pyplot(fig)
            else:
                st.warning("⚠️ 이미지 데이터가 없거나 2차원 이상이 아닙니다.")

        except Exception as e:
            st.error(f"❌ WCS 정보 없음 또는 읽기 실패: {e}")

        hdul.close()

    except Exception as e:
        st.error(f"❌ FITS 파일 열기에 실패했습니다: {e}")
