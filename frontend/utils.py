"""Small helper utilities used by components."""
def currency_format(value: float) -> str:
    try:
        return f"₹{int(value):,}"
    except Exception:
        return str(value)
