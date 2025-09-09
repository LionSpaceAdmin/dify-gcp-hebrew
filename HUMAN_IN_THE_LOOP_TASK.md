# משימת Human-in-the-Loop עם Vercel AI SDK ו-Dify

## מטרה כללית
שילוב מתקדם של Vercel AI SDK עם מערכת Dify הקיימת כדי ליצור יכולות Human-in-the-Loop (HITL) עם תמיכה מלאה בעברית ו-RTL.

## רקע טכני
הפרויקט כולל כבר:
- ✅ `vertex_ai_provider.py` - ספק Vertex AI עם תמיכה בעברית
- ✅ `dify_vertex_ai_integration.py` - שכבת אינטגרציה עם Dify
- ✅ תמיכה מלאה ב-Gemini Pro/Flash models
- ✅ עיבוד RTL ועברית מתקדם

## משימות ספציפיות

### שלב 1: התקנת Vercel AI SDK (1-2 שעות)

#### 1.1 התקנת תלויות
```bash
# בתיקיית הפרויקט
npm install ai @ai-sdk/google @ai-sdk/openai
npm install @vercel/ai @vercel/ai-ui
```

#### 1.2 יצירת קונפיגורציה בסיסית
צור קובץ `vercel-ai-config.js`:
```javascript
import { google } from '@ai-sdk/google';
import { openai } from '@ai-sdk/openai';

export const aiProviders = {
  vertex: google('gemini-1.5-pro', {
    project: process.env.GOOGLE_VERTEX_PROJECT,
    location: process.env.GOOGLE_VERTEX_LOCATION
  }),
  openai: openai('gpt-4-turbo')
};
```

### שלב 2: יצירת Human-in-the-Loop Core (2-3 שעות)

#### 2.1 מודול HITL עיקרי
צור `human_in_the_loop.py`:
```python
"""
Human-in-the-Loop integration for Dify with Vercel AI SDK
"""
import asyncio
import json
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum

class InterventionType(Enum):
    REVIEW = "review"
    APPROVE = "approve"
    EDIT = "edit"
    REJECT = "reject"

@dataclass
class HumanIntervention:
    id: str
    content: str
    intervention_type: InterventionType
    hebrew_context: bool
    response: Optional[str] = None
    approved: bool = False
```

#### 2.2 שילוב עם vertex_ai_provider.py הקיים
הוסף לקלאס `VertexAIProvider` שיטות חדשות:
```python
def generate_with_human_loop(
    self, 
    prompt: str,
    require_approval: bool = True,
    intervention_callback: Optional[Callable] = None
) -> Dict[str, Any]:
    """
    Generate response with human intervention capability
    """
    # קוד שילוב עם Vercel AI SDK
    pass

def setup_intervention_webhook(self, webhook_url: str):
    """
    Setup webhook for human interventions
    """
    pass
```

### שלב 3: Frontend Human-in-the-Loop (2-3 שעות)

#### 3.1 React Components עם תמיכה ב-RTL
צור `components/HumanInTheLoop.jsx`:
```jsx
import { useChat } from '@ai-sdk/react';
import { useState } from 'react';

export function HumanInTheLoopChat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat-hitl',
    initialMessages: []
  });

  return (
    <div dir="rtl" className="human-loop-container">
      {/* RTL Chat interface עם כפתורי התערבות */}
    </div>
  );
}
```

#### 3.2 ממשק אישור ועריכה
```jsx
export function InterventionPanel({ intervention, onApprove, onEdit, onReject }) {
  return (
    <div className="intervention-panel" dir="rtl">
      <h3>דרושה אישור אנושי</h3>
      <div className="content">{intervention.content}</div>
      {/* כפתורים לאישור/עריכה/דחייה */}
    </div>
  );
}
```

### שלב 4: API Routes עם Vercel AI SDK (1-2 שעות)

#### 4.1 יצירת /api/chat-hitl
```javascript
// pages/api/chat-hitl.js
import { streamText } from 'ai';
import { aiProviders } from '../../vercel-ai-config';

export default async function handler(req, res) {
  const { messages } = req.body;
  
  const result = await streamText({
    model: aiProviders.vertex,
    messages,
    onFinish: async ({ text, usage }) => {
      // שלח להתערבות אנושית אם נדרש
      if (requiresHumanReview(text)) {
        await requestHumanIntervention(text);
      }
    }
  });

  return result.toDataStreamResponse();
}
```

#### 4.2 Webhook לאישורים
```javascript
// pages/api/human-intervention.js
export default async function handler(req, res) {
  const { interventionId, action, editedContent } = req.body;
  
  // עיבוד התערבות אנושית
  // שמירה במסד נתונים
  // המשך תהליך AI
}
```

