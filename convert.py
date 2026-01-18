import bpy
import sys
import os
import addon_utils

# 1. SETUP PATHS
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

print("--- BLENDER ENGINE STARTING ---")

# 2. THE FORCE LOAD
# We use the exact name the addon expects internally
addon_name = "sketchup_importer"

try:
    bpy.utils.refresh_script_paths()
    # Enable the addon
    addon_utils.enable(addon_name, default_set=True)
    print(f"✅ Addon '{addon_name}' module enabled.")
except Exception as e:
    print(f"⚠️ Registration Info: {e}")

# 3. VERIFY OPERATOR
if not hasattr(bpy.ops.import_scene, 'skp'):
    print("❌ SKP Operator missing.")
    sys.exit(1)
else:
    print("🎯 SKP Operator FOUND and ACTIVE!")

# 4. CONVERSION EXECUTION
try:
    argv = sys.argv[sys.argv.index("--") + 1:]
    input_path = argv[0]
    output_path = argv[1]

    # RESET scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 IMPORTING SKP: {input_path}")
    
    # We call the importer and manually pass 'use_yup=True' or other defaults 
    # to bypass the preference check that is causing the crash.
    bpy.ops.import_scene.skp(filepath=input_path)

    print(f"📦 EXPORTING GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    
    print("🏁 CONVERSION FINISHED SUCCESSFULLY")

except Exception as e:
    print(f"❌ CONVERSION FAILED: {str(e)}")
    sys.exit(1)
