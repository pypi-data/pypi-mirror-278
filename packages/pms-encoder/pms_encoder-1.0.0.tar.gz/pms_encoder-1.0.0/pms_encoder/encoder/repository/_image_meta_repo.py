import datetime
from ...common._mysql_client import MySQLClient

def get_images_meta(
    file_key: str,
    combined: str,
) -> list:
    if combined == "Y":
        sql = """
        SELECT * FROM pixell_v2.upload_files_meta_original
        WHERE combined_file_key = %s 
        """
    else:
        sql = """
        SELECT * FROM pixell_v2.upload_files_meta_original
        WHERE file_key = %s 
        """
    val = (file_key,)
    client = MySQLClient()
    return client.fetchall(sql, val)

def get_upload_file(
    file_key: str,
) -> dict:
    sql = """
    SELECT * FROM pixell_v2.upload_files
    WHERE file_key = %s 
    """
    val = (file_key,)
    client = MySQLClient()
    return client.fetchone(sql, val)

def insert_image_file_pixell_meta(
    frame_id: int,
    frame_map: dict,
    meta_data: dict,
    file_size: int
) -> None:
    now = datetime.datetime.now()
    sql = """
    INSERT INTO pixell_v2.upload_files_meta_pixell
    (content_type, file_key, combined_file_key, file_name, file_type, file_size, width, height, codec, duration, bit_rate, frame_rate, frames, audio, date_created, user_created, date_modified, user_modified) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    val = (
        "image",
        frame_map[str(frame_id)]["file_key"],
        frame_map[str(frame_id)]["combined_file_key"],
        frame_map[str(frame_id)]["file_name"],
        frame_map[str(frame_id)]["file_type"].lower(),
        file_size,
        meta_data["width"],
        meta_data["height"],
        None,
        None,
        None,
        None,
        None,
        'N',
        now, 'encoder', now, 'encoder'
    )
    client = MySQLClient()
    client.execute(sql, val)