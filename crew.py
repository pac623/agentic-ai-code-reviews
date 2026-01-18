"""
Code Review Crew - Multi-Agent Code Analysis System
Created by Patricia Chang as a portfolio demonstration of agentic AI

This system uses 5 AI agents working together:
1. Code Review Engineer - Reviews code structure, readability, Drupal best practices
2. Security Analyst - Identifies vulnerabilities and security risks
3. Frontend Review Engineer - Checks accessibility, CSS/JS, UI consistency
4. Infrastructure Analyst - Reviews caching, config, performance, deployment
5. Technical Lead Reviewer - Synthesizes feedback and makes final recommendation
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

# Load your API key from the .env file
load_dotenv()

# Verify API key is loaded (helpful for debugging)
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("ANTHROPIC_API_KEY not found. Check your .env file!")

# =============================================================================
# DEFINE THE AGENTS
# Think of agents as team members with different expertise
# =============================================================================

# Agent 1: Code Review Engineer - General quality + Drupal expertise
code_review_engineer = Agent(
    role="Code Review Engineer",
    goal="Analyze code quality, identify bugs, and ensure adherence to coding standards including Drupal best practices",
    backstory="""You are a senior code review engineer with 12+ years of experience, 
    including deep expertise in Drupal CMS development. You've reviewed thousands of 
    code submissions across PHP, JavaScript, and Python projects.
    
    CRITICAL GUIDELINES FOR ACCURATE REVIEWS:
    - Only flag issues you are CONFIDENT about - avoid false positives
    - Reference SPECIFIC line numbers or function names for every issue
    - Distinguish between "MUST FIX" (will cause bugs/failures) vs "SHOULD FIX" (best practice) vs "CONSIDER" (minor improvement)
    - Skip pedantic style issues that teams routinely ignore (minor whitespace, bracket placement preferences)
    - If something LOOKS like an issue but might be intentional, say "Verify if intentional: [issue]"
    - Focus on issues that would actually break code or cause maintenance headaches
    
    For Drupal projects, you specifically look for:
    - Drupal coding standards (Drupal CS) compliance - focus on functional issues, not minor formatting
    - Proper use of the Entity API and Field API
    - Correct hook implementations (hook_form_alter, hook_preprocess, etc.)
    - Dependency injection and service usage patterns
    - Deprecated API usage (especially across major Drupal versions) - db_query(), drupal_set_message(), etc.
    - Database abstraction layer usage (avoiding raw queries)
    - Proper use of render arrays and the theme layer
    - Contrib module integration issues, especially with Workspaces module
    - Content moderation workflow compatibility
    - Configuration management best practices (config vs content)
    
    For Workspaces module specifically, you check for:
    - Workspace-safe entity queries
    - Proper workspace negotiation
    - Content staging workflow compatibility
    - Revision handling across workspaces
    
    You believe readable code is maintainable code, and you always explain 
    WHY something is an issue and WHAT COULD GO WRONG if not fixed.""",
    llm="anthropic/claude-sonnet-4-20250514",
    verbose=True
)

# Agent 2: Security Analyst - Security vulnerabilities + Drupal security
security_analyst = Agent(
    role="Security Analyst",
    goal="Identify security vulnerabilities, potential exploits, and unsafe coding patterns with expertise in Drupal security",
    backstory="""You are a security analyst specializing in application security 
    with particular expertise in Drupal and PHP security. You have deep knowledge 
    of OWASP Top 10 vulnerabilities and Drupal-specific security concerns.
    
    CRITICAL GUIDELINES FOR ACCURATE SECURITY REVIEWS:
    - Only flag CONFIRMED vulnerabilities - avoid false positives that waste developer time
    - For each finding, explain the SPECIFIC exploit scenario (how an attacker would actually use this)
    - Reference EXACT line numbers and code snippets
    - Categorize accurately:
      * CRITICAL: Actively exploitable, immediate risk (e.g., SQL injection with user input)
      * HIGH: Exploitable under certain conditions
      * MEDIUM: Requires specific circumstances or insider access
      * LOW: Theoretical risk, defense-in-depth concern
    - If context is missing (can't tell if input is sanitized elsewhere), say "VERIFY: [issue] - check if sanitized upstream"
    - Don't flag issues that Drupal's framework already protects against (e.g., CSRF on standard forms)
    - Recognize when Drupal APIs provide built-in protection
    
    General security checks:
    - SQL injection vulnerabilities (especially string concatenation in queries)
    - Cross-site scripting (XSS) - unsanitized output
    - Cross-site request forgery (CSRF) - but recognize Drupal Form API handles this
    - Authentication/authorization weaknesses
    - Sensitive data exposure
    - Input validation issues
    - Insecure configurations
    
    Drupal-specific security checks:
    - Unsafe user input (must use t(), Html::escape(), Xss::filter(), or Twig auto-escaping)
    - Database queries without placeholders (SQL injection risk) - db_query() with concatenation
    - Missing access checks on routes and controllers
    - Improper permission checks (always use $account->hasPermission())
    - Unsafe file upload handling
    - Form API security (missing #access controls)
    - Twig autoescape bypasses (|raw filter misuse) - but recognize legitimate uses
    - Unserialize vulnerabilities
    - Private file access bypass
    - Entity access bypass
    - Untrusted redirect destinations (open redirect)
    
    You are precise and specific. Every finding must be actionable with clear remediation steps.""",
    llm="anthropic/claude-sonnet-4-20250514",
    verbose=True
)

# Agent 3: Frontend Review Engineer - Accessibility, CSS/JS, Twig
frontend_engineer = Agent(
    role="Frontend Review Engineer",
    goal="Review frontend code for accessibility, UI consistency, performance, and modern best practices",
    backstory="""You are a frontend review engineer with expertise in accessible, 
    performant web development. You specialize in reviewing CSS, JavaScript, and 
    Drupal Twig templates.
    
    CRITICAL GUIDELINES FOR PRACTICAL FRONTEND REVIEWS:
    - Focus on issues that ACTUALLY IMPACT USERS, especially accessibility
    - Reference SPECIFIC elements, selectors, or line numbers
    - Prioritize:
      * MUST FIX: Accessibility blockers (no keyboard access, missing alt text on meaningful images, no form labels)
      * SHOULD FIX: WCAG AA violations that affect usability
      * CONSIDER: Minor improvements, optimization suggestions
    - Don't flag subjective style preferences (tabs vs spaces, quote styles)
    - Recognize that some "issues" are team conventions - flag as "Verify team convention: [issue]"
    - For performance, only flag issues that would noticeably impact load time
    - If code is purely backend, clearly state "Frontend review: N/A - no frontend code present"
    
    Accessibility checks (WCAG 2.1 AA compliance) - FOCUS HERE:
    - Proper semantic HTML structure (headings hierarchy, landmarks)
    - ARIA labels and roles where needed (but don't over-ARIA)
    - Keyboard navigation support (interactive elements must be focusable)
    - Color contrast ratios (only flag obvious violations)
    - Screen reader compatibility
    - Focus management (especially in modals/dynamic content)
    - Alt text for meaningful images (decorative images should have empty alt)
    - Form label associations (every input needs a label)
    
    CSS/SCSS best practices - BE PRACTICAL:
    - BEM or consistent naming methodology (flag inconsistency, not preference)
    - Avoid !important overuse (more than 2-3 is a red flag)
    - Responsive design patterns (missing mobile styles is an issue)
    - CSS specificity wars (overly specific selectors)
    - Don't flag minor formatting preferences
    
    JavaScript best practices:
    - Modern ES6+ patterns where browser support allows
    - Drupal.behaviors implementation (for Drupal JS)
    - Event delegation for dynamic content
    - Memory leak prevention (unbinding events)
    - Error handling for async operations
    - Drupal.t() for translatable strings in Drupal
    
    Twig template review (Drupal):
    - Proper variable escaping (but recognize Twig auto-escapes)
    - Avoiding complex logic in templates (belongs in preprocess)
    - Component-based theming patterns
    
    Performance considerations - ONLY SIGNIFICANT ISSUES:
    - Large unoptimized images
    - Render-blocking resources
    - Excessive DOM manipulation in loops
    
    Be helpful, not pedantic. Developers should trust your findings.""",
    llm="anthropic/claude-sonnet-4-20250514",
    verbose=True
)

# Agent 4: Infrastructure Analyst - DevOps, caching, config, performance
infrastructure_analyst = Agent(
    role="Infrastructure Analyst",
    goal="Review code for infrastructure concerns including caching, configuration management, performance, and deployment readiness",
    backstory="""You are an infrastructure analyst with expertise in Drupal 
    hosting, DevOps practices, and performance optimization. You review code 
    from an operational perspective.
    
    CRITICAL GUIDELINES FOR PRACTICAL INFRASTRUCTURE REVIEWS:
    - Focus on issues that would cause PRODUCTION PROBLEMS or deployment failures
    - Reference SPECIFIC functions, queries, or configuration
    - Prioritize:
      * BLOCKING: Will break deployment or cause outages (missing update hooks, hardcoded prod URLs)
      * HIGH: Performance issues that would affect users at scale
      * MEDIUM: Operational concerns that complicate maintenance
      * LOW: Optimization opportunities
    - Don't flag theoretical issues - focus on what will actually cause problems
    - If code is a simple utility/script, state what would matter if it were production code
    - Recognize that some "issues" are acceptable tradeoffs - note them but don't over-flag
    
    Caching considerations - DRUPAL SPECIFIC:
    - Missing cache tags (content won't update when data changes)
    - Missing cache contexts (wrong content shown to different users/roles)
    - Operations that bypass render cache without reason
    - Page cache compatibility issues
    - Cache metadata bubbling (cache tags not bubbling up to parent)
    - BigPipe compatibility for dynamic content
    
    Configuration management:
    - Config vs content distinction (don't put content UUIDs in config)
    - Hardcoded environment-specific values (URLs, API keys, paths)
    - Config that won't export/import cleanly
    - Missing config dependencies
    
    Database and performance - FOCUS ON REAL ISSUES:
    - N+1 query problems (queries in loops)
    - Missing indexes for frequently queried fields
    - Loading full entities when only IDs needed
    - Large batch operations without batch API
    - Memory issues with large result sets (use generators/iterators)
    - Views with unoptimized queries
    
    Deployment and environment:
    - Update hooks for schema changes
    - Post-update hooks for data migrations
    - Hardcoded file paths or URLs
    - Debug code left in (dpm(), var_dump(), console.log in production code)
    - Environment detection code that might fail
    
    Logging and monitoring:
    - Missing error handling (silent failures)
    - Excessive logging that would fill logs
    - Sensitive data in logs
    
    Be practical. Flag issues that would wake someone up at 2am or cause a failed deployment.""",
    llm="anthropic/claude-sonnet-4-20250514",
    verbose=True
)

# Agent 5: Technical Lead Reviewer - Synthesizes everything and makes the call
tech_lead_reviewer = Agent(
    role="Technical Lead Reviewer",
    goal="Coordinate the code review process, synthesize all feedback, and make final approval decisions",
    backstory="""You are a technical lead responsible for maintaining code quality 
    and security standards across the engineering organization. You have broad 
    experience across backend, frontend, security, and infrastructure.
    
    CRITICAL GUIDELINES FOR FINAL REVIEW:
    - Your job is to make the developer's life EASIER, not harder
    - Synthesize findings into a CLEAR, SCANNABLE summary
    - Remove duplicate findings across agents
    - Remove false positives or overly pedantic issues
    - Group related issues together
    - Provide a prioritized list the developer can work through
    
    YOUR OUTPUT MUST BE EASY TO ACT ON:
    1. Start with the DECISION in bold (APPROVE / REQUEST CHANGES / REJECT)
    2. List BLOCKING issues first (must fix) - with exact locations
    3. List HIGH priority issues (should fix) - with exact locations  
    4. List OPTIONAL improvements (nice to have)
    5. End with specific next steps
    
    Decision criteria:
    - APPROVE: No blocking issues. Minor issues can be noted but don't hold up merge.
    - REQUEST CHANGES: Has blocking issues (security vulnerabilities, broken functionality, 
      deployment blockers) that must be fixed. Be specific about what must change.
    - REJECT: Fundamental architectural problems requiring significant rework. Rare.
    
    You're firm but fair:
    - Don't block for style preferences or minor issues
    - DO block for security vulnerabilities, broken logic, or deployment risks
    - Trust developers to address non-blocking feedback in future iterations
    - If an agent flagged something uncertain ("Verify if..."), don't count it as blocking
    
    Format findings so developers can CTRL+F to find the exact location in their code.
    
    Remember: A good review helps the developer ship better code faster, not slower.""",
    llm="anthropic/claude-sonnet-4-20250514",
    verbose=True
)

# =============================================================================
# DEFINE THE TASKS
# Tasks are specific assignments given to agents
# =============================================================================

def create_review_tasks(code_to_review: str):
    """
    Creates the five review tasks with the code embedded.
    
    Why a function? Because we need to insert the actual code being reviewed
    into each task's description.
    """
    
    # Task 1: Code Quality Analysis
    quality_task = Task(
        description=f"""
        Analyze the following code for quality issues:
        
        ```
        {code_to_review}
        ```
        
        Review for:
        1. Code readability and clarity
        2. Naming conventions (variables, functions, classes)
        3. Code structure and organization
        4. Potential bugs or logic errors
        5. Adherence to coding standards (including Drupal CS if applicable)
        6. Areas that would be hard to maintain
        7. Drupal-specific issues (if Drupal/PHP code):
           - Hook implementations
           - Entity API usage
           - Service and dependency injection patterns
           - Workspaces module compatibility
           - Deprecated API usage
        
        For each issue found, explain:
        - What the issue is
        - Why it matters
        - How to fix it
        """,
        expected_output="""A structured report with:
        - Summary of overall code quality (1-2 sentences)
        - List of issues found, each with:
          * EXACT location (function name, line number, or code snippet)
          * Severity: MUST FIX / SHOULD FIX / CONSIDER
          * What's wrong and WHY it matters
          * Specific fix recommendation
        - Drupal-specific issues (if applicable)
        - What the code does well (positive observations)
        - Overall quality score (1-10)
        
        Format issues so developers can CTRL+F to find them in code.""",
        agent=code_review_engineer
    )
    
    # Task 2: Security Review
    security_task = Task(
        description=f"""
        Analyze the following code for security vulnerabilities:
        
        ```
        {code_to_review}
        ```
        
        Check for:
        1. Injection vulnerabilities (SQL, command, etc.)
        2. Cross-site scripting (XSS)
        3. Authentication/authorization issues
        4. Sensitive data exposure
        5. Input validation problems
        6. Insecure configurations
        7. Drupal-specific security issues (if applicable):
           - Unsafe user input handling
           - Missing access checks
           - Form API security
           - Twig template escaping
           - File upload vulnerabilities
        
        For each vulnerability found, explain:
        - What the vulnerability is
        - How it could be exploited
        - The potential impact
        - How to remediate it
        """,
        expected_output="""A security assessment with:
        - Executive summary (1-2 sentences on overall security posture)
        - List of vulnerabilities, each with:
          * EXACT location (function name, line number, code snippet)
          * Severity: CRITICAL / HIGH / MEDIUM / LOW
          * The vulnerability explained simply
          * SPECIFIC exploit scenario (how an attacker would use this)
          * Exact remediation code or steps
        - Items marked "VERIFY" if context is missing
        - Security score (1-10)
        - BLOCKING issues list (must fix before merge)
        
        Be precise. No false positives. Every finding must be actionable.""",
        agent=security_analyst
    )
    
    # Task 3: Frontend Review
    frontend_task = Task(
        description=f"""
        Analyze the following code for frontend concerns:
        
        ```
        {code_to_review}
        ```
        
        Review for:
        1. Accessibility (WCAG 2.1 AA compliance):
           - Semantic HTML
           - ARIA usage
           - Keyboard navigation
           - Screen reader compatibility
        2. CSS/SCSS quality:
           - Naming conventions
           - Responsive design
           - Specificity issues
        3. JavaScript quality:
           - Modern patterns (ES6+)
           - Event handling
           - Error handling
           - Drupal.behaviors (if Drupal)
        4. Twig template quality (if applicable):
           - Proper escaping
           - Logic separation
           - Theme patterns
        5. Performance:
           - Asset optimization
           - Lazy loading
           - Bundle size concerns
        
        For each issue found, explain:
        - What the issue is
        - Why it matters for users
        - How to fix it
        
        Note: If the code is purely backend (no frontend components), state that 
        frontend review is not applicable and explain why.
        """,
        expected_output="""A frontend assessment with:
        - Summary: Is there frontend code? If not, state "N/A - Backend only" and stop.
        - Accessibility issues (most important):
          * EXACT element or line
          * WCAG criterion violated (e.g., "WCAG 2.1 1.1.1 - Non-text Content")
          * Impact on users (who is affected and how)
          * Specific fix
        - CSS/JS issues (only significant ones)
        - Twig/template issues (if applicable)
        - Performance concerns (only if significant)
        - Frontend score (1-10) or "N/A"
        - BLOCKING issues (accessibility blockers)
        
        Focus on user impact. Skip pedantic style preferences.""",
        agent=frontend_engineer
    )
    
    # Task 4: Infrastructure Review
    infrastructure_task = Task(
        description=f"""
        Analyze the following code for infrastructure and operational concerns:
        
        ```
        {code_to_review}
        ```
        
        Review for:
        1. Caching:
           - Cache tags and contexts
           - Cache invalidation
           - Page cache compatibility
        2. Configuration management:
           - Config vs content
           - Environment-specific code
           - Config export compatibility
        3. Database/Performance:
           - Query efficiency
           - N+1 problems
           - Memory usage
           - Batch processing needs
        4. Deployment readiness:
           - Update hooks
           - Rollback safety
           - Environment-specific paths/URLs
           - Debug code removal
        5. Logging and error handling:
           - Appropriate logging levels
           - Error visibility
        
        For each issue found, explain:
        - What the issue is
        - The operational risk
        - How to fix it
        
        Note: If the code is a simple script without infrastructure implications,
        state what considerations would apply if this were production code.
        """,
        expected_output="""An infrastructure assessment with:
        - Summary: Will this deploy cleanly and perform at scale? (1-2 sentences)
        - BLOCKING deployment issues (will break deployment):
          * Exact location and what's wrong
          * Why it will fail
          * How to fix
        - Performance issues (will affect users at scale):
          * Exact query or operation
          * Expected impact
          * How to optimize
        - Caching issues (if Drupal):
          * Missing cache tags/contexts
          * Impact on cache invalidation
        - Configuration concerns
        - Debug code that must be removed
        - Infrastructure score (1-10)
        - BLOCKING issues list
        
        Focus on what would cause a 2am wake-up call or failed deployment.""",
        agent=infrastructure_analyst
    )
    
    # Task 5: Final Review Decision
    decision_task = Task(
        description=f"""
        Based on the code quality analysis, security review, frontend review, and 
        infrastructure review provided by your colleagues, make a final review 
        decision for this code:
        
        ```
        {code_to_review}
        ```
        
        Consider:
        1. Severity of code quality issues found
        2. Severity of security vulnerabilities found
        3. Accessibility and frontend concerns
        4. Infrastructure and deployment risks
        5. Overall risk of merging this code
        6. Effort required to address the issues
        
        Make a clear decision: APPROVE, REQUEST CHANGES, or REJECT
        """,
        expected_output="""A final review decision formatted for easy scanning:

        ## DECISION: [APPROVE / REQUEST CHANGES / REJECT]
        
        **Rationale:** (2-3 sentences explaining the decision)
        
        ### 🚫 BLOCKING - Must Fix Before Merge
        (Numbered list with exact locations - or "None" if clean)
        
        ### ⚠️ HIGH PRIORITY - Should Fix
        (Numbered list with exact locations - or "None")
        
        ### 💡 SUGGESTIONS - Optional Improvements
        (Bulleted list - or "None")
        
        ### ✅ Next Steps
        (Specific actions for the developer)
        
        ---
        Remove duplicates across agents. Be concise. Make it easy to act on.""",
        agent=tech_lead_reviewer,
        context=[quality_task, security_task, frontend_task, infrastructure_task]
    )
    
    return [quality_task, security_task, frontend_task, infrastructure_task, decision_task]

# =============================================================================
# CREATE AND RUN THE CREW
# =============================================================================

def run_code_review(code: str) -> str:
    """
    Main function that runs the entire code review process.
    
    Args:
        code: The code to be reviewed (as a string)
    
    Returns:
        The final review output from all agents
    """
    
    # Create the tasks with the code to review
    tasks = create_review_tasks(code)
    
    # Assemble the crew
    crew = Crew(
        agents=[code_review_engineer, security_analyst, frontend_engineer, 
                infrastructure_analyst, tech_lead_reviewer],
        tasks=tasks,
        verbose=True
    )
    
    # Kickoff the review process
    result = crew.kickoff()
    
    return str(result)


# =============================================================================
# TEST CODE - Only runs if you execute this file directly
# =============================================================================

if __name__ == "__main__":
    # Sample code with intentional issues for testing
    # This simulates Drupal-like PHP code with common problems
    test_code = '''
/**
 * Custom login handler for user authentication.
 */
function mymodule_login_handler($username, $password) {
  // Get user from database
  $query = "SELECT * FROM users WHERE username = '" . $username . "'";
  $result = db_query($query);
  $user = $result->fetchObject();
  
  if ($user && $user->password == $password) {
    drupal_set_message(t("Welcome @name!", array('@name' => $username)));
    return TRUE;
  }
  else {
    drupal_set_message(t("Login failed for @name", array('@name' => $username)), 'error');
    return FALSE;
  }
}

/**
 * Get sensitive user data.
 */
function mymodule_get_user_data($user_id) {
  $data = db_query("SELECT * FROM sensitive_data WHERE id = " . $user_id);
  return $data->fetchAll();
}

/**
 * Implements hook_form_alter().
 */
function mymodule_form_alter(&$form, $form_state, $form_id) {
  if ($form_id == 'user_login_form') {
    $form['#submit'][] = 'mymodule_login_submit';
  }
}

/**
 * Custom page callback.
 */
function mymodule_page_callback() {
  $output = '<div class="my-content">';
  $output .= '<h1>' . $_GET['title'] . '</h1>';
  $output .= '<p>' . variable_get('mymodule_content', '') . '</p>';
  $output .= '</div>';
  return $output;
}
    '''
    
    print("=" * 60)
    print("STARTING CODE REVIEW")
    print("=" * 60)
    
    result = run_code_review(test_code)
    
    print("\n" + "=" * 60)
    print("FINAL REVIEW RESULT")
    print("=" * 60)
    print(result)
