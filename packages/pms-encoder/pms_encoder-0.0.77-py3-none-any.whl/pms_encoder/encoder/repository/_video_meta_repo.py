import datetime
from ...common._mysql_client import MySQLClient

def insert_inferenced_file_meta(
    redis_data: dict,
    original_data: dict, 
    inferenced_data: dict,
    format_data: dict,
    file_size: int,
    audio: str,
) -> None:
    ffmpeg_duration = float(original_data['duration'])
    hours, remainder = divmod(ffmpeg_duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_duration = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
    frame_rate_fraction = inferenced_data["r_frame_rate"]
    frame_rate_numerator, frame_rate_denominator = map(int, frame_rate_fraction.split('/'))
    frame_rate = frame_rate_numerator / frame_rate_denominator
    now = datetime.datetime.now()
    
    sql = """
    INSERT INTO pixell_v2.upload_files_meta_pixell
    (content_type, file_key, combined_file_key, file_name, file_type, file_size, width, height, codec, duration, bit_rate, frame_rate, frames, audio, date_created, user_created, date_modified, user_modified) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    val = (
        redis_data["contentType"],
        redis_data["fileKey"],
        None,
        redis_data["fileName"],
        redis_data["format"].lower(),
        file_size,
        inferenced_data["width"],
        inferenced_data["height"],
        inferenced_data["codec_long_name"],
        formatted_duration,
        format_data["bit_rate"],
        frame_rate,
        original_data["nb_frames"],
        audio,
        now, 'encoder', now, 'encoder'
    )
    
    client = MySQLClient()
    client.execute(sql, val)