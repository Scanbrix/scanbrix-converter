import bpy
import sys
import time

# Force enable the specific RedHaloStudio plugin
addon_name = "Sketchup_Importer"
bpy.ops.preferences.addon_enable(module=addon_name)

# Allow 1 second for the plugin to register its operators
time.sleep(1)

argv = sys.argv
argv = argv[argv.index("--") + 1:]
input_path = argv[0]
output_path = argv[1]

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

try:
    print(f"🎬 Importing: {input_path}")
    # Explicitly call the SKP import operator
    bpy.ops.import_scene.skp(filepath=input_path)
    
    print(f"📦 Exporting: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print("✅ Done!")
except Exception as e:
    print(f"❌ Blender Error: {str(e)}")
    sys.exit(1)
