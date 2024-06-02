# SentimentClassification
뉴럴네트워크 없이 감정분석

cmd에서 다음 명령어를 입력해서 필요한 라이브러리를 다운받기
```
pip install -r requirements.txt
```

## 사용방법
```
from SentimentClassification import Analyzer

anlayzer = Analyzer()

text = '나 너무 배고파'
feeling = analyzer.analyze(text)[0]

print(feeling) # 슬픔
```
