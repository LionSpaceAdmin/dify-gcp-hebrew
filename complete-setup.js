const { chromium } = require('playwright');

async function completeDifySetup() {
    console.log('🎯 מבצע התקנה מלאה של Dify...');
    
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
        console.log('🌐 מחפש את נקודת הכניסה הנכונה...');
        
        // נסה כתובות שונות
        const urls = [
            'http://localhost/install',
            'http://localhost',
            'http://localhost/console',
            'http://localhost/setup'
        ];
        
        let foundUrl = null;
        
        for (const url of urls) {
            console.log(`🔍 בודק ${url}...`);
            try {
                const response = await page.goto(url, { waitUntil: 'networkidle' });
                await page.waitForTimeout(3000);
                
                // בדוק אם יש טופס התקנה או שדות משתמש
                const hasForm = await page.locator('form, input[type="email"], input[type="password"], button').count() > 0;
                const has404 = await page.locator('text="404"').count() > 0;
                
                if (hasForm && !has404) {
                    console.log(`✅ נמצא ממשק התקנה ב-${url}`);
                    foundUrl = url;
                    break;
                } else if (!has404) {
                    console.log(`⏳ ${url} נטען אבל עדיין לא מוכן`);
                }
            } catch (error) {
                console.log(`❌ ${url} לא זמין`);
            }
        }
        
        if (!foundUrl) {
            console.log('⚠️ לא נמצא ממשק התקנה מוכן. ננסה להמתין יותר...');
            await page.goto('http://localhost');
            await page.waitForTimeout(10000);
        }
        
        // צילום מסך של המצב הנוכחי
        await page.screenshot({ path: 'setup-current-state.png' });
        console.log('📸 צילום מסך נשמר: setup-current-state.png');
        
        // חפש כפתורי התקנה או הגדרה
        const setupButtons = await page.locator('button, a').filter({ 
            hasText: /setup|install|start|get started|התחל|התקן|הגדר/i 
        }).all();
        
        console.log(`🔧 נמצאו ${setupButtons.length} כפתורי הגדרה אפשריים`);
        
        // אם יש כפתור התקנה, לחץ עליו
        if (setupButtons.length > 0) {
            console.log('▶️ לוחץ על כפתור ההגדרה...');
            await setupButtons[0].click();
            await page.waitForTimeout(3000);
        }
        
        // צילום אחרי לחיצה
        await page.screenshot({ path: 'setup-after-click.png' });
        console.log('📸 צילום אחרי לחיצה: setup-after-click.png');
        
        console.log('⏸️ דפדפן פתוח להמשך ידני');
        console.log('🎯 אם רואה טופס - מלא פרטי admin');
        console.log('📧 דוגמה: admin@dify.local');
        console.log('🔑 דוגמה: password123');
        console.log('💡 לסגירה, לחץ Ctrl+C');
        
        // נשאר פתוח
        await new Promise(() => {});
        
    } catch (error) {
        console.error('❌ שגיאה בהתקנה:', error.message);
        await page.screenshot({ path: 'setup-error.png' });
    }
}

completeDifySetup().catch(console.error);