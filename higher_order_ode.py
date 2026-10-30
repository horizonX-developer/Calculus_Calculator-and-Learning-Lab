"""Second-order constant-coefficient ODE lessons and basic Laplace transforms."""
import sympy as sp
x=sp.symbols('x',real=True)
s=sp.symbols('s',positive=True)
y=sp.Function('y')

def _const(v):
    v=sp.sympify(v)
    if v.free_symbols or v.is_real is not True or v.is_finite is not True:
        raise ValueError('Coefficients must be finite real constants.')
    return v

def characteristic(a,b,c):
    a,b,c=map(_const,(a,b,c))
    if a==0:raise ValueError('Leading coefficient a must not be zero.')
    disc=sp.simplify(b*b-4*a*c)
    roots=(sp.simplify((-b+sp.sqrt(disc))/(2*a)),sp.simplify((-b-sp.sqrt(disc))/(2*a)))
    if disc.is_positive:kind='distinct real roots'
    elif disc.is_zero:kind='repeated real root'
    elif disc.is_negative:kind='complex conjugate roots'
    else:raise ValueError('Could not classify the discriminant.')
    return {'polynomial':a*sp.Symbol('r')**2+b*sp.Symbol('r')+c,'discriminant':disc,'roots':roots,'kind':kind}

def solve_second_order(a,b,c,forcing=0):
    a,b,c=map(_const,(a,b,c))
    if a==0:raise ValueError('Leading coefficient a must not be zero.')
    forcing=sp.sympify(forcing)
    if forcing.free_symbols-{x}:raise ValueError('Forcing must be a function of x only.')
    if forcing.has(sp.Derivative,sp.Integral):raise ValueError('Enter an explicit forcing expression.')
    equation=sp.Eq(a*sp.diff(y(x),x,2)+b*sp.diff(y(x),x)+c*y(x),forcing)
    solution=sp.dsolve(equation,y(x))
    if not isinstance(solution,sp.Equality):raise ValueError('No explicit solution available.')
    result=solution.rhs
    residual=sp.simplify(a*sp.diff(result,x,2)+b*sp.diff(result,x)+c*result-forcing)
    if residual!=0:raise ValueError('The symbolic solution could not be verified.')
    return {'equation':equation,'solution':result,'characteristic':characteristic(a,b,c)}

def laplace_basic(expr):
    expr=sp.sympify(expr)
    if expr.free_symbols-{x}:raise ValueError('Use x as the independent variable.')
    result,abscissa,condition=sp.laplace_transform(expr,x,s)
    if result.has(sp.LaplaceTransform) or result.has(sp.Integral):
        raise ValueError('Closed-form Laplace transform not available.')
    return {'transform':sp.simplify(result),'abscissa':abscissa,'condition':condition}

def render_higher_order_ode(parse):
    import streamlit as st
    st.header('Higher-Order Differential Equations')
    st.caption('v2.17: second-order constant-coefficient ODEs and introductory Laplace transforms.')
    lesson=st.selectbox('Lesson',['Homogeneous second-order ODE','Nonhomogeneous second-order ODE','Laplace transform'],key='v217_lesson')
    with st.expander('How to enter expressions'):
        st.write('Use `x^2`, `exp(x)`, `sin(x)`, `cos(2*x)`, or `3*x`. Enter coefficients as `2`, `-3`, or `1/2`.')
    if lesson=='Laplace transform':
        raw=st.text_input('Function f(x)',value='exp(-2*x)*sin(3*x)',key='v217_transform')
    else:
        st.latex(r'a y^{\prime\prime}+b y^{\prime}+c y=g(x)')
        a=st.text_input('a',value='1',key='v217_a')
        b=st.text_input('b',value='-3',key='v217_b')
        c=st.text_input('c',value='2',key='v217_c')
        if lesson.startswith('Nonhomogeneous'):
            forcing=st.text_input('Forcing function g(x)',value='exp(x)',key='v217_force')
    from math_preview import render_preview
    if lesson!='Laplace transform':
        for value,description in ((a,'a'),(b,'b'),(c,'c')):
            render_preview(st,parse,value,allowed=(),label=description+' coefficient preview')
    if lesson=='Laplace transform':
        render_preview(st,parse,raw,allowed=('x',),label='Function preview')
    elif lesson.startswith('Nonhomogeneous'):
        render_preview(st,parse,forcing,allowed=('x',),label='Forcing function preview')
    if st.button('Solve and explain',type='primary',key='v217_solve'):
        try:
            if lesson=='Laplace transform':
                f=parse(raw);res=laplace_basic(f)
                st.latex(r'\mathcal{L}\{f(x)\}=\int_0^\infty e^{-sx}f(x)\,dx')
                st.latex(r'\mathcal{L}\{'+sp.latex(f)+r'\}='+sp.latex(res['transform']))
                st.caption('Transform convergence depends on s and the function; this tool returns the symbolic transform and its convergence information.')
                st.write('Convergence abscissa:',str(res['abscissa']))
                st.write('Additional condition:',str(res['condition']))
            else:
                aa,bb,cc=map(parse,(a,b,c))
                g=parse(forcing) if lesson.startswith('Nonhomogeneous') else sp.Integer(0)
                res=solve_second_order(aa,bb,cc,g)
                char=res['characteristic']
                st.latex(sp.latex(res['equation']))
                st.write('Step 1: Solve the associated homogeneous characteristic equation.')
                st.latex(sp.latex(char['polynomial'])+'=0')
                st.write('Step 2: Classify the roots to choose the form of the homogeneous solution.')
                st.write('Root type:',char['kind'])
                st.latex('r_1='+sp.latex(char['roots'][0])+',\\quad r_2='+sp.latex(char['roots'][1]))
                if g!=0:st.write('Step 3: Find a particular solution for the forcing term and add it to the homogeneous solution.')
                st.write('General solution (verified by substitution):')
                st.latex('y(x)='+sp.latex(res['solution']))
        except Exception as exc:
            st.error(f'Unable to solve this example: {exc}')
    st.caption('Scope: second-order linear ODEs with constant real coefficients; Laplace transforms of supported functions. Initial-value problems, inverse transforms, systems, and variable-coefficient equations are future topics.')
