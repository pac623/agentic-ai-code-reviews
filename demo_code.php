<?php

/**
 * Demo file with intentional vulnerabilities for AI review demonstration.
 */

function mymodule_login_handler($username, $password) {
  // SQL Injection vulnerability - string concatenation
  $query = "SELECT * FROM users WHERE username = '" . $username . "'";
  $result = db_query($query);
  $user = $result->fetchObject();
  
  // Plain text password comparison
  if ($user && $user->password == $password) {
    drupal_set_message(t("Welcome @name!", array('@name' => $username)));
    return TRUE;
  }
  
  return FALSE;
}

function mymodule_page_callback() {
  // XSS vulnerability - unsanitized user input
  $output = '<h1>' . $_GET['title'] . '</h1>';
  return $output;
}