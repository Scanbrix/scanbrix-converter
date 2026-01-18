import bpy
import sys
import os
import addon_utils

# 1. SETUP PATHS
current_dir = os.path.dirname(os.path.abspath(__file__))
# Ensure /app is in the system path
if current_dir not in sys.path:
    sys.path.append(current_dir)

print("--- BLENDER ENGINE STARTING ---")

# 2. FORCE REFRESH AND ENABLE
# We point Blender specifically to the folder name
try:
    bpy.utils.refresh_script_paths()
    # This avoids the 'import' loop by using Blender's internal manager
    addon_utils.enable('sketchup_importer', default_set=True)
    print("✅ SUCCESS: sketchup_importer enabled via addon_utils.")
except Exception as e:
    print(f"❌ ERROR: Enable failed: {e}")
    sys.exit(1)

# 3. VERIFY OPERATOR
if not hasattr(bpy.ops.import_scene, 'skp'):
    print("❌ CRITICAL: 'import_scene.skp' operator not found.")
    # Show us what it DID find so we can debug
    import_ops = [op for op in dir(bpy.ops.import_scene) if not op.startswith("__")]
    print(f"Available import operators: {import_ops}")
    sys.exit(1)

# 4. CONVERSION EXECUTION
try:
    argv = sys.argv[sys.argv.index("--") + 1:]
    input_path = argv[0]
    output_path = argv[1]

    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 IMPORTING SKP: {input_path}")
    bpy.ops.import_scene.skp(filepath=input_path)

    print(f"📦 EXPORTING GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    
    print("🏁 CONVERSION FINISHED SUCCESSFULLY")

except Exception as e:
    print(f"❌ CONVERSION FAILED: {str(e)}")
    sys.exit(1)
