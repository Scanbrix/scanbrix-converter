import bpy
import sys
import os

# 1. PATH ALIGNMENT
current_dir = os.path.dirname(os.path.abspath(__file__))
importer_dir = os.path.join(current_dir, "sketchup_importer")
slapi_dir = os.path.join(importer_dir, "slapi")

# Add folders to path
for d in [current_dir, importer_dir, slapi_dir]:
    if d not in sys.path:
        sys.path.insert(0, d)

print("--- BLENDER ENGINE STARTING ---")

# 2. THE MANUAL BRAIN OVERRIDE
try:
    # We try to import the slapi folder as the module 'sketchup'
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
    
    # Import the Importer class directly from the file
    from sketchup_importer import SceneImporter
    
    # Create the importer and bypass the UI preference check
    importer = SceneImporter()
    importer.prefs = type('obj', (object,), {
        'use_yup': True, 
        'import_materials': True, 
        'import_textures': True, 
        'layers_as_collections': True
    })
    
    # Load the geometry
    importer.set_filename(input_path).load(bpy.context)
    print("✅ Geometry loaded successfully.")

    print(f"📦 EXPORTING GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    
    print("🏁 CONVERSION FINISHED SUCCESSFULLY")

except Exception as e:
    print(f"❌ MANUAL CONVERSION FAILED: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
