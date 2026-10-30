"""First-order ODE guided lessons. Exact symbolic results for supported inputs."""
import sympy as sp

x,y=sp.symbols("x y",real=True)
C=sp.Symbol("C")

def _integral(expr):
    out=sp.integrate(expr,x)
    if out.has(sp.Integral):
        raise ValueError("An exact symbolic antiderivative was not found.")
    return sp.simplify(out)

def _validate(expr,allowed):
    expr=sp.sympify(expr)
    if expr.free_symbols-set(allowed):
        raise ValueError("Unexpected symbols in the expression.")
    return expr

def linear_solution(P,Q):
    """y' + P(x)y = Q(x); y=(∫μQ dx+C)/μ."""
    P=_validate(P,{x});Q=_validate(Q,{x})
    mu=sp.exp(_integral(P))
    numerator=_integral(mu*Q)
    solution=sp.simplify((numerator+C)/mu)
    residual=sp.simplify(sp.diff(solution,x)+P*solution-Q)
    if residual!=0:raise ValueError("Unable to verify the solution.")
    return {"factor":mu,"integral":numerator,"solution":solution}

def separable_solution(g,h):
    """y'=g(x)h(y); implicit integral of 1/h(y) dy = ∫g(x)dx + C."""
    g=_validate(g,{x});h=_validate(h,{y})
    lhs=sp.integrate(1/h,y)
    rhs=_integral(g)
    if lhs.has(sp.Integral):raise ValueError("Unable to integrate 1/h(y) symbolically.")
    if sp.simplify(sp.diff(lhs,y)*h-1)!=0 or sp.simplify(sp.diff(rhs,x)-g)!=0:
        raise ValueError("Unable to verify the separated integrals.")
    return {"left":lhs,"right":rhs,"equilibria":sp.solveset(h,y,domain=sp.S.Reals)}

def bernoulli_solution(P,Q,n):
    """y'+Py=Qy^n, n!=0,1; v=y^(1-n) obeys v'+(1-n)Pv=(1-n)Q."""
    P=_validate(P,{x});Q=_validate(Q,{x});n=sp.sympify(n)
    if n.free_symbols or n.is_integer is not True or n in (0,1) or abs(int(n))>6:
        raise ValueError("Choose an integer exponent n from -6 to 6, excluding 0 and 1.")
    factor=1-n
    transformed=linear_solution(factor*P,factor*Q)
    return {"exponent":factor,"v":transformed["solution"],"factor":transformed["factor"]}

def exponential_growth(y0,k,t):
    y0,k,t=map(sp.sympify,(y0,k,t))
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in (y0,k,t)):
        raise ValueError("Enter finite real numbers.")
    if y0.is_positive is not True or t.is_nonnegative is not True:
        raise ValueError("Initial population must be positive and time nonnegative.")
    return sp.simplify(y0*sp.exp(k*t))

def newton_cooling(T0,Ta,k,t):
    T0,Ta,k,t=map(sp.sympify,(T0,Ta,k,t))
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in (T0,Ta,k,t)):
        raise ValueError("Enter finite real numbers.")
    if k.is_positive is not True or t.is_nonnegative is not True:
        raise ValueError("Cooling coefficient must be positive and time nonnegative.")
    return sp.simplify(Ta+(T0-Ta)*sp.exp(-k*t))

