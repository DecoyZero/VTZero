![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FDecoyZero%2FVTZero&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)


# VTZero

VTZero는 웹 애플리케이션으로 VirusTotal에서 IP 정보를 가져와 국가, 소유자, 유해도를 출력합니다.

## 설정
1. 리포지토리 클론
```sh
   git clone https://github.com/DecoyZero/VTZero.git
   cd your-repo
```

2. 의존성 설치
```sh
    pip install -r requirements.txt
```

3. VTZero.py 파일 최초 실행시 api값 입력
```sh
    python VTZero.py
    Please enter your VirusTotal API key:
```

## 사용법
1. 웹 브라우저에서 http://127.0.0.1:5000/에 접속합니다.
2. IP 주소를 입력하고 (한 줄에 하나씩) 제출하면 각 IP에 대한 정보를 얻을 수 있습니다.
3. 유해 값이 1 이상이면 해당 값은 빨간색으로 표시됩니다.

## Demo
# [Demo Blog](https://decoypot.com/vtzero-1dab79beace4)
![Demo](https://i.imgur.com/KLpECb1.gif)