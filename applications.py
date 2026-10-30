from volume_visualizer import create_volume_figure
"""Selected introductory integral applications, with bounded numeric inputs."""
import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from cross_section_visualizer import SHAPES, cross_section_area, create_cross_section_figure

X=sp.Symbol('x', real=True)

def riemann(f, left, right, n, method):
    if not 1 <= n <= 200: raise ValueError('Use 1 to 200 rectangles.')
    width=(right-left)/n
    xs=[left+(i+(0 if method=='Left' else 1 if method=='Right' else .5))*width for i in range(n)]
    fn=sp.lambdify(X,f,'numpy')
    heights=np.array([float(fn(z)) for z in xs])
    if not np.all(np.isfinite(heights)): raise ValueError('Function is undefined in this interval.')
    return width*sum(heights),xs,heights,width

def area_between(f,g,a,b):
    # Exact signed integral and nonnegative geometric area (absolute difference).
    signed=sp.integrate(f-g,(X,a,b))
    geometric=sp.integrate(sp.Abs(f-g),(X,a,b))
    return signed,geometric

def volume_disks(radius,a,b): return sp.pi*sp.integrate(radius**2,(X,a,b))
def volume_washers(outer,inner,a,b): return sp.pi*sp.integrate(outer**2-inner**2,(X,a,b))
def volume_shells(radius,height,a,b): return 2*sp.pi*sp.integrate(radius*height,(X,a,b))

def arc_length(f,a,b):
    return sp.integrate(sp.sqrt(1+sp.diff(f,X)**2),(X,a,b))

def surface_revolution(f,a,b):
    # x-axis revolution; input function must represent a nonnegative radius.
    return 2*sp.pi*sp.integrate(f*sp.sqrt(1+sp.diff(f,X)**2),(X,a,b))

def improper_integral(f,a,b):
    # Supports extended-real limits and selected endpoint singularities.
    return sp.integrate(f,(X,a,b))

def numerical_integral(f,a,b,n,method):
    if not 2 <= n <= 200: raise ValueError('Use between 2 and 200 subdivisions.')
    if method == 'Simpson' and n%2: raise ValueError('Simpson requires an even number of subdivisions.')
    fn=sp.lambdify(X,f,'numpy')
    h=(b-a)/n
    ys=np.array([float(fn(a+i*h)) for i in range(n+1)],dtype=float)
    if not np.all(np.isfinite(ys)): raise ValueError('Function undefined at a sample point.')
    if method=='Trapezoidal':
        return float(h*(ys[0]/2+ys[-1]/2+np.sum(ys[1:-1])))
    return float(h/3*(ys[0]+ys[-1]+4*np.sum(ys[1:-1:2])+2*np.sum(ys[2:-1:2])))

