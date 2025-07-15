from astropy.io import fits
from astropy.wcs import WCS

hdul = fits.open("your_image.fits")
header = hdul[0].header

# 헤더 출력해보기
print(repr(header))

# WCS 정보 시도
try:
    wcs = WCS(header)
    print("✅ WCS 정보 있음!")
except Exception as e:
    print("❌ WCS 정보 없음:", e)
