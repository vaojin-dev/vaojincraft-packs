import os
import re
import urllib.request
from core.file_utils import load_json, read_file, write_file, write_json

def fetch_languages(url, is_java=True):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            import json
            data = json.loads(response.read().decode('utf-8'))
            if is_java:
                return [
                    item['name'].replace('.json', '') 
                    for item in data 
                    if item['name'].endswith('.json') and not item['name'].startswith('_') and item['name'] != 'deprecated.json'
                ]
            return data
    except Exception as e:
        print(f"API Fetch Error: {e}")
        return ["en_us"] if is_java else ["en_US"]

def inject_placeholders(template_string, glossary, target_lang):
    pattern = re.compile(r"\{\{(global|localized)\.([^{}]+)\}\}")

    def replacer(match):
        scope = match.group(1)
        key = match.group(2)

        if scope == 'global':
            return glossary.get('global', {}).get(key, match.group(0))
        elif scope == 'localized':
            translations = glossary.get('localized', {}).get(key, {})
            dict_key = target_lang.lower()
            
            if dict_key in translations:
                return translations[dict_key]
            elif "en_us" in translations:
                return translations["en_us"]
        return match.group(0)

    return pattern.sub(replacer, template_string)

def run(config, paths):
    print("--- Running Language Generator ---")
    
    java_version = config.get("java", {}).get("assets_version", "1.21.11")
    bedrock_version = config.get("bedrock", {}).get("samples_version", "main")
    
    java_url = f"https://api.github.com/repos/InventivetalentDev/minecraft-assets/contents/assets/minecraft/lang?ref={java_version}"
    bedrock_url = f"https://raw.githubusercontent.com/Mojang/bedrock-samples/{bedrock_version}/resource_pack/texts/languages.json"

    java_targets = fetch_languages(java_url, is_java=True)
    bedrock_targets = fetch_languages(bedrock_url, is_java=False)
    
    lang_src_dir = os.path.join(paths["lang_source_dir"])
    glossary_path = os.path.join(lang_src_dir, "i18n.json")
    java_template_path = os.path.join(lang_src_dir, "java", "java.json")
    bedrock_template_path = os.path.join(lang_src_dir, "bedrock", "bedrock.lang")
    
    java_out_dir = os.path.join(paths["java_dist"], "assets", "minecraft", "lang")
    bedrock_out_dir = os.path.join(paths["bedrock_dist"], "texts")

    glossary = load_json(glossary_path)
    java_template = read_file(java_template_path)
    bedrock_template = read_file(bedrock_template_path)

    print(f"Generating {len(java_targets)} Java languages...")
    for lang in java_targets:
        java_final = inject_placeholders(java_template, glossary, lang)
        write_file(os.path.join(java_out_dir, f"{lang}.json"), java_final)

    print(f"Generating {len(bedrock_targets)} Bedrock languages...")
    for lang in bedrock_targets:
        bedrock_final = inject_placeholders(bedrock_template, glossary, lang)
        write_file(os.path.join(bedrock_out_dir, f"{lang}.lang"), bedrock_final)
            
    write_json(os.path.join(bedrock_out_dir, "languages.json"), bedrock_targets)
        
    print("Language generation completed.\n")