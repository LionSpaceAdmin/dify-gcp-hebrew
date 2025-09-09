const { chromium } = require('playwright');

async function openDifyConsole() {
    console.log('🎯 פותח קונסולת Dify...');
    
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
        // כניסה לקונסולת Dify
        console.log('🌐 נכנס לקונסולת Dify...');
        await page.goto('http://localhost/console');
        await page.waitForLoadState('networkidle');
        
        // המתן לטעינה מלאה
        await page.waitForTimeout(5000);
        
        // צילום של קונסולת Dify
        await page.screenshot({ path: 'dify-console.png' });
        console.log('📸 צילום מסך נשמר: dify-console.png');
        
        console.log('🔍 מחפש הגדרות וספקי מודלים...');
        
        // חיפוש כפתורי הגדרות
        const settingsButtons = await page.locator('button, a, [role="button"]').filter({ 
            hasText: /settings|model|provider|config|setup|הגדר|ספק|מודל/i 
        }).all();
        
        console.log(`⚙️ נמצאו ${settingsButtons.length} אלמנטים עם מילות מפתח של הגדרות`);
        
        // צילום נוסף
        await page.screenshot({ path: 'dify-console-loaded.png' });
        console.log('📸 צילום מסך נוסף נשמר: dify-console-loaded.png');
        
        console.log('✅ קונסולת Dify פתוחה!');
        console.log('🎯 חפש בממשק הגדרות לספקי מודלים');
        console.log('🔧 אם יש צורך, צור workspace או admin user');
        console.log('💡 לסגירה, לחץ Ctrl+C');
        
        // נמתין ללא סגירה
        await new Promise(() => {});
        
    } catch (error) {
        console.error('❌ שגיאה בפתיחת הקונסולה:', error.message);
        await page.screenshot({ path: 'console-error.png' });
    }
}

openDifyConsole().catch(console.error);