### שלב 5: שילוב OpenAI Codex (1-2 שעות)

#### 5.1 הוספת Codex למערכת
```python
# תוספת ל-vertex_ai_provider.py
class EnhancedVertexAIProvider(VertexAIProvider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_code_with_review(self, code_prompt: str) -> Dict[str, Any]:
        """
        Generate code using Codex with human review
        """
        # יצירת קוד עם Codex
        # שליחה לסקירה אנושית
        # אישור/עריכה
        pass
```

#### 5.2 Unified API עם Vercel
```javascript
// Multi-provider support
const codeGenerationResult = await streamText({
  model: req.body.useCodex ? aiProviders.openai : aiProviders.vertex,
  messages: enhanceForCoding(messages),
  tools: {
    requestCodeReview: {
      description: 'Request human review for generated code',
      parameters: z.object({
        code: z.string(),
        language: z.string()
      })
    }
  }
});
```

### שלב 6: עיבוד עברית מתקדם (1 שעה)

#### 6.1 שיפור עיבוד RTL
```python
def enhance_hebrew_processing(self, text: str) -> str:
    """
    Enhanced Hebrew text processing for HITL
    """
    # זיהוי כיוון טקסט אוטומטי
    # עיבוד מונחים טכניים בעברית
    # תיקון encoding issues
    pass
```

#### 6.2 Hebrew-aware intervention points
```python
def identify_hebrew_intervention_points(self, response: str) -> List[str]:
    """
    Identify points where Hebrew speakers should intervene
    """
    # זיהוי ביטויים שצריכים בדיקה
    # מונחים טכניים שיכולים להיות שגויים
    # הקשר תרבותי שצריך אישור
    pass
```

### שלב 7: בדיקות ואינטגרציה (2-3 שעות)

#### 7.1 Unit Tests
```python
# test_human_in_the_loop.py
def test_hebrew_intervention():
    provider = EnhancedVertexAIProvider(...)
    result = provider.generate_with_human_loop(
        "כתב לי קוד Python מתקדם",
        require_approval=True
    )
    assert result["requires_intervention"] == True
```

#### 7.2 Integration Tests
```javascript
// test-hitl-flow.js
describe('Human in the Loop Flow', () => {
  test('Hebrew text requires proper intervention', async () => {
    // בדיקת זרימה מלאה
  });
});
```

#### 7.3 E2E Tests עם Hebrew
```python
def test_full_hebrew_workflow():
    # בדיקת זרימה מלאה מקצה לקצה
    # כולל UI, API, ו-human intervention
    pass
```

## ממצאי מחקר מיושמים

### Vercel AI SDK Features לשילוב:
1. **Streaming with Interventions** - זרימת טקסט עם נקודות עצירה
2. **Multi-modal Support** - תמיכה בטקסט, תמונות וקוד
3. **Agent Framework** - מערכת סוכנים עם human oversight
4. **Performance Optimizations** - קבצים מוקטנים וביצועים טובים
5. **Tool Calling** - קריאות לכלים עם אישור אנושי

### Hebrew-Specific Enhancements:
1. **RTL UI Components** - רכיבי ממשק מותאמים לעברית
2. **Cultural Context Awareness** - זיהוי הקשר תרבותי
3. **Technical Term Validation** - אימות מונחים טכניים בעברית
4. **Bilingual Workflows** - זרימות עבודה דו-לשוניות

## זמנים משוערים:
- **סה"כ: 10-15 שעות עבודה**
- שלב 1-2: 3-5 שעות (תשתית)
- שלב 3-4: 4-6 שעות (Frontend + API)
- שלב 5-6: 3-4 שעות (Features מתקדמות)
- שלב 7: 2-3 שעות (בדיקות)

## קבצים שייווצרו:
1. `vercel-ai-config.js` - קונפיגורציה
2. `human_in_the_loop.py` - מודול Python עיקרי
3. `components/HumanInTheLoop.jsx` - רכיבי React
4. `pages/api/chat-hitl.js` - API routes
5. `enhanced_vertex_ai_provider.py` - ספק משופר
6. `test_human_in_the_loop.py` - בדיקות

## הערות חשובות:
- ✅ הפרויקט מוכן טכנית לשילוב
- ✅ יש תשתית Vertex AI עובדת
- ✅ תמיכה בעברית קיימת ויציבה
- 🔄 נדרש API key עבור OpenAI (לCodex)
- 🔄 נדרש webhook URL לinterventions

## הצעד הבא:
התחל עם שלב 1 - התקנת Vercel AI SDK ויצירת הקונפיגורציה הבסיסית.