"""Additional introductory integral applications with symbolic results."""
import sympy as sp
X=sp.Symbol("x",real=True)

def _bounds(a,b):
    a,b=sp.sympify(a),sp.sympify(b)
    if a.free_symbols or b.free_symbols or a.is_real is not True or b.is_real is not True or a.is_finite is not True or b.is_finite is not True or sp.ask(sp.Q.positive(b-a)) is not True:
        raise ValueError("Bounds must be finite real numbers with lower < upper.")
    return a,b

def _function(f):
    f=sp.sympify(f)
    if f.free_symbols-{X}:
        raise ValueError("Enter a function of x only.")
    return f

def _integrate(f,a,b):
    result=sp.integrate(f,(X,a,b))
    if result.has(sp.Integral) or result.is_real is False or result.is_finite is False:
        raise ValueError("Integral is not available as a finite exact result.")
    return sp.simplify(result)

def average_value(f,a,b):
    a,b=_bounds(a,b); f=_function(f)
    return sp.simplify(_integrate(f,a,b)/(b-a))

def area_under_nonnegative_curve(f,a,b):
    a,b=_bounds(a,b); f=_function(f)
    # Require a nonnegative polynomial on the entire interval (critical points + endpoints).
    if not f.is_polynomial(X):
        raise ValueError("This introductory centroid lesson supports polynomial heights only.")
    d=sp.diff(f,X)
    roots=sp.solveset(d,X,domain=sp.Interval(a,b))
    if roots == sp.S.EmptySet: roots=[]
    if not isinstance(roots,(sp.FiniteSet,list)):
        if d==0: roots=[]
        else: raise ValueError("Unable to verify the curve stays nonnegative.")
    if len(roots)>40:raise ValueError("Too many stationary points.")
    for pt in [a,b,*roots]:
        value=sp.simplify(f.subs(X,pt))
        if value.is_nonnegative is not True:
            raise ValueError("Height must be nonnegative throughout the interval.")
    return _integrate(f,a,b)

def centroid_under_curve(f,a,b):
    a,b=_bounds(a,b); f=_function(f)
    area=area_under_nonnegative_curve(f,a,b)
    if area.is_positive is not True: raise ValueError("The area must be positive.")
    mx=_integrate(X*f,a,b)
    my=_integrate(f**2/2,a,b)
    return {"area":area,"x_bar":sp.simplify(mx/area),"y_bar":sp.simplify(my/area),"moment_y":mx,"moment_x":my}

def hydrostatic_force_vertical_plate(width,top_depth,bottom_depth,density=1000,gravity=sp.Rational(981,100)):
    """Rectangular vertical plate width in meters; depths below water surface."""
    w=sp.sympify(width); rho=sp.sympify(density); g=sp.sympify(gravity)
    a,b=_bounds(top_depth,bottom_depth)
    if any(v.free_symbols or v.is_real is not True or v.is_positive is not True or v.is_finite is not True for v in (w,rho,g)):
        raise ValueError("Width, density and gravitational acceleration must be positive constants.")
    return sp.simplify(rho*g*w*_integrate(X,a,b))

def pumping_work_cylindrical_tank(area,water_depth,tank_height,density=1000,gravity=sp.Rational(981,100)):
    """Pump water to the top rim; tank bottom at y=0, constant cross-sectional area."""
    A=sp.sympify(area); h=sp.sympify(water_depth); H=sp.sympify(tank_height)
    rho=sp.sympify(density); g=sp.sympify(gravity)
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in (A,h,H,rho,g)):
        raise ValueError("Enter finite real constants.")
    if any(v.is_positive is not True for v in (A,h,H,rho,g)) or sp.ask(sp.Q.nonnegative(H-h)) is not True:
        raise ValueError("Require 0 < water depth <= tank height and positive constants.")
    y=sp.Symbol("y",real=True)
    return sp.simplify(sp.integrate(rho*g*A*(H-y),(y,0,h)))

