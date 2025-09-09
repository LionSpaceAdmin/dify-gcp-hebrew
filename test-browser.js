#!/usr/bin/env node

// Automated browser test for Dify Hebrew/Vertex AI system
// Using Playwright for comprehensive testing

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

class DifySystemTester {
    constructor() {
        this.browser = null;
        this.context = null;
        this.page = null;
        this.testResults = [];
        this.startTime = Date.now();
    }

    async initialize() {
        console.log('🚀 מאתחל דפדפן לבדיקות אוטומטיות...');
        
        this.browser = await chromium.launch({
            headless: false,  // Show browser for debugging
            args: [
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--lang=he'  // Hebrew locale
            ]
        });

        this.context = await this.browser.newContext({
            locale: 'he-IL',
            timezoneId: 'Asia/Jerusalem',
            viewport: { width: 1440, height: 900 }
        });

        this.page = await this.context.newPage();
        
        // Enable Hebrew fonts and RTL
        await this.page.addStyleTag({
            content: `
                * { 
                    font-family: 'Arial Hebrew', 'Noto Sans Hebrew', Arial, sans-serif !important;
                    direction: rtl !important;
                }
                body { 
                    direction: rtl !important;
                    text-align: right !important;
                }
            `
        });
    }

    async logResult(test, status, message, screenshot = null) {
        const result = {
            test,
            status, // 'pass', 'fail', 'warning'
            message,
            timestamp: new Date().toISOString(),
            screenshot
        };
        
        this.testResults.push(result);
        
        const emoji = status === 'pass' ? '✅' : status === 'fail' ? '❌' : '⚠️';
        console.log(`${emoji} ${test}: ${message}`);
        
        if (screenshot) {
            await this.page.screenshot({ 
                path: `./screenshots/${test.replace(/\s+/g, '_')}.png`,
                fullPage: true 
            });
        }
    }

    async testProjectTracker() {
        console.log('\n📊 בודק את מעקב הפרויקט...');
        
        try {
            const trackerPath = path.join(__dirname, 'project-tracker.html');
            await this.page.goto(`file://${trackerPath}`);
            await this.page.waitForTimeout(2000);

            // Check Hebrew content
            const hebrewTitle = await this.page.textContent('h1');
            if (hebrewTitle && hebrewTitle.includes('מעקב משימות')) {
                await this.logResult('Project Tracker Hebrew', 'pass', 'כותרת בעברית נטענה בהצלחה', true);
            } else {
                await this.logResult('Project Tracker Hebrew', 'fail', 'בעיה בטעינת תוכן עברי');
            }

            // Check RTL layout
            const bodyDir = await this.page.getAttribute('html', 'dir');
            if (bodyDir === 'rtl') {
                await this.logResult('RTL Layout', 'pass', 'פריסה מימין לשמאל פועלת');
            } else {
                await this.logResult('RTL Layout', 'fail', 'פריסה RTL לא פועלת כהלכה');
            }

            // Check statistics
            const completedCount = await this.page.textContent('#completed-count');
            await this.logResult('Statistics Display', 'pass', `סטטיסטיקות מוצגות: ${completedCount} הושלמו`);

        } catch (error) {
            await this.logResult('Project Tracker', 'fail', `שגיאה: ${error.message}`);
        }
    }

    async testDifyServices() {
        console.log('\n🔧 בודק שירותי Dify...');
        
        const services = [
            { name: 'Dify Web UI', url: 'http://localhost:3000', timeout: 10000 },
            { name: 'Dify API', url: 'http://localhost:5001', timeout: 5000 },
            { name: 'Dify API Health', url: 'http://localhost:5001/health', timeout: 5000 },
            { name: 'Swagger UI', url: 'http://localhost:5001/swagger-ui.html', timeout: 5000 }
        ];

        for (const service of services) {
            try {
                console.log(`🔍 בודק ${service.name}...`);
                
                const response = await this.page.goto(service.url, {
                    waitUntil: 'networkidle',
                    timeout: service.timeout
                });

                if (response.status() === 200) {
                    await this.logResult(service.name, 'pass', 'שירות זמין ומגיב', true);
                    
                    // Special checks for main UI
                    if (service.name === 'Dify Web UI') {
                        await this.page.waitForTimeout(3000);
                        
                        // Check for Hebrew support
                        const pageContent = await this.page.content();
                        if (pageContent.includes('lang="he"') || pageContent.includes('dir="rtl"')) {
                            await this.logResult('Hebrew UI Support', 'pass', 'תמיכה בעברית זוהתה');
                        } else {
                            await this.logResult('Hebrew UI Support', 'warning', 'תמיכה בעברית לא זוהתה במפורש');
                        }
                    }
                    
                } else {
                    await this.logResult(service.name, 'fail', `קוד תגובה: ${response.status()}`);
                }
                
            } catch (error) {
                if (error.message.includes('net::ERR_CONNECTION_REFUSED')) {
                    await this.logResult(service.name, 'fail', 'שירות לא פועל - חיבור נדחה');
                } else if (error.message.includes('Timeout')) {
                    await this.logResult(service.name, 'fail', 'פג זמן החיבור - שירות אינו מגיב');
                } else {
                    await this.logResult(service.name, 'fail', `שגיאה: ${error.message}`);
                }
            }
        }
    }

