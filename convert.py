import bpy
import sys
import os

# Enable the importer plugin
bpy.ops.preferences.addon_enable(module='SketchUp_Importer')

# Get input and output paths from the command line
argv = sys.argv
argv = argv[argv.index("--") + 1:]
input_path = argv[0]
output_path = argv[1]

# Clear default objects (cube, camera, light)
bpy.ops.wm.read_factory_settings(use_empty=True)

# Import the SketchUp file
try:
    bpy.ops.import_scene.skp(filepath=input_path)
    
    # Optional: Join all objects to simplify the GLB for Scanbrix
    bpy.ops.object.select_all(action='SELECT')
    
    # Export as GLB
    bpy.ops.export_scene.gltf(
        filepath=output_path, 
        export_format='GLB',
        export_apply=True
    )
    print("✅ Conversion Successful")
except Exception as e:
    print(f"❌ Blender Conversion Error: {str(e)}")
    sys.exit(1)
