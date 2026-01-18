import bpy
import sys
import os
import addon_utils

# 1. Manually check if the file exists where we put it
plugin_path = "/usr/share/blender/scripts/addons/sketchup_importer/__init__.py"
print(f"Checking for plugin at: {plugin_path}")
if os.path.exists(plugin_path):
    print("📁 Plugin file detected on disk!")
else:
    print("❌ Plugin file NOT found on disk. Check Docker COPY command.")

# 2. Refresh and Enable
bpy.utils.refresh_script_paths()
try:
    addon_utils.enable('sketchup_importer', default_set=True)
    print("Attempted to enable 'sketchup_importer'")
except Exception as e:
    print(f"Enable Error: {e}")

# 3. The Final Operator Check
if not hasattr(bpy.ops.import_scene, 'skp'):
    print("❌ SKP Operator missing. Available:", [op for op in dir(bpy.ops.import_scene) if not op.startswith("__")])
    sys.exit(1)

print("✅ SUCCESS: Importer is active.")

# --- Rest of conversion logic ---
argv = sys.argv[sys.argv.index("--") + 1:]
bpy.ops.import_scene.skp(filepath=argv[0])
bpy.ops.export_scene.gltf(filepath=argv[1], export_format='GLB')
