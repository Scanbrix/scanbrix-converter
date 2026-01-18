import bpy
import sys
import os

# 1. SETUP PATHS
current_dir = os.path.dirname(os.path.abspath(__file__))
importer_dir = os.path.join(current_dir, "sketchup_importer")
slapi_dir = os.path.join(importer_dir, "slapi")

for d in [current_dir, importer_dir, slapi_dir]:
    if d not in sys.path:
        sys.path.insert(0, d)

print("--- BLENDER ENGINE STARTING ---")

# 2. CONVERSION EXECUTION
try:
    argv = sys.argv[sys.argv.index("--") + 1:]
    # FORCE ABSOLUTE PATHS
    input_path = os.path.abspath(argv[0])
    output_path = os.path.abspath(argv[1])

    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 IMPORTING SKP: {input_path}")
    
    from sketchup_importer import SceneImporter
    importer = SceneImporter()
    
    settings = {
        'use_yup': True,
        'import_materials': True,
        'import_textures': True,
        'layers_as_collections': True,
        'reuse_material': True,
        'reuse_existing_groups': True,
        'max_instance': 1000,
        'import_hidden': False,
        'import_texts': False,
        'import_dimensions': False,
        'import_cameras': False,
        'set_instancing': True,
        'pages_as_scenes': False,
        'extract_color': True
    }
    
    importer.prefs = type('obj', (object,), settings)
    
    # Run the load
    importer.set_filename(input_path).load(bpy.context, **settings)
    
    # --- DEBUG: CHECK FOR DATA ---
    obj_count = len(bpy.data.objects)
    print(f"📊 Scene Scan: Found {obj_count} objects in Blender memory.")
    
    if obj_count == 0:
        print("❌ CRITICAL: The importer ran but produced NO 3D DATA.")
    else:
        print(f"📦 EXPORTING GLB: {output_path}")
        bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    
    print("🏁 PROCESS FINISHED")

except Exception as e:
    print(f"❌ FAILED: {str(e)}")
    sys.exit(1)
