import bpy
import sys
import os
import addon_utils

# 1. Get the current directory (/app)
current_dir = os.path.dirname(os.path.abspath(__file__))
# 2. Add /app to the paths Blender looks for scripts
# This is the "Force" method
scripts_path = os.path.join(current_dir, "sketchup_importer")

if os.path.exists(scripts_path):
    print(f"📁 Local Plugin Folder Detected at: {scripts_path}")
    # We add the parent directory to sys.path so it's importable
    sys.path.append(current_dir)
else:
    print(f"❌ Plugin Folder NOT found at {scripts_path}")

# 3. Use the internal load function
try:
    # We import it as a standard module first to force registration
    import sketchup_importer
    sketchup_importer.register()
    print("🚀 Manual Registration Successful")
except Exception as e:
    print(f"⚠️ Manual Registration Error (usually ignorable): {e}")

# 4. Standard Enable
try:
    addon_utils.enable('sketchup_importer', default_set=True)
except Exception as e:
    print(f"Enable Error: {e}")

# 5. Final Check
if not hasattr(bpy.ops.import_scene, 'skp'):
    print("❌ Operator still missing.")
    sys.exit(1)

# ... Rest of the code ...
