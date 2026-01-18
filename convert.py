import bpy
import sys
import os
import time

# Give the system a second to stabilize
time.sleep(1)

# Enable the addon
try:
    bpy.ops.preferences.addon_enable(module='Sketchup_Importer')
    print("✅ SketchUp Importer officially enabled!")
except Exception as e:
    print(f"❌ Enable failed: {e}")

# Arguments
argv = sys.argv
argv = argv[argv.index("--") + 1:]
input_path = argv[0]
output_path = argv[1]

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

try:
    print(f"🎬 Importing SKP: {input_path}")
    # The plugin operator
    bpy.ops.import_scene.skp(filepath=input_path)
    
    print(f"📦 Exporting GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print("✅ Conversion Successful!")
    
except Exception as e:
    print(f"❌ Blender Error: {str(e)}")
    # Log available operators to see if 'skp' appeared
    print("Available import operators:", [op for op in dir(bpy.ops.import_scene) if not op.startswith("__")])
    sys.exit(1)
