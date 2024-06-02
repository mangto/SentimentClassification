import numpy as np
from kiwipiepy import Kiwi
from json import load

class Analyzer:
    table = ['공포', '놀람', '분노', '슬픔', '중립', '행복', '혐오']
    def __init__(self) -> None:
        self.frequency = Analyzer.load_frequency() # 단어별 감정 빈도 불러오기
        self.total_frequency = Analyzer.load_total_frequency() # 전체 빈도 -> 자주 나오는 단어는 기여도를 낮추기 위함
        self.kiwi = Kiwi() # 토큰화

        self.kiwi.tokenize('') # 첫 토큰화가 느린점을 해결하기 위함
        # cf. kiwi는 aho-corasick 알고리즘을 사용함
        pass

    def load_frequency() -> dict:
        with open(".\\dataset\\frequency.txt", 'r', encoding='utf8') as file:
            frequency = file.read()

        result = {}

        for freq in frequency.splitlines():
            token = freq.split(' ')
            result[token[0]] = np.array([float(f[:7]) for f in token[1:]])

        return result
    
    def load_total_frequency() -> dict:
        with open(".\\dataset\\dictionary.json", 'r', encoding='utf8') as file:
            freq = load(file)

        return freq
    
    def softmax(x): # 행열 총합이 1이 되도록 보정해줌
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0) # only difference
    
    def get_frequency(self, word:str) -> np.ndarray: # 단어의 출현빈도 불러오기
        freq = self.frequency.get(
            word, np.array([1/7]*7)
        )

        return freq
    
    def tokenize(self, text:str) -> list: # 토큰화: 문장을 형태소 기준으로 쪼갬
        analyzed = self.kiwi.tokenize(text)
        analyzed_ = []
        for t in analyzed:
            token = t.form
            l =''

            # 밑의 for 루프를 하는 이유는 연속되는 단어를 좀 더 깔끔하게 하기위함임
            # ex) ㅋㅋㅋㅋㅋㅠㅠ -> ㅋㅠ
            for i, c in enumerate(token[:-1]):
                if (c != token[i+1]): l+= c

            token = l+token[-1]

            analyzed_.append(token.replace(' ', '_'))

        return analyzed_
    
    def analyze(self, text:str, STD_Threshold:float=0.001) -> np.ndarray:

        # 토큰화
        tokenized = self.tokenize(text)

        frequency = np.zeros((7, ))
        
        # 단어별 빈도를 가져와서 합함
        # 기존에 없던 단어인 경우에는 모든 감정에 대해서 같은 값을 더함
        for token in tokenized:
            frequency += Analyzer.softmax(self.get_frequency(token))

        # 행렬의 합을 1로 맞춰줌
        frequency = Analyzer.softmax(frequency)

        # 가장 값이 큰 감정의 index를 가져와서(np.argmax) 감정 이름을 가져옴(Anlayzer.table[...]) 
        feeling = Analyzer.table[np.argmax(frequency)]

        # 표준편차를 구함
        std = round(np.std(frequency), 5)

        # 표준편차가 임계값보다 작은 경우 감정을 중립으로 설정함
        if (std <= STD_Threshold): feeling = '중립'

        return feeling, frequency
        
if __name__ == "__main__":
    analyzer = Analyzer()
    print(analyzer.analyze('아니 너무 배고파 ㅜㅜ'))