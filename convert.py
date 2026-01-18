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

# 3. THE MONKEYPATCH (The Surgical Fix)
# We reach into the loaded module and override the preference-finding logic
try:
    import sketchup_importer
    
    # We define a "fake" preference object
    class FakePrefs:
        def __init__(self):
            # These match the default settings the plugin usually looks for
            self.use_yup = True
            self.import_materials = True
            self.import_textures = True
            self.layers_as_collections = True

    # We force the SceneImporter class to use our fake preferences instead of searching Blender's UI
    original_load = sketchup_importer.SceneImporter.load
    
    def patched_load(self, context, **keywords):
        print("🔧 Monkeypatch active: Using default preferences to bypass KeyError.")
        self.prefs = FakePrefs()
        return original_load(self, context, **keywords)

    # Apply the patch
    sketchup_importer.SceneImporter.load = patched_load
    print("🎯 Monkeypatch successfully applied to SceneImporter.")

except Exception as e:
    print(f"❌ Monkeypatch failed: {e}")

# 4. CONVERSION EXECUTION
try:
    argv = sys.argv[sys.argv.index("--") + 1:]
    input_path = argv[0]
    output_path = argv[1]

    # Reset Blender scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    print(f"🎬 IMPORTING SKP: {input_path}")
    # This now calls our 'patched_load' which skips the problematic line 172
    bpy.ops.import_scene.skp(filepath=input_path)

    print(f"📦 EXPORTING GLB: {output_path}")
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    
    print("🏁 CONVERSION FINISHED SUCCESSFULLY")

except Exception as e:
    print(f"❌ CONVERSION FAILED: {str(e)}")
    sys.exit(1)
