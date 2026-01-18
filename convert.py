import bpy
import sys
import time

# Wait for Blender to register the folder
time.sleep(1)

# Enable the addon using the exact folder name from your screenshot
try:
    bpy.ops.preferences.addon_enable(module='sketchup_importer')
    print("✅ SketchUp Importer officially enabled!")
except Exception as e:
    print(f"❌ Enable failed: {e}")

# Arguments setup
argv = sys.argv
argv = argv[argv.index("--") + 1:]
input_path = argv[0]
output_path = argv[1]

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

try:
    print(f"🎬 Importing SKP: {input_path}")
    bpy.ops.import_scene.skp(filepath=input_path)
    
    print(f"📦 Exporting GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print("✅ Conversion Successful!")
except Exception as e:
    print(f"❌ Blender Error: {str(e)}")
    sys.exit(1)
