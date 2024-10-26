from django.http import JsonResponse
from .models import ASTNode, Rule
import json
from django.views.decorators.csrf import csrf_exempt
import re
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def ast_to_string(ast_node):
    """ Recursively converts the AST structure to a readable string format. """
    if ast_node.type == 'operand':
        return ast_node.value  # This handles conditions like 'age > 30'
    elif ast_node.type == 'operator':
        # Recursively get the left and right side of the operator
        left_str = ast_to_string(ast_node.left)
        right_str = ast_to_string(ast_node.right)
        # Combine left and right side with the operator, like '(left AND right)'
        return f"({left_str} {ast_node.operator} {right_str})"

@csrf_exempt
def create_rule_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        rule_string = data.get('rule_string')

        # Save the rule string in the Rule model
        rule = Rule.objects.create(rule_string=rule_string)
        
        # Create the AST from the rule string
        ast = create_rule(rule_string)
        
        # Convert the AST structure to a readable format
        ast_representation = ast_to_string(ast)
        
        return JsonResponse({
            "message": "Rule created successfully", 
            "rule_id": rule.id,
            "ast_structure": ast_representation
        })

@csrf_exempt
def get_all_rules_view(request):
    if request.method == 'GET':
        rules = Rule.objects.all()
        rules_list = [{"id": rule.id, "rule_string": rule.rule_string} for rule in rules]
        return JsonResponse({"rules": rules_list})


@csrf_exempt
def delete_rule_view(request, rule_id):
    if request.method == 'DELETE':
        try:
            rule = Rule.objects.get(id=rule_id)
            rule.delete()
            return JsonResponse({"message": "Rule deleted successfully!"})
        except Rule.DoesNotExist:
            return JsonResponse({"error": "Rule not found!"}, status=404)

# Assuming your `create_rule` is similar to this function
def create_rule(rule_string):
    tokens = re.findall(r'\(|\)|AND|OR|>|<|=|[a-zA-Z_]+|\d+', rule_string)

    def parse_expression(tokens):
        if not tokens:
            return None
        token = tokens.pop(0)
        if token == "(":
            left_node = parse_expression(tokens)
            operator = tokens.pop(0)
            right_node = parse_expression(tokens)
            tokens.pop(0)
            return ASTNode.objects.create(type="operator", operator=operator, left=left_node, right=right_node)
        elif re.match(r'[a-zA-Z_]+', token):
            operand = token
            operator = tokens.pop(0)
            value = tokens.pop(0)
            return ASTNode.objects.create(type="operand", value=f"{operand} {operator} {value}")

    return parse_expression(tokens)
def combine_rules(rules):
    combined_ast = None
    ast_list = [create_rule(rule_string) for rule_string in rules]
    
    if ast_list:
        combined_ast = ast_list[0]
    
    for ast in ast_list[1:]:
        combined_ast = ASTNode.objects.create(type="operator", operator="AND", left=combined_ast, right=ast)
    
    return combined_ast

def evaluate_ast(ast_node, data):
    if ast_node.type == 'operand':
        operand, operator, value = re.split(r'(<|>|=)', ast_node.value)
        operand = operand.strip()
        value = value.strip()
        if operator == ">":
            return data.get(operand, 0) > int(value)
        elif operator == "<":
            return data.get(operand, 0) < int(value)
        elif operator == "=":
            return data.get(operand, "") == value
    elif ast_node.type == "operator":
        left_result = evaluate_ast(ast_node.left, data)
        right_result = evaluate_ast(ast_node.right, data)
        if ast_node.operator == "AND":
            return left_result and right_result
        elif ast_node.operator == "OR":
            return left_result or right_result

@csrf_exempt
def evaluate_rule_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        rule_strings = data.get('rule_strings', [])
        
        if not rule_strings:
            return JsonResponse({"error": "At least one rule string is required"}, status=400)
        
        combined_ast = combine_rules(rule_strings)

        user_data = {
            "age": data.get('age'),
            "department": data.get('department'),
            "salary": data.get('salary'),
            "experience": data.get('experience'),
        }
        
        result = evaluate_ast(combined_ast, user_data)
        return JsonResponse({"result": result, "combined_ast": str(combined_ast)})
