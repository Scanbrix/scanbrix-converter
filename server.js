const express = require('express');
const { createClient } = require('@supabase/supabase-js');

const app = express();
app.use(express.json()); // Essential to read the Supabase JSON trigger

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

let assimpReady = null;

async function initializeAssimp() {
  console.log('🚀 Initializing Assimp.js...');
  try {
    const assimpFactory = require('assimpjs');
    assimpReady = await assimpFactory(); 
    console.log('✅ Assimp.js initialized successfully');
  } catch (error) {
    console.error('❌ Failed to initialize Assimp.js:', error);
    throw error;
  }
}

app.post('/convert', async (req, res) => {
  const { fileName, bucketId } = req.body;
  const startTime = Date.now();
  
  try {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`📂 Fetching ${fileName} from ${bucketId}...`);
    
    // 1. Download raw file bytes
    const { data: fileBlob, error: downloadError } = await supabase.storage
      .from(bucketId)
      .download(fileName);

    if (downloadError) throw new Error(`Download failed: ${downloadError.message}`);
    const fileBuffer = new Uint8Array(await fileBlob.arrayBuffer());

    // 2. Run Native Conversion
    const fileList = new assimpReady.FileList();
    fileList.AddFile('input.skp', fileBuffer);
    const result = assimpReady.ConvertFileList(fileList, 'glb');
    
    if (!result.IsSuccess()) {
      fileList.delete();
      result.delete();
      throw new Error('Assimp conversion failed');
    }

    // 3. Upload GLB back to Supabase
    const glbFile = result.FileList().GetFile(0);
    const glbBuffer = Buffer.from(glbFile.GetContent());
    const glbFileName = fileName.replace(/\.[^/.]+$/, "") + ".glb";

    const { data, error: uploadError } = await supabase.storage
      .from('converted-files')
      .upload(glbFileName, glbBuffer, { upsert: true });

    if (uploadError) throw uploadError;

    fileList.delete();
    result.delete();
    
    console.log(`✅ Success! Created: ${glbFileName}`);
    res.json({ success: true, path: data.path });
    
  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    res.status(500).json({ success: false, error: error.message });
  }
});

const PORT = process.env.PORT || 10000;
initializeAssimp().then(() => {
  app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 Scanbrix Converter-1 ONLINE on Port ${PORT}`);
  });
});
