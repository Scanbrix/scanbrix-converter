const express = require('express');
const { createClient } = require('@supabase/supabase-js');

const app = express();
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
    console.log(`\n${'='.repeat(60)}`);
    console.log(`📂 Fetching ${fileName} from ${bucketId}...`);
    
    // 1. Download raw file bytes
    const { data: fileBlob, error: downloadError } = await supabase.storage
      .from(bucketId)
      .download(fileName);

    if (downloadError) throw new Error(`Download failed: ${downloadError.message}`);
    const fileBuffer = new Uint8Array(await fileBlob.arrayBuffer());
    console.log(`📦 File downloaded. Size: ${fileBuffer.length} bytes`);

    // 2. Run Native Conversion with Hinting
    const fileList = new assimpReady.FileList();
    
    // OPTION 2: Hint the parser by ensuring the extension is explicitly .skp
    const hintName = fileName.toLowerCase().endsWith('.skp') ? fileName : `${fileName}.skp`;
    fileList.AddFile(hintName, fileBuffer);
    
    console.log(`⚙️  Starting Assimp conversion (Target: GLB)...`);
    const result = assimpReady.ConvertFileList(fileList, 'glb');
    
    if (!result.IsSuccess()) {
      // Capture the actual engine error if available
      const engineError = result.GetErrors ? result.GetErrors() : 'No detailed engine error provided';
      console.error(`❌ Engine Failure: ${engineError}`);
      
      fileList.delete();
      result.delete();
      throw new Error(`Assimp conversion failed: ${engineError}`);
    }

    // 3. Upload GLB back to Supabase
    const glbFile = result.FileList().GetFile(0);
    const glbBuffer = Buffer.from(glbFile.GetContent());
    const glbFileName = fileName.replace(/\.[^/.]+$/, "") + ".glb";

    console.log(`☁️  Uploading converted file: ${glbFileName}`);
    const { data, error: uploadError } = await supabase.storage
      .from('converted-files')
      .upload(glbFileName, glbBuffer, { 
        upsert: true,
        contentType: 'model/gltf-binary'
      });

    if (uploadError) throw uploadError;

    // Memory Cleanup
    fileList.delete();
    result.delete();
    
    const duration = ((Date.now() - startTime) / 1000).toFixed(2);
    console.log(`✅ Success! Created: ${glbFileName} in ${duration}s`);
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
