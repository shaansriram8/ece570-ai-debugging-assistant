# Lovable.dev Prompt: AI-Powered Code Quality & Bug Explanation Assistant

## Project Overview

Build a **TypeScript/React frontend** for an AI-powered code debugging assistant. This is a single-page web application that helps developers and students understand and fix code errors by analyzing source code and error messages using AI models.

## Core Purpose

The application solves a real problem: developers spend too much time interpreting cryptic error messages and manually debugging with low-level logs. This tool provides **instant, structured feedback** that includes:
- A clear root-cause explanation of bugs
- Concrete suggested fixes
- A confidence score (0-100) indicating the quality of the explanation

**Target Users:**
- Junior software engineers
- Students in programming-heavy courses
- Developers who regularly encounter confusing runtime or compile-time errors

## Application Functionality

### User Flow

1. **Input Phase:**
   - User pastes/enters their buggy code into a code editor
   - User pastes/enters the error message or stack trace
   - User optionally selects the programming language (JavaScript, Python, Java, C, etc.)
   - User clicks "Analyze" button

2. **Processing Phase:**
   - Show loading indicator
   - Send request to backend API
   - Display loading state with helpful message (e.g., "Analyzing your code...")

3. **Results Phase:**
   - Display structured results in an organized, readable format
   - Show explanation, suggestion, score, and optional metadata
   - Allow user to analyze another code/error pair

## Required Frontend Components

### 1. Main Layout Component
- Clean, modern single-page application layout
- Header with application title/logo
- Main content area with clear sections
- Footer (optional) with attribution/version info

### 2. Input Form Component
**Purpose:** Capture user inputs (code, error message, optional language)

**Fields:**
- **Code Editor/Textarea:**
  - Multi-line textarea or code editor component
  - Syntax highlighting preferred but not required
  - Placeholder text: "Paste your code here..."
  - Should support code of various lengths (small snippets to larger blocks)
  
- **Error Message Field:**
  - Multi-line textarea for error message/stack trace
  - Placeholder text: "Paste error message or stack trace here..."
  - Required field
  
- **Language Selector (Optional):**
  - Dropdown/select component
  - Options: JavaScript, Python, Java, C, C++, TypeScript, etc.
  - "Auto-detect" option or allow empty
  - Not required but helpful for context
  
- **Analyze Button:**
  - Primary action button
  - Disabled when code or error message is empty
  - Shows loading state during request

### 3. Loading State Component
**Purpose:** Show user that analysis is in progress

**Display:**
- Loading spinner/indicator
- Status message: "Analyzing your code with AI models..."
- Optionally show estimated time or progress (backend latency is ~2-4 seconds typically)
- Should replace or overlay the results area

### 4. Results Display Component
**Purpose:** Present the analysis results in a clear, structured format

**Sections to Display:**
- **Explanation Section:**
  - Card/panel with clear heading "Root Cause Explanation"
  - Display the `explanation` text from API response
  - Format as readable text (not raw JSON)
  - Styled for readability (appropriate font size, spacing)
  
- **Suggestion Section:**
  - Card/panel with heading "Suggested Fix"
  - Display the `suggestion` text from API response
  - Format code snippets (if any) with monospace font
  - Make actionable suggestions stand out
  
- **Score Badge/Indicator:**
  - Visual representation of the `score` (0-100)
  - Use color coding:
    - Green (80-100): High confidence
    - Yellow (50-79): Medium confidence
    - Red (0-49): Low confidence
  - Could be a progress bar, circular indicator, or badge
  - Show numeric score alongside visual
  
- **Optional Fields (if provided by API):**
  - **Severity Badge:** Display `severity` (low/medium/high) with color-coded badge
  - **Bug Type Tag:** Display `bug_type` (e.g., "null reference", "type error") as a tag/chip

### 5. Metadata Display Component (Collapsible/Expandable)
**Purpose:** Show technical details for transparency (can be collapsed by default)

