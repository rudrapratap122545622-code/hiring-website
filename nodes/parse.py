import os
import re
import requests
import gdown
from pypdf import PdfReader


def download_google_drive_file(file_id: str, output_path: str) -> bool:
    """Downloads Google Drive file using gdown with a requests session fallback."""
    # Method 1: gdown
    try:
        res = gdown.download(id=file_id, output=output_path, quiet=True)
        if res and os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            with open(output_path, "rb") as f:
                if f.read(4).startswith(b"%PDF"):
                    return True
    except Exception:
        pass

    # Method 2: Direct HTTP request stream with session cookie handling
    try:
        url = "https://docs.google.com/uc?export=download"
        session = requests.Session()
        response = session.get(url, params={"id": file_id}, stream=True)

        # Check for Google Drive download warning token (large files)
        token = None
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                token = value
                break

        if token:
            response = session.get(url, params={"id": file_id, "confirm": token}, stream=True)

        if response.status_code == 200:
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=32768):
                    if chunk:
                        f.write(chunk)

            if os.path.exists(output_path) and os.path.getsize(output_path) > 500:
                with open(output_path, "rb") as f:
                    if f.read(4).startswith(b"%PDF"):
                        return True
    except Exception:
        pass

    return False


def extract_text_from_file(file_path_or_url: str) -> str:
    """Extracts raw text from local PDF files or Google Drive URLs."""
    temp_filename = "temp_resume.pdf"

    # Handle remote URLs vs local file paths
    if file_path_or_url.startswith(("http://", "https://")):
        match = re.search(r"/d/([a-zA-Z0-9_-]+)", file_path_or_url) or re.search(r"id=([a-zA-Z0-9_-]+)", file_path_or_url)

        if not match:
            raise ValueError(f"Could not extract Google Drive File ID from URL: {file_path_or_url}")

        file_id = match.group(1)
        success = download_google_drive_file(file_id, temp_filename)

        if not success:
            raise RuntimeError(
                "Failed to download PDF from Google Drive. "
                "Ensure the link permission is set to 'Anyone with the link'."
            )
        file_path = temp_filename
    else:
        file_path = file_path_or_url

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Extract text using PyPDF
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    # Clean up temporary downloaded file
    if file_path_or_url.startswith(("http://", "https://")) and os.path.exists(temp_filename):
        os.remove(temp_filename)

    return text.strip()
