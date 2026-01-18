import bpy
import sys
import os
import types
import importlib

# 1. SETUP PATHS
current_dir = os.path.dirname(os.path.abspath(__file__))
importer_dir = os.path.join(current_dir, "sketchup_importer")
slapi_dir = os.path.join(importer_dir, "slapi")
model_subdir = os.path.join(slapi_dir, "model")

for d in [current_dir, importer_dir, slapi_dir, model_subdir]:
    if d not in sys.path:
        sys.path.insert(0, d)

print("--- BLENDER ENGINE STARTING ---")

# 2. SURGICAL MODEL DISCOVERY
# We will manually search the model directory for the class definition
def get_actual_model():
    print(f"🔍 Scanning {model_subdir} for Model class...")
    for filename in os.listdir(model_subdir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            try:
                # We import the file directly
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(model_subdir, filename))
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, 'Model'):
                    print(f"🎯 Found 'Model' class in: {filename}")
                    return mod.Model
            except Exception as e:
                print(f"   Could not read {filename}: {e}")
    return None

ActualModelClass = get_actual_model()

if ActualModelClass:
    # Build the 'sketchup' module the importer expects
    skp_bridge = types.ModuleType("sketchup")
    skp_bridge.Model = ActualModelClass
    sys.modules['sketchup'] = skp_bridge
    print("✅ Brain Injected: sketchup.Model is mapped.")
else:
    print("❌ CRITICAL: 'Model' class not found in any .py file in slapi/model/")

# 3. CONVERSION EXECUTION
try:
    argv = sys.argv[sys.argv.index("--") + 1:]
    input_path = os.path.abspath(argv[0])
    output_path = os.path.abspath(argv[1])

    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 STARTING IMPORT: {input_path}")
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

    if obj_count > 0:
        print(f"📦 EXPORTING GLB: {output_path}")
        bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
        print("🏁 SUCCESS")
    else:
        print("❌ ERROR: Scene is empty. The Model class exists but didn't create geometry.")
        sys.exit(1)

except Exception as e:
    print(f"❌ CONVERSION CRASHED: {str(e)}")
    sys.exit(1)