def render_applications(parse):
    st.header('📐 Integral Applications Lab')
    st.caption('Selected introductory problems with explicit bounds and formulas. Local prototype; verify assumptions and units.')
    kind=st.selectbox('Application', ['Riemann sums','Area between curves','Volume: disks','Volume: washers','Volume: cylindrical shells','Volume: known cross-sections','Arc length','Surface area of revolution','Improper integral','Numerical integration'])
    st.info('Enter expressions using x, e^(x²), sin(x), etc. Use decimal or integer bounds. Choose valid geometry and nonnegative radii.')
    ftext=st.text_input('First function f(x)', 'x^2')
    gtext=st.text_input('Second function g(x) / inner radius / shell height (when applicable)', '0') if kind in ('Area between curves','Volume: washers','Volume: cylindrical shells') else None
    a=st.number_input('Lower x bound',value=0.0)
    b=st.number_input('Upper x bound',value=2.0)
    n=st.slider('Number of rectangles',1,100,4) if kind=='Riemann sums' else None
    subdivisions=st.number_input('Number of subdivisions',min_value=2,max_value=200,value=10,step=2) if kind=='Numerical integration' else None
    numeric_method=st.radio('Numerical method',['Trapezoidal','Simpson'],horizontal=True) if kind=='Numerical integration' else None
    improper_side=st.selectbox('Improper interval',['Upper bound +infinity','Lower bound -infinity','Both bounds infinite','Finite interval (endpoint singularity)']) if kind=='Improper integral' else None
    method=st.radio('Sample points',['Left','Right','Midpoint'],horizontal=True) if kind=='Riemann sums' else None
    volume_kind=kind.startswith('Volume:')
    cross_shape=st.selectbox('Cross-section shape', SHAPES) if kind=='Volume: known cross-sections' else None
    if volume_kind:
        st.subheader('Interactive 3D volume visualizer')
        st.caption('Rotate or zoom the solid. Disks and washers rotate about x; shells rotate about y. Known cross-sections are perpendicular to x, with base width f(x) above y=0.')
        slices=st.slider('Illustrative slices / shells',4,30,12)
        show_solid=st.checkbox('Show 3D surface',value=True)
    if st.button('Calculate application'):
        try:
            if not a<b: raise ValueError('The lower bound must be less than the upper bound.')
            f=parse(ftext)
            if f.has(sp.Symbol('y',real=True)): raise ValueError('Use x only.')
            f=f.subs(sp.Symbol('x',real=True),X)
            g=parse(gtext).subs(sp.Symbol('x',real=True),X) if gtext is not None else None
            if g is not None and g.has(sp.Symbol('y',real=True)): raise ValueError('Use x only.')
            if kind=='Riemann sums':
                val,xs,ys,width=riemann(f,a,b,n,method)
                st.latex(r'\Delta x=\frac{b-a}{n}='+sp.latex(sp.Float(width,4)))
                st.latex(r'S_n=\sum_{i=1}^{n}f(x_i^*)\Delta x')
                st.write('Sample x values:', [round(float(z),4) for z in xs])
                st.write('Function values:', [round(float(z),4) for z in ys])
                st.success(f'Riemann sum ≈ {val:.8g}')
                xx=np.linspace(a,b,250); fn=sp.lambdify(X,f,'numpy'); yy=np.array([float(fn(t)) for t in xx])
                fig,ax=plt.subplots(); ax.plot(xx,yy,label='f(x)'); ax.bar(xs,ys,width=width,align='center',alpha=.3,edgecolor='black',label='Rectangles'); ax.axhline(0,color='gray',linewidth=.8); ax.legend(); st.pyplot(fig);plt.close(fig)
                st.caption('This is a signed Riemann sum, not necessarily the geometric area.')
            elif kind=='Area between curves':
                signed,geo=area_between(f,g,a,b)
                result=geo
                st.latex(r'A=\int_a^b |f(x)-g(x)|\,dx')
                st.latex(r'\int_a^b(f-g)\,dx='+sp.latex(signed))
                st.latex(r'A='+sp.latex(geo))
                st.caption('Absolute difference handles curves that cross within the interval. Check whether your region is actually bounded by these curves and vertical lines.')
                xx=np.linspace(a,b,300)
                ff=sp.lambdify(X,f,'numpy'); gg=sp.lambdify(X,g,'numpy')
                yy=np.broadcast_to(np.asarray(ff(xx),dtype=float),xx.shape)
                zz=np.broadcast_to(np.asarray(gg(xx),dtype=float),xx.shape)
                if np.all(np.isfinite(yy)) and np.all(np.isfinite(zz)):
                    fig,ax=plt.subplots()
                    ax.plot(xx,yy,label='f(x)');ax.plot(xx,zz,label='g(x)')
                    ax.fill_between(xx,yy,zz,alpha=.25,label='Area between curves')
                    ax.legend();ax.grid(alpha=.2);st.pyplot(fig);plt.close(fig)
            elif kind=='Volume: disks':
                result=volume_disks(f,a,b)
                st.latex(r'V=\pi\int_a^b R(x)^2\,dx='+sp.latex(result))
                st.caption('Assumes rotation about the x-axis and a nonnegative radius R(x).')
            elif kind=='Volume: washers':
                result=volume_washers(f,g,a,b)
                st.latex(r'V=\pi\int_a^b(R(x)^2-r(x)^2)\,dx='+sp.latex(result))
                st.caption('Assumes rotation about x-axis and 0 ≤ inner radius ≤ outer radius throughout interval. Validate geometry before interpreting.')
            elif kind=='Volume: known cross-sections':
                result=cross_section_area(f,a,b,cross_shape)
                factor={'Squares':sp.Integer(1),'Semicircles':sp.pi/8,'Equilateral triangles':sp.sqrt(3)/4}[cross_shape]
                st.latex(r'V=\int_a^b A(x)\,dx='+sp.latex(factor)+r'\int_a^b [f(x)]^2\,dx='+sp.latex(result))
                st.caption('The base runs from y=0 to y=f(x). Cross-sections perpendicular to the x-axis have the selected shape.')
            elif kind=='Arc length':
                result=arc_length(f,a,b)
                st.latex(r'L=\int_a^b\sqrt{1+[f\prime(x)]^2}\,dx='+sp.latex(result))
                st.caption('Length of y=f(x) over the selected interval.')
            elif kind=='Surface area of revolution':
                result=surface_revolution(f,a,b)
                st.latex(r'S=2\pi\int_a^b f(x)\sqrt{1+[f\prime(x)]^2}\,dx='+sp.latex(result))
                st.caption('Rotation around x-axis. Requires f(x) >= 0 over the interval.')
            elif kind=='Improper integral':
                ia,ib={'Upper bound +infinity':(a,sp.oo),'Lower bound -infinity':(-sp.oo,b),'Both bounds infinite':(-sp.oo,sp.oo),'Finite interval (endpoint singularity)':(a,b)}[improper_side]
                result=improper_integral(f,ia,ib)
                st.latex(r'\int_{'+sp.latex(ia)+'}^{'+sp.latex(ib)+'} '+sp.latex(f)+r'\,dx='+sp.latex(result))
                if result in (sp.oo,-sp.oo,sp.zoo,sp.nan) or result.has(sp.oo,sp.zoo,sp.nan):
                    st.warning('This improper integral diverges or is undefined.')
                else: st.success('Improper integral evaluated; verify convergence conditions.')
            elif kind=='Numerical integration':
                result=numerical_integral(f,a,b,int(subdivisions),numeric_method)
                st.latex(r'I\approx '+sp.latex(sp.Float(result,9)))
                st.caption(f'{numeric_method} approximation with {subdivisions} subdivisions. This is not generally an exact integral.')
            else:
                result=volume_shells(f,g,a,b)
                st.latex(r'V=2\pi\int_a^b r(x)h(x)\,dx='+sp.latex(result))
                st.caption('Assumes nonnegative radius and height and a valid shell geometry.')
            if volume_kind:
                try:
                    fig3d=(create_cross_section_figure(f,a,b,cross_shape,slices,show_solid) if cross_shape else create_volume_figure(kind,f,g,a,b,slices,show_solid))
                    st.plotly_chart(fig3d,use_container_width=True)
                    st.caption('Illustration uses sampled surfaces; exact volume comes from the integral above. The number of visible slices does not change the exact result.')
                except (ValueError,TypeError,OverflowError) as visual_error:
                    st.warning(f'3D visualization unavailable: {visual_error}')
            if kind not in ('Riemann sums','Improper integral','Numerical integration'):
                if sp.sympify(result).has(sp.Integral): st.warning('Could not evaluate the integral symbolically.')
                else: st.success('Exact symbolic result shown above.')
        except Exception as exc:
            st.error(f'Could not calculate this example: {exc}')
    st.warning('Local prototype only. These calculations are not isolated in resource-limited workers; do not deploy publicly.')
