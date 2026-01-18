import bpy
import sys
import time

# 1. Clean up and try to enable the addon the official way
try:
    # This matches the folder name we created in the Dockerfile
    bpy.ops.preferences.addon_enable(module='Sketchup_Importer')
    print("✅ SketchUp Importer officially enabled!")
except Exception as e:
    print(f"❌ Standard enable failed: {e}")

# Setup arguments
argv = sys.argv
argv = argv[argv.index("--") + 1:]
input_path = argv[0]
output_path = argv[1]

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

try:
    time.sleep(1) # Wait for registration
    print(f"🎬 Importing SKP: {input_path}")
    
    # Try the operator
    bpy.ops.import_scene.skp(filepath=input_path)
    
    print(f"📦 Exporting GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print("✅ Conversion Successful!")
    
except Exception as e:
    print(f"❌ Final Blender Error: {str(e)}")
    # Last ditch debug: print all available operators again
    print("Available operators:")
    print([op for op in dir(bpy.ops.import_scene) if not op.startswith("__")])
    sys.exit(1)
