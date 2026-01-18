const express = require('express');
const multer = require('multer');
const { createClient } = require('@supabase/supabase-js');

const app = express();
const upload = multer({ 
  storage: multer.memoryStorage(),
  limits: { fileSize: 20 * 1024 * 1024 }
});

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

let assimpReady = null;

async function initializeAssimp() {
  console.log('🚀 Initializing Assimp.js...');
  try {
    const assimpFactory = require('assimpjs');
    // Version 0.0.10 initialization pattern
    assimpReady = await assimpFactory(); 
    
    console.log('✅ Assimp.js initialized successfully');
    
    if (typeof assimpReady.FileList !== 'function') {
      throw new Error('FileList is not available!');
    }
    console.log('✅ FileList and ConvertFileList verified');
    
  } catch (error) {
    console.error('❌ Failed to initialize Assimp.js:', error);
    throw error;
  }
}

app.post('/convert', upload.single('file'), async (req, res) => {
  const startTime = Date.now();
  
  try {
    if (!req.file) {
      return res.status(400).json({ success: false, error: 'No file uploaded' });
    }

    console.log(`\n${'='.repeat(60)}`);
    console.log(`📂 Converting ${req.file.originalname}`);
    console.log(`   File size: ${(req.file.size / 1024).toFixed(2)} KB`);
    
    if (!assimpReady) {
      throw new Error('Assimp.js not initialized');
    }

    console.log(`🏗️   Creating FileList...`);
    const fileList = new assimpReady.FileList();
    
    console.log(`📝  Adding file...`);
    fileList.AddFile(req.file.originalname, new Uint8Array(req.file.buffer));
    
    console.log(`⚙️   Converting to GLB...`);
    const conversionStart = Date.now();
    const result = assimpReady.ConvertFileList(fileList, 'glb2');
    const conversionTime = ((Date.now() - conversionStart) / 1000).toFixed(2);
    
    console.log(`✨  Conversion completed in ${conversionTime}s`);
    
    if (!result.IsSuccess()) {
      if (fileList.delete) fileList.delete();
      if (result.delete) result.delete();
      throw new Error('Conversion failed');
    }
    
    const glbFile = result.FileList().GetFile(0);
    const glbBuffer = Buffer.from(glbFile.GetContent());
    const glbFileName = req.file.originalname.replace(/\.(skp|liar)$/i, '.glb');
    
    console.log(`☁️   Uploading to Supabase...`);
    const { data, error } = await supabase.storage
      .from('converted-files')
      .upload(glbFileName, glbBuffer, {
        contentType: 'model/gltf-binary',
        upsert: true
      });
    
    if (error) {
      if (fileList.delete) fileList.delete();
      if (result.delete) result.delete();
      throw error;
    }
    
    if (fileList.delete) fileList.delete();
    if (result.delete) result.delete();
    
    const totalTime = ((Date.now() - startTime) / 1000).toFixed(2);
    console.log(`✅  Complete! Total: ${totalTime}s`);
    console.log(`${'='.repeat(60)}\n`);
    
    res.json({ 
      success: true, 
      glbPath: data.path,
      conversionTime: parseFloat(conversionTime),
      totalTime: parseFloat(totalTime)
    });
    
  } catch (error) {
    console.error(`❌  Error: ${error.message}`);
    res.status(500).json({ success: false, error: error.message });
  }
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', assimpReady: assimpReady !== null });
});

const PORT = process.env.PORT || 10000;

initializeAssimp()
  .then(() => {
    app.listen(PORT, '0.0.0.0', () => {
      console.log(`\n${'='.repeat(60)}`);
      console.log(`🚀  Scanbrix Conversion Service ONLINE`);
      console.log(`   Port: ${PORT}`);
      console.log(`${'='.repeat(60)}\n`);
    });
  })
  .catch((error) => {
    console.error('❌  Failed to start:', error);
    process.exit(1);
  });
