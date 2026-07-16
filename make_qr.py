# -*- coding: utf-8 -*-
"""
WSM-6035 매뉴얼 QR코드 생성기
사용법:
    python make_qr.py "https://your-domain.com/wsm6035/"
    python make_qr.py "https://your-domain.com/wsm6035/" 라벨텍스트

- 오류정정 레벨 H(30%) : 중앙에 로고/라벨을 넣어도 인식 가능
- 우성하이텍 레드 색상 적용
- 출력: qr_wsm6035.png (인쇄용 고해상도)
"""
import sys
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont

# 기본값(임시). 실제 호스팅 URL 결정 후 인자로 넘겨서 재생성하세요.
URL = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/wsm6035/"
LABEL = sys.argv[2] if len(sys.argv) > 2 else "WSM-6035"

RED = (200, 16, 46)      # 우성하이텍 레드
DARK = (26, 26, 26)      # QR 모듈 색(가독성 위해 진한색 권장)
BOX = 20                 # 모듈당 픽셀(인쇄용 고해상도)
BORDER = 4               # 여백(quiet zone) 모듈 수

qr = qrcode.QRCode(
    version=None,
    error_correction=ERROR_CORRECT_H,
    box_size=BOX,
    border=BORDER,
)
qr.add_data(URL)
qr.make(fit=True)

img = qr.make_image(fill_color=DARK, back_color="white").convert("RGB")
W, H = img.size

# 하단 라벨 바 추가
bar_h = int(W * 0.14)
canvas = Image.new("RGB", (W, H + bar_h), "white")
canvas.paste(img, (0, 0))
draw = ImageDraw.Draw(canvas)
draw.rectangle([0, H, W, H + bar_h], fill=RED)

# 라벨 텍스트
try:
    font = ImageFont.truetype("malgunbd.ttf", int(bar_h * 0.42))
except Exception:
    try:
        font = ImageFont.truetype("malgun.ttf", int(bar_h * 0.42))
    except Exception:
        font = ImageFont.load_default()

text = f"{LABEL} 사용설명서"
tb = draw.textbbox((0, 0), text, font=font)
tw, th = tb[2] - tb[0], tb[3] - tb[1]
draw.text(((W - tw) / 2, H + (bar_h - th) / 2 - tb[1]), text, fill="white", font=font)

out = "qr_wsm6035.png"
canvas.save(out, dpi=(300, 300))
print(f"[OK] 생성됨: {out}")
print(f"     URL   : {URL}")
print(f"     크기  : {canvas.size[0]}x{canvas.size[1]}px (300dpi 인쇄용)")
if URL.startswith("https://example.com"):
    print("     [주의] 임시 URL입니다. 실제 호스팅 URL로 다시 실행하세요:")
    print('            python make_qr.py \"https://실제주소/\"')
