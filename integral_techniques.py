"""Guided integral techniques and bounded numerical integration exercises."""
import sympy as sp
x=sp.symbols('x',real=True)

def verified_antiderivative(f):
    if f.free_symbols-{x}:raise ValueError('Enter an expression in x only.')
    result=sp.integrate(f,x)
    if result.has(sp.Integral):raise ValueError('An elementary antiderivative was not found.')
    if sp.simplify(sp.diff(result,x)-f)!=0:raise ValueError('Could not verify the antiderivative.')
    return result

def substitution_example(outer,inner):
    """Integrate outer(inner(x))*inner'(x) with a verified u-substitution."""
    u=sp.symbols('u',real=True)
    if inner.free_symbols-{x} or outer.free_symbols-{u}:raise ValueError('Use x in the inner function and u in the outer function.')
    if sp.diff(inner,x)==0:raise ValueError('The inner function must vary with x.')
    integrand=sp.simplify(outer.subs(u,inner)*sp.diff(inner,x))
    primitive=verified_antiderivative(integrand)
    outer_integral=sp.integrate(outer,u)
    if outer_integral.has(sp.Integral):raise ValueError('Cannot integrate the outer function in u.')
    substituted=outer_integral.subs(u,inner)
    if sp.simplify(sp.diff(substituted,x)-integrand)!=0:raise ValueError('Substitution verification failed.')
    return {'integrand':integrand,'du':sp.diff(inner,x),'u':inner,'outer_integral':outer_integral,'answer':substituted}

def integration_by_parts(u,dv):
    if u.free_symbols-{x} or dv.free_symbols-{x}:raise ValueError('Enter functions of x only.')
    v=verified_antiderivative(dv)
    du=sp.diff(u,x)
    remainder=sp.simplify(v*du)
    remainder_primitive=verified_antiderivative(remainder)
    result=sp.simplify(u*v-remainder_primitive)
    if sp.simplify(sp.diff(result,x)-u*dv)!=0:raise ValueError('Integration by parts verification failed.')
    return {'v':v,'du':du,'remainder':remainder,'answer':result}

def partial_fractions(f):
    if f.free_symbols-{x}:raise ValueError('Enter a rational expression in x only.')
    num,den=sp.fraction(sp.cancel(f))
    if not num.is_polynomial(x) or not den.is_polynomial(x):raise ValueError('This lesson requires a rational function.')
    decomposition=sp.apart(f,x)
    answer=verified_antiderivative(f)
    return {'decomposition':decomposition,'answer':answer}

def trig_integral(f):
    if f.free_symbols-{x}:raise ValueError('Enter a trigonometric expression in x only.')
    if not f.has(sp.sin,sp.cos,sp.tan,sp.sec,sp.csc,sp.cot):raise ValueError('Enter an expression containing a trigonometric function.')
    return {'rewritten':sp.trigsimp(sp.expand_trig(f)),'answer':verified_antiderivative(f)}

def numerical_integral(f,a,b,n,method='midpoint'):
    if f.free_symbols-{x}:raise ValueError('Enter a function of x only.')
    if not isinstance(n,int) or n<1 or n>2000:raise ValueError('Number of intervals must be between 1 and 2000.')
    if method=='simpson38' and n%3:raise ValueError('Simpson 3/8 requires an interval count divisible by 3.')
    if method not in ('midpoint','simpson38'):raise ValueError('Unsupported method.')
    a=sp.sympify(a);b=sp.sympify(b)
    if a.free_symbols or b.free_symbols or a.is_real is not True or b.is_real is not True or a.is_finite is not True or b.is_finite is not True or sp.N(b-a)<=0:raise ValueError('Use finite real bounds with upper > lower.')
    fn=sp.lambdify(x,f,'math')
    af,bf=float(a),float(b)
    if abs(bf-af)>1e6:raise ValueError('Integration interval is too large for this demonstration.')
    h=(bf-af)/n
    import math
    def val(z):
        result=float(fn(z))
        if not math.isfinite(result):raise ValueError('Function is not finite at a sampled point.')
        return result
    if method=='midpoint':value=h*sum(val(af+(i+.5)*h) for i in range(n))
    else:value=3*h/8*(val(af)+val(bf)+sum((2 if i%3==0 else 3)*val(af+i*h) for i in range(1,n)))
    return value

