const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

app.post('/convert', async (req, res) => {
  const { fileName, bucketId } = req.body;
  const tempInput = path.join(__dirname, fileName);
  const tempOutput = tempInput.replace(/\.[^/.]+$/, "") + ".glb";

  try {
    // 1. Download from Supabase
    const { data: fileBlob, error: downloadError } = await supabase.storage
      .from(bucketId)
      .download(fileName);
    if (downloadError) throw downloadError;
    
    fs.writeFileSync(tempInput, Buffer.from(await fileBlob.arrayBuffer()));

    // 2. Trigger Headless Blender
    console.log(`⚙️  Blender starting conversion for ${fileName}...`);
    const cmd = `blender --background --python convert.py -- "${tempInput}" "${tempOutput}"`;
    
    exec(cmd, async (error, stdout, stderr) => {
      if (error) {
        console.error(`❌ Blender Error: ${stderr}`);
        return res.status(500).json({ success: false, error: stderr });
      }

      // 3. Upload converted GLB to Supabase
      const glbBuffer = fs.readFileSync(tempOutput);
      const glbName = path.basename(tempOutput);

      const { error: uploadError } = await supabase.storage
        .from('converted-files')
        .upload(glbName, glbBuffer, { upsert: true, contentType: 'model/gltf-binary' });

      // Cleanup temp files
      fs.unlinkSync(tempInput);
      fs.unlinkSync(tempOutput);

      if (uploadError) throw uploadError;
      console.log(`✅ Success! Created: ${glbName}`);
      res.json({ success: true, file: glbName });
    });

  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    res.status(500).json({ success: false, error: error.message });
  }
});
