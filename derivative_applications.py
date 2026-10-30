"""Differential calculus applications: symbolic derivatives, extrema, and related rates."""
import sympy as sp

x=sp.symbols("x", real=True)
t=sp.symbols("t", real=True)

def derivative_rules(expr, order=1):
    if not isinstance(order,int) or not 1<=order<=5:
        raise ValueError("Derivative order must be from 1 to 5.")
    if expr.free_symbols-{x}:
        raise ValueError("Enter a function of x only.")
    steps=[]
    current=expr
    for n in range(1,order+1):
        current=sp.diff(current,x)
        steps.append((n,sp.simplify(current)))
    return steps

def tangent_line(expr, point):
    if expr.free_symbols-{x} or point.free_symbols:
        raise ValueError("Enter a function of x and a constant point.")
    y0=sp.simplify(expr.subs(x,point))
    m=sp.simplify(sp.diff(expr,x).subs(x,point))
    if y0.is_real is not True or y0.is_finite is not True or m.is_real is not True or m.is_finite is not True:
        raise ValueError("The function and derivative must be finite and real at the point.")
    return {"point":(point,y0),"slope":m,"line":sp.expand(y0+m*(x-point))}

def critical_points(expr):
    if expr.free_symbols-{x}:
        raise ValueError("Enter a function of x only.")
    d=sp.diff(expr,x)
    roots=sp.solveset(d,x,domain=sp.S.Reals)
    if not isinstance(roots,sp.FiniteSet):
        raise ValueError("Critical points cannot be enumerated exactly for this function.")
    if len(roots)>25:
        raise ValueError("Too many critical points to list.")
    out=[]
    second=sp.diff(expr,x,2)
    for a in sorted(roots,key=lambda v:float(sp.N(v))):
        y=sp.simplify(expr.subs(x,a))
        if y.is_real is not True or y.is_finite is not True:
            continue
        curvature=sp.simplify(second.subs(x,a))
        kind="local minimum" if curvature.is_positive else "local maximum" if curvature.is_negative else "inconclusive (second derivative test)"
        out.append((a,y,kind))
    return out

def rectangle_optimization(perimeter):
    p=sp.sympify(perimeter)
    if p.free_symbols or p.is_real is not True or p.is_positive is not True or p.is_finite is not True:
        raise ValueError("Perimeter must be a positive finite real constant.")
    width=sp.symbols("w",positive=True)
    area=sp.expand(width*(p/2-width))
    optimum=sp.simplify(p/4)
    return {"area_function":area,"derivative":sp.diff(area,width),"width":optimum,"length":optimum,"max_area":sp.simplify(p**2/16)}

def circle_area_related_rate(radius, dr_dt):
    r=sp.sympify(radius)
    rate=sp.sympify(dr_dt)
    if r.free_symbols or rate.free_symbols or r.is_real is not True or r.is_positive is not True or r.is_finite is not True or rate.is_real is not True or rate.is_finite is not True:
        raise ValueError("Radius must be positive and both inputs must be finite real constants.")
    return sp.simplify(2*sp.pi*r*rate)

def render_derivative_applications(parse):
    import streamlit as st
    st.header("Differential Calculus · Derivatives and Applications")
    st.caption("v2.13: derivative rules, tangents, critical points, introductory optimization, and related rates.")
    topic=st.selectbox("Lesson",["Derivative rules","Tangent line","Critical points","Optimization: rectangle","Related rates: circle"],key="v213_lesson")
    with st.expander("How should I enter the problem?"):
        st.write("Functions: `x^3-3*x`, `sin(x)`, `exp(x)`, `(x^2+1)/(x+1)`. Use `*` for multiplication. Numeric inputs: `4`, `3/2`, or `pi`.")
    if topic in ("Derivative rules","Tangent line","Critical points"):
        raw=st.text_input("Function f(x)",value="x^3-3*x",key="v213_function")
    from math_preview import render_preview
    if topic in ("Derivative rules","Tangent line","Critical points"):
        render_preview(st,parse,raw,label="Function preview")
    if topic=="Derivative rules":
        order=st.slider("Derivative order",1,5,1)
    elif topic=="Tangent line":
        raw_point=st.text_input("x-coordinate of tangency",value="2")
    elif topic=="Optimization: rectangle":
        raw_perimeter=st.text_input("Rectangle perimeter",value="40")
    elif topic=="Related rates: circle":
        raw_radius=st.text_input("Circle radius",value="3")
        raw_rate=st.text_input("Rate of radius change dr/dt",value="2")
    if st.button("Solve and explain",type="primary",key="v213_solve"):
        try:
            if topic=="Derivative rules":
                f=parse(raw)
                st.latex("f(x)="+sp.latex(f))
                for n,derivative in derivative_rules(f,order):
                    st.latex("f^{("+str(n)+")}(x)="+sp.latex(derivative))
                st.write("Each derivative is obtained by differentiating the preceding expression with respect to x.")
            elif topic=="Tangent line":
                f=parse(raw); a=parse(raw_point)
                result=tangent_line(f,a)
                st.latex("f'(x)="+sp.latex(sp.diff(f,x)))
                st.latex("m=f'("+sp.latex(a)+")="+sp.latex(result["slope"]))
                st.latex("y-f(a)=m(x-a)")
                st.latex("y="+sp.latex(result["line"]))
            elif topic=="Critical points":
                f=parse(raw)
                st.latex("f'(x)="+sp.latex(sp.diff(f,x)))
                st.write("Solve f'(x) = 0 and classify with the second derivative test:")
                pts=critical_points(f)
                if not pts:st.info("No stationary points found.")
                for a,y,kind in pts:
                    st.latex("("+sp.latex(a)+","+sp.latex(y)+")")
                    st.write(kind)
                st.caption("This finds stationary points; nondifferentiable critical points and global endpoint extrema require separate analysis.")
            elif topic=="Optimization: rectangle":
                p=parse(raw_perimeter); result=rectangle_optimization(p)
                st.latex("A(w)=w("+sp.latex(p/2)+"-w)="+sp.latex(result["area_function"]))
                st.latex("A'(w)="+sp.latex(result["derivative"])+"=0")
                st.latex("w=l="+sp.latex(result["width"]))
                st.latex("A_{max}="+sp.latex(result["max_area"]))
                st.write("The area is a concave quadratic, so its stationary point is the maximum.")
            else:
                r=parse(raw_radius); rate=parse(raw_rate)
                st.latex("A=\\pi r^2")
                st.latex("\\frac{dA}{dt}=2\\pi r\\frac{dr}{dt}")
                st.latex("\\frac{dA}{dt}="+sp.latex(circle_area_related_rate(r,rate)))
        except Exception as exc:
            st.error(f"Unable to solve this example: {exc}")
    st.caption("Scope: introductory cases only. General constrained optimization, arbitrary related-rate geometry, and nondifferentiable extrema remain on the curriculum roadmap.")