def render_first_order_ode(parse):
    import streamlit as st
    st.header("Differential Equations · First-Order Methods")
    st.caption("v2.16 guided examples: separable, linear, Bernoulli, growth, and cooling. Exact and homogeneous methods remain in ODE Methods.")
    topic=st.selectbox("Lesson",["Separable equation","First-order linear equation","Bernoulli equation","Population growth model","Newton's law of cooling"],key="v216_topic")
    with st.expander("How do I enter answers and expressions?"):
        st.write("Use `x^2`, `exp(x)`, `sin(x)`, `2*x`, `1/2`. For ODEs, enter coefficient functions only; the app constructs the equation. `C` represents an arbitrary constant in the displayed solution.")
    if topic=="Separable equation":
        st.latex(r"\frac{dy}{dx}=g(x)h(y)")
        a=st.text_input("g(x)",value="2*x",key="v216_a")
        b=st.text_input("h(y)",value="y",key="v216_b")
    elif topic in ("First-order linear equation","Bernoulli equation"):
        st.latex(r"y'+P(x)y=Q(x)"+(r"y^n" if topic=="Bernoulli equation" else ""))
        a=st.text_input("P(x)",value="2",key="v216_a")
        b=st.text_input("Q(x)",value="exp(x)",key="v216_b")
        if topic=="Bernoulli equation":
            n=st.selectbox("Exponent n",[-6,-5,-4,-3,-2,-1,2,3,4,5,6],index=6,key="v216_n")
    elif topic=="Population growth model":
        st.latex(r"\frac{dP}{dt}=kP,\quad P(0)=P_0")
        a=st.text_input("Initial population P₀",value="500",key="v216_a")
        b=st.text_input("Growth rate k (per time unit)",value="1/10",key="v216_b")
        c=st.text_input("Elapsed time",value="3",key="v216_c")
    else:
        st.latex(r"\frac{dT}{dt}=-k(T-T_a)")
        a=st.text_input("Initial temperature T₀",value="90",key="v216_a")
        b=st.text_input("Ambient temperature Tₐ",value="20",key="v216_b")
        c=st.text_input("Positive cooling coefficient k",value="1/5",key="v216_c")
        d=st.text_input("Elapsed time",value="5",key="v216_d")
    from math_preview import render_preview
    if topic=="Separable equation":
        render_preview(st,parse,a,allowed=("x",),label="g(x) preview")
        render_preview(st,parse,b,allowed=("y",),label="h(y) preview")
    elif topic in ("First-order linear equation","Bernoulli equation"):
        render_preview(st,parse,a,allowed=("x",),label="P(x) preview")
        render_preview(st,parse,b,allowed=("x",),label="Q(x) preview")
    elif topic=="Population growth model":
        render_preview(st,parse,a,allowed=(),label="Initial population preview")
        render_preview(st,parse,b,allowed=(),label="Growth rate preview")
        render_preview(st,parse,c,allowed=(),label="Elapsed time preview")
    else:
        for raw_value,description in ((a,"Initial temperature"),(b,"Ambient temperature"),(c,"Cooling coefficient"),(d,"Elapsed time")):
            render_preview(st,parse,raw_value,allowed=(),label=description+" preview")
    if st.button("Solve with steps",type="primary",key="v216_solve"):
        try:
            if topic=="Separable equation":
                g,h=parse(a),parse(b)
                result=separable_solution(g,h)
                st.write("Separate the variables and integrate both sides:")
                st.latex(r"\int\frac{1}{h(y)}\,dy=\int g(x)\,dx+C")
                st.latex(sp.latex(result["left"])+"="+sp.latex(result["right"])+r"+C")
                st.caption("Any zeros of h(y) may be equilibrium solutions excluded by division. Check the original ODE and solution domains.")
            elif topic=="First-order linear equation":
                P,Q=parse(a),parse(b);res=linear_solution(P,Q)
                st.write("Find the integrating factor and multiply the ODE by it:")
                st.latex(r"\mu(x)=e^{\int P(x)\,dx}="+sp.latex(res["factor"]))
                st.latex(r"(\mu y)'=\mu Q")
                st.latex(r"y="+sp.latex(res["solution"]))
                st.success("Verified by substitution into the differential equation.")
            elif topic=="Bernoulli equation":
                P,Q=parse(a),parse(b);res=bernoulli_solution(P,Q,n)
                st.write("For nonzero y, substitute v=y^(1−n) to obtain a linear ODE:")
                st.latex("v=y^{"+str(res["exponent"])+r"}")
                st.latex(r"v'+(1-n)Pv=(1-n)Q")
                st.latex("v="+sp.latex(res["v"]))
                st.latex("y^{"+str(res["exponent"])+"}="+sp.latex(res["v"]))
                st.caption("The substitution assumes y ≠ 0. Check possible zero solutions and real-valued domains separately.")
            elif topic=="Population growth model":
                res=exponential_growth(parse(a),parse(b),parse(c))
                st.latex(r"P(t)=P_0e^{kt}")
                st.latex(r"P(t)="+sp.latex(res))
                st.write("Population at the specified time (same units as the initial population).")
            else:
                res=newton_cooling(parse(a),parse(b),parse(c),parse(d))
                st.latex(r"T(t)=T_a+(T_0-T_a)e^{-kt}")
                st.latex(r"T(t)="+sp.latex(res))
                st.write("Temperature at the specified time.")
        except Exception as exc:
            st.error(f"Unable to solve this example: {exc}")
    st.caption("Scope: selected solvable first-order equations. Piecewise solutions, singularities, and exceptional solutions may require manual analysis.")
