import ffmpeg
import subprocess
import json

def get_media_metadata(
    filePath: str
):
    command = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_error",
        "-show_format",
        "-show_streams",
        filePath
    ]
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = process.stdout.decode('utf-8')
    
    jsonObject = json.loads(result)
    
    audio = "N"
    metaObject = None
    
    streams = jsonObject.get("streams", [])
    for stream in streams:
        if stream.get("codec_type") == "video":
            metaObject = stream
        if stream.get("codec_type") == "audio":
            audio = "Y"
    
    if metaObject is None:
        logger.warn(f">>> File {filePath} Not Found Meta Data")
        raise IOError("Not Found Meta Data")
    
    metaObject["audio"] = audio
    
    return metaObject