"""Input validation utilities to ensure requests are code debugging related."""
import re
from typing import Tuple, Optional


def looks_like_code(text: str) -> bool:
    """
    Check if text looks like source code.
    
    Heuristics:
    - Contains common code patterns (operators, brackets, keywords)
    - Has code-like structure (indentation, semicolons, etc.)
    - Not just plain English questions
    """
    if not text or len(text.strip()) < 3:
        return False
    
    # Common code patterns
    code_indicators = [
        r'[{}()\[\]]',  # Brackets
        r'[=+\-*/%<>!&|]',  # Operators
        r'[;:]',  # Statement terminators
        r'\b(function|def|class|const|let|var|if|for|while|return|import|from)\b',  # Keywords
        r'\.\w+\s*\(',  # Method calls
        r'#.*|//.*|/\*.*\*/',  # Comments
    ]
    
    # Count how many code indicators are present
    matches = sum(1 for pattern in code_indicators if re.search(pattern, text, re.IGNORECASE | re.MULTILINE))
    
    # If 2+ indicators, likely code
    if matches >= 2:
        return True
    
    # Check for common question patterns (NOT code)
    question_patterns = [
        r'^(what|where|when|who|why|how)\s+',
        r'\?$',  # Ends with question mark
        r'^(tell me|explain|describe|what is|what are)',
    ]
    
    if any(re.search(pattern, text.strip(), re.IGNORECASE) for pattern in question_patterns):
        # If it looks like a question and has few code indicators, it's probably not code
        if matches < 2:
            return False
    
    # If it has at least one code indicator, consider it code
    # Also allow very short snippets (might be minimal test cases)
    if len(text.strip()) <= 10:
        return True  # Very short - assume it's code
    
    return matches >= 1


def looks_like_error_message(text: str) -> bool:
    """
    Check if text looks like an error message or stack trace.
    
    Heuristics:
    - Contains error keywords (Error, Exception, Traceback, etc.)
    - Has stack trace format (file paths, line numbers)
    - Contains technical error terminology
    - Short error messages (like "Error", "TypeError") are also acceptable
    """
    if not text or len(text.strip()) < 1:
        return False
    
    # Very short error messages (1-2 words) are acceptable
    if len(text.strip()) <= 20:
        return True
    
    # Error message indicators
    error_indicators = [
        r'\b(Error|Exception|Traceback|Warning|Fatal|SyntaxError|TypeError|ReferenceError|RuntimeError)\b',
        r'at\s+\w+\.\w+\([^)]+\)',  # Stack trace format
        r'line\s+\d+',  # Line numbers
        r'File\s+["\']',  # File paths
        r'^\s*at\s+',  # Stack trace "at" lines
        r'^\s*File\s+',  # Stack trace "File" lines
        r'^\s*Traceback',  # Python traceback
        r'is not defined|is not a function|Cannot read|Cannot access',  # Common error phrases
    ]
    
    # If any error indicator is present, it's likely an error message
    return any(re.search(pattern, text, re.IGNORECASE | re.MULTILINE) for pattern in error_indicators)


def validate_debugging_request(code: str, error_message: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that a request is actually a code debugging request.
    
    Returns:
        (is_valid, error_message)
        - is_valid: True if request is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    # Check if code looks like actual code
    # Be lenient - allow very short code snippets (might be minimal test cases)
    if len(code.strip()) < 2:
        return False, "The 'code' field is too short. Please provide actual code with the bug."
    
    if not looks_like_code(code):
        # Check if it's clearly a question
        question_patterns = [
            r'^(what|where|when|who|why|how)\s+',
            r'^(tell me|explain|describe|what is|what are)',
        ]
        if any(re.search(pattern, code.strip(), re.IGNORECASE) for pattern in question_patterns):
            return False, "This service is for debugging code errors only. Please provide actual code, not general questions."
        return False, "The 'code' field does not appear to contain source code. Please provide actual code with the bug."
    
    # Check if error_message is "N/A" or similar - warn but allow
    error_upper = error_message.upper().strip()
    if error_upper in ["N/A", "NA", "NONE", ""]:
        # Allow N/A but note that analysis may be limited
        pass  # Continue validation
    elif not looks_like_error_message(error_message):
        # Error message might be optional or in a different format
        # But if it's clearly a general question, reject it
        if looks_like_code(error_message):
            # If error_message looks like code, it might be a mistake
            return False, "The 'error_message' field should contain an error message or stack trace, not code."
        
        # If it's a plain question (and not short), reject it
        if len(error_message.strip()) > 20:  # Only check longer messages
            question_patterns = [
                r'^(what|where|when|who|why|how)\s+',
                r'^(tell me|explain|describe|what is|what are)',
            ]
            if any(re.search(pattern, error_message.strip(), re.IGNORECASE) for pattern in question_patterns):
                return False, "This service is for debugging code errors only. Please provide code and an error message, not general questions."
    
    return True, None

