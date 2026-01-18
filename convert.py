import bpy
import sys
import os
import time

# 1. Add the custom addons folder to the path
script_dir = "/app/addons"
if script_dir not in sys.path:
    sys.path.append(script_dir)

# 2. Force Register the plugin properly
try:
    import Sketchup_Importer
    # This is the secret sauce: explicitly calling the internal register
    Sketchup_Importer.register()
    print("✅ SketchUp Importer module loaded and operators registered!")
except Exception as e:
    print(f"❌ Registration Error: {e}")
    # If the above fails, try the alternative internal name some versions use
    try:
        import Sketchup_Importer.worker as worker
        worker.register()
        print("✅ SketchUp Importer (worker) registered!")
    except:
        pass

# Setup arguments
argv = sys.argv
argv = argv[argv.index("--") + 1:]
input_path = argv[0]
output_path = argv[1]

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# 3. Final Conversion attempt
try:
    # Give Blender a split second to catch up with the new registration
    time.sleep(0.5)
    
    print(f"🎬 Importing SKP: {input_path}")
    
    # We call the operator. If it fails, we'll see a specific error.
    bpy.ops.import_scene.skp(filepath=input_path)
    
    print(f"📦 Exporting GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print("✅ Conversion Successful!")
    
except Exception as e:
    print(f"❌ Blender Error: {str(e)}")
    # Debug: Print all available import operators to see what name it took
    print("Available operators starting with 'import':")
    for op in dir(bpy.ops.import_scene):
        print(f" - {op}")
    sys.exit(1)
