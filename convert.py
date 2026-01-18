import bpy
import sys
import os
import addon_utils

# 1. SETUP PATHS
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

print("--- BLENDER ENGINE STARTING ---")

# 2. SYSTEM HEALTH CHECK
try:
    import numpy
    print(f"✅ Numpy verified: v{numpy.__version__}")
except ImportError:
    print("❌ CRITICAL: Numpy missing. GLTF export will fail.")

# 3. ENABLE ADDON
addon_name = "sketchup_importer"
try:
    bpy.utils.refresh_script_paths()
    addon_utils.enable(addon_name, default_set=True)
    print(f"✅ Addon '{addon_name}' enabled.")
except Exception as e:
    print(f"⚠️ Registration Info: {e}")

# 4. CONVERSION
try:
    argv = sys.argv[sys.argv.index("--") + 1:]
    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 IMPORTING: {argv[0]}")
    bpy.ops.import_scene.skp(filepath=argv[0])

    print(f"📦 EXPORTING: {argv[1]}")
    bpy.ops.export_scene.gltf(filepath=argv[1], export_format='GLB')
    
    print("🏁 CONVERSION FINISHED SUCCESSFULLY")

except Exception as e:
    print(f"❌ FAILED: {str(e)}")
    sys.exit(1)
