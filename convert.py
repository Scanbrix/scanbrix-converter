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
# We use a try/except that ignores the circular import but still registers the ops
try:
    bpy.utils.refresh_script_paths()
    # Force unregister first to clear the "partial initialization"
    try:
        addon_utils.disable('sketchup_importer')
    except:
        pass
        
    addon_utils.enable('sketchup_importer', default_set=True)
    print("✅ Addon manager enabled the module.")
except Exception as e:
    print(f"⚠️ Registration Info: {e}")

# 3. VERIFY AND LIST ALL 'IMPORT_SCENE' OPERATORS
# This is crucial. If 'skp' isn't there, we'll see what IS there.
ops = [op for op in dir(bpy.ops.import_scene) if not op.startswith("__")]
print(f"Verified Operators in import_scene: {ops}")

if 'skp' not in ops:
    print("❌ SKP Operator is MISSING from the internal list.")
    sys.exit(1)
else:
    print("🎯 SKP Operator FOUND and ACTIVE!")

# 4. CONVERSION EXECUTION
try:
    argv = sys.argv[sys.argv.index("--") + 1:]
    input_path = argv[0]
    output_path = argv[1]

    # Reset Blender to factory settings (empty scene)
    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 IMPORTING SKP: {input_path}")
    # Force Blender to call the operator directly
    getattr(bpy.ops.import_scene, 'skp')(filepath=input_path)

    print(f"📦 EXPORTING GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    
    print("🏁 CONVERSION FINISHED SUCCESSFULLY")

except Exception as e:
    print(f"❌ CONVERSION FAILED: {str(e)}")
    sys.exit(1)
