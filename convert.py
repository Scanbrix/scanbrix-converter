import bpy
import sys
import os
import addon_utils

# 1. PATH CONFIGURATION
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

print("--- BLENDER ENGINE STARTING ---")

# 2. SAFE ADDON REGISTRATION
try:
    # We refresh paths so Blender sees the slapi folder inside the importer
    bpy.utils.refresh_script_paths()
    
    # Enable via addon manager; this correctly handles the internal sub-module imports
    addon_utils.enable('sketchup_importer', default_set=True)
    print("✅ Addon engine successfully initialized.")
except Exception as e:
    print(f"⚠️ Registration Note: {e}")

# 3. FINAL OPERATOR VERIFICATION
# This confirms if the redirection to .slapi worked and created the command
available_ops = [op for op in dir(bpy.ops.import_scene) if not op.startswith("__")]
print(f"Verified Operators: {available_ops}")

if 'skp' not in available_ops:
    print("❌ CRITICAL: 'skp' command failed to register. Check slapi folder.")
    sys.exit(1)

# 4. CONVERSION EXECUTION
try:
    argv = sys.argv[sys.argv.index("--") + 1:]
    input_path = argv[0]
    output_path = argv[1]

    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 IMPORTING SKP: {input_path}")
    # Using the verified internal name
    bpy.ops.import_scene.skp(filepath=input_path)

    print(f"📦 EXPORTING GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    
    print("🏁 CONVERSION FINISHED SUCCESSFULLY")

except Exception as e:
    print(f"❌ CONVERSION FAILED: {str(e)}")
    sys.exit(1)
