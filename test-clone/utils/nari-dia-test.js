// Nari Dia TTS API Test Utility
// Test if the Nari Dia server is running correctly and accessible

const axios = require('axios');

const NARI_DIA_ENDPOINT = 'http://localhost:7860/api/v1/generate';
const TEST_TEXT = 'Hello, this is a test of Nari Dia TTS integration with VAPI.';

/**
 * Test the Nari Dia TTS API connection
 */
async function testNariDiaAPI() {
  console.log('🎙️ Testing Nari Dia TTS API...');
  console.log(`📍 Endpoint: ${NARI_DIA_ENDPOINT}`);
  console.log(`📝 Test text: "${TEST_TEXT}"`);
  console.log('');

  try {
    // Test 1: Health check
    console.log('🔍 Step 1: Health check...');
    
    const healthResponse = await axios.get('http://localhost:7860/', {
      timeout: 5000
    });
    
    if (healthResponse.status === 200) {
      console.log('✅ Nari Dia server is running');
    }

    // Test 2: API endpoint test
    console.log('🔍 Step 2: Testing TTS generation...');
    
    const ttsPayload = {
      text: TEST_TEXT,
      temperature: 0.7,
      top_p: 0.95,
      cfg_scale: 3.5,
      speed: 1.0
    };

    const ttsResponse = await axios.post(NARI_DIA_ENDPOINT, ttsPayload, {
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (ttsResponse.status === 200) {
      console.log('✅ TTS generation successful');
      console.log(`📊 Response type: ${typeof ttsResponse.data}`);
      
      if (ttsResponse.data.audio_url) {
        console.log(`🔗 Audio URL: ${ttsResponse.data.audio_url}`);
      }
      
      if (ttsResponse.data.audio_data) {
        console.log(`💾 Audio data size: ${ttsResponse.data.audio_data.length} bytes`);
      }
    }

    // Test 3: VAPI compatibility check
    console.log('🔍 Step 3: VAPI compatibility check...');
    
    const vapiTestPayload = {
      text: TEST_TEXT,
      voice_settings: {
        temperature: 0.7,
        top_p: 0.95,
        cfg_scale: 3.5
      },
      format: 'wav',
      sample_rate: 24000
    };

    try {
      const vapiResponse = await axios.post(NARI_DIA_ENDPOINT, vapiTestPayload, {
        timeout: 30000,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'audio/wav'
        }
      });

      if (vapiResponse.status === 200) {
        console.log('✅ VAPI-compatible response format');
      }
    } catch (vapiError) {
      console.log('⚠️  VAPI format may need adjustment');
      console.log(`   Error: ${vapiError.message}`);
    }

    console.log('');
    console.log('🎉 Nari Dia API test completed successfully!');
    console.log('');
    console.log('📱 Next steps:');
    console.log('1. Open your VAPI demo at http://localhost:3000');
    console.log('2. Select "Nari Dia TTS" in the voice selector');
    console.log('3. Start a conversation and test the voice synthesis');
    console.log('');
    
    return true;

  } catch (error) {
    console.error('❌ Nari Dia API test failed:');
    console.error('');
    
    if (error.code === 'ECONNREFUSED') {
      console.error('🔌 Connection refused - Nari Dia server is not running');
      console.error('');
      console.error('💡 To fix this:');
      console.error('1. Make sure you have installed Nari Dia TTS');
      console.error('2. Start the server: cd nari-dia && python app.py');
      console.error('3. Wait for the server to fully load (may take a few minutes)');
      console.error('4. Try this test again');
    } else if (error.code === 'ENOTFOUND') {
      console.error('🌐 Host not found - Check if localhost:7860 is correct');
    } else if (error.code === 'ETIMEDOUT') {
      console.error('⏰ Request timeout - Server may be starting up or overloaded');
      console.error('   Wait a few minutes and try again');
    } else {
      console.error(`🚨 Unexpected error: ${error.message}`);
      if (error.response) {
        console.error(`   Status: ${error.response.status}`);
        console.error(`   Data: ${JSON.stringify(error.response.data, null, 2)}`);
      }
    }
    
    console.error('');
    return false;
  }
}

/**
 * Monitor Nari Dia server status
 */
async function monitorNariDiaStatus() {
  console.log('👀 Monitoring Nari Dia server status...');
  console.log('Press Ctrl+C to stop monitoring');
  console.log('');

  let consecutiveFailures = 0;
  const maxFailures = 3;

  const checkStatus = async () => {
    try {
      const response = await axios.get('http://localhost:7860/', { timeout: 3000 });
      
      if (response.status === 200) {
        console.log(`✅ ${new Date().toLocaleTimeString()} - Nari Dia server is running`);
        consecutiveFailures = 0;
      }
    } catch (error) {
      consecutiveFailures++;
      console.log(`❌ ${new Date().toLocaleTimeString()} - Server not responding (${consecutiveFailures}/${maxFailures})`);
      
      if (consecutiveFailures >= maxFailures) {
        console.log('');
        console.log('🚨 Server appears to be down. Please check:');
        console.log('1. Is the Nari Dia process still running?');
        console.log('2. Check the server logs for errors');
        console.log('3. Try restarting: python app.py');
        console.log('');
      }
    }
  };

  // Check immediately, then every 10 seconds
  await checkStatus();
  const interval = setInterval(checkStatus, 10000);

  // Handle Ctrl+C gracefully
  process.on('SIGINT', () => {
    clearInterval(interval);
    console.log('\n👋 Monitoring stopped');
    process.exit(0);
  });
}

// CLI interface
if (require.main === module) {
  const command = process.argv[2];

  switch (command) {
    case 'test':
      testNariDiaAPI();
      break;
    case 'monitor':
      monitorNariDiaStatus();
      break;
    default:
      console.log('Nari Dia TTS Test Utility');
      console.log('');
      console.log('Usage:');
      console.log('  node nari-dia-test.js test    - Test API functionality');
      console.log('  node nari-dia-test.js monitor - Monitor server status');
      console.log('');
      console.log('Make sure Nari Dia server is running on localhost:7860');
  }
}

module.exports = {
  testNariDiaAPI,
  monitorNariDiaStatus
}; 