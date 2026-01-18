import bpy
import sys
import os

# 1. Add our custom addons folder to the path so Python can see it
script_dir = "/app/addons"
if script_dir not in sys.path:
    sys.path.append(script_dir)

# 2. Load the importer module
try:
    import Sketchup_Importer
    print("✅ SketchUp Importer module loaded successfully!")
except Exception as e:
    print(f"❌ Failed to load addon module: {e}")
    sys.exit(1)

# Setup arguments
argv = sys.argv
argv = argv[argv.index("--") + 1:]
input_path = argv[0]
output_path = argv[1]

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

try:
    print(f"🎬 Importing SKP: {input_path}")
    
    # We use the operator directly. 
    # The plugin registers this into Blender's ops when imported.
    bpy.ops.import_scene.skp(filepath=input_path)
    
    print(f"📦 Exporting GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print("✅ Conversion Successful!")
    
except Exception as e:
    print(f"❌ Blender Error during conversion: {str(e)}")
    sys.exit(1)
