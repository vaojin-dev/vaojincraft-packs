import os
import sys
import shutil

from core import config_loader
from modules import dependencies, mapper, lang_gen, glyph_gen, manifest, packager

def main():
    print("Starting VaojinCraft Pack Build Process...\n")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    paths = {
        "commons_dir": "../commons",
        "lang_source_dir": "../lang_source",
        "java_templates": "../java/templates",
        "java_exclusive": "../java/exclusive",
        "bedrock_templates": "../bedrock/templates",
        "bedrock_exclusive": "../bedrock/exclusive",
        "mappings_dir": "mappings",
        "java_dist": "../dist/java",
        "bedrock_dist": "../dist/bedrock"
    }

    config_path = "../config.json"
    try:
        config = config_loader.load(config_path)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    dist_dir = "../dist"
    print("Cleaning up old distribution folder...")
    shutil.rmtree(dist_dir, ignore_errors=True)
    os.makedirs(paths["java_dist"], exist_ok=True)
    os.makedirs(paths["bedrock_dist"], exist_ok=True)
    print("Cleanup completed.\n")

    try:
        dependencies.run(config, paths)

        mapper.run(config, paths)
        
        lang_gen.run(config, paths)
        
        glyph_gen.run(config, paths)
        
        manifest.run(config, paths)
        
        packager.run(config, paths)

        print("=========================================")
        print("Build completed successfully!")
        print("Packages are ready in the /dist directory.")
        print("=========================================")

    except Exception as e:
        print(f"\nCRITICAL ERROR: Build failed during pipeline execution.")
        print(f"Details: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()