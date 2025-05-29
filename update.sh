#!/bin/bash

echo "yt-dlp를 최신 버전으로 업데이트합니다..."
echo ""

# 스크립트가 있는 디렉토리로 이동
cd "$(dirname "$0")"

# 가상환경 활성화
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ 가상환경이 없습니다. install.sh를 먼저 실행해주세요."
    exit 1
fi

# 현재 버전 표시
echo "현재 버전:"
yt-dlp --version

# yt-dlp nightly 빌드로 업데이트
echo ""
echo "최신 nightly 빌드로 업데이트 중..."
pip install --upgrade --force-reinstall "yt-dlp @ https://github.com/yt-dlp/yt-dlp-nightly-builds/releases/latest/download/yt-dlp.tar.gz"

echo ""
echo "✅ 업데이트 완료!"
echo "새 버전:"
yt-dlp --version
