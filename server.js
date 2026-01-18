const express = require('express');
const { createClient } = require('@supabase/supabase-js');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

// 1. Initialize Express
const app = express();
app.use(express.json());

// 2. Initialize Supabase Client
const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// 3. Your Conversion Route
app.post('/convert', async (req, res) => {
  const { fileName, bucketId } = req.body;
  
  // FIX: Sanitize filename by replacing spaces/special chars with underscores
  const safeFileName = fileName.replace(/[^a-z0-9.]/gi, '_');
  const tempInput = path.join(__dirname, safeFileName);
  const tempOutput = tempInput.replace(/\.[^/.]+$/, "") + ".glb";

  try {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`📂 Fetching ${fileName} from ${bucketId}...`);

    // Download from Supabase
    const { data: fileBlob, error: downloadError } = await supabase.storage
      .from(bucketId)
      .download(fileName);
    
    if (downloadError) throw downloadError;
    fs.writeFileSync(tempInput, Buffer.from(await fileBlob.arrayBuffer()));

    // Trigger Headless Blender
    console.log(`⚙️  Blender starting conversion for ${safeFileName}...`);
    // Added double quotes around paths to handle any remaining edge cases
    const cmd = `blender --background --python convert.py -- "${tempInput}" "${tempOutput}"`;
    
    exec(cmd, async (error, stdout, stderr) => {
      // Log Blender's internal output for debugging
      console.log('Blender Output:', stdout);

      if (error) {
        console.error(`❌ Blender Process Error: ${stderr || stdout}`);
        return res.status(500).json({ success: false, error: stderr || stdout });
      }

      // Check if the GLB file actually exists before trying to read it
      if (!fs.existsSync(tempOutput)) {
        console.error(`❌ Conversion failed: ${tempOutput} not found.`);
        return res.status(500).json({ success: false, error: "Blender exited but GLB was not created." });
      }

      // Upload converted GLB to Supabase
      console.log(`⬆️  Uploading ${path.basename(tempOutput)} to Supabase...`);
      const glbBuffer = fs.readFileSync(tempOutput);
      const glbName = path.basename(tempOutput);

      const { error: uploadError } = await supabase.storage
        .from('converted-files')
        .upload(glbName, glbBuffer, { upsert: true, contentType: 'model/gltf-binary' });

      // Cleanup
      if (fs.existsSync(tempInput)) fs.unlinkSync(tempInput);
      if (fs.existsSync(tempOutput)) fs.unlinkSync(tempOutput);

      if (uploadError) throw uploadError;
      console.log(`✅ Success! Created: ${glbName}`);
      res.json({ success: true, file: glbName });
    });

  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    res.status(500).json({ success: false, error: error.message });
  }
});

// 4. Start the Server
const PORT = process.env.PORT || 10000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Scanbrix Blender-Engine ONLINE on Port ${PORT}`);
});