def render_integral_expansion(parse):
    import streamlit as st
    import numpy as np
    import matplotlib.pyplot as plt
    st.header("Integral Applications · Expanded")
    st.caption("v2.15: average value, centroid, hydrostatic force, and pumping work. Assumes SI units for physical applications.")
    kind=st.selectbox("Lesson",["Average value of a function","Centroid of a region under a curve","Hydrostatic force on a vertical rectangular plate","Pumping water from a cylindrical tank"],key="v215_lesson")
    with st.expander("How do I enter values?"):
        st.write("Functions: `x^2`, `2*x+1`, `sin(x)`; use `*` for multiplication. Enter constants as `2`, `3/2`, or `pi`. For force and work use meters, kg/m³, and m/s².")
    if kind in ("Average value of a function","Centroid of a region under a curve"):
        raw=st.text_input("Function f(x)",value="x^2",key="v215_function")
        a=st.text_input("Lower bound",value="0",key="v215_a")
        b=st.text_input("Upper bound",value="2",key="v215_b")
    elif kind=="Hydrostatic force on a vertical rectangular plate":
        width=st.text_input("Plate width (m)",value="2")
        a=st.text_input("Depth of plate top below water surface (m)",value="1")
        b=st.text_input("Depth of plate bottom below water surface (m)",value="3")
    else:
        area=st.text_input("Tank horizontal cross-sectional area (m²)",value="2")
        depth=st.text_input("Water depth (m)",value="3")
        height=st.text_input("Tank height / outlet elevation (m)",value="5")
    from math_preview import render_preview
    if kind in ("Average value of a function","Centroid of a region under a curve"):
        render_preview(st,parse,raw,label="Function preview")
    if st.button("Calculate and explain",type="primary",key="v215_solve"):
        try:
            if kind=="Average value of a function":
                f=parse(raw);lo=parse(a);hi=parse(b)
                value=average_value(f,lo,hi)
                st.latex(r"f_{\mathrm{avg}}=\frac{1}{b-a}\int_a^b f(x)\,dx")
                st.latex(r"f_{\mathrm{avg}}="+sp.latex(value))
            elif kind=="Centroid of a region under a curve":
                f=parse(raw);lo=parse(a);hi=parse(b)
                result=centroid_under_curve(f,lo,hi)
                st.latex(r"A=\int_a^b f(x)\,dx="+sp.latex(result["area"]))
                st.latex(r"\bar{x}=\frac{\int_a^b xf(x)\,dx}{A}="+sp.latex(result["x_bar"]))
                st.latex(r"\bar{y}=\frac{\frac12\int_a^b f(x)^2\,dx}{A}="+sp.latex(result["y_bar"]))
                xs=np.linspace(float(lo),float(hi),250)
                fn=sp.lambdify(X,f,"numpy")
                ys=np.broadcast_to(np.asarray(fn(xs),dtype=float),xs.shape)
                if not np.all(np.isfinite(ys)):raise ValueError("Cannot graph this function.")
                fig,ax=plt.subplots()
                ax.plot(xs,ys,label="f(x)");ax.fill_between(xs,0,ys,alpha=.2)
                ax.scatter([float(result["x_bar"])],[float(result["y_bar"])],label="Centroid",zorder=4)
                ax.legend();ax.set_xlabel("x");ax.set_ylabel("y")
                st.pyplot(fig);plt.close(fig)
            elif kind=="Hydrostatic force on a vertical rectangular plate":
                w=parse(width);lo=parse(a);hi=parse(b)
                val=hydrostatic_force_vertical_plate(w,lo,hi)
                st.latex(r"F=\rho g w\int_{d_1}^{d_2}y\,dy")
                st.latex(r"F="+sp.latex(val)+r"\ \mathrm{N}")
                st.caption("Assumes a fully submerged vertical rectangular plate in freshwater (density 1000 kg/m³).")
            else:
                A=parse(area);h=parse(depth);H=parse(height)
                val=pumping_work_cylindrical_tank(A,h,H)
                st.latex(r"W=\rho g A\int_0^h(H-y)\,dy")
                st.latex(r"W="+sp.latex(val)+r"\ \mathrm{J}")
                st.caption("Assumes a constant-area tank, water pumped to the top rim, and no energy losses.")
        except Exception as exc:
            st.error(f"Unable to calculate: {exc}")
