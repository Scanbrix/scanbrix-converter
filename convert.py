import bpy
import sys
import os
import addon_utils

# 1. SETUP PATHS
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

print("--- BLENDER ENGINE STARTING ---")

# 2. MATCH NAMES EXACTLY
# The folder is 'sketchup_importer', but bl_info name is 'SketchUp Importer'
folder_name = "sketchup_importer"
internal_name = "SketchUp Importer"

try:
    bpy.utils.refresh_script_paths()
    # Enable using the folder name (module name)
    addon_utils.enable(folder_name, default_set=True)
    
    # --- CRITICAL PATCH FOR INTERNAL NAME ---
    # We check both the folder name and the internal name in preferences
    registered_addons = bpy.context.preferences.addons.keys()
    print(f"Registered Addons in memory: {list(registered_addons)}")

    # If the internal name isn't found, we force it
    if internal_name not in registered_addons and folder_name not in registered_addons:
        print(f"🔧 Forcing registration for: {internal_name}")
        bpy.ops.preferences.addon_enable(module=folder_name)
    
    print("✅ Addon engine successfully initialized.")
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

    # Factory reset for a clean scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 IMPORTING SKP: {input_path}")
    # Force the call to the verified operator
    bpy.ops.import_scene.skp(filepath=input_path)

    print(f"📦 EXPORTING GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    
    print("🏁 CONVERSION FINISHED SUCCESSFULLY")

except Exception as e:
    print(f"❌ CONVERSION FAILED: {str(e)}")
    sys.exit(1)
