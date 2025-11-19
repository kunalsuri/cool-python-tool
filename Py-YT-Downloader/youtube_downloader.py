import streamlit as st
import yt_dlp
import os
import time
from pathlib import Path
import shutil

# --- Page Configuration ---
st.set_page_config(
    page_title="Ultra YT Downloader",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for "Wow" Effect ---
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .video-card {
        background-color: #262730;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stat-box {
        background-color: #0e1117;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Constants ---
DOWNLOAD_DIR = Path.home() / "Downloads"
if not os.access(DOWNLOAD_DIR, os.W_OK):
    st.warning(f"⚠️ No write access to {DOWNLOAD_DIR}. Using local 'downloads' folder instead.")
    DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

if not shutil.which("ffmpeg"):
    st.error("⚠️ FFmpeg is not installed. Some features (like Audio Only or High Quality Video merging) may not work. Please install FFmpeg.")

# --- Helper Functions ---

def format_bytes(size):
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {power_labels[n]}B"

def get_video_info(url):
    ydl_opts = {'quiet': True, 'no_warnings': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)
    except Exception:
        return None

def download_content(url, type_mode, resolution=None):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    def progress_hook(d):
        if d['status'] == 'downloading':
            try:
                p = d.get('_percent_str', '0%').replace('%','')
                progress_bar.progress(float(p)/100)
                status_text.markdown(f"**Downloading...** {d.get('_percent_str')} | 🚀 {d.get('_speed_str')} | ⏳ {d.get('_eta_str')}")
            except Exception:
                pass
        elif d['status'] == 'finished':
            progress_bar.progress(1.0)
            status_text.markdown("**Processing completed!** ✅")

    ydl_opts = {
        'outtmpl': str(DOWNLOAD_DIR / '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_warnings': True,
        'merge_output_format': 'mp4',  # Force MP4 container
    }

    if type_mode == "Audio Only (MP3)":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        # Video mode
        if resolution == "Best Available":
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
        elif resolution == "4K":
            ydl_opts['format'] = 'bestvideo[height>=2160]+bestaudio/best[height>=2160]'
        elif resolution == "1080p":
            ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
        elif resolution == "720p":
            ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True, "Download successful!"
    except Exception as e:
        return False, str(e)

# --- Main App Structure ---

def main():
    st.sidebar.title("⚡ Ultra Downloader")
    app_mode = st.sidebar.radio("Navigation", ["📥 Downloader", "📂 Library"])
    
    if app_mode == "📥 Downloader":
        render_downloader()
    elif app_mode == "📂 Library":
        render_library()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown('Made with ❤️ by [Kunal Suri](https://github.com/kunalsuri/)')

def render_video_info(info):
    st.markdown("---")
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.image(info.get('thumbnail'), use_container_width=True, output_format="JPEG")
        
    with col2:
        st.subheader(info.get('title'))
        st.markdown(f"**👤 Channel:** {info.get('uploader')}")
        
        # Stats Grid
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='stat-box'>⏱️ {time.strftime('%H:%M:%S', time.gmtime(info.get('duration', 0)))}</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='stat-box'>👁️ {info.get('view_count', 0):,}</div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='stat-box'>📅 {info.get('upload_date', 'N/A')}</div>", unsafe_allow_html=True)

def render_download_options(url):
    st.markdown("### ⚙️ Download Options")
    
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        type_mode = st.selectbox("Format", ["Video + Audio", "Audio Only (MP3)"])
    
    resolution = None
    if type_mode == "Video + Audio":
        with d_col2:
            resolution = st.selectbox("Quality", ["Best Available", "4K", "1080p", "720p"])
    
    col_start, col_stop = st.columns(2)
    with col_start:
        if st.button("⬇️ Start Download", type="primary"):
            with st.spinner("Initializing download..."):
                success, msg = download_content(url, type_mode, resolution)
                if success:
                    st.balloons()
                    st.success(f"Done! Saved to {DOWNLOAD_DIR}")
                    st.toast("Download Completed!", icon="🎉")
                else:
                    st.error(f"Download failed: {msg}")
    
    with col_stop:
        if st.button("🛑 Stop / Cancel"):
            st.warning("To stop the download, please refresh the page or close the tab. (Streamlit limitation)")
            st.stop()

def render_downloader():
    st.title("🚀 Ultimate YouTube Downloader")
    st.markdown("### Download videos in highest quality with ease")
    
    # URL Input Section
    url = st.text_input("Paste YouTube URL here", placeholder="https://youtube.com/watch?v=...")
    
    if url:
        if 'current_url' not in st.session_state or st.session_state.current_url != url:
            st.session_state.current_url = url
            st.session_state.video_info = None
        
        if st.button("🔍 Analyze Video"):
            with st.spinner("Fetching video metadata..."):
                info = get_video_info(url)
                if info:
                    st.session_state.video_info = info
                else:
                    st.error("Could not fetch video info. Please check the URL.")

    # Display Video Info & Download Options
    if st.session_state.get('video_info'):
        render_video_info(st.session_state.video_info)
        render_download_options(url)

def render_file_item(file_path):
    with st.expander(f"📄 {file_path.name}"):
        c1, c2 = st.columns([3, 1])
        with c1:
            st.caption(f"Size: {format_bytes(file_path.stat().st_size)} | Date: {time.ctime(file_path.stat().st_mtime)}")
        with c2:
            if st.button("🗑️ Delete", key=f"del_{file_path.name}"):
                os.remove(file_path)
                st.rerun()
        
        if file_path.suffix.lower() in ['.mp4', '.mkv', '.webm']:
            st.video(str(file_path))
        elif file_path.suffix.lower() in ['.mp3', '.m4a', '.wav']:
            st.audio(str(file_path))

def render_library():
    st.title("📂 Download Library")
    st.markdown("### Your downloaded content")
    
    files = sorted(DOWNLOAD_DIR.glob("*.*"), key=os.path.getmtime, reverse=True)
    
    if not files:
        st.info("No downloads yet. Go to the Downloader tab to get started!")
        return

    # Filter options
    filter_type = st.selectbox("Filter by type", ["All", "Video", "Audio"])
    
    for file_path in files:
        is_video = file_path.suffix.lower() in ['.mp4', '.mkv', '.webm']
        is_audio = file_path.suffix.lower() in ['.mp3', '.m4a', '.wav']
        
        if filter_type == "Video" and not is_video:
            continue
        if filter_type == "Audio" and not is_audio:
            continue
            
        render_file_item(file_path)

if __name__ == "__main__":
    main()
