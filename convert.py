import bpy
import sys
import os
import addon_utils

# 1. PATH INJECTION
current_dir = os.path.dirname(os.path.abspath(__file__))
importer_dir = os.path.join(current_dir, "sketchup_importer")
slapi_dir = os.path.join(importer_dir, "slapi")

# Add all folders to the system path
for d in [current_dir, importer_dir, slapi_dir]:
    if d not in sys.path:
        sys.path.insert(0, d)

print("--- BLENDER ENGINE STARTING ---")

# 2. VERIFY LIBRARIES
try:
    import numpy
    print(f"✅ Numpy verified: v{numpy.__version__}")
except:
    print("❌ Numpy load failed")

# 3. MANUALLY REGISTER THE ADDON CLASSES
# This bypasses the broken 'import' lines in the plugin's __init__.py
try:
    bpy.utils.refresh_script_paths()
    addon_utils.enable("sketchup_importer", default_set=True)
    print("✅ Addon 'sketchup_importer' enabled.")
except Exception as e:
    print(f"⚠️ Registration Info: {e}")

# 4. CONVERSION
try:
    argv = sys.argv[sys.argv.index("--") + 1:]
    input_path = argv[0]
    output_path = argv[1]

    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 IMPORTING: {input_path}")
    # Force search for the operator
    if hasattr(bpy.ops.import_scene, 'skp'):
        bpy.ops.import_scene.skp(filepath=input_path)
    else:
        # Final attempt: Manually call the importer class if the operator is hidden
        print("🔍 Operator hidden, attempting manual class call...")
        from sketchup_importer import SceneImporter
        # Bypassing the prefs check entirely
        importer = SceneImporter()
        importer.prefs = type('obj', (object,), {'use_yup': True, 'import_materials': True, 'import_textures': True, 'layers_as_collections': True})
        importer.set_filename(input_path).load(bpy.context)

    print(f"📦 EXPORTING: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    
    print("🏁 CONVERSION FINISHED SUCCESSFULLY")

except Exception as e:
    print(f"❌ FAILED: {str(e)}")
    sys.exit(1)
