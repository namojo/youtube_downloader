#!/bin/bash

# 스크립트가 있는 디렉토리로 이동
cd "$(dirname "$0")"

# 가상환경 활성화
if [ ! -d "venv" ]; then
    echo "가상환경이 없습니다. install.sh를 먼저 실행해주세요."
    exit 1
fi

source venv/bin/activate

# Flask 앱 실행
python3 app.py
