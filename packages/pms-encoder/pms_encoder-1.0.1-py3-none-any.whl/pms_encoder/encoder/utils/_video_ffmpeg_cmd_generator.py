import ffmpeg
from ...common._config import *

def split_frame_command(
    redis_data: dict,
    meta_data: dict,
    audio: str,
) -> list:
    file_key = redis_data["fileKey"]
    output_format = redis_data["format"].lower()
    input_stream = ffmpeg.input(redis_data["filePath"])
    # if meta_data["codec_name"] == "h264":
    #     input_stream = input_stream.filter('scale', 'in_color_matrix=bt709:out_color_matrix=bt709,format=rgb24')
    args = (
        input_stream
        .output("pipe:", format="rawvideo", pix_fmt="rgb24")
        .overwrite_output()
        .compile()
    )
    if audio == "Y":
        if output_format == "mp4":
            args += [
                "-map", "0:a", "-acodec", "aac",
                "{}{}_audio.{}".format(WORK_ROOT_DIR, file_key, output_format),
            ]
        elif output_format == "mov":
            args += [
                "-map",  "0:a", "-acodec", "pcm_s16le",
                "{}{}_audio.{}".format(WORK_ROOT_DIR, file_key, output_format),
            ]
        else:
            args += [
                "-map", "0:a", "-acodec", "copy",
                "{}{}_audio.{}".format(WORK_ROOT_DIR, file_key, output_format),
            ]
    return args

def merge_frame_command(
    redis_data: dict,
    meta_data: dict,
) -> list:
    file_key = redis_data["fileKey"]
    output_format = redis_data["format"].lower()
    width = int(meta_data["width"]) if redis_data["model"] == "M001" else 2 * int(meta_data["width"])
    height = int(meta_data["height"]) if redis_data["model"] == "M001" else 2 * int(meta_data["height"])
    
    # Default value
    bv = "200000k"
    max_rate = "200000k"
    min_rate = "200000k"
    buf_size = "500000k"
    
    filter_complex = (
        "[0:v]crop=trunc(iw/2)*2:trunc(ih/2)*2[cr];[cr]colorspace=bt709:iall=bt601-6-625:fast=1" 
        if redis_data["model"] == "M001" 
        else "[0:v]colorspace=bt709:iall=bt601-6-625:fast=1"
    )
    
    filters = {
        "b:v": bv,  # Video bit_rate
        "minrate": min_rate,  # min bit_rate
        "maxrate": max_rate,  # max bit_rate
        "bufsize": buf_size,  # buffer_size
        "vcodec": redis_data["codec"],
        "filter_complex": filter_complex,
    }
    
    input_stream = ffmpeg.input(
        "pipe:",
        format="rawvideo",
        pix_fmt="rgb24",
        s="{}x{}".format(width, height),
        framerate=str(meta_data["frame_rate"]),
    )
    
    if redis_data["bestQuality"] == "Y":
        if redis_data["codec"] == "libx264" or redis_data["codec"] == "libx265":
            filters["crf"] = "0"
            
            args = (
                input_stream.output(
                    "{}{}_tmp.{}".format(WORK_ROOT_DIR, file_key, output_format),
                    pix_fmt="yuv420p10le",
                    **filters
                )
                .overwrite_output()
                .compile()
            )
            return args
        elif redis_data["codec"] == "prores_ks":
            filters["profile:v"] = "3"
            
            args = (
                input_stream.output(
                    "{}{}_tmp.{}".format(WORK_ROOT_DIR, file_key, output_format),
                    pix_fmt="yuv422p10le",
                    **filters
                )
                .overwrite_output()
                .compile()
            )
            return args
    else:
        if redis_data["twoPass"] == "N":
            filters["b:v"] = str(redis_data["bitRate"]) + "k"
            # bv = str(1000 if redis_data["bitRate"] == 0 else redis_data["bitRate"]) + "k"
            if redis_data["br"] == "VBR":
                filters["maxrate"] = "50000k"
                filters["minrate"] = "0k"
                filters["bufsize"] = "100000k"
            elif redis_data["br"] == "CBR":
                filters["maxrate"] = str(redis_data["bitRate"]) + "k"
                filters["minrate"] = str(redis_data["bitRate"]) + "k"
                filters["bufsize"] = "200000k"
        
        if redis_data["codec"] == "libx264":
            filters["profile:v"] = "high"
            filters["level:v"] = "4.2"

            args = (
                input_stream.output(
                    "{}{}_tmp.{}".format(WORK_ROOT_DIR, file_key, output_format)
                    if redis_data["twoPass"] == "N"
                    else "{}{}_max.{}".format(WORK_ROOT_DIR, file_key, output_format),
                    pix_fmt="yuv420p",
                    **filters
                )
                .overwrite_output()
                .compile()
            )
            return args
        elif redis_data["codec"] == "libx265":
            args = (
                input_stream.output(
                    "{}{}_tmp.{}".format(WORK_ROOT_DIR, file_key, output_format)
                    if redis_data["twoPass"] == "N"
                    else "{}{}_max.{}".format(WORK_ROOT_DIR, file_key, output_format),
                    pix_fmt="yuv420p10le",
                    **filters
                )
                .overwrite_output()
                .compile()
            )
            return args
        elif redis_data["codec"] == "prores_ks":
            filters["profile:v"] = "3"
            args = (
                input_stream.output(
                    "{}{}_tmp.{}".format(WORK_ROOT_DIR, file_key, output_format)
                    if redis_data["twoPass"] == "N"
                    else "{}{}_max.{}".format(WORK_ROOT_DIR, file_key, output_format),
                    pix_fmt="yuv422p10le",
                    **filters
                )
                .overwrite_output()
                .compile()
            )
            return args
        