**Display:**
- Collapsible section with heading like "Technical Details" or "Analysis Metadata"
- Show:
  - Models used: List of AI models that analyzed the code
  - Total latency: How long the analysis took (in milliseconds or seconds)
  - Per-model latency: Breakdown of each model's response time
  - Cache status: Whether result came from cache
  - JSON repair status: Whether JSON had to be repaired (technical detail)
  - Backend version: Version info (optional)

**Design:**
- Accordion or collapsible panel
- Can be hidden by default (advanced users can expand)
- Use subtle styling to not distract from main results

### 6. Error State Component
**Purpose:** Handle and display errors gracefully

**Scenarios:**
- Network errors (backend unreachable)
- API errors (500, 400, etc.)
- Timeout errors
- Invalid input errors

**Display:**
- User-friendly error message
- Clear call-to-action (e.g., "Try Again" button)
- Optionally show technical error details in expandable section
- Don't show raw error stack traces to users (too technical)

### 7. Empty State Component
**Purpose:** Initial state when no analysis has been performed

**Display:**
- Welcome message
- Brief instructions on how to use the app
- Example or placeholder showing expected format
- Encourage user to paste their code and error

### 8. "Clear" / "Analyze Another" Button
**Purpose:** Reset form and start fresh analysis

**Placement:**
- Near the Analyze button or in results area
- Clears all input fields
- Resets results display
- Returns to empty state

## Backend API Integration

### API Base URL
- **Development:** `http://localhost:8000`
- **Production:** (Will be set during deployment)
- Make API URL configurable via environment variable

### Endpoints

#### 1. Health Check: `GET /health`
**Purpose:** Check if backend is available before allowing analysis

**Response:**
```json
{
  "status": "healthy",
  "hf_api_reachable": true,
  "models_configured": ["01-ai/Yi-1.5B-Coder", "mistralai/Mistral-7B-Instruct-v0.2"],
  "backend_version": "1.0.0"
}
```

**Usage:** Optional - can call on app load to show backend status

#### 2. Analyze Endpoint: `POST /analyze`
**Purpose:** Main endpoint for code analysis

**Request Body:**
```typescript
{
  code: string;              // Required - source code with bug
  error_message: string;     // Required - error message or stack trace
  language?: string;         // Optional - programming language
}
```

**Response Body:**
```typescript
{
  explanation: string;       // Root-cause explanation
  suggestion: string;        // Concrete suggested fix
  score: number;             // Quality/confidence score (0-100)
  severity?: string;         // Optional - "low" | "medium" | "high"
  bug_type?: string;         // Optional - type of bug
  meta: {
    models_used: string[];                          // AI models used
    per_model_latency_ms: Record<string, number>;  // Latency per model
    total_latency_ms: number;                      // Total latency
    had_repair: boolean;                           // Whether JSON was repaired
    from_cache: boolean;                           // Whether result was cached
    backend_version?: string;                      // Backend version
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid request (missing required fields)
- `500 Internal Server Error`: Backend error (display user-friendly message)
- Network errors: Handle connection failures gracefully

## Design Requirements

### Visual Design
- **Modern, Clean UI:** Professional appearance suitable for developers
- **Readable Typography:** Clear fonts, appropriate sizes
- **Good Contrast:** Ensure text is readable
- **Responsive Design:** Works on desktop, tablet, and mobile
- **Color Scheme:** 
  - Use a clean, developer-friendly color palette
  - Avoid overly bright or distracting colors
  - Ensure accessibility (WCAG AA compliant)

### User Experience
- **Clear Visual Hierarchy:** Most important information (explanation, suggestion) is most prominent
- **Immediate Feedback:** Loading states, button disabled states
- **Error Prevention:** Validate inputs before allowing submit
- **Helpful Placeholders:** Guide users on what to input
- **Progressive Disclosure:** Metadata/details can be hidden initially

### Performance
- **Fast Initial Load:** Optimize bundle size
- **Smooth Transitions:** Loading states, result appearance
- **Efficient API Calls:** Don't spam the backend, handle timeouts

## Technical Requirements

### Technology Stack
- **Framework:** React (via lovable.dev)
- **Language:** TypeScript
- **Styling:** CSS/Tailwind (use lovable.dev's styling system)
- **HTTP Client:** Fetch API or axios for API calls
- **State Management:** React hooks (useState, useEffect)

### Code Quality
- **Type Safety:** Use TypeScript interfaces for API request/response types
- **Error Handling:** Try-catch blocks around API calls
- **Loading States:** Manage loading state properly
- **Form Validation:** Client-side validation before API calls
- **No Core Logic:** Frontend should only display data; all logic is in backend

### Environment Configuration
- Make API base URL configurable:
  ```typescript
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
  ```

## Example User Flow Visualization

```
[Initial State]
┌─────────────────────────────────────┐
│  AI Code Bug Explanation Assistant  │
├─────────────────────────────────────┤
│                                     │
│  Welcome! Paste your code below...  │
│                                     │
│  [Code Editor: Empty]               │
│                                     │
│  [Error Message: Empty]             │
│                                     │
│  Language: [Dropdown: Auto-detect]  │
│                                     │
│  [Analyze Button - Disabled]        │
│                                     │
└─────────────────────────────────────┘

