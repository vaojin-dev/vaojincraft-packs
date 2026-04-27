import os
import shutil
from core.file_utils import load_json, ensure_dir

def _load_all_mappings(mappings_dir):
    combined_mapping = {"files": {}, "directories": {}}
    
    if not os.path.exists(mappings_dir):
        print(f"Warning: Mappings directory not found at {mappings_dir}.")
        return combined_mapping

    for filename in os.listdir(mappings_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(mappings_dir, filename)
            data = load_json(filepath)
            combined_mapping["files"].update(data.get("files", {}))
            combined_mapping["directories"].update(data.get("directories", {}))
                
    return combined_mapping

def _is_excluded(filename, excludes_list):
    for ext in excludes_list:
        if filename.endswith(ext):
            return True
    return False

def _resolve_bedrock_path(source_rel_path, mapping_config):
    files_mapping = mapping_config.get("files", {})
    if source_rel_path in files_mapping:
        return files_mapping[source_rel_path]

    dirs_mapping = mapping_config.get("directories", {})
    for source_dir, target_dir in dirs_mapping.items():
        source_dir_normalized = source_dir.replace("\\", "/")
        if source_rel_path.startswith(source_dir_normalized):
            return source_rel_path.replace(source_dir_normalized, target_dir, 1)

    return None

def _copy_exclusive_files(exclusive_dir, target_dir, platform_name):
    if os.path.exists(exclusive_dir):
        # dirs_exist_ok=True allows merging into an existing directory
        shutil.copytree(exclusive_dir, target_dir, dirs_exist_ok=True)
        print(f"Copied {platform_name} exclusive files.")
    else:
        print(f"Notice: No exclusive folder found for {platform_name} at {exclusive_dir}")

def run(config, paths):
    print("--- Running Static Assets Mapper ---")
    
    _copy_exclusive_files(paths["java_exclusive"], paths["java_dist"], "Java")
    _copy_exclusive_files(paths["bedrock_exclusive"], paths["bedrock_dist"], "Bedrock")
    
    commons_dir = paths["commons_dir"]
    java_dist = paths["java_dist"]
    bedrock_dist = paths["bedrock_dist"]
    mappings_dir = paths["mappings_dir"]
    
    excludes = config.get("global_excludes", [])
    mappings = _load_all_mappings(mappings_dir)

    java_copied = 0
    bedrock_copied = 0

    print("Mapping shared assets from commons...")
    for root, _, files in os.walk(commons_dir):
        for file in files:
            if _is_excluded(file, excludes):
                continue
                
            absolute_source_path = os.path.join(root, file)
            rel_path = os.path.relpath(absolute_source_path, commons_dir).replace("\\", "/")

            java_target_path = os.path.join(java_dist, rel_path)
            ensure_dir(os.path.dirname(java_target_path))
            shutil.copy2(absolute_source_path, java_target_path)
            java_copied += 1

            bedrock_rel_path = _resolve_bedrock_path(rel_path, mappings)
            if bedrock_rel_path:
                bedrock_target_path = os.path.join(bedrock_dist, bedrock_rel_path)
                ensure_dir(os.path.dirname(bedrock_target_path))
                shutil.copy2(absolute_source_path, bedrock_target_path)
                bedrock_copied += 1

    print(f"Mapped {java_copied} shared files to Java.")
    print(f"Mapped {bedrock_copied} shared files to Bedrock.")
    print("Mapper execution completed.\n")