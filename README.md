# 🔍 AI Code Review Crew

A multi-agent AI system that performs automated code reviews using five specialized AI agents working collaboratively. Built with deep expertise in **Drupal CMS** development patterns and web development best practices.

**Built by [Patricia Chang](https://www.linkedin.com/in/patriciachang23)** — Senior Project Manager & AI Solutions Architect

![Python](https://img.shields.io/badge/Python-3.12+-blue)
![CrewAI](https://img.shields.io/badge/CrewAI-Framework-green)
![Claude](https://img.shields.io/badge/LLM-Claude_Sonnet-orange)
![Drupal](https://img.shields.io/badge/Expertise-Drupal_CMS-blue)

---

## 📋 Table of Contents

- [What This Project Demonstrates](#-what-this-project-demonstrates)
- [The 5-Agent Team](#-the-5-agent-team)
- [How It Works](#-how-it-works)
- [This Prototype vs Production Integration](#-this-prototype-vs-production-integration)
- [Quick Start](#-quick-start)
- [Technical Deep Dive](#-technical-deep-dive)
- [Sample Output](#-sample-output)
- [About the Creator](#-about-the-creator)

---

## 🎯 What This Project Demonstrates

### Agentic AI Capabilities
- **Multi-Agent Orchestration**: Five specialized AI agents collaborating on a complex task
- **Role-Based Expertise**: Each agent has distinct knowledge and review criteria
- **Context Passing**: Agents build on each other's findings
- **Synthesized Decision-Making**: Final agent consolidates all feedback into actionable output

### Practical Application
- **Real Developer Workflow Problem**: Code review is time-consuming and inconsistent
- **Human-in-the-Loop Design**: Augments human reviewers, doesn't replace them
- **Actionable Output**: Specific line numbers, clear severity levels, exact fixes
- **Low False Positives**: Agents are tuned to avoid noise that wastes developer time

### Domain Expertise
- **Drupal CMS**: Coding standards, security patterns, Entity API, Workspaces module
- **Web Security**: OWASP Top 10, Drupal-specific vulnerabilities
- **Frontend/Accessibility**: WCAG 2.1 AA compliance, CSS/JS best practices
- **Infrastructure**: Caching, configuration management, deployment readiness

---

## 🤖 The 5-Agent Team

| Agent | Role | Focus Area |
|-------|------|------------|
| 🎯 **Code Review Engineer** | Senior Developer | Code quality, Drupal coding standards, deprecated APIs, Workspaces compatibility |
| 🔒 **Security Analyst** | AppSec Engineer | SQL injection, XSS, access control, Drupal Form API security |
| 🎨 **Frontend Review Engineer** | UI/UX Developer | WCAG 2.1 accessibility, CSS/JS patterns, Twig templates |
| ⚙️ **Infrastructure Analyst** | DevOps Engineer | Caching (tags/contexts), config management, performance, deployment |
| 👤 **Technical Lead Reviewer** | Tech Lead | Synthesizes all findings, removes duplicates, prioritizes, makes final decision |

### How They Work Together

```
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   Code Review    │  │    Security      │  │    Frontend      │  │  Infrastructure  │
│    Engineer      │  │    Analyst       │  │    Engineer      │  │    Analyst       │
│                  │  │                  │  │                  │  │                  │
│  • Code quality  │  │  • SQL injection │  │  • Accessibility │  │  • Caching       │
│  • Drupal CS     │  │  • XSS/CSRF      │  │  • WCAG 2.1 AA   │  │  • Config mgmt   │
│  • Deprecated    │  │  • Access checks │  │  • CSS/JS        │  │  • Performance   │
│    APIs          │  │  • Form security │  │  • Twig          │  │  • Deployment    │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         │                     │                     │                     │
         └─────────────────────┴─────────────────────┴─────────────────────┘
                                          │
                                          ▼
                            ┌──────────────────────────┐
                            │  Technical Lead Reviewer │
                            │                          │
                            │  • Removes duplicates    │
                            │  • Filters false +       │
                            │  • Prioritizes issues    │
                            │  • Makes final decision  │
                            └────────────┬─────────────┘
                                         │
                                         ▼
                            ┌──────────────────────────┐
                            │     FINAL DECISION       │
                            │                          │
                            │  ✅ APPROVE              │
                            │  🔄 REQUEST CHANGES      │
                            │  ❌ REJECT               │
                            └──────────────────────────┘
```

---

## 🔄 How It Works

### The Review Process

1. **Developer submits code** → Paste code into the web interface
2. **Agents analyze in parallel** → Each agent reviews from their expertise
3. **Findings are passed to Lead** → Technical Lead receives all reports
4. **Lead synthesizes and prioritizes** → Duplicates removed, issues ranked
5. **Developer receives actionable report** → Clear list of what to fix

### Output Format (Designed for Developers)

The final output is scannable and actionable:

```
## DECISION: REQUEST CHANGES

**Rationale:** Critical SQL injection vulnerability in login handler. 
Security issues must be resolved before merge.

### 🚫 BLOCKING - Must Fix Before Merge
1. `mymodule_login_handler()` line 4: SQL injection via string concatenation
2. `mymodule_page_callback()` line 23: XSS via unsanitized $_GET['title']

### ⚠️ HIGH PRIORITY - Should Fix
1. `mymodule_login_handler()`: Uses deprecated db_query() — migrate to database service
2. Missing cache tags on rendered output

### 💡 SUGGESTIONS - Optional Improvements
- Consider using Drupal's built-in authentication service
- Add type hints for better IDE support

### ✅ Next Steps
1. Fix the two SQL injection issues using parameterized queries
2. Sanitize user input with Html::escape() or Xss::filter()
3. Run security review again after fixes
```

---

## 🏭 This Prototype vs Production Integration

### What This Prototype Is

This is a **proof of concept** demonstrating the AI review logic via a web interface. Developers paste code manually and receive a review.

**Best for:**
- Demonstrating the technology
- Testing agent configurations
- Reviewing code snippets outside of Git workflow
- Learning and experimentation

### How It Would Work in Production

In a real development team, this would integrate directly into the **GitHub Pull Request workflow** — no extra steps for developers.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  DEVELOPER'S NORMAL WORKFLOW (No Changes Required)                          │
└─────────────────────────────────────────────────────────────────────────────┘

    1. Developer works on Jira ticket (PROJ-123)
                            │
                            ▼
    2. Creates branch: feature/PROJ-123-user-login
                            │
                            ▼
    3. Writes code, commits, pushes
                            │
                            ▼
    4. Opens Pull Request in GitHub
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  AUTOMATED (Happens Without Developer Action)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   GitHub Action Triggers:                                                   │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  • Detects new/updated PR                                           │   │
│   │  • Extracts changed files (git diff)                                │   │
│   │  • Sends code to AI Code Review Crew                                │   │
│   │  • Receives structured review                                       │   │
│   │  • Posts review as PR comment                                       │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
    5. Developer sees AI review comments on their PR
       (alongside linting, tests, etc.)
                            │
                            ▼
    6. Human reviewer focuses on architecture & logic
       (AI already caught the obvious stuff)
                            │
                            ▼
    7. Approved & merged
```

### Production Integration Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| **GitHub Action** | Triggers on PR open/update | YAML workflow file |
| **Code Extractor** | Gets changed files from PR | GitHub API |
| **AI Review Service** | Runs the 5-agent crew | This project (hosted) |
| **Comment Poster** | Adds review to PR | GitHub API |
| **Jira Linker** (optional) | Links findings to ticket | Jira API |

### Benefits of Production Integration

| For Developers | For Reviewers | For the Team |
|----------------|---------------|--------------|
| No workflow change | Focus on high-level concerns | Consistent review quality |
| Instant feedback | AI catches obvious issues | Faster PR turnaround |
| Clear fix locations | Less repetitive feedback | Knowledge captured in agents |
| Learn patterns over time | Review more PRs in less time | Reduced security incidents |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher (3.12 recommended)
- Anthropic API key ([get one here](https://console.anthropic.com/))

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/agentic-ai-code-reviews.git
cd agentic-ai-code-reviews

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install crewai python-dotenv streamlit anthropic

# Set up your API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Run the Web Interface

```bash
streamlit run app.py
```

Opens in browser at http://localhost:8501

### Run from Command Line

```bash
python crew.py
```

Runs review on built-in test code and outputs to terminal.

---

## 🧠 Technical Deep Dive

### Agent Design Principles

Each agent is configured with specific guidelines to ensure **accuracy** and **usefulness**:

```python
# Example: Security Analyst is tuned to avoid false positives
security_analyst = Agent(
    role="Security Analyst",
    backstory="""
    CRITICAL GUIDELINES FOR ACCURATE SECURITY REVIEWS:
    - Only flag CONFIRMED vulnerabilities - avoid false positives
    - For each finding, explain the SPECIFIC exploit scenario
    - Reference EXACT line numbers and code snippets
    - If context is missing, say "VERIFY: [issue]" instead of flagging
    - Don't flag issues that Drupal's framework already protects against
    ...
    """
)
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **5 specialized agents** | Better than 1 generalist — each agent has deep expertise |
| **Severity levels** | MUST FIX / SHOULD FIX / CONSIDER — clear prioritization |
| **"VERIFY" markers** | Uncertain items don't block, but get flagged for human check |
| **Exact locations** | Function names, line numbers — developers can CTRL+F |
| **Lead synthesizes** | Removes duplicates, filters noise, presents clean output |

### Context Passing

The Technical Lead receives all other agents' findings via CrewAI's `context` parameter:

```python
decision_task = Task(
    description="Based on all reviews, make a final decision...",
    agent=tech_lead_reviewer,
    context=[quality_task, security_task, frontend_task, infrastructure_task]
)
```

### Why Claude Sonnet?

- **Strong reasoning** for nuanced code analysis
- **Reliable structured output** for consistent formatting
- **Cost-effective** for multi-agent workflows
- **Good security knowledge** for vulnerability detection

---

## 📸 Sample Output

### Input: Vulnerable Drupal Code

```php
function mymodule_page_callback() {
  $output = '<h1>' . $_GET['title'] . '</h1>';
  return $output;
}
```

### Output: AI Review

```
## DECISION: REQUEST CHANGES

**Rationale:** Critical XSS vulnerability that allows arbitrary script injection.

### 🚫 BLOCKING - Must Fix Before Merge

1. **`mymodule_page_callback()` — XSS Vulnerability**
   - **Location:** Line where `$_GET['title']` is concatenated
   - **Issue:** User input rendered without sanitization
   - **Exploit:** Attacker crafts URL: `?title=<script>steal(cookies)</script>`
   - **Fix:** Use `Html::escape($_GET['title'])` or `Xss::filter()`

### ✅ Next Steps
1. Sanitize all user input before rendering
2. Consider using Drupal's render array system instead of raw HTML
```

---

## 📚 About the Creator

**Patricia Chang** is a Senior Project Manager & AI Solutions Architect with 10+ years of enterprise project management experience.

[LinkedIn](https://www.linkedin.com/in/patriciachang23) | [Portfolio](https://patricia-chang-portfolio.netlify.app)

This project demonstrates practical application of:
- Multi-agent AI systems (CrewAI)
- Prompt engineering for domain expertise
- Agentic AI architectures
- Human-in-the-loop AI design

---

## 🔌 Integration Examples

This prototype demonstrates the AI review logic. In a production environment, it integrates seamlessly into existing developer workflows. Below are examples of what each integration looks like.

### GitHub Pull Request Integration

When a developer opens a PR, the AI review automatically runs and posts as a comment:

---

> #### 🤖 AI Code Review
> 
> **PR:** #142 — Add user authentication module  
> **Author:** @developer-jane  
> **Reviewed:** 5 files changed
> 
> ---
> 
> ## DECISION: REQUEST CHANGES
> 
> **Rationale:** Critical SQL injection vulnerability in login handler. Security issues must be resolved before merge. Code quality is otherwise good.
> 
> ### 🚫 BLOCKING — Must Fix Before Merge
> 
> | # | File | Line | Issue | Severity |
> |---|------|------|-------|----------|
> | 1 | `src/Auth/LoginHandler.php` | 34 | SQL injection via string concatenation in user query | CRITICAL |
> | 2 | `src/Auth/LoginHandler.php` | 67 | Password compared in plain text, not hashed | CRITICAL |
> | 3 | `templates/login.html.twig` | 12 | Unsanitized user input rendered with `\|raw` filter | HIGH |
> 
> ### ⚠️ HIGH PRIORITY — Should Fix
> 
> | # | File | Line | Issue |
> |---|------|------|-------|
> | 1 | `src/Auth/LoginHandler.php` | 15 | Uses deprecated `db_query()` — migrate to database service |
> | 2 | `src/Auth/LoginHandler.php` | — | Missing cache tags on user data render array |
> 
> ### 💡 SUGGESTIONS
> 
> - Consider using Drupal's built-in authentication service
> - Add rate limiting to prevent brute force attacks
> - Add logging for failed authentication attempts
> 
> ### ✅ Next Steps
> 
> 1. Fix SQL injection using parameterized queries
> 2. Implement password hashing with `password_verify()`
> 3. Remove `|raw` filter or sanitize input with `Html::escape()`
> 4. Re-request review after fixes
> 
> ---
> 
> <sub>🔍 Powered by AI Code Review Crew | 5 agents • 47 sec review time • [View detailed logs]()</sub>

---

### Slack Notification Integration

When a review completes, the team channel receives a notification:

---

> **#dev-notifications**
> 
> 🤖 **AI Code Review Bot** · 2:34 PM
> 
> **Code Review Complete** for PR #142
> 
> │ **Status:** 🔴 Request Changes  
> │ **PR:** Add user authentication module  
> │ **Author:** Jane Developer  
> │ **Review Time:** 47 seconds  
> 
> **Summary:**
> > 2 critical security issues, 2 high priority issues
> 
> **Blocking Issues:**
> • `LoginHandler.php:34` — SQL injection vulnerability
> • `LoginHandler.php:67` — Plain text password comparison
> 
> ┌────────────────────────────────────┐
> │  [View PR ↗]   [View Full Review ↗]  │
> └────────────────────────────────────┘

---

### Jira Ticket Integration

When issues are found, they can automatically be added as a comment on the linked Jira ticket:

---

> **PROJ-1234** — Implement user authentication
> 
> ---
> 
> **AI Code Review** added a comment · Today at 2:34 PM
> 
> 🤖 **Automated Code Review Results**
> 
> **Pull Request:** [PR #142 — Add user authentication module](https://github.com)  
> **Decision:** 🔴 **REQUEST CHANGES**
> 
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> 
> **🚫 Blocking Issues (2)**
> 
> 1. **CRITICAL — SQL Injection**  
>    `LoginHandler.php` line 34  
>    User input concatenated directly into SQL query
> 
> 2. **CRITICAL — Insecure Password Handling**  
>    `LoginHandler.php` line 67  
>    Passwords compared in plain text
> 
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> 
> **Recommended Action:** Address security issues before moving to QA.
> 
> [View Full Review →](https://github.com)

---

### How to Enable These Integrations

#### GitHub Action (Ready to Use)

The repository includes a complete GitHub Action at `.github/workflows/ai-code-review.yml`.

**To enable:**
1. Copy the workflow file to your repository
2. Add `ANTHROPIC_API_KEY` to repository secrets
3. Open a PR — review runs automatically

```yaml
# Triggers automatically on PR
on:
  pull_request:
    types: [opened, synchronize, ready_for_review]
```

#### Slack Integration (Webhook)

```python
# Post review to Slack channel
import requests

def post_to_slack(review_result, pr_info):
    webhook_url = os.environ['SLACK_WEBHOOK_URL']
    
    message = {
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "🤖 Code Review Complete"}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*PR:* {pr_info['title']}"},
                    {"type": "mrkdwn", "text": f"*Status:* {review_result['decision']}"}
                ]
            }
        ]
    }
    
    requests.post(webhook_url, json=message)
```

#### Jira Integration (API)

```python
# Add review as Jira comment
from jira import JIRA

def add_jira_comment(ticket_id, review_result):
    jira = JIRA(server=JIRA_URL, basic_auth=(JIRA_USER, JIRA_TOKEN))
    
    comment = f"""
    🤖 *Automated Code Review Results*
    
    *Decision:* {review_result['decision']}
    
    *Blocking Issues:*
    {format_issues(review_result['blocking'])}
    """
    
    jira.add_comment(ticket_id, comment)
```

---

## 🔮 Roadmap

### Current Release (v1.0)
- ✅ 5 specialized review agents
- ✅ Drupal CMS 
- ✅ Web interface for manual reviews
- ✅ GitHub Action workflow (ready to deploy)

### Planned Enhancements
- ⏳ Slack webhook integration
- ⏳ Jira API integration
- ⏳ Custom agent configurations per project
- ⏳ Review analytics dashboard
- ⏳ Support for additional languages (Go, Ruby, etc.)

---

## 🙏 Acknowledgments

- [CrewAI](https://www.crewai.com/) for the multi-agent framework
- [Anthropic](https://www.anthropic.com/) for Claude
- [Tag1](https://www.tag1.com/) for Drupal expertise inspiration
