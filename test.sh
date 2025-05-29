#!/bin/bash

echo "YouTube Downloader 간단 테스트"
echo "=============================="
echo ""

cd "$(dirname "$0")"

# 가상환경 활성화
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ 가상환경이 없습니다."
    exit 1
fi

echo "1. Python에서 yt-dlp 직접 테스트..."
python3 << 'EOF'
import yt_dlp

# 간단한 테스트
url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
print(f"테스트 URL: {url}")

try:
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print(f"✅ 성공: {info.get('title', 'Unknown')}")
        print(f"   업로더: {info.get('uploader', 'Unknown')}")
        print(f"   길이: {info.get('duration', 0)}초")
        
except Exception as e:
    print(f"❌ 실패: {str(e)}")
    print("\n해결 방법:")
    print("1. ./update.sh 실행")
    print("2. ./emergency_fix.sh 실행")

EOF

echo ""
echo "2. Flask 앱 테스트 (5초간)..."
echo "브라우저에서 http://localhost:6274/test 접속"
echo ""

# 5초 타임아웃으로 Flask 실행
timeout 5 python3 app.py || true

echo ""
echo "테스트 완료!"
echo ""
echo "문제가 없다면 ./run.sh로 정상 실행하세요."
