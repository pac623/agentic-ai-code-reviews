# Production Setup Guide

**AI Code Review Crew — From Prototype to Production**

This guide provides step-by-step instructions for deploying the AI Code Review Crew in a real development environment. It covers GitHub Action setup, Slack integration, Jira integration, and customization options.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [GitHub Action Setup](#2-github-action-setup)
3. [Slack Integration Setup](#3-slack-integration-setup)
4. [Jira Integration Setup](#4-jira-integration-setup)
5. [Customization Guide](#5-customization-guide)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. Prerequisites

Before setting up any integration, ensure you have:

### Required
- [ ] **Anthropic API Key** — Get one at [console.anthropic.com](https://console.anthropic.com/)
- [ ] **GitHub Repository** — Where your code lives
- [ ] **Repository Admin Access** — Needed to add secrets and workflows

### Optional (for specific integrations)
- [ ] **Slack Workspace Admin Access** — For creating webhooks
- [ ] **Jira Admin Access** — For creating API tokens

### Cost Considerations

| Component | Cost |
|-----------|------|
| Anthropic API | ~$0.50-2.00 per review (depends on code size) |
| GitHub Actions | Free for public repos, 2000 min/month for private |
| Slack | Free (webhooks are included in all plans) |
| Jira | Free (API access included in all plans) |

---

## 2. GitHub Action Setup

This section walks through setting up automatic code reviews on every Pull Request.

### Step 2.1: Add the Workflow File

The workflow file tells GitHub when and how to run the AI review.

**Option A: If you cloned this repository**
The file is already at `.github/workflows/ai-code-review.yml` — skip to Step 2.2.

**Option B: Adding to an existing repository**

1. In your repository, create the folders:
   ```
   .github/
   └── workflows/
   ```

2. Create a new file called `ai-code-review.yml` in the workflows folder

3. Copy the entire contents from this project's `.github/workflows/ai-code-review.yml`

4. Commit and push:
   ```bash
   git add .github/workflows/ai-code-review.yml
   git commit -m "Add AI code review workflow"
   git push
   ```

### Step 2.2: Add Your API Key as a Secret

GitHub Secrets store sensitive information securely. Your API key will never be visible in logs or to other users.

1. Go to your repository on GitHub

2. Click **Settings** (tab at the top)

3. In the left sidebar, click **Secrets and variables** → **Actions**

4. Click the green **New repository secret** button

5. Fill in:
   - **Name:** `ANTHROPIC_API_KEY`
   - **Secret:** Your actual API key (starts with `sk-ant-...`)

6. Click **Add secret**

**Verification:** You should now see `ANTHROPIC_API_KEY` listed under Repository secrets.

### Step 2.3: Test the Integration

1. Create a new branch in your repository:
   ```bash
   git checkout -b test/ai-review
   ```

2. Make a small code change (edit any `.php`, `.js`, `.py`, or other code file)

3. Commit and push:
   ```bash
   git add .
   git commit -m "Test AI review"
   git push -u origin test/ai-review
   ```

4. Open a Pull Request on GitHub

5. Watch the **Checks** section at the bottom of the PR — you should see "AI Code Review" running

6. After 60-90 seconds, a comment will appear on your PR with the review results

### Step 2.4: Customize Which Files Trigger Reviews

By default, the action reviews these file types:
- `.php`, `.module`, `.theme` (Drupal/PHP)
- `.js`, `.css` (Frontend)
- `.twig` (Drupal templates)
- `.py` (Python)

**To change this**, edit the `paths` section in `ai-code-review.yml`:

```yaml
on:
  pull_request:
    paths:
      # Add or remove file patterns here
      - '**.php'
      - '**.module'
      - '**.theme'
      - '**.js'
      - '**.jsx'        # Add React files
      - '**.ts'         # Add TypeScript
      - '**.tsx'        # Add TypeScript React
      - '**.css'
      - '**.scss'       # Add SCSS
      - '**.twig'
      - '**.py'
      - '**.go'         # Add Go files
      - '**.rb'         # Add Ruby files
```

### Step 2.5: Control When Reviews Run

**Current behavior:** Reviews run when PRs are opened, updated, or marked ready for review.

**To also run on specific branches only:**

```yaml
on:
  pull_request:
    types: [opened, synchronize, ready_for_review]
    branches:
      - main
      - develop
      - 'release/**'
```

**To skip reviews on draft PRs** (already configured):
```yaml
if: github.event.pull_request.draft == false
```

**To require reviews to pass before merging:**

1. Go to repository **Settings** → **Branches**
2. Under "Branch protection rules," click **Add rule**
3. Enter branch name (e.g., `main`)
4. Check **Require status checks to pass before merging**
5. Search for and select **AI Code Review**
6. Click **Create** or **Save changes**

Now PRs cannot be merged if the AI review finds blocking issues.

---

## 3. Slack Integration Setup

Get notified in Slack when code reviews complete.

### Step 3.1: Create a Slack Webhook

1. Go to [api.slack.com/apps](https://api.slack.com/apps)

2. Click **Create New App** → **From scratch**

3. Enter:
   - **App Name:** `AI Code Review Bot`
   - **Workspace:** Select your workspace

4. Click **Create App**

5. In the left sidebar, click **Incoming Webhooks**

6. Toggle **Activate Incoming Webhooks** to **On**

7. Click **Add New Webhook to Workspace**

8. Select the channel where you want notifications (e.g., `#dev-notifications`)

9. Click **Allow**

10. Copy the **Webhook URL** — it looks like:
    ```
    https://hooks.slack.com/services/TXXXXX/BXXXXX/your-webhook-token-here
    ```
    (Your actual URL will have real characters instead of X's)

### Step 3.2: Add Webhook to GitHub Secrets

1. Go to your repository **Settings** → **Secrets and variables** → **Actions**

2. Click **New repository secret**

3. Fill in:
   - **Name:** `SLACK_WEBHOOK_URL`
   - **Secret:** The webhook URL you copied

4. Click **Add secret**

### Step 3.3: Add Slack Notification to Workflow

Add this step to your `ai-code-review.yml` file, after the "Post review comment" step:

```yaml
      # Step 9: Send Slack notification
      - name: Notify Slack
        if: always() && steps.prepare-code.outputs.skip_review != 'true'
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        run: |
          # Determine status emoji
          if grep -q "DECISION: APPROVE" review_result.md; then
            STATUS="✅ Approved"
            COLOR="good"
          elif grep -q "DECISION: REJECT" review_result.md; then
            STATUS="❌ Rejected"
            COLOR="danger"
          else
            STATUS="🔄 Changes Requested"
            COLOR="warning"
          fi
          
          # Send to Slack
          curl -X POST -H 'Content-type: application/json' \
            --data "{
              \"attachments\": [{
                \"color\": \"$COLOR\",
                \"blocks\": [
                  {
                    \"type\": \"header\",
                    \"text\": {\"type\": \"plain_text\", \"text\": \"🤖 Code Review Complete\"}
                  },
                  {
                    \"type\": \"section\",
                    \"fields\": [
                      {\"type\": \"mrkdwn\", \"text\": \"*PR:* ${{ github.event.pull_request.title }}\"},
                      {\"type\": \"mrkdwn\", \"text\": \"*Status:* $STATUS\"},
                      {\"type\": \"mrkdwn\", \"text\": \"*Author:* ${{ github.event.pull_request.user.login }}\"},
                      {\"type\": \"mrkdwn\", \"text\": \"*Repo:* ${{ github.repository }}\"}
                    ]
                  },
                  {
                    \"type\": \"actions\",
                    \"elements\": [
                      {
                        \"type\": \"button\",
                        \"text\": {\"type\": \"plain_text\", \"text\": \"View PR\"},
                        \"url\": \"${{ github.event.pull_request.html_url }}\"
                      }
                    ]
                  }
                ]
              }]
            }" \
            $SLACK_WEBHOOK_URL
```

### Step 3.4: Test Slack Integration

1. Open a new PR (or push to an existing one)
2. Wait for the review to complete
3. Check your Slack channel for the notification

---

## 4. Jira Integration Setup

Automatically add review results as comments on linked Jira tickets.

### Step 4.1: Get Jira API Credentials

1. Go to [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)

2. Click **Create API token**

3. Enter a label: `AI Code Review Bot`

4. Click **Create**

5. **Copy the token immediately** — you won't be able to see it again

6. Note your Jira email address (used for authentication)

7. Note your Jira base URL (e.g., `https://yourcompany.atlassian.net`)

### Step 4.2: Add Jira Credentials to GitHub Secrets

Add these three secrets to your repository:

| Secret Name | Value |
|-------------|-------|
| `JIRA_BASE_URL` | `https://yourcompany.atlassian.net` |
| `JIRA_USER_EMAIL` | Your Jira email address |
| `JIRA_API_TOKEN` | The API token you created |

### Step 4.3: Add Jira Integration to Workflow

This integration assumes your PR titles or branch names contain the Jira ticket ID (e.g., `PROJ-123`).

Add this step to your `ai-code-review.yml` file:

```yaml
      # Step 10: Update Jira ticket
      - name: Update Jira ticket
        if: steps.prepare-code.outputs.skip_review != 'true'
        env:
          JIRA_BASE_URL: ${{ secrets.JIRA_BASE_URL }}
          JIRA_USER_EMAIL: ${{ secrets.JIRA_USER_EMAIL }}
          JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
        run: |
          # Extract Jira ticket ID from PR title or branch name
          # Looks for patterns like PROJ-123, ABC-456, etc.
          TICKET_ID=$(echo "${{ github.event.pull_request.title }} ${{ github.head_ref }}" | grep -oE '[A-Z]+-[0-9]+' | head -1)
          
          if [ -z "$TICKET_ID" ]; then
            echo "No Jira ticket ID found in PR title or branch name"
            exit 0
          fi
          
          echo "Found Jira ticket: $TICKET_ID"
          
          # Determine decision
          if grep -q "DECISION: APPROVE" review_result.md; then
            DECISION="✅ APPROVED"
          elif grep -q "DECISION: REJECT" review_result.md; then
            DECISION="❌ REJECTED"
          else
            DECISION="🔄 CHANGES REQUESTED"
          fi
          
          # Create comment body (escape for JSON)
          COMMENT_BODY=$(cat << EOF
          🤖 *AI Code Review Results*
          
          *Pull Request:* [${{ github.event.pull_request.title }}|${{ github.event.pull_request.html_url }}]
          *Decision:* $DECISION
          
          [View full review on GitHub|${{ github.event.pull_request.html_url }}]
          EOF
          )
          
          # Escape newlines for JSON
          COMMENT_JSON=$(echo "$COMMENT_BODY" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')
          
          # Post comment to Jira
          curl -s -X POST \
            -H "Content-Type: application/json" \
            -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
            -d "{\"body\": $COMMENT_JSON}" \
            "$JIRA_BASE_URL/rest/api/2/issue/$TICKET_ID/comment"
          
          echo "Posted review to Jira ticket $TICKET_ID"
```

### Step 4.4: Link PRs to Jira Tickets

For the integration to work, include the Jira ticket ID in either:

- **PR Title:** `PROJ-123: Add user authentication`
- **Branch Name:** `feature/PROJ-123-user-auth`

The script looks for patterns like `ABC-123` and uses the first match.

---

## 5. Customization Guide

### 5.1: Changing What Agents Look For

Each agent's behavior is defined by its `backstory` in `crew.py`. To change what an agent focuses on:

1. Open `crew.py`

2. Find the agent you want to modify (e.g., `security_analyst`)

3. Edit the `backstory` text:

```python
security_analyst = Agent(
    role="Security Analyst",
    goal="...",
    backstory="""
    # Add your custom instructions here
    # Be specific about what to look for
    # Include examples of issues to flag
    
    THINGS TO ALWAYS CHECK:
    - Your custom check 1
    - Your custom check 2
    
    THINGS TO IGNORE:
    - Stuff your team doesn't care about
    """,
    llm="anthropic/claude-sonnet-4-20250514",
    verbose=True
)
```

### 5.2: Adding a New Agent

1. **Define the agent** (copy an existing one as a template):

```python
# New agent for database review
database_reviewer = Agent(
    role="Database Reviewer",
    goal="Review database queries, schema changes, and data handling",
    backstory="""You are a database specialist who reviews code for:
    - Query efficiency
    - Index usage
    - N+1 problems
    - Schema migration safety
    """,
    llm="anthropic/claude-sonnet-4-20250514",
    verbose=True
)
```

2. **Create a task for the agent** in `create_review_tasks()`:

```python
database_task = Task(
    description=f"""
    Review the following code for database concerns:
    
    ```
    {code_to_review}
    ```
    
    Check for query efficiency, proper indexing, etc.
    """,
    expected_output="""Database review with issues found...""",
    agent=database_reviewer
)
```

3. **Add to the crew** in `run_code_review()`:

```python
crew = Crew(
    agents=[code_review_engineer, security_analyst, frontend_engineer, 
            infrastructure_analyst, database_reviewer, tech_lead_reviewer],  # Added here
    tasks=tasks,
    verbose=True
)
```

4. **Add to Tech Lead's context** so they see the findings:

```python
decision_task = Task(
    # ...
    context=[quality_task, security_task, frontend_task, 
             infrastructure_task, database_task]  # Added here
)
```

### 5.3: Removing an Agent

To skip an agent (e.g., frontend review for backend-only repos):

1. Remove the agent from the `agents=[]` list in the Crew
2. Remove their task from the `tasks=[]` list
3. Remove the task from Tech Lead's `context=[]`

### 5.4: Changing the LLM Model

In each agent definition, change the `llm` parameter:

```python
# More capable, more expensive
llm="anthropic/claude-opus-4-20250514"

# Current default (recommended balance)
llm="anthropic/claude-sonnet-4-20250514"

# Faster, cheaper, less capable
llm="anthropic/claude-haiku-4-20250514"
```

**Cost comparison:**
| Model | Input Cost | Output Cost | Best For |
|-------|------------|-------------|----------|
| Opus | $15/1M tokens | $75/1M tokens | Critical reviews |
| Sonnet | $3/1M tokens | $15/1M tokens | Daily use (recommended) |
| Haiku | $0.25/1M tokens | $1.25/1M tokens | High volume, simple checks |

### 5.5: Adjusting Severity Levels

The agents use these severity levels:
- **CRITICAL** — Security vulnerabilities, will break production
- **HIGH** — Significant issues that should be fixed
- **MEDIUM** — Best practice violations
- **LOW** — Minor suggestions

To change how agents classify severity, edit their `backstory` to include your criteria:

```python
backstory="""
...
SEVERITY CLASSIFICATION FOR OUR TEAM:
- CRITICAL: Only security issues that are actively exploitable
- HIGH: Bugs that would affect users
- MEDIUM: Code quality issues
- LOW: Style preferences

DO NOT mark as CRITICAL:
- Deprecated APIs (mark as MEDIUM)
- Missing documentation (mark as LOW)
...
"""
```

---

## 6. Troubleshooting

### GitHub Action Issues

**Problem:** Action doesn't run when PR is opened

**Check:**
1. Is the workflow file in `.github/workflows/`?
2. Does the PR include files matching the `paths` filter?
3. Is the PR a draft? (drafts are skipped by default)

**Solution:** Check the Actions tab for errors, or remove the `paths` filter temporarily.

---

**Problem:** "ANTHROPIC_API_KEY not found" error

**Check:**
1. Go to Settings → Secrets → Actions
2. Verify `ANTHROPIC_API_KEY` exists (exact spelling)

**Solution:** Delete and re-add the secret, ensuring no extra spaces.

---

**Problem:** Review takes too long / times out

**Cause:** 5 agents = 5 API calls = ~60-90 seconds

**Solutions:**
- This is normal; GitHub Actions allows up to 6 hours
- To speed up: Use fewer agents or switch to Haiku model
- For very large PRs, the review may take 2-3 minutes

---

### Slack Issues

**Problem:** No notification in Slack

**Check:**
1. Is `SLACK_WEBHOOK_URL` secret set correctly?
2. Is the webhook still active? (check Slack app settings)
3. Is the channel correct?

**Solution:** Test webhook manually:
```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test message"}' \
  YOUR_WEBHOOK_URL
```

---

### Jira Issues

**Problem:** No comment appears on Jira ticket

**Check:**
1. Does the PR title/branch contain a valid ticket ID (e.g., `PROJ-123`)?
2. Are all three Jira secrets set (`JIRA_BASE_URL`, `JIRA_USER_EMAIL`, `JIRA_API_TOKEN`)?
3. Does the API token have permission to add comments?

**Solution:** Test API access manually:
```bash
curl -s -u "your-email@company.com:your-api-token" \
  "https://yourcompany.atlassian.net/rest/api/2/myself"
```

---

**Problem:** "Ticket not found" error

**Check:** The ticket ID extraction regex looks for `[A-Z]+-[0-9]+`

**Solution:** Ensure your ticket ID format matches (letters, hyphen, numbers).

---

### General Issues

**Problem:** Review output is blank or truncated

**Cause:** Code may be too long for context window

**Solution:** 
- Review smaller chunks of code
- Increase `max_tokens` in agent configuration
- Use a model with larger context window

---

**Problem:** False positives in reviews

**Solution:** Edit agent backstories to be more specific:
```python
backstory="""
...
DO NOT FLAG:
- Specific pattern your team uses intentionally
- Framework conventions that look unusual
...
"""
```

---

## Quick Reference

### GitHub Secrets Needed

| Secret | Required For |
|--------|--------------|
| `ANTHROPIC_API_KEY` | All reviews |
| `SLACK_WEBHOOK_URL` | Slack notifications |
| `JIRA_BASE_URL` | Jira integration |
| `JIRA_USER_EMAIL` | Jira integration |
| `JIRA_API_TOKEN` | Jira integration |

### File Locations

| File | Purpose |
|------|---------|
| `.github/workflows/ai-code-review.yml` | GitHub Action |
| `crew.py` | Agent definitions (edit to customize) |
| `app.py` | Web interface (optional) |

### Useful Links

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Slack Webhooks Guide](https://api.slack.com/messaging/webhooks)
- [Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [CrewAI Documentation](https://docs.crewai.com/)

---

*Last updated: January 17, 2026*
