# PPE(안전모·조끼·마스크) 감지 켜기

worksite에 **PPE 미착용 감지 슬롯**이 이미 들어가 있습니다. `ppe.onnx` 파일만 이 폴더에 넣으면 자동으로 켜집니다.

## 1) best.pt → ppe.onnx 변환 (1줄)
받으신 `best.pt`(YOLOv11)는 브라우저에서 바로 못 돌립니다. ONNX로 한 번 변환하세요.

**가장 쉬움 — Google Colab** (새 노트북에 붙여넣고 실행):
```python
!pip -q install ultralytics
from google.colab import files
up = files.upload()                 # best.pt 업로드
from ultralytics import YOLO
YOLO('best.pt').export(format='onnx', imgsz=640, opset=12)
files.download('best.onnx')         # 다운로드
```
또는 로컬/Kaggle에서:
```
pip install ultralytics
yolo export model=best.pt format=onnx imgsz=640 opset=12
```

## 2) 폴더에 넣기
다운로드한 `best.onnx` 를 **`ppe.onnx`** 로 이름 바꿔 이 폴더(`라이브데모/`)에 둡니다.

## 3) 끝
worksite를 다시 시작하면 카메라마다 PPE를 검사해:
- **안전모/조끼/마스크 미착용** → 화면에 `🦺 미착용: 안전모·조끼` 표시 + 경고음 + 관제·근로자 전송.

## 클래스 순서 (중요)
`ppe.js` 의 `NAMES` 배열은 학습에 쓴 **dataset.yaml 의 names 순서**와 같아야 합니다. Kaggle Output의 `dataset.yaml` 을 열어 순서가 다르면 `ppe.js` 의 `NAMES` 를 그대로 맞춰 주세요. (기본값은 css-data 데이터셋 순서)
