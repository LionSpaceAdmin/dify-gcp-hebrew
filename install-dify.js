const { chromium } = require('playwright');

async function installDify() {
    console.log('🚀 מתחיל התקנה אוטומטית של Dify...');
    
    const browser = await chromium.launch({ 
        headless: false,
        slowMo: 2000,
        args: ['--start-maximized']
    });
    
    const context = await browser.newContext({
        locale: 'he-IL',
        timezoneId: 'Asia/Jerusalem',
        viewport: { width: 1920, height: 1080 }
    });
    
    const page = await context.newPage();
    
    try {
        // כניסה לעמוד ההתקנה
        console.log('🌐 נכנס לעמוד ההתקנה...');
        await page.goto('http://localhost/install');
        await page.waitForLoadState('networkidle');
        
        // צילום מסך של עמוד ההתקנה
        await page.screenshot({ path: 'install-step-1.png' });
        console.log('📸 צילום מסך נשמר: install-step-1.png');
        
        // חיפוש שדות ההתקנה
        console.log('🔍 מחפש שדות התקנה...');
        
        // נמתין שהעמוד יטען לגמרי
        await page.waitForTimeout(3000);
        
        // נבדוק מה יש בעמוד
        const pageContent = await page.content();
        console.log('📄 תוכן העמוד נטען');
        
        // חיפוש כפתור או קישור להמשיך
        const nextButton = await page.locator('button, a').filter({ hasText: /next|continue|התחל|המשך|install/i }).first();
        
        if (await nextButton.isVisible()) {
            console.log('✅ נמצא כפתור המשך');
            await nextButton.click();
            await page.waitForTimeout(2000);
        }
        
        // צילום מסך של השלב הבא
        await page.screenshot({ path: 'install-step-2.png' });
        console.log('📸 צילום מסך נשמר: install-step-2.png');
        
        console.log('⏸️ דפדפן נשאר פתוח למילוי ידני של פרטי Admin');
        console.log('🎯 כעת מלא את פרטי המשתמש הראשון בדפדפן');
        console.log('💡 לסגירה, לחץ Ctrl+C');
        
        // נמתין ללא סגירה
        await new Promise(() => {});
        
    } catch (error) {
        console.error('❌ שגיאה בהתקנה:', error.message);
        await page.screenshot({ path: 'install-error.png' });
        console.log('📸 צילום מסך של השגיאה נשמר');
    }
}

installDify().catch(console.error);