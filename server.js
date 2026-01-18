const express = require('express');
const { createClient } = require('@supabase/supabase-js');

const app = express();
// Enable JSON parsing to read the fileName and bucketId from Supabase
app.use(express.json());

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
    if (!fileName || !bucketId) {
      throw new Error('Missing fileName or bucketId in request body');
    }

    console.log(`\n${'='.repeat(60)}`);
    console.log(`📂 Fetching ${fileName} from ${bucketId}...`);
    
    // 1. Download the raw file from Supabase Storage
    const { data: fileBlob, error: downloadError } = await supabase.storage
      .from(bucketId)
      .download(fileName);

    if (downloadError) throw new Error(`Download failed: ${downloadError.message}`);
    const fileBuffer = new Uint8Array(await fileBlob.arrayBuffer());

    if (!assimpReady) throw new Error('Assimp.js not initialized');

    // 2. Perform Native 3D Conversion
    const fileList = new assimpReady.FileList();
    fileList.AddFile(fileName, fileBuffer);
    
    const result = assimpReady.ConvertFileList(fileList, 'glb2');
    
    if (!result.IsSuccess()) {
      if (fileList.delete) fileList.delete();
      if (result.delete) result.delete();
      throw new Error('Conversion failed - unsupported or corrupt file');
    }
    
    // 3. Upload the resulting GLB back to Supabase
    const glbFile = result.FileList().GetFile(0);
    const glbBuffer = Buffer.from(glbFile.GetContent());
    const glbFileName = fileName.replace(/\.[^/.]+$/, "") + ".glb";

    console.log(`☁️   Uploading finished GLB: ${glbFileName}`);
    const { data, error: uploadError } = await supabase.storage
      .from('converted-files')
      .upload(glbFileName, glbBuffer, { upsert: true });

    if (uploadError) throw uploadError;

    // Cleanup memory
    fileList.delete();
    result.delete();
    
    const totalTime = ((Date.now() - startTime) / 1000).toFixed(2);
    console.log(`✅  Complete! Total Time: ${totalTime}s`);
    
    res.json({ success: true, path: data.path, totalTime: parseFloat(totalTime) });
    
  } catch (error) {
    console.error(`❌  Error: ${error.message}`);
    res.status(500).json({ success: false, error: error.message });
  }
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', assimpReady: assimpReady !== null });
});

const PORT = process.env.PORT || 10000;

initializeAssimp().then(() => {
  app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀  Scanbrix Conversion Service ONLINE on Port ${PORT}`);
  });
});
