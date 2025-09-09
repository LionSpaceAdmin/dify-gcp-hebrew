// ייבוא מודולים נדרשים
const { devices } = require('@playwright/test');

module.exports = {
  // הגדרות כלליות
  timeout: 30 * 1000,
  expect: {
    timeout: 5000
  },
  
  // הגדרות דפדפן
  use: {
    // שפה עברית
    locale: 'he-IL',
    timezoneId: 'Asia/Jerusalem',
    
    // מסך מלא
    viewport: { width: 1920, height: 1080 },
    
    // צילומי מסך כשיש כשלים
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    
    // שמירת קשרי רשת
    trace: 'retain-on-failure',
    
    // הגדרות נוספות
    acceptDownloads: true,
    ignoreHTTPSErrors: true
  },

  // פרויקטים - דפדפנים שונים
  projects: [
    {
      name: 'chromium',
      use: { 
        ...devices['Desktop Chrome'],
        headless: false,  // תמיד מציג דפדפן
        slowMo: 1000      // האטה לראות מה קורה
      }
    },
    {
      name: 'firefox',
      use: { 
        ...devices['Desktop Firefox'],
        headless: false,
        slowMo: 1000
      }
    }
  ],

  // תיקיות קלט ופלט
  testDir: './tests',
  outputDir: './test-results',
  
  // דוחות
  reporter: [
    ['html', { outputFolder: './playwright-report', open: 'never' }],
    ['json', { outputFile: './test-results.json' }]
  ],

  // שרת מקומי
  webServer: {
    command: 'echo "Dify server should be running on localhost"',
    url: 'http://localhost',
    reuseExistingServer: true,
    timeout: 5 * 1000
  }
};