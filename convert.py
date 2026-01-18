import bpy
import sys
import os

# 1. MANUALLY IMPORT THE FOLDER AS A MODULE
current_dir = os.path.dirname(os.path.abspath(__file__))
plugin_path = os.path.join(current_dir, "sketchup_importer")

if current_dir not in sys.path:
    sys.path.append(current_dir)

print(f"--- BLENDER PLUGIN LOAD ---")
print(f"Checking local path: {plugin_path}")

try:
    # We manually import the Python package and run its internal register function
    import sketchup_importer
    sketchup_importer.register()
    print("✅ SUCCESS: sketchup_importer manually registered.")
except Exception as e:
    print(f"❌ ERROR: Manual registration failed: {e}")
    sys.exit(1)

# 2. VERIFY OPERATOR
# Sometimes the operator takes a split second to register
if not hasattr(bpy.ops.import_scene, 'skp'):
    print("❌ CRITICAL: 'import_scene.skp' operator not found.")
    print("Available operators:", [op for op in dir(bpy.ops.import_scene) if not op.startswith("__")])
    sys.exit(1)

# 3. CONVERSION EXECUTION
try:
    argv = sys.argv[sys.argv.index("--") + 1:]
    input_path = argv[0]
    output_path = argv[1]

    # Clear scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 IMPORTING SKP: {input_path}")
    # Force the use of the operator we just registered
    bpy.ops.import_scene.skp(filepath=input_path)

    print(f"📦 EXPORTING GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    
    print("🏁 CONVERSION FINISHED SUCCESSFULLY")

except Exception as e:
    print(f"❌ CONVERSION FAILED: {str(e)}")
    sys.exit(1)
