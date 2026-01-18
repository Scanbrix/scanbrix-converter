import bpy
import sys
import time

# Give the system a split second to stabilize
time.sleep(1)

# 1. Enable the addon using the official Blender method
try:
    # This matches the folder name 'Sketchup_Importer' we created in the Dockerfile
    bpy.ops.preferences.addon_enable(module='Sketchup_Importer')
    print("✅ SketchUp Importer officially enabled!")
except Exception as e:
    print(f"❌ Enable failed: {e}")

# 2. Setup arguments
argv = sys.argv
if "--" not in argv:
    print("❌ Error: Use -- to separate Blender args from script args.")
    sys.exit(1)

argv = argv[argv.index("--") + 1:]
input_path = argv[0]
output_path = argv[1]

# 3. Clear scene for a fresh start
bpy.ops.wm.read_factory_settings(use_empty=True)

try:
    print(f"🎬 Importing SKP: {input_path}")
    # The actual conversion command
    bpy.ops.import_scene.skp(filepath=input_path)
    
    print(f"📦 Exporting GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print("✅ Conversion Successful!")
    
except Exception as e:
    print(f"❌ Blender Error during processing: {str(e)}")
    # Log available import operators if it fails
    print("Available import operators:", [op for op in dir(bpy.ops.import_scene) if not op.startswith("__")])
    sys.exit(1)
