import streamlit as st
from astropy.io import fits
import matplotlib.pyplot as plt

st.title("성단 별 색-광도도 (C-M도) 그리기 앱")

uploaded_file = st.file_uploader("FITS 테이블 파일 업로드 (별 색지수, 광도 포함)", type=["fits", "fit"])

if uploaded_file is not None:
    try:
        hdul = fits.open(uploaded_file)
        st.success("FITS 파일 열기 성공!")

        # 첫 번째 테이블 HDU 찾기 (보통 1번에 있음)
        table_hdu = None
        for hdu in hdul:
            if hdu.is_image:
                continue
            if hdu.data is not None:
                table_hdu = hdu
                break

        if table_hdu is None:
            st.error("테이블 데이터를 찾을 수 없습니다.")
        else:
            data = table_hdu.data

            st.write(f"테이블 컬럼 목록: {data.names}")

            # 사용자에게 컬럼 선택 받기 (색지수, 광도)
            color_index_col = st.selectbox("색지수 컬럼 선택 (예: B-V)", options=data.names)
            magnitude_col = st.selectbox("광도 컬럼 선택 (예: Vmag)", options=data.names)

            # 데이터 추출
            color_index = data[color_index_col]
            magnitude = data[magnitude_col]

            # C-M도 그리기 (광도는 보통 아래로 갈수록 밝으므로 -magnitude)
            fig, ax = plt.subplots()
            ax.scatter(color_index, -magnitude, s=10, color='blue', alpha=0.7)
            ax.set_xlabel(f"색지수 ({color_index_col})")
            ax.set_ylabel(f"절대 등급 또는 광도 (-{magnitude_col})")
            ax.set_title("색-광도도 (Color-Magnitude Diagram)")
            ax.grid(True)

            st.pyplot(fig)

        hdul.close()

    except Exception as e:
        st.error(f"오류 발생: {e}")
