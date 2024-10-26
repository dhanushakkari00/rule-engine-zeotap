# Rule Engine

This project is a simple rule-based evaluation system built using Django. The project allows users to create, combine, and evaluate rules based on different parameters like age, department, salary, and experience.

## Features

- **Create Rule**: Users can create individual rules using simple expressions like `age > 30 AND salary > 50000`.
- **Combine Rules**: Multiple rules can be combined logically (e.g., `OR`, `AND`) into a single rule.
- **Evaluate Rule**: Evaluate the combined rules against user-provided data.
- **Delete Rule**: Existing rules can be deleted.
- **AST Representation**: Displays the Abstract Syntax Tree (AST) of rules.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Django 5.1.2 (Python 3.11)
- **Database**: SQLite (default Django setup)
- **API Communication**: AJAX, JSON

## Installation and Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/rule-engine.git
    cd rule-engine
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv env
    source env/bin/activate   # For Windows: env\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run database migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

6. **Access the app**:
   Open your browser and go to `http://127.0.0.1:8000/`

## Usage

1. **Creating a Rule**:
   - Enter a rule in the "Create Rule" section using a format like `age > 30 AND salary > 50000`.
   - Click "Create Rule". The rule will be added to the list of rules and the AST representation will be displayed.

2. **Combining Rules**:
   - Enter multiple rules, separated by lines, in the "Combine Rules" section.
   - Click "Combine Rules". The combined AST will be displayed.

3. **Evaluating Rules**:
   - Enter values for the parameters like age, department, salary, and experience in the "Evaluate Rule" section.
   - Click "Evaluate Rule". The result will be displayed as either `True` or `False` depending on the evaluation.

## API Endpoints

- **Create Rule**: `POST /rule_engine/create_rule/`
- **Combine Rules**: `POST /rule_engine/combine_rules/`
- **Evaluate Rule**: `POST /rule_engine/evaluate_rule/`
- **Delete Rule**: `DELETE /rule_engine/delete_rule/<rule_id>/`
- **Get All Rules**: `GET /rule_engine/get_all_rules/`

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.