def render_integral_techniques(parse):
    import streamlit as st
    st.header('Integral Calculus · Techniques')
    st.caption('v2.14: guided examples of substitution, parts, partial fractions, trigonometric integrals, and numerical integration.')
    lesson=st.selectbox('Technique',['Substitution','Integration by parts','Partial fractions','Trigonometric integrals','Numerical integration'],key='v214_lesson')
    with st.expander('How do I enter expressions?'):
        st.write('Use `x^2`, `3*x`, `sin(x)`, `cos(x)`, `exp(x)`, `1/(x^2-1)`. For substitution, the outer function uses `u` and the inner function uses `x`.')
    if lesson=='Substitution':
        outer=st.selectbox('Outer function F(u)',['u^2','sin(u)','cos(u)','exp(u)','1/u'],key='v214_outer')
        inner=st.text_input('Inner function u = g(x)',value='x^2+1',key='v214_inner')
    elif lesson=='Integration by parts':
        raw_u=st.text_input('Choose u(x)',value='x',key='v214_u')
        raw_dv=st.text_input('Choose dv/dx',value='exp(x)',key='v214_dv')
    elif lesson=='Partial fractions':raw_f=st.text_input('Rational integrand',value='1/(x^2-1)',key='v214_partial')
    elif lesson=='Trigonometric integrals':raw_f=st.text_input('Trigonometric integrand',value='sin(x)*cos(x)',key='v214_trig')
    else:
        raw_f=st.text_input('Integrand f(x)',value='x^2',key='v214_num_f')
        raw_a=st.text_input('Lower bound',value='0',key='v214_a')
        raw_b=st.text_input('Upper bound',value='2',key='v214_b')
        n=st.number_input('Number of equal intervals',min_value=1,max_value=2000,value=6,step=1,key='v214_n')
        method=st.selectbox('Method',['Midpoint rule','Simpson 3/8 rule'],key='v214_method')
    from math_preview import render_preview
    if lesson=="Substitution":
        render_preview(st,parse,inner,label="Inner function preview")
    elif lesson=="Integration by parts":
        render_preview(st,parse,raw_u,label="u(x) preview")
        render_preview(st,parse,raw_dv,label="dv/dx preview")
    else:
        render_preview(st,parse,raw_f,label="Integrand preview")
    if lesson=="Numerical integration":
        render_preview(st,parse,raw_a,allowed=(),label="Lower bound preview")
        render_preview(st,parse,raw_b,allowed=(),label="Upper bound preview")
    if st.button('Calculate and explain',type='primary',key='v214_run'):
        try:
            if lesson=='Substitution':
                u=sp.symbols('u',real=True)
                outer_map={'u^2':u**2,'sin(u)':sp.sin(u),'cos(u)':sp.cos(u),'exp(u)':sp.exp(u),'1/u':1/u}
                r=substitution_example(outer_map[outer],parse(inner))
                st.latex('u='+sp.latex(r['u'])+',\\quad du='+sp.latex(r['du'])+'\\,dx')
                st.latex('\\int '+sp.latex(r['integrand'])+'\\,dx=\\int '+sp.latex(outer_map[outer])+'\\,du')
                st.latex('='+sp.latex(r['outer_integral'])+'+C='+sp.latex(r['answer'])+'+C')
            elif lesson=='Integration by parts':
                u=parse(raw_u);dv=parse(raw_dv);r=integration_by_parts(u,dv)
                st.latex('\\int u\\,dv=uv-\\int v\\,du')
                st.latex('v='+sp.latex(r['v'])+',\\quad du='+sp.latex(r['du'])+'\\,dx')
                st.latex('\\int '+sp.latex(u*dv)+'\\,dx='+sp.latex(u*r['v'])+'-\\int '+sp.latex(r['remainder'])+'\\,dx')
                st.latex('='+sp.latex(r['answer'])+'+C')
            elif lesson=='Partial fractions':
                r=partial_fractions(parse(raw_f));st.latex(sp.latex(r['decomposition']))
                st.write('Decompose the rational function into simpler fractions, then integrate term by term.')
                st.latex('\\int f(x)\\,dx='+sp.latex(r['answer'])+'+C')
            elif lesson=='Trigonometric integrals':
                r=trig_integral(parse(raw_f));st.latex('f(x)='+sp.latex(r['rewritten']))
                st.latex('\\int f(x)\\,dx='+sp.latex(r['answer'])+'+C')
            else:
                f=parse(raw_f);a=parse(raw_a);b=parse(raw_b)
                key='midpoint' if method=='Midpoint rule' else 'simpson38'
                approx=numerical_integral(f,a,b,int(n),key)
                st.latex('\\Delta x=\\frac{b-a}{n}='+sp.latex((b-a)/n))
                st.write(f'Approximate integral ({method}): **{approx:.10g}**')
                exact=sp.integrate(f,(x,a,b))
                if not exact.has(sp.Integral) and exact.is_finite is True:
                    st.latex('\\int_{'+sp.latex(a)+'}^{'+sp.latex(b)+'}'+sp.latex(f)+'\\,dx='+sp.latex(exact))
                    st.write(f'Absolute error: {abs(approx-float(exact)):.6g}')
                st.caption('Numerical quadrature assumes the integrand is well-behaved on the entire interval; sampled values alone cannot guarantee this.')
            st.success('Result computed. Verify the domain and any singularities for your specific problem.')
        except Exception as exc:st.error(f'Could not complete this example: {exc}')
    st.caption('These are guided introductory examples. Full general-purpose method detection and detailed proofs remain future work.')
