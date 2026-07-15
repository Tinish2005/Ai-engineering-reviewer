# AI Engineering Review Platform

An MCP-powered AI Engineering Review Platform that performs multi-language code analysis using deterministic engineering checks and AI-powered reasoning.

The platform evaluates code quality across security, complexity, maintainability, company standards, and engineering best practices before generating actionable recommendations, engineering scores, refactor suggestions, review history, and exportable reports.

---

## Features

### Engineering Analysis

- Engineering Score (0–100)
- Security Analysis
- Complexity Analysis
- Maintainability Analysis
- Company Rule Validation
- AI Engineering Reasoning

### Multi-Language Support

- Python
- Java
- C
- C++

### Security Review

- Dangerous System Call Detection
- Unsafe Deserialization Detection
- Command Execution Detection
- Security Rule Validation

### Complexity Analysis

- Cyclomatic Complexity
- Cognitive Complexity
- Function-Level Analysis
- Complexity-Based Recommendations

### Maintainability Analysis

- Missing Documentation Detection
- Long Function Detection
- Excessive Parameter Detection

### AI Features

- AI Review Summary
- Priority Issue Detection
- Risk-Based Recommendations
- AI Refactor Generation

### Reporting

- Review History Tracking
- PDF Export
- JSON Export
- Markdown Export

### Frontend Experience

- React Dashboard
- Monaco Code Editor
- Dynamic A2UI Rendering
- Interactive History Charts

---

## Architecture

```text
React Frontend
      ↓
Flask Backend
      ↓
MCP Client
      ↓
MCP Server
      ↓
Engineering Analysis Tools
      ↓
Gemini Reasoning Engine
```

### MCP Role

MCP acts as the orchestration layer between the application and engineering analysis tools.

Instead of directly coupling Flask to every analysis module, the platform exposes reusable engineering-review capabilities through MCP tools.

This enables multiple clients to reuse the same review engine without duplicating logic.

---

## Technology Stack

### Frontend

- React
- Vite
- Monaco Editor
- Axios
- Recharts

### Backend

- Flask
- Python

### AI Layer

- Google Gemini

### Protocol Layer

- MCP (Model Context Protocol)

### Analysis Engine

- AST-Based Analysis
- Deterministic Security Scanning
- Complexity Analysis
- Company Rule Engine
- Engineering Score Engine

---

## Example Workflow

```text
Paste Code
      ↓
Run Engineering Review
      ↓
Security Analysis
Complexity Analysis
Maintainability Analysis
Company Rules
      ↓
Engineering Score
      ↓
AI Reasoning
      ↓
Generate Refactor
      ↓
Export Report
```

---

## Export Options

- PDF Export
- JSON Export
- Markdown Export

---

## Review History

The platform stores review history and visualizes engineering score progression through interactive charts.

---

## Refactor Generation

The platform generates improved code suggestions using AI-powered refactoring recommendations.

---

## How To Run

### Backend

```bash
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Project Highlights

- MCP-first Architecture
- Multi-Language Review Engine
- Deterministic Engineering Analysis
- AI Reasoning Layer
- Interactive React Dashboard
- Engineering Score System
- Refactor Generation
- History Tracking
- Exportable Reports

---

## Future Enhancements

- Repository-Level Code Reviews
- Multi-File Analysis
- IDE Integrations
- Team Dashboards
- Custom Rule Management

---

## Author

Tinish

AI Engineering Review Platform  
MCP-Powered Engineering Intelligence
