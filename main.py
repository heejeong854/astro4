import streamlit as st
from astropy.io import fits
from astropy.table import Table
import tempfile
import matplotlib.pyplot as plt

st.title("성단 별 색-광도도 (C-M도) 그리기 앱 (.fits/.fits.fz 지원)")

uploaded_file = st.file_uploader("FITS 또는 압축된 FITS (.fits.fz) 테이블 파일 업로드", type=["fits", "fz"])

if uploaded_file is not None:
    # 임시파일로 저장 (.fits 또는 .fits.fz 확장자 유지)
    suffix = ".fits" if uploaded_file.name.endswith(".fits") else ".fits.fz"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_filename = tmp_file.name

    try:
        # astropy로 FITS 파일 열기
        hdul = fits.open(temp_filename)
        st.success("FITS 파일 열기 성공!")

        # 테이블 HDU 찾기 (비이미지 HDU 중 데이터가 있는 첫 번째)
        table_hdu = None
        for hdu in hdul:
            if not hdu.is_image and hdu.data is not None:
                table_hdu = hdu
                break

        if table_hdu is None:
            st.error("테이블 데이터가 포함된 HDU를 찾지 못했습니다.")
        else:
            data = Table(table_hdu.data)

            st.write(f"테이블 컬럼 목록: {data.colnames}")

            # 사용자에게 색지수, 광도 컬럼 선택 받기
            color_index_col = st.selectbox("색지수 컬럼 선택 (예: B-V)", options=data.colnames)
            magnitude_col = st.selectbox("광도 컬럼 선택 (예: Vmag, 절대 등급 등)", options=data.colnames)

            # 컬럼 데이터 추출
            color_index = data[color_index_col]
            magnitude = data[magnitude_col]

            # NaN 제거 (결측치 있는 데이터 제거)
            import numpy as np
            mask = (~np.isnan(color_index)) & (~np.isnan(magnitude))
            color_index = color_index[mask]
            magnitude = magnitude[mask]

            # C-M도 그리기 (광도는 -값으로 아래로 갈수록 밝음)
            fig, ax = plt.subplots()
            ax.scatter(color_index, -magnitude, s=10, color='blue', alpha=0.7)
            ax.set_xlabel(f"색지수 ({color_index_col})")
            ax.set_ylabel(f"광도 (-{magnitude_col})")
            ax.set_title("색-광도도 (Color-Magnitude Diagram)")
            ax.grid(True)
            st.pyplot(fig)

        hdul.close()

    except Exception as e:
        st.error(f"오류 발생: {e}")
