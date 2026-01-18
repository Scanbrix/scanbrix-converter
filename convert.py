import bpy
import sys
import os

# 1. MANUALLY INJECT THE FOLDER
# We point Python directly to the folder in your GitHub
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

print("--- BLENDER ENGINE STARTING ---")

try:
    # We manually "wake up" the importer folder
    import sketchup_importer
    sketchup_importer.register()
    print("✅ SUCCESS: sketchup_importer manually registered.")
except Exception as e:
    print(f"❌ ERROR: Manual registration failed: {e}")
    sys.exit(1)

# 2. VERIFY THE 'SKP' COMMAND IS READY
if not hasattr(bpy.ops.import_scene, 'skp'):
    print("❌ CRITICAL: The SketchUp importer command is still missing.")
    # This debug line will show us what Blender DID find if it fails
    print("Found commands:", [op for op in dir(bpy.ops.import_scene) if not op.startswith("__")])
    sys.exit(1)

# 3. EXECUTE CONVERSION
try:
    # Separate the system arguments from Blender arguments
    argv = sys.argv[sys.argv.index("--") + 1:]
    input_path = argv[0]
    output_path = argv[1]

    # Wipe the default Blender cube/light
    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 IMPORTING SKP: {input_path}")
    bpy.ops.import_scene.skp(filepath=input_path)

    print(f"📦 EXPORTING GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    
    print("🏁 CONVERSION FINISHED SUCCESSFULLY")

except Exception as e:
    print(f"❌ CONVERSION FAILED: {str(e)}")
    sys.exit(1)
