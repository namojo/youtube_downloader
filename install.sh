#!/bin/bash

echo "YouTube Downloader 설치를 시작합니다..."
echo ""

# Python 3 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3가 설치되어 있지 않습니다."
    echo "   Homebrew를 통해 Python을 설치해주세요: brew install python3"
    exit 1
fi

echo "✅ Python 3 확인됨"

# FFmpeg 확인
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg가 설치되어 있지 않습니다."
    echo "   고화질 다운로드를 위해 FFmpeg가 필요합니다."
    echo "   설치하려면: brew install ffmpeg"
else
    echo "✅ FFmpeg 확인됨"
fi

# 가상환경 생성
echo ""
echo "가상환경을 생성합니다..."
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

# pip 업그레이드
echo ""
echo "pip를 최신 버전으로 업그레이드합니다..."
pip install --upgrade pip

# 필요한 패키지 설치
echo ""
echo "필요한 패키지를 설치합니다..."
pip install flask

# yt-dlp nightly 빌드 설치
echo ""
echo "yt-dlp 최신 nightly 빌드를 설치합니다..."
pip install --force-reinstall "yt-dlp @ https://github.com/yt-dlp/yt-dlp-nightly-builds/releases/latest/download/yt-dlp.tar.gz"

echo ""
echo "설치된 버전 확인:"
echo "Python: $(python3 --version)"
echo "Flask: $(pip show flask | grep Version)"
echo "yt-dlp: $(yt-dlp --version)"

echo ""
echo "✅ 설치가 완료되었습니다!"
echo ""
echo "실행 방법:"
echo "1. ./run.sh"
echo "2. 웹 브라우저에서 http://localhost:6274 접속"
echo ""
echo "주의: FFmpeg가 없으면 고화질 다운로드가 실패할 수 있습니다."
