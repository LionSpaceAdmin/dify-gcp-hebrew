const { chromium } = require('playwright');

async function exploreDify() {
    console.log('🔍 מתחיל חקירה של ממשק Dify...');
    
    const browser = await chromium.launch({ 
        headless: false,
        slowMo: 1000,
        args: ['--start-maximized']
    });
    
    const context = await browser.newContext({
        locale: 'he-IL',
        timezoneId: 'Asia/Jerusalem',
        viewport: { width: 1920, height: 1080 }
    });
    
    const page = await context.newPage();
    
    try {
        // כניסה לדף הראשי
        console.log('🌐 נכנס ל-Dify...');
        await page.goto('http://localhost');
        await page.waitForLoadState('networkidle');
        
        // צילום של הדף הראשי
        await page.screenshot({ path: 'dify-main.png' });
        console.log('📸 צילום מסך נשמר: dify-main.png');
        
        console.log('🔍 מחפש איפה להגדיר ספקי מודלים...');
        
        // חיפוש כפתורי הגדרות או קישורים לניהול
        const settingsLinks = await page.locator('a, button').filter({ 
            hasText: /settings|model|provider|config|הגדר|ספק|מודל/i 
        }).all();
        
        console.log(`🎯 נמצאו ${settingsLinks.length} קישורים פוטנציאליים להגדרות`);
        
        // נסה לחפש בניווט
        const navItems = await page.locator('nav a, .nav a, [role="navigation"] a').all();
        console.log(`📋 נמצאו ${navItems.length} פריטי ניווט`);
        
        // צילום נוסף אחרי הטעינה
        await page.screenshot({ path: 'dify-loaded.png' });
        console.log('📸 צילום מסך נשמר: dify-loaded.png');
        
        console.log('⏸️ דפדפן נשאר פתוח לחקירה ידנית');
        console.log('🎯 חפש באזור העליון או הצדדי קישורים להגדרות ספקי מודלים');
        console.log('💡 לסגירה, לחץ Ctrl+C');
        
        // נמתין ללא סגירה
        await new Promise(() => {});
        
    } catch (error) {
        console.error('❌ שגיאה בחקירה:', error.message);
        await page.screenshot({ path: 'explore-error.png' });
    }
}

exploreDify().catch(console.error);