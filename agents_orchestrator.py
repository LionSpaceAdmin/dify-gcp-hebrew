#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orchestrator לניהול סוכני AI מרובים
משתמש ב-LangGraph לתיאום משימות מורכבות
"""

import os
from typing import List, Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict
import json

class AgentState(TypedDict):
    """מצב המשותף בין הסוכנים"""
    messages: List[Any]
    current_task: str
    completed_tasks: List[str]
    context: Dict[str, Any]
    next_agent: str

class MultiAgentOrchestrator:
    """מנהל הסוכנים הראשי"""
    
    def __init__(self, anthropic_api_key: str):
        """
        אתחול המערכת
        """
        # הגדרת המודל
        self.llm = ChatAnthropic(
            anthropic_api_key=anthropic_api_key,
            model="claude-3-sonnet-20240229"
        )
        
        # רישום הסוכנים
        self.agents = {
            "planner": self._create_planner_agent(),
            "researcher": self._create_researcher_agent(),
            "coder": self._create_coder_agent(),
            "reviewer": self._create_reviewer_agent(),
        }
        
        # בניית הגרף
        self.workflow = self._build_workflow()
    
    def _create_planner_agent(self):
        """סוכן תכנון - מחליט מה לעשות"""
        system_prompt = """
        אתה סוכן תכנון חכם. המשימה שלך:
        1. לנתח את הבקשה של המשתמש
        2. לחלק אותה למשימות קטנות
        3. להחליט איזה סוכן צריך לבצע כל משימה
        4. לתת הוראות ברורות
        
        השב תמיד בפורמט JSON:
        {
          "plan": ["משימה 1", "משימה 2"],
          "next_agent": "researcher/coder/reviewer",
          "instructions": "הוראות ספציפיות"
        }
        """
        
        def planner_logic(state: AgentState) -> Dict[str, Any]:
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend([{"role": "human" if isinstance(m, HumanMessage) else "assistant", 
                           "content": m.content} for m in state["messages"]])
            
            response = self.llm.invoke(messages)
            
            try:
                result = json.loads(response.content)
                return {
                    "messages": state["messages"] + [AIMessage(content=response.content)],
                    "current_task": result.get("instructions", ""),
                    "next_agent": result.get("next_agent", "researcher"),
                    "context": {**state.get("context", {}), "plan": result.get("plan", [])}
                }
            except:
                return {
                    "messages": state["messages"] + [AIMessage(content=response.content)],
                    "next_agent": "researcher",
                    "context": state.get("context", {})
                }
        
        return planner_logic
    
    def _create_researcher_agent(self):
        """סוכן מחקר - אוסף מידע"""
        system_prompt = """
        אתה סוכן מחקר מקצועי. המשימה שלך:
        1. לחקור ולאסוף מידע רלוונטי
        2. לנתח ולסכם את הממצאים
        3. להמליץ על הצעד הבא
        
        השב תמיד בפורמט JSON:
        {
          "research_results": "סיכום הממצאים",
          "recommendations": "המלצות לצעד הבא",
          "next_agent": "coder/planner/reviewer"
        }
        """
        
        def researcher_logic(state: AgentState) -> Dict[str, Any]:
            messages = [{"role": "system", "content": system_prompt}]
            messages.append({"role": "human", "content": f"חקור: {state['current_task']}"})
            
            response = self.llm.invoke(messages)
            
            try:
                result = json.loads(response.content)
                return {
                    "messages": state["messages"] + [AIMessage(content=response.content)],
                    "completed_tasks": state.get("completed_tasks", []) + [state.get("current_task", "")],
                    "next_agent": result.get("next_agent", "coder"),
                    "context": {**state.get("context", {}), "research": result}
                }
            except:
                return {
                    "messages": state["messages"] + [AIMessage(content=response.content)],
                    "next_agent": "coder",
                    "context": state.get("context", {})
                }
        
        return researcher_logic
    
    def _create_coder_agent(self):
        """סוכן קודינג - כותב קוד"""
        system_prompt = """
        אתה מפתח תוכנה מומחה. המשימה שלך:
        1. לכתוב קוד איכותי ומתועד
        2. לפתור בעיות טכניות
        3. להציע פתרונות יעילים
        
        השב תמיד בפורמט JSON:
        {
          "code": "הקוד שנכתב",
          "explanation": "הסבר על הקוד",
          "next_agent": "reviewer/planner"
        }
        """
        
        def coder_logic(state: AgentState) -> Dict[str, Any]:
            messages = [{"role": "system", "content": system_prompt}]
            messages.append({"role": "human", "content": f"כתוב קוד עבור: {state['current_task']}"})
            
            response = self.llm.invoke(messages)
            
            try:
                result = json.loads(response.content)
                return {
                    "messages": state["messages"] + [AIMessage(content=response.content)],
                    "completed_tasks": state.get("completed_tasks", []) + [state.get("current_task", "")],
                    "next_agent": result.get("next_agent", "reviewer"),
                    "context": {**state.get("context", {}), "code": result}
                }
            except:
                return {
                    "messages": state["messages"] + [AIMessage(content=response.content)],
                    "next_agent": "reviewer",
                    "context": state.get("context", {})
                }
        
        return coder_logic
    
    def _create_reviewer_agent(self):
        """סוכן ביקורת - בודק ומאשר"""
        system_prompt = """
        אתה סוכן ביקורת קפדני. המשימה שלך:
        1. לבדוק את איכות העבודה
        2. להציע שיפורים
        3. להחליט אם סיימנו או צריך עוד עבודה
        
        השב תמיד בפורמט JSON:
        {
          "review": "ביקורת מפורטת",
          "approved": true/false,
          "next_agent": "END/planner/coder"
        }
        """
        
        def reviewer_logic(state: AgentState) -> Dict[str, Any]:
            messages = [{"role": "system", "content": system_prompt}]
            messages.append({"role": "human", "content": f"בדוק: {state.get('context', {})}"})
            
            response = self.llm.invoke(messages)
            
            try:
                result = json.loads(response.content)
                next_step = "END" if result.get("approved", False) else result.get("next_agent", "planner")
                
                return {
                    "messages": state["messages"] + [AIMessage(content=response.content)],
                    "completed_tasks": state.get("completed_tasks", []) + ["review"],
                    "next_agent": next_step,
                    "context": {**state.get("context", {}), "review": result}
                }
            except:
                return {
                    "messages": state["messages"] + [AIMessage(content=response.content)],
                    "next_agent": "END",
                    "context": state.get("context", {})
                }
        
        return reviewer_logic
    
    def _build_workflow(self):
        """בניית גרף העבודה"""
        workflow = StateGraph(AgentState)
        
        # הוספת הצמתים (הסוכנים)
        for agent_name, agent_func in self.agents.items():
            workflow.add_node(agent_name, agent_func)
        
        # הגדרת נקודת ההתחלה
        workflow.set_entry_point("planner")
        
        # הוספת המעברים המותנים
        def route_next(state: AgentState) -> str:
            next_agent = state.get("next_agent", "END")
            if next_agent in self.agents:
                return next_agent
            return END
        
        # חיבור כל הסוכנים לראוטר
        for agent_name in self.agents.keys():
            workflow.add_conditional_edges(
                agent_name,
                route_next,
                {name: name for name in self.agents.keys()} | {"END": END}
            )
        
        return workflow.compile()
    
    def run(self, user_input: str) -> Dict[str, Any]:
        """הפעלת המערכת עם קלט מהמשתמש"""
        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "current_task": user_input,
            "completed_tasks": [],
            "context": {},
            "next_agent": "planner"
        }
        
        try:
            result = self.workflow.invoke(initial_state)
            return result
        except Exception as e:
            return {
                "error": str(e),
                "messages": [AIMessage(content=f"שגיאה: {str(e)}")]
            }

def main():
    """פונקציה ראשית לבדיקה"""
    
    # בדיקה אם יש API KEY
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ חסר ANTHROPIC_API_KEY במשתני הסביבה")
        print("הגדר אותו עם: export ANTHROPIC_API_KEY='your-key-here'")
        return
    
    # יצירת האורקסטרטור
    orchestrator = MultiAgentOrchestrator(api_key)
    
    print("🤖 מערכת הסוכנים מוכנה!")
    print("דוגמה לשימוש:")
    print("orchestrator.run('בנה לי מערכת ניהול משימות בפייתון')")
    
    # דוגמה לרצת בדיקה
    if input("האם להריץ דוגמה? (y/n): ").lower() == 'y':
        result = orchestrator.run("כתוב פונקציה פשוטה לחישוב פיבונאצ'י")
        print("\n📊 תוצאה:")
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()