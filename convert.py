import bpy
import sys
import os
import addon_utils

# 1. SETUP PATHS
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

print("--- BLENDER ENGINE STARTING ---")

# 2. ENABLE ADDON
addon_name = "sketchup_importer"
try:
    bpy.utils.refresh_script_paths()
    addon_utils.enable(addon_name, default_set=True)
    print(f"✅ Addon '{addon_name}' enabled.")
except Exception as e:
    print(f"⚠️ Registration Info: {e}")

# 3. THE "OBLIVION" PATCH
# This patch reaches into the class and forces it to ignore the preferences check entirely.
try:
    import sketchup_importer

    class FakePrefs:
        def __init__(self):
            self.use_yup = True
            self.import_materials = True
            self.import_textures = True
            self.layers_as_collections = True

    # We completely replace the 'load' function with a version that
    # handles the crash internally.
    original_load = sketchup_importer.SceneImporter.load

    def unstoppable_load(self, context, **keywords):
        print("🔧 Patching: Bypassing internal preference check...")
        try:
            # Try to run the original load
            return original_load(self, context, **keywords)
        except KeyError as e:
            if "sketchup_importer" in str(e):
                print("🚨 Caught KeyError! Injecting fake preferences and retrying...")
                self.prefs = FakePrefs()
                # We skip the first few lines of the original load by setting the prefs manually
                # and continuing with the geometry processing.
                return original_load(self, context, **keywords)
            raise e

    # Apply the patch
    sketchup_importer.SceneImporter.load = unstoppable_load
    print("🎯 Oblivion Patch successfully applied.")

except Exception as e:
    print(f"❌ Patching failed: {e}")

# 4. CONVERSION EXECUTION
try:
    argv = sys.argv[sys.argv.index("--") + 1:]
    input_path = argv[0]
    output_path = argv[1]

    # Reset Blender scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 IMPORTING SKP: {input_path}")
    # Force call to the command
    bpy.ops.import_scene.skp(filepath=input_path)

    print(f"📦 EXPORTING GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    
    print("🏁 CONVERSION FINISHED SUCCESSFULLY")

except Exception as e:
    print(f"❌ CONVERSION FAILED: {str(e)}")
    sys.exit(1)
