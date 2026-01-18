import bpy
import sys
import os
import types

# 1. SETUP ABSOLUTE PATHS
base_dir = "/app"
importer_dir = os.path.join(base_dir, "sketchup_importer")
slapi_dir = os.path.join(importer_dir, "slapi")
# This is where your nested __init__.py is located
model_subdir = os.path.join(slapi_dir, "model")

for d in [base_dir, importer_dir, slapi_dir, model_subdir]:
    if d not in sys.path:
        sys.path.insert(0, d)

print("--- BLENDER ENGINE STARTING ---")

# 2. THE NESTED MODEL BRIDGE
try:
    # We reach into the nested sub-package shown in your screenshot
    from slapi.model import Model as ActualModel
    
    # We create a virtual module named 'sketchup' to satisfy the importer
    skp_bridge = types.ModuleType("sketchup")
    skp_bridge.Model = ActualModel
    
    # Inject it into the system so all other files see it
    sys.modules['sketchup'] = skp_bridge
    
    print(f"✅ Bridge Successful: sketchup.Model is now mapped to slapi.model.Model")
except Exception as e:
    print(f"❌ Bridge Failed: {e}")

# 3. CONVERSION EXECUTION
try:
    argv = sys.argv[sys.argv.index("--") + 1:]
    input_path = os.path.abspath(argv[0])
    output_path = os.path.abspath(argv[1])

    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 STARTING IMPORT: {input_path}")
    
    # Import the importer class now that the bridge is built
    from sketchup_importer import SceneImporter
    importer = SceneImporter()
    
    # Standard Importer Settings
    settings = {
        'use_yup': True, 'import_materials': True, 'import_textures': True,
        'layers_as_collections': True, 'reuse_material': True, 'reuse_existing_groups': True,
        'max_instance': 1000, 'import_hidden': False, 'import_texts': False,
        'import_dimensions': False, 'import_cameras': False, 'set_instancing': True,
        'pages_as_scenes': False, 'extract_color': True
    }
    
    importer.prefs = type('obj', (object,), settings)
    
    # Load the 3D data
    importer.set_filename(input_path).load(bpy.context, **settings)
    
    obj_count = len(bpy.data.objects)
    print(f"📊 Scene Scan: Found {obj_count} objects in memory.")

    if obj_count == 0:
        print("❌ ERROR: Still no geometry. The Model class was found but failed to read the file.")
        sys.exit(1)

    print(f"📦 EXPORTING GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print("🏁 SUCCESS")

except Exception as e:
    print(f"❌ CONVERSION CRASHED: {str(e)}")
    sys.exit(1)
