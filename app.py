"""
Code Review Crew - Streamlit Web Interface
A simple web UI for the multi-agent code review system

To run locally: streamlit run app.py
"""

import streamlit as st
from crew import run_code_review

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="AI Code Review Crew",
    page_icon="🔍",
    layout="wide"
)

# =============================================================================
# HEADER AND DESCRIPTION
# =============================================================================

st.title("🔍 AI Code Review Crew")
st.markdown("""
**A Multi-Agent Code Analysis System** built by [Patricia Chang](https://www.linkedin.com/in/patriciachang23)

This tool demonstrates agentic AI using five specialized AI agents working together:

| Agent | Focus Area |
|-------|------------|
| 🎯 **Code Review Engineer** | Code quality, Drupal best practices, coding standards |
| 🔒 **Security Analyst** | Vulnerabilities, OWASP Top 10, Drupal security |
| 🎨 **Frontend Review Engineer** | Accessibility (WCAG), CSS/JS, Twig templates |
| ⚙️ **Infrastructure Analyst** | Caching, config management, performance, deployment |
| 👤 **Technical Lead Reviewer** | Synthesizes all feedback, makes final decision |

Paste your code below and click **Run Review** to see the agents collaborate.
""")

st.divider()

# =============================================================================
# SAMPLE CODE OPTIONS
# =============================================================================

# Drupal code with security vulnerabilities
SAMPLE_DRUPAL_VULNERABLE = '''/**
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
 * Custom page callback with XSS vulnerability.
 */
function mymodule_page_callback() {
  $output = '<div class="my-content">';
  $output .= '<h1>' . $_GET['title'] . '</h1>';
  $output .= '</div>';
  return $output;
}'''

# Python code with issues
SAMPLE_PYTHON_VULNERABLE = '''def login(username, password):
    # Check if user exists
    query = f"SELECT * FROM users WHERE username = '{username}'"
    user = database.execute(query)
    
    if user and user.password == password:
        print(f"Welcome {username}!")
        return True
    else:
        print(f"Login failed for {username}")
        return False

def get_user_data(user_id):
    data = database.execute(f"SELECT * FROM sensitive_data WHERE id = {user_id}")
    return data'''

# Frontend code with accessibility issues
SAMPLE_FRONTEND_ISSUES = '''<div onclick="handleClick()">
  <img src="banner.jpg">
  <div class="btn" onclick="submit()">Click Here</div>
  <input type="text" placeholder="Enter email">
  <div style="color: #999; background: #fff;">Low contrast text</div>
</div>

<script>
var data = [];
$('.item').each(function() {
  data.push($(this).html());
});

function handleClick() {
  document.location = userInput;
}
</script>

<style>
.btn { color: red !important; }
.header { color: blue !important; }
#main .content .wrapper .inner { padding: 10px; }
</style>'''

# Clean Drupal code example
SAMPLE_DRUPAL_CLEAN = '''<?php

namespace Drupal\\mymodule\\Controller;

use Drupal\\Core\\Controller\\ControllerBase;
use Drupal\\Core\\Database\\Connection;
use Drupal\\Core\\Session\\AccountProxyInterface;
use Symfony\\Component\\DependencyInjection\\ContainerInterface;

/**
 * Controller for user data display.
 */
class UserDataController extends ControllerBase {

  /**
   * The database connection.
   *
   * @var \\Drupal\\Core\\Database\\Connection
   */
  protected $database;

  /**
   * The current user.
   *
   * @var \\Drupal\\Core\\Session\\AccountProxyInterface
   */
  protected $currentUser;

  /**
   * Constructs a UserDataController object.
   */
  public function __construct(Connection $database, AccountProxyInterface $current_user) {
    $this->database = $database;
    $this->currentUser = $current_user;
  }

  /**
   * {@inheritdoc}
   */
  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('database'),
      $container->get('current_user')
    );
  }

  /**
   * Displays user profile data.
   *
   * @return array
   *   A render array.
   */
  public function content() {
    // Check access.
    if (!$this->currentUser->hasPermission('view own profile')) {
      throw new AccessDeniedHttpException();
    }

    // Use parameterized query.
    $query = $this->database->select('user_data', 'ud')
      ->fields('ud', ['data_value'])
      ->condition('uid', $this->currentUser->id())
      ->execute();

    $items = [];
    foreach ($query as $record) {
      $items[] = Html::escape($record->data_value);
    }

    return [
      '#theme' => 'item_list',
      '#items' => $items,
      '#cache' => [
        'contexts' => ['user'],
        'tags' => ['user:' . $this->currentUser->id()],
      ],
    ];
  }

}'''

