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

// Global array to store all rule strings
let ruleStrings = [];

// Handle Rule Creation and Add Rule to the List
document.getElementById('create-rule-form').addEventListener('submit', async function(event) {
  event.preventDefault();  // Prevent the default form submission behavior

  // Debugging: Check if this part is being triggered
  console.log("Form submission triggered");

  const ruleString = document.getElementById('rule-string').value;
  const csrfToken = getCSRFToken();  // Get CSRF token from cookies

  // Debugging: Log the CSRF token and rule string
  console.log("Rule String:", ruleString);
  console.log("CSRF Token:", csrfToken);

  // Send the rule to the backend to create AST
  const response = await fetch(`http://127.0.0.1:8000/rule_engine/create_rule/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken  // Add the CSRF token to headers
    },
    body: JSON.stringify({
      rule_string: ruleString
    }),
  });

  const result = await response.json();

  // Debugging: Check the server response
  console.log("Server response:", result);

  // Check if the rule was created successfully
  if (result.message === "Rule created successfully") {
    // Add the rule to the global array of rule strings
    ruleStrings.push(ruleString);

    // Update the rules list on the front-end
    const rulesList = document.getElementById('rules-list');
    const newRuleItem = document.createElement('li');
    newRuleItem.textContent = ruleString;
    rulesList.appendChild(newRuleItem);

    // Display the AST
    document.getElementById('ast-output').textContent = `AST: ${result.ast_structure}`;

    // Clear the rule input after adding
    document.getElementById('rule-string').value = '';

    // Display a success message
    document.getElementById('rule-message').textContent = 'Rule added successfully!';
  } else {
    // Display error message if the rule wasn't added successfully
    document.getElementById('rule-message').textContent = 'Failed to add rule!';
  }
});
