from django.test import TestCase
from .views import create_rule, evaluate_ast, combine_rules


class RuleEngineComplexTestCase(TestCase):
    
    def test_rule1(self):
        rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
        ast_rule1 = create_rule(rule1)
        
        data1 = {
            "age": 35,
            "department": "Sales",
            "salary": 60000,
            "experience": 3
        }
        result_rule1 = evaluate_ast(ast_rule1, data1)
        self.assertTrue(result_rule1)
    
    def test_rule2(self):
        rule2 = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
        ast_rule2 = create_rule(rule2)
        
        data2 = {
            "age": 32,
            "department": "Marketing",
            "salary": 25000,
            "experience": 6
        }
        result_rule2 = evaluate_ast(ast_rule2, data2)
        self.assertTrue(result_rule2)
    
    def test_rule1_fail(self):
        rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
        ast_rule1 = create_rule(rule1)
        
        data3 = {
            "age": 28,
            "department": "Marketing",
            "salary": 40000,
            "experience": 2
        }
        result_rule1_fail = evaluate_ast(ast_rule1, data3)
        self.assertFalse(result_rule1_fail)
    
    def test_combined_rules(self):
        rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
        rule2 = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
        
        combined_ast = combine_rules([rule1, rule2])
        
        combined_data = {
            "age": 35,
            "department": "Marketing",
            "salary": 60000,
            "experience": 6
        }
        
        result_combined = evaluate_ast(combined_ast, combined_data)
        self.assertTrue(result_combined)