# =============================================================================
# USER INTERFACE
# =============================================================================

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Code Input")
    
    # Sample code selector
    sample_option = st.selectbox(
        "Load a sample (or paste your own below):",
        ["-- Select a sample --", 
         "🔴 Drupal - Vulnerable Code (SQL Injection + XSS)", 
         "🔴 Python - Vulnerable Code (SQL Injection)",
         "🟡 Frontend - Accessibility Issues",
         "🟢 Drupal - Clean Code Example"]
    )
    
    # Set initial code based on selection
    if sample_option == "🔴 Drupal - Vulnerable Code (SQL Injection + XSS)":
        initial_code = SAMPLE_DRUPAL_VULNERABLE
    elif sample_option == "🔴 Python - Vulnerable Code (SQL Injection)":
        initial_code = SAMPLE_PYTHON_VULNERABLE
    elif sample_option == "🟡 Frontend - Accessibility Issues":
        initial_code = SAMPLE_FRONTEND_ISSUES
    elif sample_option == "🟢 Drupal - Clean Code Example":
        initial_code = SAMPLE_DRUPAL_CLEAN
    else:
        initial_code = "# Paste your code here..."
    
    # Code input area
    code_input = st.text_area(
        "Code to review:",
        value=initial_code,
        height=400,
        help="Paste PHP, JavaScript, Python, Twig, CSS, or any code you want reviewed"
    )
    
    # Run button
    run_review = st.button("🚀 Run Review", type="primary", use_container_width=True)
    
    st.caption("⏱️ Review typically takes 60-90 seconds (5 agents analyzing)")

with col2:
    st.subheader("📋 Review Results")
    
    if run_review:
        if code_input.strip() == "" or code_input.strip() == "# Paste your code here...":
            st.warning("Please paste some code to review!")
        else:
            with st.spinner("🤖 Agents are reviewing your code... (this takes 60-90 seconds)"):
                try:
                    result = run_code_review(code_input)
                    st.success("Review complete!")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.info("Make sure your ANTHROPIC_API_KEY is set correctly in the .env file")
    else:
        st.info("👈 Paste code and click **Run Review** to start")
        
        with st.expander("ℹ️ What each agent reviews"):
            st.markdown("""
            **🎯 Code Review Engineer**
            - Code readability and structure
            - Naming conventions
            - Drupal coding standards
            - Hook implementations
            - Deprecated API usage
            - Workspaces module compatibility
            
            **🔒 Security Analyst**
            - SQL injection
            - Cross-site scripting (XSS)
            - CSRF vulnerabilities
            - Access control issues
            - Drupal Form API security
            - Input sanitization
            
            **🎨 Frontend Review Engineer**
            - WCAG 2.1 AA accessibility
            - Semantic HTML
            - CSS best practices
            - JavaScript patterns
            - Twig template quality
            - Performance concerns
            
            **⚙️ Infrastructure Analyst**
            - Cache tags and contexts
            - Configuration management
            - Database query efficiency
            - Deployment readiness
            - Environment-specific code
            
            **👤 Technical Lead Reviewer**
            - Synthesizes all feedback
            - Prioritizes issues
            - Makes final APPROVE/REQUEST CHANGES/REJECT decision
            """)

# =============================================================================
# FOOTER
# =============================================================================

st.divider()
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.9em;">
    Built with CrewAI + Claude | 
    <a href="https://patricia-chang-portfolio.netlify.app" target="_blank">Portfolio</a> | 
    <a href="https://github.com/patriciachang" target="_blank">GitHub</a> |
    <a href="https://www.linkedin.com/in/patriciachang23" target="_blank">LinkedIn</a>
</div>
""", unsafe_allow_html=True)
