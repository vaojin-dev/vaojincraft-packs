import os
from core.file_utils import load_json, write_json

def run(config, paths):
    print("--- Running Manifest & Meta Injector ---")
    
    pack_version = config.get("pack_version", "1.0.0")
    pack_version_array = [int(v) for v in pack_version.split('.')]
    
    # bedrock manifest
    bedrock_template_path = os.path.join(paths["bedrock_templates"], "manifest.json")
    if os.path.exists(bedrock_template_path):
        manifest = load_json(bedrock_template_path)
        bedrock_config = config.get("bedrock", {})
        
        manifest["header"]["version"] = pack_version_array
        if "min_engine_version" in bedrock_config:
            manifest["header"]["min_engine_version"] = bedrock_config["min_engine_version"]
        if "header_uuid" in bedrock_config:
            manifest["header"]["uuid"] = bedrock_config["header_uuid"]
            
        for module in manifest.get("modules", []):
            module["version"] = pack_version_array
            if module.get("type") == "resources" and "module_uuid" in bedrock_config:
                module["uuid"] = bedrock_config["module_uuid"]
                
        output_path = os.path.join(paths["bedrock_dist"], "manifest.json")
        write_json(output_path, manifest)
        print(f"Injected Bedrock configuration into manifest.json")
    else:
        print(f"Warning: Bedrock manifest template not found at {bedrock_template_path}")

    # java mcmeta
    java_template_path = os.path.join(paths["java_templates"], "pack.mcmeta")
    if os.path.exists(java_template_path):
        mcmeta = load_json(java_template_path)
        java_config = config.get("java", {})
        
        if "min_format" in java_config:
            mcmeta["pack"]["min_format"] = java_config["min_format"]
        if "max_format" in java_config:
            mcmeta["pack"]["max_format"] = java_config["max_format"]
            
        output_path = os.path.join(paths["java_dist"], "pack.mcmeta")
        write_json(output_path, mcmeta)
        print(f"Injected Java configuration into pack.mcmeta")
    else:
        print(f"Warning: Java pack.mcmeta template not found at {java_template_path}")
        
    print("Manifest injection completed.\n")