    async testDockerServices() {
        console.log('\n🐳 בודק שירותי Docker...');
        
        const { exec } = require('child_process');
        const util = require('util');
        const execPromise = util.promisify(exec);
        
        try {
            const { stdout } = await execPromise('docker-compose -f docker-compose.dev.yaml ps --services --filter "status=running"');
            const runningServices = stdout.trim().split('\n').filter(s => s.length > 0);
            
            const expectedServices = ['db', 'redis'];
            for (const service of expectedServices) {
                if (runningServices.includes(service)) {
                    await this.logResult(`Docker Service: ${service}`, 'pass', 'שירות פועל');
                } else {
                    await this.logResult(`Docker Service: ${service}`, 'fail', 'שירות לא פועל');
                }
            }
        } catch (error) {
            await this.logResult('Docker Services', 'fail', `שגיאה בבדיקת Docker: ${error.message}`);
        }
    }

    async generateReport() {
        console.log('\n📋 יוצר דוח בדיקות...');
        
        const totalTests = this.testResults.length;
        const passedTests = this.testResults.filter(r => r.status === 'pass').length;
        const failedTests = this.testResults.filter(r => r.status === 'fail').length;
        const warningTests = this.testResults.filter(r => r.status === 'warning').length;
        const duration = Math.round((Date.now() - this.startTime) / 1000);

        const report = {
            timestamp: new Date().toISOString(),
            duration: `${duration} seconds`,
            summary: {
                total: totalTests,
                passed: passedTests,
                failed: failedTests,
                warnings: warningTests,
                success_rate: Math.round((passedTests / totalTests) * 100)
            },
            results: this.testResults
        };

        // Save JSON report
        fs.writeFileSync('./test-report.json', JSON.stringify(report, null, 2));
        
        // Generate HTML report
        const htmlReport = this.generateHtmlReport(report);
        fs.writeFileSync('./test-report.html', htmlReport);

        console.log(`\n📊 סיכום בדיקות:`);
        console.log(`⏱️  משך זמן: ${duration} שניות`);
        console.log(`✅ עברו: ${passedTests}/${totalTests}`);
        console.log(`❌ נכשלו: ${failedTests}/${totalTests}`);
        console.log(`⚠️  אזהרות: ${warningTests}/${totalTests}`);
        console.log(`🎯 שיעור הצלחה: ${report.summary.success_rate}%`);
        
        return report;
    }

    generateHtmlReport(report) {
        return `
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>דוח בדיקות Dify Hebrew/Vertex AI</title>
    <style>
        body { font-family: Arial, Hebrew; direction: rtl; background: #f5f5f5; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        .header { text-align: center; border-bottom: 2px solid #007acc; padding-bottom: 20px; }
        .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }
        .test-result { margin: 10px 0; padding: 15px; border-radius: 5px; border-left: 4px solid; }
        .pass { background: #d5f4e6; border-color: #27ae60; }
        .fail { background: #ffeaa7; border-color: #e17055; }
        .warning { background: #fdcb6e; border-color: #f39c12; }
        .timestamp { color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 דוח בדיקות מערכת Dify</h1>
            <p class="timestamp">נוצר: ${new Date(report.timestamp).toLocaleString('he-IL')}</p>
        </div>
        
        <div class="summary">
            <div class="stat-card">
                <h3>${report.summary.total}</h3>
                <p>סה"כ בדיקות</p>
            </div>
            <div class="stat-card" style="background: linear-gradient(135deg, #27ae60, #2d3436);">
                <h3>${report.summary.passed}</h3>
                <p>עברו בהצלחה</p>
            </div>
            <div class="stat-card" style="background: linear-gradient(135deg, #e17055, #2d3436);">
                <h3>${report.summary.failed}</h3>
                <p>נכשלו</p>
            </div>
            <div class="stat-card" style="background: linear-gradient(135deg, #f39c12, #2d3436);">
                <h3>${report.summary.success_rate}%</h3>
                <p>שיעור הצלחה</p>
            </div>
        </div>

        <div class="results">
            ${report.results.map(result => `
                <div class="test-result ${result.status}">
                    <h4>${result.test}</h4>
                    <p>${result.message}</p>
                    <small class="timestamp">${new Date(result.timestamp).toLocaleString('he-IL')}</small>
                </div>
            `).join('')}
        </div>
    </div>
</body>
</html>`;
    }

    async cleanup() {
        if (this.browser) {
            await this.browser.close();
        }
    }

    async runAllTests() {
        try {
            await this.initialize();
            
            // Create screenshots directory
            if (!fs.existsSync('./screenshots')) {
                fs.mkdirSync('./screenshots');
            }

            // Run all tests
            await this.testProjectTracker();
            await this.testDockerServices();
            await this.testDifyServices();
            
            // Generate report
            const report = await this.generateReport();
            
            // Auto-open test report
            const reportPath = path.join(__dirname, 'test-report.html');
            console.log(`\n🌐 פותח דוח בדיקות: file://${reportPath}`);
            await this.page.goto(`file://${reportPath}`);
            await this.page.waitForTimeout(5000);
            
            return report;
            
        } catch (error) {
            console.error('❌ שגיאה כללית בבדיקות:', error.message);
        }
    }
}

// Run tests if called directly
if (require.main === module) {
    const tester = new DifySystemTester();
    
    tester.runAllTests()
        .then(report => {
            console.log('\n🎉 בדיקות הושלמו! דפדפן נשאר פתוח לבחינה ידנית.');
            console.log('לסגירת הדפדפן, לחץ Ctrl+C');
        })
        .catch(error => {
            console.error('💥 שגיאה חמורה:', error);
            process.exit(1);
        });
        
    // Keep process alive
    process.on('SIGINT', async () => {
        console.log('\n👋 סוגר דפדפן...');
        await tester.cleanup();
        process.exit(0);
    });
}

module.exports = DifySystemTester;