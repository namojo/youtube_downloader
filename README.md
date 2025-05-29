# YouTube Downloader for macOS

최고 화질로 YouTube 비디오를 다운로드하는 웹 기반 애플리케이션입니다.

## 주요 기능

- YouTube 비디오 정보 실시간 조회
- **최고 화질(Best Quality) 자동 다운로드** - 비디오와 오디오를 자동으로 병합
- 실시간 다운로드 진행률 표시
- 다운로드 완료 파일 목록 관리
- 직관적인 웹 인터페이스

## 시스템 요구사항

- macOS 10.12 이상
- Python 3.6 이상
- FFmpeg (고화질 다운로드에 필수)
- 인터넷 연결

## 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/namojo/youtube_downloader.git
cd youtube_downloader
```

### 2. 실행 권한 부여
```bash
chmod +x install.sh run.sh update.sh test.sh
```

### 3. FFmpeg 설치 (필수)
```bash
brew install ffmpeg
```

### 4. 애플리케이션 설치
```bash
./install.sh
```

설치 스크립트는 자동으로:
- Python 가상환경 생성
- Flask 웹 프레임워크 설치
- yt-dlp 최신 nightly 빌드 설치

## 사용 방법

### 1. 애플리케이션 실행
```bash
./run.sh
```

### 2. 웹 브라우저에서 접속
http://localhost:6274

### 3. 다운로드 단계
1. YouTube URL 입력 (예: https://www.youtube.com/watch?v=...)
2. "정보 가져오기" 클릭
3. 비디오 정보 확인
4. "다운로드 시작" 클릭
5. 다운로드된 파일은 `~/Downloads/YouTube` 폴더에 저장됨

## 다운로드 품질

이 애플리케이션은 자동으로 최고 품질로 다운로드합니다:
- **비디오**: 사용 가능한 최고 해상도 (4K, 1080p, 720p 등)
- **오디오**: 사용 가능한 최고 음질
- **형식**: MP4 (호환성이 가장 좋음)

## 스크립트 설명

- `install.sh`: 초기 설치 및 의존성 설치
- `run.sh`: 애플리케이션 실행
- `update.sh`: yt-dlp 업데이트
- `test.sh`: 시스템 테스트 및 문제 진단

## 문제 해결

### FFmpeg가 설치되지 않은 경우
```bash
brew install ffmpeg
```

### YouTube 접속 오류가 발생하는 경우
```bash
./update.sh
```

### 포트 6274가 사용 중인 경우
`app.py` 파일의 마지막 줄에서 포트 번호 변경:
```python
app.run(debug=True, port=8080, host='0.0.0.0')  # 6274를 8080으로 변경
```

### 시스템 테스트
```bash
./test.sh
```

또는 브라우저에서: http://localhost:6274/test

## 디렉토리 구조

```
youtube_downloader/
├── app.py              # Flask 메인 애플리케이션
├── templates/
│   └── index.html      # 웹 인터페이스
├── install.sh          # 설치 스크립트
├── run.sh              # 실행 스크립트
├── update.sh           # 업데이트 스크립트
├── test.sh             # 테스트 스크립트
├── venv/               # Python 가상환경
└── README.md           # 이 파일
```

## 주의사항

- 다운로드된 파일은 `~/Downloads/YouTube` 폴더에 저장됩니다
- 저작권이 있는 콘텐츠는 개인 사용 목적으로만 다운로드하세요
- YouTube 서비스 약관을 준수하여 사용하세요

## 업데이트

yt-dlp는 YouTube의 변경사항에 대응하기 위해 자주 업데이트됩니다:
```bash
./update.sh
```

## 라이선스

MIT License

## 기여

버그 리포트와 기능 제안은 Issues에 등록해주세요.
풀 리퀘스트는 언제나 환영합니다!
