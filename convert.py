import bpy
import sys
import os
import addon_utils

print("--- BLENDER PATH DEBUG ---")
found_path = None

# 1. Ask Blender for its internal script paths and scan them
for path in bpy.utils.script_paths():
    print(f"Blender looks for scripts in: {path}")
    # Check for the __init__.py with double underscores
    potential_path = os.path.join(path, "addons", "sketchup_importer", "__init__.py")
    if os.path.exists(potential_path):
        print(f"🎯 FOUND PLUGIN AT: {potential_path}")
        found_path = potential_path

print("--------------------------")

# 2. Refresh paths and attempt to enable
bpy.utils.refresh_script_paths()

try:
    # default_set=True forces it to load even if it wasn't saved in preferences
    addon_utils.enable('sketchup_importer', default_set=True)
    print("🚀 Attempted to enable 'sketchup_importer'")
except Exception as e:
    print(f"❌ Enable Error: {e}")

# 3. The Final Operator Check
# This is the moment of truth - does 'skp' exist in the import list?
if not hasattr(bpy.ops.import_scene, 'skp'):
    print("❌ SKP Operator missing.")
    print("Available import operators:", [op for op in dir(bpy.ops.import_scene) if not op.startswith("__")])
    sys.exit(1)

print("✅ SUCCESS: Importer is active and operator found.")

# 4. Conversion Logic
try:
    # Ensure we have the -- separator in args
    if "--" not in sys.argv:
        print("❌ Error: Missing '--' separator in command line arguments.")
        sys.exit(1)

    argv = sys.argv[sys.argv.index("--") + 1:]
    input_file = argv[0]
    output_file = argv[1]

    # Clear scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 Importing SKP: {input_file}")
    bpy.ops.import_scene.skp(filepath=input_file)

    print(f"📦 Exporting GLB: {output_file}")
    bpy.ops.export_scene.gltf(filepath=output_file, export_format='GLB')
    
    print("🏁 CONVERSION COMPLETE")

except Exception as e:
    print(f"❌ Conversion failed: {str(e)}")
    sys.exit(1)