[After User Inputs]
┌─────────────────────────────────────┐
│  AI Code Bug Explanation Assistant  │
├─────────────────────────────────────┤
│  Code:                              │
│  [Code Editor: const arr = ...]     │
│                                     │
│  Error:                             │
│  [Error: TypeError: Cannot read...] │
│                                     │
│  Language: [JavaScript ▼]           │
│                                     │
│  [Analyze Button - Active]          │
│                                     │
└─────────────────────────────────────┘

[Loading State]
┌─────────────────────────────────────┐
│  [Loading Spinner]                  │
│  Analyzing your code with AI...     │
└─────────────────────────────────────┘

[Results Display]
┌─────────────────────────────────────┐
│  ✓ Analysis Complete                │
├─────────────────────────────────────┤
│  Root Cause Explanation             │
│  ┌─────────────────────────────┐   │
│  │ The variable 'arr' is        │   │
│  │ undefined, so calling .map() │   │
│  │ on it throws a TypeError...  │   │
│  └─────────────────────────────┘   │
│                                     │
│  Suggested Fix                      │
│  ┌─────────────────────────────┐   │
│  │ Initialize 'arr' as an empty │   │
│  │ array: const arr = []; ...   │   │
│  └─────────────────────────────┘   │
│                                     │
│  Confidence Score: [85/100] ████   │
│  Severity: [High]  Bug Type: [null]│
│                                     │
│  [Technical Details ▼]              │
│  [Analyze Another]                  │
└─────────────────────────────────────┘
```

## Key Implementation Notes

1. **No Business Logic in Frontend:** All analysis happens in backend. Frontend is purely presentational.

2. **Handle Edge Cases:**
   - Empty inputs
   - Very long code snippets
   - Very long error messages
   - Network failures
   - Slow responses (timeouts)

3. **Accessibility:**
   - Proper form labels
   - Keyboard navigation
   - Screen reader friendly
   - Focus management

4. **Mobile Responsiveness:**
   - Stack inputs vertically on mobile
   - Ensure buttons are tappable
   - Readable text sizes

5. **Code Editor:**
   - Basic textarea is acceptable for MVP
   - Code editor with syntax highlighting is nice-to-have (e.g., CodeMirror, Monaco Editor)

## Success Criteria

The frontend is successful when:
- ✅ Users can easily paste code and error messages
- ✅ Results are displayed clearly and readably
- ✅ Loading and error states are handled gracefully
- ✅ The UI is clean and professional
- ✅ The application works on different screen sizes
- ✅ API integration is stable and handles errors well

---

**Note for Implementation:** This is a prototype for an academic project. Focus on clean, functional UI that demonstrates the core value proposition. Polish is appreciated but functionality is the priority.

