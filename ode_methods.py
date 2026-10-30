"""Additional educational ODE methods; restricted parser supplied by app."""
import sympy as s
import streamlit as st

X,Y=s.symbols('x y', real=True)

def exact_solution(M,N):
    if s.simplify(s.diff(M,Y)-s.diff(N,X)) != 0:
        raise ValueError('Not exact: ∂M/∂y does not equal ∂N/∂x. Try a different method.')
    potential=s.integrate(M,X)
    if potential.has(s.Integral): raise ValueError('Cannot integrate M symbolically in this prototype.')
    correction=s.simplify(N-s.diff(potential,Y))
    if correction.has(X): raise ValueError('Could not establish a y-only correction term.')
    correction_int=s.integrate(correction,Y)
    if correction_int.has(s.Integral): raise ValueError('Cannot integrate the correction term symbolically.')
    phi=s.simplify(potential+correction_int)
    if s.simplify(s.diff(phi,X)-M)!=0 or s.simplify(s.diff(phi,Y)-N)!=0:
        raise ValueError('Potential function verification failed.')
    return phi, correction

def homogeneous_rhs(F):
    t=s.symbols('t',real=True)
    test=s.simplify(F.subs({X:t*X,Y:t*Y}, simultaneous=True)-F)
    if test!=0: raise ValueError('F(x,y) is not verified as degree-zero homogeneous.')
    v=s.symbols('v',real=True)
    transformed=s.simplify(F.subs(Y,v*X)-v)
    if transformed.has(X): raise ValueError('The substitution did not eliminate x.')
    antiderivative=s.integrate(1/transformed,v)
    if antiderivative.has(s.Integral): raise ValueError('The transformed integral is not supported symbolically.')
    return transformed,antiderivative

def render_ode_methods(parse):
    st.header('Differential Equations · Additional Methods')
    st.info('Educational methods for selected first-order equations. Verify domains and exceptional solutions separately. Local testing only.')
    method=st.selectbox('Choose a method',['Exact equations: M dx + N dy = 0','Homogeneous substitution: dy/dx = F(x,y)'])
    from math_preview import render_preview
    if method.startswith('Exact'):
        m=st.text_input('M(x,y)',value='2*x*y+1',key='v227_exact_m')
        n=st.text_input('N(x,y)',value='x^2+2*y',key='v227_exact_n')
        render_preview(st,parse,m,allowed=('x','y'),label='M(x,y) preview')
        render_preview(st,parse,n,allowed=('x','y'),label='N(x,y) preview')
    else:
        f=st.text_input('F(x,y)',value='1+y/x',key='v227_homogeneous_f')
        render_preview(st,parse,f,allowed=('x','y'),label='F(x,y) preview')
    submit=st.button('Solve',type='primary',key='v227_ode_solve')
    if not submit:return
    try:
        if method.startswith('Exact'):
            M,N=parse(m),parse(n)
            phi,correction=exact_solution(M,N)
            st.subheader('Step-by-step solution')
            st.latex(r'\frac{\partial M}{\partial y}='+s.latex(s.diff(M,Y))+r',\quad \frac{\partial N}{\partial x}='+s.latex(s.diff(N,X)))
            st.write('Step 1: Compare the two partial derivatives. They match, so the differential form is exact.')
            st.write('Step 2: Integrate M with respect to x while treating y as constant.')
            st.latex(r'\Phi(x,y)=\int M\,dx+h(y)')
            st.write('Step 3: Differentiate the potential with respect to y, then match N to find h\u2032(y).')
            st.latex(r'h\prime(y)='+s.latex(correction))
            st.write('Step 4: Integrate the correction and write the implicit solution.')
            st.latex(s.latex(phi)+r'=C')
            st.success('Verified: Φₓ = M and Φᵧ = N.')
        else:
            F=parse(f)
            transformed,antiderivative=homogeneous_rhs(F)
            st.subheader('Step-by-step solution')
            st.write('Confirmed that F(tx,ty)=F(x,y). Let y=vx, so dy/dx=v+x dv/dx.')
            st.latex(r'x\frac{dv}{dx}='+s.latex(transformed))
            st.latex(r'\int \frac{dv}{'+s.latex(transformed)+r'}=\ln|x|+C')
            st.latex(s.latex(antiderivative.subs(s.Symbol('v',real=True),Y/X))+r'=\ln|x|+C')
            st.warning('Implicit general solution for x ≠ 0, where divisions are defined. Check constant-v solutions separately when the transformed right side is zero.')
    except (ValueError,SyntaxError,TypeError,ZeroDivisionError,NotImplementedError,s.SympifyError) as e:
        st.error(str(e))
    except Exception:
        st.error('Unable to complete this example with the supported method.')
