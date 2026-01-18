import bpy
import sys
import os

# 1. ABSOLUTE PATH INJECTION
# We tell Python: "Your libraries are in these specific folders. No excuses."
base_dir = "/app"
importer_dir = os.path.join(base_dir, "sketchup_importer")
slapi_dir = os.path.join(importer_dir, "slapi")

for d in [base_dir, importer_dir, slapi_dir]:
    if d not in sys.path:
        sys.path.insert(0, d)

print("--- BLENDER ENGINE STARTING ---")

# 2. FORCE-MAP THE BRAIN
# We manually map the folder to the name 'sketchup' so the code doesn't crash
try:
    import slapi
    sys.modules['sketchup'] = slapi
    print("🧠 BRAIN INJECTED: slapi is now mapped to sketchup.")
except Exception as e:
    print(f"❌ BRAIN INJECTION FAILED: {e}")

# 3. CONVERSION EXECUTION
try:
    argv = sys.argv[sys.argv.index("--") + 1:]
    input_path = os.path.abspath(argv[0])
    output_path = os.path.abspath(argv[1])

    # Clean Slate
    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 STARTING GEOMETRY READ: {input_path}")
    
    # We reach into the file and grab the Importer class directly
    from sketchup_importer import SceneImporter
    
    importer = SceneImporter()
    
    # We provide the "Kitchen Sink" settings to satisfy all internal checks
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
    
    # Inject settings into the importer object
    importer.prefs = type('obj', (object,), settings)
    
    # THE BIG MOMENT: Load the actual 3D data
    importer.set_filename(input_path).load(bpy.context, **settings)
    
    # Verify we actually have data now
    obj_count = len(bpy.data.objects)
    print(f"📊 Scene Scan: Found {obj_count} objects in memory.")

    if obj_count == 0:
        print("❌ ERROR: Importer finished but scene is still empty.")
        sys.exit(1)

    print(f"📦 EXPORTING GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    
    print("🏁 CONVERSION FINISHED SUCCESSFULLY")

except Exception as e:
    print(f"❌ CONVERSION CRASHED: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
