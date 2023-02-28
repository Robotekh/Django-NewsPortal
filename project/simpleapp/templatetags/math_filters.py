from django import template

#Две строки для того чтобы убрать ошибку превышени лимит на число
#Exceeds the limit (4300) for integer string conversion;
import sys
sys.set_int_max_str_digits(0)



register = template.Library()

@register.filter
def pow(value, pow):
    return value**pow