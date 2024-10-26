from django.db import models
import json

class ASTNode(models.Model):
    TYPE_CHOICES = [
        ('operator', 'Operator'),
        ('operand', 'Operand'),
    ]
    
    OPERATOR_CHOICES = [
        ('AND', 'AND'),
        ('OR', 'OR'),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    operator = models.CharField(max_length=10, choices=OPERATOR_CHOICES, blank=True, null=True)
    left = models.ForeignKey('self', on_delete=models.CASCADE, related_name='left_child', blank=True, null=True)
    right = models.ForeignKey('self', on_delete=models.CASCADE, related_name='right_child', blank=True, null=True)
    value = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.type}: {self.value or self.operator}"

class Rule(models.Model):
    rule_string = models.TextField()  # Field for storing rule as string

    def __str__(self):
        return self.rule_string