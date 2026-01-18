import bpy
import sys
import os
import addon_utils

# 1. FORCE PATH INJECTION
# Tells Blender's Python to look in the current directory (/app) for the plugin
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 2. REFRESH & ENABLE
print("--- BLENDER PLUGIN LOAD ---")
bpy.utils.refresh_script_paths()

try:
    # This specifically looks for the folder named 'sketchup_importer'
    addon_utils.enable('sketchup_importer', default_set=True)
    print("✅ SUCCESS: sketchup_importer enabled.")
except Exception as e:
    print(f"❌ ERROR: Could not enable plugin: {e}")
    sys.exit(1)

# 3. VERIFY OPERATOR
if not hasattr(bpy.ops.import_scene, 'skp'):
    print("❌ CRITICAL: 'import_scene.skp' operator not found.")
    print("Available operators:", [op for op in dir(bpy.ops.import_scene) if not op.startswith("__")])
    sys.exit(1)

# 4. CONVERSION EXECUTION
try:
    # Get file paths from command line arguments
    # Expected: blender -b -P convert.py -- input.skp output.glb
    argv = sys.argv[sys.argv.index("--") + 1:]
    input_path = argv[0]
    output_path = argv[1]

    # Clear the default Blender scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 IMPORTING: {input_path}")
    bpy.ops.import_scene.skp(filepath=input_path)

    print(f"📦 EXPORTING: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    
    print("🏁 CONVERSION FINISHED SUCCESSFULLY")

except Exception as e:
    print(f"❌ CONVERSION FAILED: {str(e)}")
    sys.exit(1)
