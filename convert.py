import bpy
import sys
import os
import addon_utils

# 1. SETUP PATHS
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

print("--- BLENDER ENGINE STARTING ---")

# 2. FORCE LOAD & PATCH PREFERENCES
addon_folder_name = "sketchup_importer"

try:
    bpy.utils.refresh_script_paths()
    addon_utils.enable(addon_folder_name, default_set=True)
    
    # --- THE SURGERY ---
    # The addon crashes because it wants context.preferences.addons['sketchup_importer']
    # If it's not there, we manually inject it.
    if addon_folder_name not in bpy.context.preferences.addons:
        print(f"🔧 Injecting missing preference key: {addon_folder_name}")
        # We use a built-in Blender operator to force-register the preference entry
        bpy.ops.preferences.addon_enable(module=addon_folder_name)
    
    # If it's STILL not there (headless quirk), we map it to whatever IS there
    if addon_folder_name not in bpy.context.preferences.addons:
        for key in bpy.context.preferences.addons.keys():
            if "sketchup" in key.lower():
                print(f"🔗 Mapping {addon_folder_name} to existing key: {key}")
                bpy.context.preferences.addons[addon_folder_name] = bpy.context.preferences.addons[key]
                break

    print("✅ Addon preference patch applied.")
except Exception as e:
    print(f"⚠️ Patch Info: {e}")

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

    # Clear scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 IMPORTING SKP: {input_path}")
    # We call the operator; it should now find the 'sketchup_importer' key it needs
    bpy.ops.import_scene.skp(filepath=input_path)

    print(f"📦 EXPORTING GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    
    print("🏁 CONVERSION FINISHED SUCCESSFULLY")

except Exception as e:
    print(f"❌ CONVERSION FAILED: {str(e)}")
    sys.exit(1)
