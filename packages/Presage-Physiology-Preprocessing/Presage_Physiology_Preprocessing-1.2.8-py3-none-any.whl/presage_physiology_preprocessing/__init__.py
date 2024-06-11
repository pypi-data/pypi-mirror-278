from .preprocessing import video_preprocess
from .version import __version__
def process(video_path, HR_FPS=30, DN_SAMPLE=1):
    return video_preprocess(video_path, HR_FPS, DN_SAMPLE)
