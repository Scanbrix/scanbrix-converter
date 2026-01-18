import bpy
import sys
import os
import addon_utils

# 1. SETUP PATHS
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

print("--- BLENDER ENGINE STARTING ---")

# 2. FORCE MANUAL IMPORT AND REGISTRATION
try:
    # We import the actual code directly
    import sketchup_importer
    
    # We force the register function to run
    sketchup_importer.register()
    print("✅ SUCCESS: sketchup_importer manually registered.")
    
    # We also trigger the addon_utils enable just to be safe
    addon_utils.enable('sketchup_importer', default_set=True)
    
except Exception as e:
    print(f"⚠️ Registration Info: {e}")

# 3. CRITICAL: LIST ALL OPERATORS (Debug list)
# This will show us exactly what the importer added to Blender
print("Checking for SKP operator...")
if not hasattr(bpy.ops.import_scene, 'skp'):
    print("❌ SKP Operator still not found in 'import_scene'.")
    # Let's check if it registered under a different name
    all_ops = dir(bpy.ops.import_scene)
    print(f"Available import operators: {[op for op in all_ops if not op.startswith('__')]}")
    sys.exit(1)

print("🎯 SKP Operator Verified!")

# 4. CONVERSION EXECUTION
try:
    argv = sys.argv[sys.argv.index("--") + 1:]
    input_path = argv[0]
    output_path = argv[1]

    # Factory reset to ensure clean scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 IMPORTING SKP: {input_path}")
    bpy.ops.import_scene.skp(filepath=input_path)

    print(f"📦 EXPORTING GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    
    print("🏁 CONVERSION FINISHED SUCCESSFULLY")

except Exception as e:
    print(f"❌ CONVERSION FAILED: {str(e)}")
    sys.exit(1)
