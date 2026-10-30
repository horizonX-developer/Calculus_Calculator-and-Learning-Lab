"""Differential calculus foundations: verified symbolic limits and first principles."""
import sympy as sp
x=sp.symbols('x',real=True)
h=sp.symbols('h',real=True)

def evaluate_limits(expr, point):
    left=sp.limit(expr,x,point,dir='-')
    right=sp.limit(expr,x,point,dir='+')
    exists=left==right or sp.simplify(left-right)==0
    return {'left':left,'right':right,'exists':bool(exists),'limit':left if exists else None}

def check_continuity(expr,point,value=None):
    result=evaluate_limits(expr,point)
    at=sp.simplify(expr.subs(x,point)) if value is None else value
    defined=at.is_finite is True
    continuous=bool(result['exists'] and defined and sp.simplify(result['limit']-at)==0)
    return {**result,'value':at,'defined':defined,'continuous':continuous}

def first_principles(expr):
    quotient=sp.cancel((expr.subs(x,x+h)-expr)/h)
    result=sp.limit(quotient,h,0)
    if sp.simplify(result-sp.diff(expr,x))!=0:
        raise ValueError('First-principles result could not be verified.')
    return quotient,result

def classify_discontinuity(left,right,value):
    if left!=right and sp.simplify(left-right)!=0:
        return 'jump or infinite discontinuity (one-sided limits disagree)'
    if left in (sp.oo,-sp.oo,sp.zoo,sp.nan):
        return 'infinite discontinuity'
    if value is None or value.is_finite is not True or sp.simplify(left-value)!=0:
        return 'removable discontinuity (limit exists but value differs or is undefined)'
    return 'continuous'

def render_foundations(parse):
    import streamlit as st
    st.header('Differential Calculus · Foundations')
    st.caption('Limits, continuity, and the derivative from first principles. This is an introductory module, not yet full curriculum coverage.')
    topic=st.selectbox('Lesson',['One-sided and two-sided limits','Continuity at a point','Derivative from first principles'])
    with st.expander('How do I enter expressions?',expanded=False):
        st.write('Use `x^2`, `(x^2-1)/(x-1)`, `sin(x)`, `sqrt(x)`, or `exp(x)`. Use `*` for multiplication. Enter the point separately.')
    raw=st.text_input('Function f(x)',value='(x^2-1)/(x-1)' if topic!='Derivative from first principles' else 'x^2+3*x')
    point_raw=st.text_input('Approach/evaluation point',value='1') if topic!='Derivative from first principles' else None
    custom_value=st.checkbox('Specify a separately defined f(a) value',value=False) if topic=='Continuity at a point' else False
    value_raw=st.text_input('Value f(a)',value='2') if custom_value else None
    if st.button('Analyze lesson',type='primary'):
        try:
            f=parse(raw)
            if f.free_symbols-{x}:raise ValueError('Enter a function of x only.')
            if topic=='Derivative from first principles':
                q,answer=first_principles(f)
                st.latex(r"f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}h")
                st.latex(r'\frac{f(x+h)-f(x)}h='+sp.latex(q))
                st.latex(r"f'(x)="+sp.latex(answer))
                st.success('Verified against symbolic differentiation.')
            else:
                a=parse(point_raw)
                if a.free_symbols or a.is_real is not True or a.is_finite is not True:raise ValueError('The point must be a finite real constant.')
                if topic=='One-sided and two-sided limits':
                    r=evaluate_limits(f,a)
                    st.latex(r'\lim_{x\to '+sp.latex(a)+r'^-}f(x)='+sp.latex(r['left']))
                    st.latex(r'\lim_{x\to '+sp.latex(a)+r'^+}f(x)='+sp.latex(r['right']))
                    st.write('Two-sided limit: '+(str(r['limit']) if r['exists'] else 'does not exist'))
                else:
                    v=parse(value_raw) if custom_value else None
                    if v is not None and v.free_symbols:raise ValueError('The specified function value must be constant.')
                    r=check_continuity(f,a,v)
                    st.latex(r'\lim_{x\to a^-}f(x)='+sp.latex(r['left']))
                    st.latex(r'\lim_{x\to a^+}f(x)='+sp.latex(r['right']))
                    st.latex(r'f(a)='+sp.latex(r['value']))
                    st.write('Classification: '+classify_discontinuity(r['left'],r['right'],r['value']))
                    st.write('Continuous at the point: **'+('Yes' if r['continuous'] else 'No')+'**')
        except Exception as exc:st.error(f'Could not analyze this example: {exc}')
    st.info('Note: an algebraically simplified expression can lose information about a hole in its original domain. For a removable discontinuity, specify f(a) explicitly when necessary.')
