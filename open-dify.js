#!/usr/bin/env node

const { chromium } = require('playwright');

/**
 * פתיחת דפדפן עם Dify בשפה העברית
 */
async function openDify() {
  console.log('🚀 פותח דפדפן עם Dify...');
  
  const browser = await chromium.launch({
    headless: false,
    slowMo: 1000,
    args: [
      '--start-maximized',
      '--lang=he',
      '--disable-features=TranslateUI',
      '--accept-lang=he-IL,he,en-US,en'
    ]
  });

  const context = await browser.newContext({
    locale: 'he-IL',
    timezoneId: 'Asia/Jerusalem',
    viewport: { width: 1920, height: 1080 }
  });

  const page = await context.newPage();
  
  try {
    console.log('🌐 נכנס ל-Dify...');
    await page.goto('http://localhost', { 
      waitUntil: 'networkidle',
      timeout: 30000 
    });
    
    console.log('✅ דפדפן פתוח! כתובת:', page.url());
    console.log('💡 לסגירה, לחץ Ctrl+C');
    
    // הישאר פתוח עד סגירה ידנית
    await page.waitForTimeout(3600000); // שעה
    
  } catch (error) {
    console.error('❌ שגיאה:', error.message);
  } finally {
    await browser.close();
  }
}

// הרצה רק אם זה הקובץ הראשי
if (require.main === module) {
  openDify().catch(console.error);
}

module.exports = { openDify };