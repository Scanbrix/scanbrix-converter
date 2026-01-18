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

# 2. THE DEEP BRAIN INJECTION
try:
    import slapi
    # If slapi is a folder, we try to grab the actual compiled module inside it
    if not hasattr(slapi, 'Model'):
        print("🔍 Deep scanning slapi for Model attribute...")
        try:
            from slapi import sketchup as skp_core
            sys.modules['sketchup'] = skp_core
            print("🧠 Success: Deep-mapped slapi.sketchup to sketchup.")
        except ImportError:
            sys.modules['sketchup'] = slapi
    else:
        sys.modules['sketchup'] = slapi
    
    print(f"✅ Brain Check: Model attribute found: {hasattr(sys.modules['sketchup'], 'Model')}")
except Exception as e:
    print(f"❌ BRAIN INJECTION FAILED: {e}")

# 3. CONVERSION EXECUTION
try:
    argv = sys.argv[sys.argv.index("--") + 1:]
    input_path = os.path.abspath(argv[0])
    output_path = os.path.abspath(argv[1])

    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 STARTING GEOMETRY READ: {input_path}")
    
    from sketchup_importer import SceneImporter
    importer = SceneImporter()
    
    settings = {
        'use_yup': True, 'import_materials': True, 'import_textures': True,
        'layers_as_collections': True, 'reuse_material': True, 'reuse_existing_groups': True,
        'max_instance': 1000, 'import_hidden': False, 'import_texts': False,
        'import_dimensions': False, 'import_cameras': False, 'set_instancing': True,
        'pages_as_scenes': False, 'extract_color': True
    }
    
    importer.prefs = type('obj', (object,), settings)
    importer.set_filename(input_path).load(bpy.context, **settings)
    
    obj_count = len(bpy.data.objects)
    print(f"📊 Scene Scan: Found {obj_count} objects in memory.")

    if obj_count == 0:
        print("❌ ERROR: Scene is still empty. Library link issue remains.")
        sys.exit(1)

    print(f"📦 EXPORTING GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print("🏁 CONVERSION FINISHED SUCCESSFULLY")

except Exception as e:
    print(f"❌ CONVERSION CRASHED: {str(e)}")
    sys.exit(1)
