from django import template

register = template.Library()

@register.filter
def format_cents_as_money(value):
    """
    Converts an integer representing cents to a formatted currency string (e.g., $123.45).
    """
    try:
        # Convert cents to dollars (float)
        dollars = float(value) / 100
        # Format as currency with two decimal places and comma separators
        return "${:,.2f}".format(dollars)
    except (ValueError, TypeError):
        return value
