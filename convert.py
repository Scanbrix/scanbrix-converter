import bpy
import sys
import os

# 1. Force Blender to recognize our custom addons folder
# 
script_dir = "/app/addons"
if script_dir not in sys.path:
    sys.path.append(script_dir)

# 2. Manually register the importer
try:
    import Sketchup_Importer
    Sketchup_Importer.register()
    print("✅ SketchUp Importer manually registered and loaded!")
except Exception as e:
    print(f"❌ Failed to manually load addon: {e}")
    sys.exit(1)

# Setup arguments
argv = sys.argv
argv = argv[argv.index("--") + 1:]
input_path = argv[0]
output_path = argv[1]

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

try:
    print(f"🎬 Importing: {input_path}")
    # Using the direct operator provided by the RedHalo plugin
    bpy.ops.import_scene.skp(filepath=input_path)
    
    print(f"📦 Exporting: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print("✅ Conversion Successful!")
except Exception as e:
    print(f"❌ Blender Error: {str(e)}")
    sys.exit(1)
