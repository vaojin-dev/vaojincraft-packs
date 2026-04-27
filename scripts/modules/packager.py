import os
import shutil

def run(config, paths):
    print("--- Running Packager ---")
    
    pack_version = config.get("pack_version", "1.0.0")
    
    dist_dir = os.path.dirname(paths["java_dist"]) 
    
    java_file_name = f"VaojinCraft-Java-{pack_version}"
    java_archive_base = os.path.join(dist_dir, java_file_name)
    
    print(f"Compressing Java pack...")
    shutil.make_archive(java_archive_base, 'zip', paths["java_dist"])
    print(f"Created: {java_file_name}.zip")

    bedrock_file_name = f"VaojinCraft-Bedrock-{pack_version}"
    bedrock_archive_base = os.path.join(dist_dir, bedrock_file_name)
    
    print(f"Compressing Bedrock pack...")
    shutil.make_archive(bedrock_archive_base, 'zip', paths["bedrock_dist"])
    
    zip_path = f"{bedrock_archive_base}.zip"
    mcpack_path = f"{bedrock_archive_base}.mcpack"
    
    if os.path.exists(mcpack_path):
        os.remove(mcpack_path)
        
    os.rename(zip_path, mcpack_path)
    print(f"Created: {bedrock_file_name}.mcpack")

    print("Packaging completed.\n")