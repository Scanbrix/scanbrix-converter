import bpy
import sys
import os
import types
import importlib

# 1. SETUP PATHS
base_dir = "/app"
importer_dir = os.path.join(base_dir, "sketchup_importer")
slapi_dir = os.path.join(importer_dir, "slapi")
model_subdir = os.path.join(slapi_dir, "model")

for d in [base_dir, importer_dir, slapi_dir, model_subdir]:
    if d not in sys.path:
        sys.path.insert(0, d)

print("--- BLENDER ENGINE STARTING ---")

# 2. AUTO-DISCOVERY BRIDGE
try:
    actual_model_class = None
    
    # Scan the model folder for the actual file containing the Model class
    for file in os.listdir(model_subdir):
        if file.endswith(".py") and file != "__init__.py":
            module_name = f"slapi.model.{file[:-3]}"
            print(f"🔍 Checking module: {module_name}")
            try:
                temp_mod = importlib.import_module(module_name)
                if hasattr(temp_mod, 'Model'):
                    actual_model_class = temp_mod.Model
                    print(f"🎯 Found Model class in {file}")
                    break
            except Exception as e:
                print(f"   Skipping {file}: {e}")

    if actual_model_class:
        # Create the 'sketchup' module the importer expects
        skp_bridge = types.ModuleType("sketchup")
        skp_bridge.Model = actual_model_class
        sys.modules['sketchup'] = skp_bridge
        print("✅ Bridge Successful: sketchup.Model is mapped and ready.")
    else:
        # Final fallback: just try to import slapi directly
        import slapi
        sys.modules['sketchup'] = slapi
        print("⚠️ Warning: Auto-discovery failed. Falling back to direct slapi import.")

except Exception as e:
    print(f"❌ Bridge System Failed: {e}")

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
        print("❌ ERROR: Scene is empty. The Model class didn't load any geometry.")
        sys.exit(1)

except Exception as e:
    print(f"❌ CONVERSION CRASHED: {str(e)}")
    sys.exit(1)
