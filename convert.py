import bpy
import sys
import os
import addon_utils

# 1. SETUP PATHS
current_dir = os.path.dirname(os.path.abspath(__file__))
importer_dir = os.path.join(current_dir, "sketchup_importer")
# Add all levels to path
for d in [current_dir, importer_dir, os.path.join(importer_dir, "slapi")]:
    if d not in sys.path:
        sys.path.append(d)

print("--- BLENDER ENGINE STARTING ---")

# 2. FORCE ENABLE
try:
    bpy.utils.refresh_script_paths()
    # Enable the addon
    addon_utils.enable('sketchup_importer', default_set=True)
    print("✅ Addon module enabled.")
except Exception as e:
    print(f"⚠️ Enable Warning: {e}")

# 3. MANUAL CLASS REGISTRATION (The "Brute Force")
# If the operator is missing, we manually call the register function from the file
if not hasattr(bpy.ops.import_scene, 'skp'):
    print("Empty operator detected. Attempting manual registration...")
    try:
        import sketchup_importer
        sketchup_importer.register()
        print("🚀 Manual registration command executed.")
    except Exception as e:
        print(f"❌ Manual registration failed: {e}")

# 4. VERIFY
ops = [op for op in dir(bpy.ops.import_scene) if not op.startswith("__")]
print(f"Available operators: {ops}")

if 'skp' not in ops:
    print("❌ CRITICAL: 'skp' command still not found.")
    sys.exit(1)

# 5. CONVERT
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
