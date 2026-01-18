import bpy
import sys
import time

# Give the system a moment
time.sleep(1)

# Try to enable
print("Attempting to enable sketchup_importer...")
bpy.ops.preferences.addon_enable(module='sketchup_importer')

# VERIFY if it actually loaded the operators
if not hasattr(bpy.ops.import_scene, 'skp'):
    print("❌ CRITICAL: sketchup_importer operators NOT found in bpy.ops.import_scene")
    # List what IS there for debugging
    print("Available operators:", [op for op in dir(bpy.ops.import_scene) if not op.startswith("__")])
    sys.exit(1)
else:
    print("✅ sketchup_importer operators verified and ready!")

# Arguments
argv = sys.argv
argv = argv[argv.index("--") + 1:]
input_path = argv[0]
output_path = argv[1]

bpy.ops.wm.read_factory_settings(use_empty=True)

try:
    print(f"🎬 Importing: {input_path}")
    bpy.ops.import_scene.skp(filepath=input_path)
    
    print(f"📦 Exporting: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print("✅ Conversion Successful!")
except Exception as e:
    print(f"❌ Blender Error: {str(e)}")
    sys.exit(1)
