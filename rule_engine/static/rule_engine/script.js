// Function to get the CSRF token from cookies
function getCSRFToken() {
  let csrfToken = null;
  const cookies = document.cookie.split(';');
  cookies.forEach(cookie => {
      const [name, value] = cookie.trim().split('=');
      if (name === 'csrftoken') {
          csrfToken = value;
      }
  });
  return csrfToken;
}

// Function to fetch and display all rules and their AST representations
async function fetchAllRules() {
  try {
      const response = await fetch(`http://127.0.0.1:8000/rule_engine/get_all_rules/`, {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json',
          },
      });

      const result = await response.json();
      const rulesList = document.getElementById('rules-list');
      const astRepresentation = document.getElementById('ast-representation');

      // Clear previous content
      rulesList.innerHTML = '';
      astRepresentation.innerHTML = '';

      // Populate rule list and AST representations
      result.rules.forEach(rule => {
          const ruleItem = document.createElement('li');
          ruleItem.textContent = rule.rule_string;

          // Create delete button
          const deleteButton = document.createElement('button');
          deleteButton.textContent = 'Delete';
          deleteButton.style.marginLeft = '10px';
          deleteButton.onclick = () => deleteRule(rule.id);

          ruleItem.appendChild(deleteButton);
          rulesList.appendChild(ruleItem);

          // Display AST representation
          const astItem = document.createElement('div');
          astItem.textContent = rule.ast_representation;
          astRepresentation.appendChild(astItem);
      });
  } catch (error) {
      console.error("Error fetching rules:", error);
  }
}

// Function to create a rule
document.getElementById('create-rule-form').addEventListener('submit', async function(event) {
  event.preventDefault();
  const ruleString = document.getElementById('rule-string').value;
  const csrfToken = getCSRFToken();

  try {
      const response = await fetch(`http://127.0.0.1:8000/rule_engine/create_rule/`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({ rule_string: ruleString })
      });

      const result = await response.json();
      document.getElementById('rule-string').value = '';  // Clear input field
      fetchAllRules();  // Refresh the rules list
  } catch (error) {
      console.error("Error creating rule:", error);
  }
});

// Function to combine rules
document.getElementById('combine-rules-button').addEventListener('click', async function() {
  const rulesTextarea = document.getElementById('combine-rules-textarea').value.split('\n');
  const csrfToken = getCSRFToken();

  try {
      const response = await fetch(`http://127.0.0.1:8000/rule_engine/combine_rules/`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({ rules: rulesTextarea })
      });

      const result = await response.json();
      document.getElementById('combined-ast-representation').textContent = result.combined_ast;
  } catch (error) {
      console.error("Error combining rules:", error);
  }
});

// Function to evaluate a rule
document.getElementById('evaluate-rule-form').addEventListener('submit', async function(event) {
  event.preventDefault();
  const age = document.getElementById('age').value;
  const department = document.getElementById('department').value;
  const salary = document.getElementById('salary').value;
  const experience = document.getElementById('experience').value;
  const csrfToken = getCSRFToken();

  try {
      const response = await fetch(`http://127.0.0.1:8000/rule_engine/evaluate_rule/`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({ age, department, salary, experience })
      });

      const result = await response.json();
      document.getElementById('evaluation-result').textContent = result.evaluation_result ? "True" : "False";
  } catch (error) {
      console.error("Error evaluating rule:", error);
  }
});

// Function to delete a rule
async function deleteRule(ruleId) {
  const csrfToken = getCSRFToken();
  try {
      const response = await fetch(`http://127.0.0.1:8000/rule_engine/delete_rule/${ruleId}/`, {
          method: 'DELETE',
          headers: {
              'X-CSRFToken': csrfToken,
          },
      });

      const result = await response.json();
      fetchAllRules();  // Refresh the rules list after deletion
  } catch (error) {
      console.error("Error deleting rule:", error);
  }
}

// Fetch all rules when the page loads
document.addEventListener('DOMContentLoaded', fetchAllRules);
