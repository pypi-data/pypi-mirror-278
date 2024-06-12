import zipfile
import os

def zip_directory(
    folder_path: str,
    output_path: str 
) -> None:
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # absolute path
                abs_path = os.path.join(root, file)
                # 파일을 ZIP 파일에 추가합니다 (압축 경로 내에서의 상대 경로로 저장)
                zipf.write(abs_path, os.path.relpath(abs_path, folder_path))