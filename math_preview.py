"""Safe presentation helper: preview expressions using the app's restricted parser."""
import sympy as sp

def preview_latex(parse, raw, allowed=('x',)):
    """Return LaTeX or raise ValueError; never evaluate arbitrary Python code."""
    if not isinstance(raw,str) or not raw.strip():
        raise ValueError('Enter an expression to preview.')
    expression=parse(raw)
    if not {str(v) for v in expression.free_symbols}.issubset(set(allowed)):
        raise ValueError('This field accepts only '+', '.join(allowed)+'.')
    return sp.latex(expression)

def render_preview(st, parse, raw, allowed=('x',), label='Math preview'):
    """Render the typed expression separately from the editable text field."""
    try:
        latex=preview_latex(parse,raw,allowed)
    except (ValueError, SyntaxError, TypeError, OverflowError, ZeroDivisionError) as exc:
        st.caption(f'{label}: enter a valid expression ({exc}).')
        return
    st.caption(label)
    st.latex(latex)
