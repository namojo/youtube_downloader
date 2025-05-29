#!/bin/bash

echo "YouTube Downloader 긴급 패치"
echo "============================"
echo ""

# 스크립트가 있는 디렉토리로 이동
cd "$(dirname "$0")"

# 가상환경 확인
if [ ! -d "venv" ]; then
    echo "❌ 가상환경이 없습니다. install.sh를 먼저 실행하세요."
    exit 1
fi

source venv/bin/activate

echo "1. 시스템 yt-dlp 확인..."
if command -v yt-dlp &> /dev/null; then
    echo "시스템 yt-dlp 버전: $(yt-dlp --version)"
fi

echo ""
echo "2. 모든 yt-dlp 제거..."
pip uninstall -y yt-dlp yt-dlp-nightly-builds youtube-dl

echo ""
echo "3. pip 캐시 완전 삭제..."
pip cache purge
rm -rf ~/.cache/pip

echo ""
echo "4. 최신 nightly 빌드 설치..."
pip install -U --force-reinstall "yt-dlp @ https://github.com/yt-dlp/yt-dlp-nightly-builds/releases/latest/download/yt-dlp.tar.gz"

echo ""
echo "5. 설치 확인..."
python -c "import yt_dlp; print(f'yt-dlp 버전: {yt_dlp.version.__version__}')"

echo ""
echo "6. 간단한 테스트..."
TEST_URL="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
echo "테스트 URL: $TEST_URL"

if python -c "
import yt_dlp
ydl_opts = {
    'quiet': True,
    'no_warnings': True,
    'extract_flat': True,
    'extractor_args': {
        'youtube': {
            'player_client': ['android', 'web', 'ios'],
            'player_skip': ['config', 'initial']
        }
    }
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info('$TEST_URL', download=False)
    print(f'✅ 성공: {info.get(\"title\", \"Unknown\")}')
" 2>/dev/null; then
    echo ""
    echo "✅ 테스트 성공!"
else
    echo ""
    echo "❌ 아직 문제가 있습니다. 추가 조치를 시도합니다..."
    
    echo ""
    echo "7. 대체 방법: 직접 최신 커밋 설치..."
    pip uninstall -y yt-dlp
    pip install --no-deps -U "git+https://github.com/yt-dlp/yt-dlp.git@master"
    pip install -U pycryptodomex websockets brotli certifi requests
fi

echo ""
echo "8. 최종 버전:"
yt-dlp --version

echo ""
echo "✅ 패치 완료!"
echo ""
echo "이제 다음을 실행하세요:"
echo "1. ./run.sh"
echo ""
echo "여전히 문제가 있다면:"
echo "1. 몇 시간 후 다시 시도 (YouTube 측 일시적 변경)"
echo "2. 다른 동영상 URL로 테스트"
echo "3. VPN 사용 시 끄고 재시도"
