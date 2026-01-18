{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 const express = require('express');\
const multer = require('multer');\
const \{ createClient \} = require('@supabase/supabase-js');\
\
const app = express();\
const upload = multer(\{ \
  storage: multer.memoryStorage(),\
  limits: \{ fileSize: 20 * 1024 * 1024 \}\
\});\
\
const supabase = createClient(\
  process.env.SUPABASE_URL,\
  process.env.SUPABASE_SERVICE_ROLE_KEY\
);\
\
let assimpReady = null;\
\
async function initializeAssimp() \{\
  console.log('\uc0\u55357 \u56615  Initializing Assimp.js...');\
  try \{\
    const assimpFactory = require('assimpjs');
    const assimpModule = assimpFactory();\
    assimpReady = await assimpModule;\
    \
    console.log('\uc0\u9989  Assimp.js initialized successfully');\
    \
    if (typeof assimpReady.FileList !== 'function') \{\
      throw new Error('FileList is not available!');\
    \}\
    if (typeof assimpReady.ConvertFileList !== 'function') \{\
      throw new Error('ConvertFileList is not available!');\
    \}\
    \
    console.log('\uc0\u9989  FileList and ConvertFileList verified');\
    \
  \} catch (error) \{\
    console.error('\uc0\u10060  Failed to initialize Assimp.js:', error);\
    throw error;\
  \}\
\}\
\
app.post('/convert', upload.single('file'), async (req, res) => \{\
  const startTime = Date.now();\
  \
  try \{\
    if (!req.file) \{\
      return res.status(400).json(\{ success: false, error: 'No file uploaded' \});\
    \}\
\
    console.log(`\\n$\{'='.repeat(60)\}`);\
    console.log(`\uc0\u55357 \u56549  Converting $\{req.file.originalname\}`);\
    console.log(`   File size: $\{(req.file.size / 1024).toFixed(2)\} KB`);\
    \
    if (!assimpReady) \{\
      throw new Error('Assimp.js not initialized');\
    \}\
\
    console.log(`\uc0\u55356 \u57303 \u65039   Creating FileList...`);\
    const fileList = new assimpReady.FileList();\
    \
    console.log(`\uc0\u55357 \u56541  Adding file...`);\
    fileList.AddFile(req.file.originalname, new Uint8Array(req.file.buffer));\
    \
    console.log(`\uc0\u55357 \u56580  Converting to GLB...`);\
    const conversionStart = Date.now();\
    const result = assimpReady.ConvertFileList(fileList, 'glb2');\
    const conversionTime = ((Date.now() - conversionStart) / 1000).toFixed(2);\
    \
    console.log(`\uc0\u10024  Conversion completed in $\{conversionTime\}s`);\
    \
    if (!result.IsSuccess()) \{\
      fileList.delete();\
      result.delete();\
      throw new Error('Conversion failed');\
    \}\
    \
    const glbFile = result.FileList().GetFile(0);\
    const glbBuffer = Buffer.from(glbFile.GetContent());\
    const glbFileName = req.file.originalname.replace(/\\.(skp|liar)$/i, '.glb');\
    \
    console.log(`\uc0\u9729 \u65039   Uploading to Supabase...`);\
    const \{ data, error \} = await supabase.storage\
      .from('converted-files')\
      .upload(glbFileName, glbBuffer, \{\
        contentType: 'model/gltf-binary',\
        upsert: true\
      \});\
    \
    if (error) \{\
      fileList.delete();\
      result.delete();\
      throw error;\
    \}\
    \
    fileList.delete();\
    result.delete();\
    \
    const totalTime = ((Date.now() - startTime) / 1000).toFixed(2);\
    console.log(`\uc0\u9989  Complete! Total: $\{totalTime\}s`);\
    console.log(`$\{'='.repeat(60)\}\\n`);\
    \
    res.json(\{ \
      success: true, \
      glbPath: data.path,\
      conversionTime: parseFloat(conversionTime),\
      totalTime: parseFloat(totalTime)\
    \});\
    \
  \} catch (error) \{\
    console.error(`\uc0\u10060  Error: $\{error.message\}`);\
    res.status(500).json(\{ success: false, error: error.message \});\
  \}\
\});\
\
app.get('/health', (req, res) => \{\
  res.json(\{ \
    status: 'ok', \
    assimpReady: assimpReady !== null\
  \});\
\});\
\
app.get('/status', (req, res) => \{\
  res.json(\{\
    assimpInitialized: assimpReady !== null,\
    fileListAvailable: assimpReady ? typeof assimpReady.FileList === 'function' : false\
  \});\
\});\
\
const PORT = process.env.PORT || 10000;\
\
initializeAssimp()\
  .then(() => \{\
    app.listen(PORT, '0.0.0.0', () => \{\
      console.log(`\\n$\{'='.repeat(60)\}`);\
      console.log(`\uc0\u55357 \u56960  Scanbrix Conversion Service ONLINE`);\
      console.log(`   Port: $\{PORT\}`);\
      console.log(`$\{'='.repeat(60)\}\\n`);\
    \});\
  \})\
  .catch((error) => \{\
    console.error('\uc0\u10060  Failed to start:', error);\
    process.exit(1);\
  \});}
