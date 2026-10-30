"""Optional bounded visual support for symbolic practice exercises."""
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import streamlit as st

X = sp.Symbol('x', real=True)

def visualization_data(subject, prompt, expected, parse, item=None):
    """Return graph arrays for function-valued answers, or None for scalar answers."""
    if subject not in ('Differential Calculus','Integral Calculus','Differential Equations'):
        return None
    # Word problems asking for a scalar do not benefit from an arbitrary function plot.
    if any(key in prompt.lower() for key in ('slope of the tangent','maximum area','find the area',
        'riemann sum','find the volume','find volume','one euler step',
        'particular solution','at x=', 'dA/dt'.lower())):
        return None
    if subject == 'Integral Calculus' and ('evaluate' in prompt.lower() or 'volume' in prompt.lower()):
        return None
    expr = parse(expected)
    if not expr.has(X):
        return None
    if expr.free_symbols - {X}:
        return None
    domain = (0.0, 3.0) if subject == 'Differential Equations' else (-3.0,3.0)
    if subject == 'Integral Calculus':
        domain = (-2.0,2.0)
    xs = np.linspace(*domain, 240)
    fn = sp.lambdify(X, expr, modules=['numpy'])
    with np.errstate(all='ignore'):
        ys = np.asarray(fn(xs),dtype=float)
    if ys.ndim == 0:
        ys = np.full(xs.shape,float(ys))
    if ys.shape != xs.shape:
        return None
    ys[~np.isfinite(ys)] = np.nan
    ys[np.abs(ys)>1e5] = np.nan
    if np.isfinite(ys).sum() < 15:
        return None
    return xs,ys,expr

def show_practice_visual(subject,prompt,expected,parse,item=None):
    try:
        result = visualization_data(subject,prompt,expected,parse,item)
    except (ValueError, TypeError, OverflowError, ZeroDivisionError, ArithmeticError):
        result = None
    if result is None:
        st.info('This question is best understood through its worked solution rather than a function graph.')
        return
    xs,ys,expr = result
    fig,ax=plt.subplots(figsize=(7,3.6))
    try:
        ax.plot(xs,ys,label='Answer function')
        ax.axhline(0,color='gray',lw=.7)
        ax.axvline(0,color='gray',lw=.7)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(alpha=.25)
        ax.legend()
        st.pyplot(fig,clear_figure=True)
        st.latex('y='+sp.latex(expr))
        st.caption('Illustrative graph of the expected function over a sample interval; it is not a proof of correctness.')
    finally:
        plt.close(fig)
