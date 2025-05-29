#!/usr/bin/env python3
"""
YouTube Video Downloader Web App
A simple web-based YouTube downloader for macOS
"""

from flask import Flask, render_template, request, jsonify
import yt_dlp
import os
import json
from datetime import datetime
import threading
import re
import sys

app = Flask(__name__)

# 다운로드 디렉토리 설정
DOWNLOAD_DIR = os.path.expanduser("~/Downloads/YouTube")
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# 다운로드 진행 상태를 저장하는 딕셔너리
download_progress = {}

# 디버깅 모드
DEBUG_MODE = True

def log_debug(message):
    """디버그 메시지 출력"""
    if DEBUG_MODE:
        print(f"[DEBUG] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")

def sanitize_filename(filename):
    """파일명에서 사용할 수 없는 문자 제거"""
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = filename.strip('. ')
    if not filename:
        filename = "download"
    return filename

def download_video(url, download_id):
    """비디오 다운로드 함수"""
    try:
        log_debug(f"다운로드 시작: {url}")
        
        def progress_hook(d):
            if d['status'] == 'downloading':
                download_progress[download_id] = {
                    'status': 'downloading',
                    'percent': d.get('_percent_str', '0%'),
                    'speed': d.get('_speed_str', 'N/A'),
                    'eta': d.get('_eta_str', 'N/A')
                }
                log_debug(f"다운로드 중: {d.get('_percent_str', '0%')}")
            elif d['status'] == 'finished':
                download_progress[download_id] = {
                    'status': 'processing',
                    'percent': '99%'
                }
                log_debug("다운로드 완료, 처리 중...")
            elif d['status'] == 'error':
                download_progress[download_id] = {
                    'status': 'error',
                    'error': 'Download failed'
                }

        # 고화질 다운로드를 위한 포맷 설정
        ydl_opts = {
            # 최고 화질 비디오 + 최고 음질 오디오
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',  # 병합 후 mp4로 저장
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            # 디버깅 옵션
            'quiet': False,
            'verbose': True,
            # 안정성 옵션
            'no_warnings': False,
            'ignoreerrors': False,
            'no_color': True,
            'prefer_ffmpeg': True,
            'keepvideo': False,
            # 네트워크 옵션
            'retries': 10,
            'fragment_retries': 10,
            'concurrent_fragment_downloads': 4,
            # 후처리 옵션
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }

        # 다운로드 실행
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            log_debug("yt-dlp 인스턴스 생성 완료")
            info = ydl.extract_info(url, download=True)
            log_debug(f"다운로드 완료: {info.get('title', 'Unknown')}")
            
            download_progress[download_id] = {
                'status': 'finished',
                'percent': '100%'
            }
            
    except Exception as e:
        error_msg = str(e)
        log_debug(f"오류 발생: {error_msg}")
        
        # 사용자 친화적 에러 메시지
        if 'Unsupported URL' in error_msg:
            error_msg = "지원하지 않는 URL 형식입니다. YouTube URL인지 확인해주세요."
        elif 'Failed to extract any player response' in error_msg:
            error_msg = "YouTube 접속 오류. yt-dlp를 업데이트하거나 다른 동영상을 시도해보세요."
        elif 'Private video' in error_msg:
            error_msg = "비공개 동영상입니다."
        elif 'Video unavailable' in error_msg:
            error_msg = "사용할 수 없는 동영상입니다."
        elif 'Requested format is not available' in error_msg:
            error_msg = "요청한 화질을 사용할 수 없습니다."
        elif 'ffmpeg' in error_msg.lower() or 'FFmpeg' in error_msg:
            error_msg = "FFmpeg가 설치되지 않았습니다. 터미널에서 'brew install ffmpeg'를 실행해주세요."
        
        download_progress[download_id] = {
            'status': 'error',
            'error': error_msg
        }

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_video_info():
    """비디오 정보 가져오기"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL이 필요합니다.'}), 400
        
        log_debug(f"정보 조회: {url}")
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # 사용 가능한 포맷 정보 로깅
            formats = info.get('formats', [])
            video_formats = [f for f in formats if f.get('vcodec') != 'none']
            audio_formats = [f for f in formats if f.get('acodec') != 'none']
            
            log_debug(f"비디오 포맷 수: {len(video_formats)}")
            log_debug(f"오디오 포맷 수: {len(audio_formats)}")
            
            # 최고 화질 확인
            if video_formats:
                best_video = max(video_formats, key=lambda x: x.get('height', 0))
                log_debug(f"최고 화질: {best_video.get('height', 0)}p")
            
            video_info = {
                'title': info.get('title', 'Unknown'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': info.get('view_count', 0)
            }
            
            log_debug(f"비디오 정보: {video_info['title']}")
            return jsonify(video_info)
            
    except Exception as e:
        error_msg = str(e)
        log_debug(f"정보 조회 오류: {error_msg}")
        
        if 'Unsupported URL' in error_msg:
            return jsonify({'error': '올바른 YouTube URL을 입력해주세요.'}), 400
        else:
            return jsonify({'error': '동영상 정보를 가져올 수 없습니다.'}), 500

@app.route('/download', methods=['POST'])
def download():
    """다운로드 시작"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL이 필요합니다.'}), 400
        
        download_id = f"{datetime.now().timestamp()}"
        download_progress[download_id] = {
            'status': 'starting',
            'percent': '0%'
        }
        
        log_debug(f"다운로드 작업 시작: ID={download_id}")
        
        thread = threading.Thread(
            target=download_video,
            args=(url, download_id)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({'download_id': download_id})
        
    except Exception as e:
        log_debug(f"다운로드 시작 오류: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/progress/<download_id>')
def get_progress(download_id):
    """다운로드 진행 상태 확인"""
    progress = download_progress.get(download_id, {'status': 'not_found'})
    return jsonify(progress)

@app.route('/downloads')
def list_downloads():
    """다운로드된 파일 목록"""
    try:
        files = []
        if os.path.exists(DOWNLOAD_DIR):
            for filename in os.listdir(DOWNLOAD_DIR):
                # .DS_Store 등 숨김 파일 제외
                if filename.startswith('.'):
                    continue
                    
                filepath = os.path.join(DOWNLOAD_DIR, filename)
                if os.path.isfile(filepath):
                    files.append({
                        'name': filename,
                        'size': os.path.getsize(filepath),
                        'modified': os.path.getmtime(filepath)
                    })
        
        files.sort(key=lambda x: x['modified'], reverse=True)
        return jsonify(files)
        
    except Exception as e:
        log_debug(f"파일 목록 오류: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/test')
def test():
    """테스트 엔드포인트"""
    try:
        import yt_dlp
        version = yt_dlp.version.__version__
    except:
        version = "Unknown"
    
    return jsonify({
        'status': 'ok',
        'python_version': sys.version,
        'yt_dlp_version': version,
        'download_dir': DOWNLOAD_DIR,
        'ffmpeg_check': os.system('which ffmpeg > /dev/null 2>&1') == 0
    })

if __name__ == '__main__':
    print(f"""
    ╔════════════════════════════════════════╗
    ║     YouTube Downloader for macOS       ║
    ╠════════════════════════════════════════╣
    ║  웹 브라우저에서 다음 주소로 접속하세요:  ║
    ║  http://localhost:6274                 ║
    ║                                        ║
    ║  다운로드 위치:                         ║
    ║  {DOWNLOAD_DIR:<36}║
    ║                                        ║
    ║  종료하려면 Ctrl+C를 누르세요           ║
    ╚════════════════════════════════════════╝
    
    테스트: http://localhost:6274/test
    """)
    
    # 디버그 모드로 실행
    app.run(debug=True, port=6274, host='0.0.0.0')