def generate_two_pass_log_file_command(
    redis_data: dict,
    meta_data: dict,
) -> list:
    file_key = redis_data["fileKey"]
    output_format = redis_data["format"]
    
    bv = str(1000 if redis_data["bitRate"] == 0 else redis_data["bitRate"]) + "k"
    if redis_data["br"] == "VBR":
        max_rate = "50000k"
        min_rate = "0k"
        buf_size = "100000k"
    elif redis_data["br"] == "CBR":
        max_rate = str(redis_data["bitRate"]) + "k"
        min_rate = str(redis_data["bitRate"]) + "k"
        buf_size = "200000k"
        
    filters = {
        "b:v": bv,  # Video bit_rate
        "minrate": min_rate,  # min bit_rate
        "maxrate": max_rate,  # max bit_rate
        "bufsize": buf_size,  # buffer_size
        "vcodec": redis_data["codec"],
        "passlogfile": "{}{}".format(WORK_ROOT_DIR, file_key),
        "pass": "1",
    }
        
    if redis_data["codec"] == "libx264":
        filters["profile:v"] = "high"
        filters["level:v"] = "4.2"
        args = (
            ffmpeg.input(
                 "{}{}_max.{}".format(WORK_ROOT_DIR, file_key, output_format),
            )
            .output(
                "{}{}_dummy.{}".format(WORK_ROOT_DIR, file_key, output_format),
                pix_fmt="yuv420p",
                **filters,
            )
            .overwrite_output()
            .compile()
        )
        return args
    elif redis_data["codec"] == "libx265":
        args = (
            ffmpeg.input(
                 "{}{}_max.{}".format(WORK_ROOT_DIR, file_key, output_format),
            )
            .output(
                "{}{}_dummy.{}".format(WORK_ROOT_DIR, file_key, output_format),
                pix_fmt="yuv420p10le",
                **filters,
            )
            .overwrite_output()
            .compile()
        )
        return args
    elif redis_data["codec"] == "prores_ks":
        filters["profile:v"] = "3"
        args = (
            ffmpeg.input(
                 "{}{}_max.{}".format(WORK_ROOT_DIR, file_key, output_format),
            )
            .output(
                "{}{}_dummy.{}".format(WORK_ROOT_DIR, file_key, output_format),
                pix_fmt="yuv422p10le",
                **filters,
            )
            .overwrite_output()
            .compile()
        )
        return args
    
def two_pass_encode_command(
    redis_data: dict,
    meta_data: dict,
) -> list:
    file_key = redis_data["fileKey"]
    output_format = redis_data["format"]
    
    bv = str(1000 if redis_data["bitRate"] == 0 else redis_data["bitRate"]) + "k"
    if redis_data["br"] == "VBR":
        max_rate = "50000k"
        min_rate = "0k"
        buf_size = "100000k"
    elif redis_data["br"] == "CBR":
        max_rate = str(redis_data["bitRate"]) + "k"
        min_rate = str(redis_data["bitRate"]) + "k"
        buf_size = "200000k"
        
    filters = {
        "b:v": bv,  # Video bit_rate
        "minrate": min_rate,  # min bit_rate
        "maxrate": max_rate,  # max bit_rate
        "bufsize": buf_size,  # buffer_size
        "vcodec": redis_data["codec"],
        "passlogfile": "{}{}".format(WORK_ROOT_DIR, file_key),
        "pass": "2",
    }
        
    if redis_data["codec"] == "libx264":
        filters["profile:v"] = "high"
        filters["level:v"] = "4.2"
        args = (
            ffmpeg.input(
                 "{}{}_max.{}".format(WORK_ROOT_DIR, file_key, output_format),
            )
            .output(
                "{}{}_tmp.{}".format(WORK_ROOT_DIR, file_key, output_format),
                pix_fmt="yuv420p",
                **filters,
            )
            .overwrite_output()
            .compile()
        )
        return args
    elif redis_data["codec"] == "libx265":
        args = (
            ffmpeg.input(
                 "{}{}_max.{}".format(WORK_ROOT_DIR, file_key, output_format),
            )
            .output(
                "{}{}_tmp.{}".format(WORK_ROOT_DIR, file_key, output_format),
                pix_fmt="yuv420p10le",
                **filters,
            )
            .overwrite_output()
            .compile()
        )
        return args
    elif redis_data["codec"] == "prores_ks":
        filters["profile:v"] = "3"
        args = (
            ffmpeg.input(
                 "{}{}_max.{}".format(WORK_ROOT_DIR, file_key, output_format),
            )
            .output(
                "{}{}_tmp.{}".format(WORK_ROOT_DIR, file_key, output_format),
                pix_fmt="yuv422p10le",
                **filters,
            )
            .overwrite_output()
            .compile()
        )
        return args

def merge_audio_command(
    redis_data: dict
) -> list:
    file_key = redis_data["fileKey"]
    output_format = redis_data["format"].lower()
    
    args = [
        "ffmpeg", "-i", "{}{}_tmp.{}".format(WORK_ROOT_DIR, file_key, output_format),
        "-i", "{}{}_audio.{}".format(WORK_ROOT_DIR, file_key, output_format),
        "-map", "0:v",  "-map", "1:a",  "-c", "copy", "-y",
        "{}{}.{}".format(WORK_ROOT_DIR, file_key, output_format),
    ]
    return args
    
    
def generate_sub_output(
    redis_data: dict,
    output_file_path: str,
    sub_output_path: str,
) -> list:
    args = (
        ffmpeg.input(
            output_file_path
        )
        .output(
            sub_output_path,
            vf="scale={}x{},setsar=1".format(redis_data["resizeWidth"], redis_data["resizeHeight"])
        )
        .overwrite_output()
        .compile()
    )
    return args