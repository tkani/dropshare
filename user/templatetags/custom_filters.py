from django import template
from django.utils import timezone
from datetime import datetime, timedelta


register = template.Library()

@register.filter
def split_path(value):
    return value.split('/')[-1]

@register.filter
def format_utc_date(value):
    # Assuming the input date string is in ISO 8601 format
    input_format = '%Y-%m-%dT%H:%M:%SZ'
    output_format = '%B %d, %Y %I:%M %p'

    # Parse the input date string
    input_date = datetime.strptime(value, input_format)

    # Add UTC offset (assuming UTC)
    input_date = input_date + timedelta(hours=0)

    # Convert to the desired output format
    output_date = input_date.strftime(output_format)

    return output_date

@register.filter
def size_checker(value):
    
    if value > 1000:
        value=str(int(value/1000))+' TB'
        return value
    elif value > 1:
        value=str(int(value))+' MB'
        return value
    else:
        value=str(int(value*1000))+' KB'
        return value


    return output_date