import bpy
import sys
import time
import addon_utils

def enable_sketchup_importer():
    # 1. Look through all available modules to find the SketchUp importer
    skp_addon_module = None
    for mod in addon_utils.modules():
        name = mod.bl_info.get("name", "")
        # Check for common names used by RedHaloStudio or other versions
        if "Sketchup" in name or "SketchUp" in name:
            skp_addon_module = mod.__name__
            break
    
    if skp_addon_module:
        print(f"🔍 Found SketchUp addon module: {skp_addon_module}")
        # Enable the found module
        addon_utils.enable(skp_addon_module, default_set=True)
        return True
    else:
        print("❌ Error: Could not find any SketchUp Importer addon installed.")
        return False

# Setup arguments
argv = sys.argv
if "--" not in argv:
    print("❌ Error: Use -- to separate Blender args from script args.")
    sys.exit(1)

argv = argv[argv.index("--") + 1:]
input_path = argv[0]
output_path = argv[1]

# Clear scene for a fresh start
bpy.ops.wm.read_factory_settings(use_empty=True)

# Try to enable the plugin
if enable_sketchup_importer():
    # Allow a moment for registration
    time.sleep(1)
    
    try:
        print(f"🎬 Importing: {input_path}")
        # Call the operator
        # Most versions use import_scene.skp, but we'll try-except for safety
        bpy.ops.import_scene.skp(filepath=input_path)
        
        print(f"📦 Exporting: {output_path}")
        bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
        print("✅ Conversion Successful!")
    except Exception as e:
        print(f"❌ Blender Error during processing: {str(e)}")
        sys.exit(1)
else:
    sys.exit(1)
