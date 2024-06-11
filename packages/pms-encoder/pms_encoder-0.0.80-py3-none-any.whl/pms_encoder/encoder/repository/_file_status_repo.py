import datetime
from ...common._mysql_client import MySQLClient

def set_start_status(
    file_key: str,
) -> None:
    sql = """
    UPDATE pixell_v2.upload_files
    SET status = 'T',
    date_started = %s,
    date_modified = %s,
    user_modified = 'encoder' 
    WHERE file_key = %s
    """
    now = datetime.datetime.now()
    val = (now, now, file_key)
    client = MySQLClient()
    client.execute(sql, val)
    
    
def set_reject_status(
    file_key: str,
) -> None:
    sql = """
    UPDATE pixell_v2.upload_files
    SET status = 'R',
    date_modified = %s,
    user_modified = 'encoder' 
    WHERE file_key = %s
    """
    now = datetime.datetime.now()
    val = (now, file_key)
    client = MySQLClient()
    client.execute(sql, val)

def set_success_status(
    file_key: str,
) -> None:
    sql = """
    UPDATE pixell_v2.upload_files
    SET status = 'S',
    date_worked = %s, 
    date_modified = %s,
    user_modified = 'encoder' 
    WHERE file_key = %s
    """
    now = datetime.datetime.now()
    val = (now, now, file_key)
    client = MySQLClient()
    client.execute(sql, val)