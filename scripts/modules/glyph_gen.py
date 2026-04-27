import os
from PIL import Image
from core.file_utils import load_json, ensure_dir

def run(config, paths):
    print("--- Running Bedrock Glyph Generator ---")
    
    json_path = os.path.join(paths["java_exclusive"], "assets", "minecraft", "font", "default.json")
    source_assets_dir = os.path.join(paths["commons_dir"], "assets")
    output_dir = os.path.join(paths["bedrock_dist"], "font")
    
    try:
        data = load_json(json_path)
    except FileNotFoundError:
        print(f"Warning: Java font config not found at {json_path}. Skipping glyph generation.")
        return

    glyph_sheets = {}

    for provider in data.get("providers", []):
        if provider.get("type") != "bitmap":
            continue

        raw_path = provider.get("file", "")
        if ":" in raw_path:
            namespace, rel_path = raw_path.split(":", 1)
            file_path = os.path.join(source_assets_dir, namespace, "textures", rel_path)
        else:
            file_path = os.path.join(source_assets_dir, "minecraft", "textures", raw_path)

        for char_string in provider.get("chars", []):
            for char in char_string:
                unicode_val = ord(char)
                hex_str = f"{unicode_val:04X}"
                
                prefix = hex_str[:2]
                position = int(hex_str[2:], 16)

                if prefix not in glyph_sheets:
                    glyph_sheets[prefix] = []

                glyph_sheets[prefix].append({
                    "path": file_path.replace("/", os.sep).replace("\\", os.sep),
                    "position": position,
                    "char_hex": hex_str
                })

    sheet_size = 2048
    grid_columns = 16
    cell_size = sheet_size // grid_columns

    ensure_dir(output_dir)

    for prefix, items in glyph_sheets.items():
        sheet_img = Image.new("RGBA", (sheet_size, sheet_size), (0, 0, 0, 0))

        for item in items:
            if not os.path.exists(item["path"]):
                print(f"Warning: Texture file missing -> {item['path']}")
                continue

            try:
                sprite = Image.open(item["path"]).convert("RGBA")
                row = item["position"] // grid_columns
                col = item["position"] % grid_columns
                
                if sprite.width > cell_size or sprite.height > cell_size:
                    sprite.thumbnail((cell_size, cell_size), Image.Resampling.LANCZOS)

                offset_x = (col * cell_size) + (cell_size - sprite.width) // 2
                offset_y = (row * cell_size) + (cell_size - sprite.height) // 2

                sheet_img.paste(sprite, (offset_x, offset_y), sprite)
            except Exception as e:
                print(f"Error processing {item['path']}: {e}")

        output_file = os.path.join(output_dir, f"glyph_{prefix}.png")
        sheet_img.save(output_file)
        print(f"Successfully generated: {output_file}")
        
    print("Glyph generation completed.\n")