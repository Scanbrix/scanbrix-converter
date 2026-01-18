import bpy
import sys
import os

# 1. PATH ALIGNMENT
current_dir = os.path.dirname(os.path.abspath(__file__))
importer_dir = os.path.join(current_dir, "sketchup_importer")
slapi_dir = os.path.join(importer_dir, "slapi")

for d in [current_dir, importer_dir, slapi_dir]:
    if d not in sys.path:
        sys.path.insert(0, d)

print("--- BLENDER ENGINE STARTING ---")

# 2. THE MANUAL BRAIN OVERRIDE
try:
    import slapi
    sys.modules['sketchup'] = slapi
    print("🧠 Manual Brain Override: slapi mapped to sketchup.")
except Exception as e:
    print(f"⚠️ Brain Override Note: {e}")

# 3. EXECUTE CONVERSION
try:
    argv = sys.argv[sys.argv.index("--") + 1:]
    input_path = argv[0]
    output_path = argv[1]

    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 STARTING MANUAL IMPORT: {input_path}")
    
    from sketchup_importer import SceneImporter
    
    importer = SceneImporter()
    
    # --- THE "KITCHEN SINK" SETTINGS ---
    # These match the internal keys of the SketchUp Importer addon
    settings = {
        'use_yup': True,
        'import_materials': True,
        'import_textures': True,
        'layers_as_collections': True,
        'reuse_material': True,
        'reuse_existing_groups': True,  # This was the missing key!
        'import_hidden': False,
        'import_texts': False,
        'import_dimensions': False,
        'import_cameras': False,
        'set_instancing': True
    }
    
    # Attach to the fake prefs object
    importer.prefs = type('obj', (object,), settings)
    
    # Pass the full dictionary to the load function
    importer.set_filename(input_path).load(bpy.context, **settings)
    print("✅ Geometry loaded successfully into Blender scene.")

    print(f"📦 EXPORTING GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    
    print("🏁 CONVERSION FINISHED SUCCESSFULLY")

except Exception as e:
    print(f"❌ MANUAL CONVERSION FAILED: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
