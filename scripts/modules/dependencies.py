import os
import urllib.request
import zipfile
import tempfile
from core.file_utils import ensure_dir

def _is_excluded(filename, excludes_list):
    filename_lower = filename.lower()
    return any(filename_lower.endswith(ext.lower()) for ext in excludes_list)

def _download_and_extract(url, target_dir, excludes):
    print(f"  -> Downloading: {url}")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_file:
        tmp_path = tmp_file.name
        
    try:
        with urllib.request.urlopen(req) as response:
            with open(tmp_path, 'wb') as out_file:
                out_file.write(response.read())
                
        print(f"  -> Extracting into {target_dir}...")
        with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                base_name = os.path.basename(member)
                
                if base_name and _is_excluded(base_name, excludes):
                    print(f"    [Skipped] {member}")
                    continue
                    
                zip_ref.extract(member, target_dir)
            
    except zipfile.BadZipFile:
        print(f"  [ERROR] The downloaded file from {url} is not a valid zip archive.")
    except Exception as e:
        print(f"  [ERROR] Failed to process {url}: {e}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def run(config, paths):
    print("--- Running Dependencies Manager ---")
    
    deps = config.get("dependencies", {})
    java_urls = deps.get("java", [])
    bedrock_urls = deps.get("bedrock", [])
    
    excludes = config.get("global_excludes", [])
    
    if java_urls:
        print(f"Processing {len(java_urls)} Java dependencies...")
        ensure_dir(paths["java_dist"])
        for url in java_urls:
            _download_and_extract(url, paths["java_dist"], excludes)
            
    if bedrock_urls:
        print(f"Processing {len(bedrock_urls)} Bedrock dependencies...")
        ensure_dir(paths["bedrock_dist"])
        for url in bedrock_urls:
            _download_and_extract(url, paths["bedrock_dist"], excludes)
            
    print("Dependencies merging completed.\n")