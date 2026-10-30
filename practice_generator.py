"""Verified, varied symbolic exercise families for all three calculus subjects."""
import random
import sympy as sp

x = sp.Symbol('x', real=True)

def _item(prompt, expected, hint, steps, kind='exact', family='General', topic=None):
    return dict(prompt=prompt, expected=sp.sstr(expected), hint=hint, steps=steps,
                kind=kind, family=family, topic=topic or family)

FAMILIES = {
 'Differential Calculus': {
  'Beginner': ('Polynomial derivatives','Trigonometric derivatives','Exponential derivatives','Tangent slopes'),
  'Intermediate': ('Chain rule','Product rule','Quotient rule','Implicit differentiation'),
  'Advanced': ('Logarithmic differentiation','Second derivatives','Optimization','Related rates')},
 'Integral Calculus': {
  'Beginner': ('Power rule','Trigonometric antiderivatives','Definite integrals','Exponential antiderivatives'),
  'Intermediate': ('U-substitution','Integration by parts','Area between curves','Riemann sums'),
  'Advanced': ('Partial fractions','Improper integrals','Volume by disks','Volume by washers')},
 'Differential Equations': {
  'Beginner': ('Exponential growth','Direct integration','Separable equations','Initial conditions'),
  'Intermediate': ('First-order linear','Bernoulli equations','Second-order homogeneous','Cooling models'),
  'Advanced': ('Repeated roots','Forced second-order','Coupled growth interpretation','Euler numerical step')}
}

def families(subject, difficulty):
    return FAMILIES[subject][difficulty]

def generate(subject, difficulty='Beginner', scenario=False, rng=None, family=None):
    r = rng if rng is not None else random.Random()
    a,b,c = r.randint(1,5),r.randint(2,6),r.randint(1,4)
    n=r.randint(2,5)
    choices=families(subject,difficulty)
    fam=family or r.choice(choices)
    if fam not in choices: raise ValueError('Topic does not belong to the chosen subject/difficulty')
    if subject=='Differential Calculus':
        if fam=='Polynomial derivatives':
            f=a*x**n+b*x-c; q=f'Differentiate f(x)={sp.sstr(f)}.'; hint='Differentiate each power separately.'
        elif fam=='Trigonometric derivatives':
            f=a*sp.sin(b*x); q=f'Differentiate f(x)={sp.sstr(f)}.'; hint='Remember the chain rule for sin(kx).'
        elif fam=='Exponential derivatives':
            f=a*sp.exp(b*x); q=f'Differentiate f(x)={sp.sstr(f)}.'; hint='The derivative of exp(u) includes u′.'
        elif fam=='Tangent slopes':
            f=a*x**2+b*x; val=sp.diff(f,x).subs(x,c)
            return _item(f'Find the slope of the tangent to y={sp.sstr(f)} at x={c}.',val,'Evaluate the derivative at the specified x.',f'f′(x)={sp.diff(f,x)}; f′({c})={val}.',family=fam)
        elif fam=='Chain rule':
            f=sp.sin(a*x**2+b); q=f'Differentiate f(x)={sp.sstr(f)}.'; hint='Set u equal to the inner polynomial.'
        elif fam=='Product rule':
            f=x**n*sp.exp(a*x); q=f'Differentiate f(x)={sp.sstr(f)}.'; hint='Use (uv)′=u′v+uv′.'
        elif fam=='Quotient rule':
            f=(a*x+b)/(x**2+c); q=f'Differentiate f(x)=({a}x+{b})/(x²+{c}).'; hint='Use (u/v)′=(vu′−uv′)/v².'
        elif fam=='Implicit differentiation':
            return _item(f'For x²+y²={b*b}, find dy/dx in terms of x and y.', '-x/y','Differentiate both sides with respect to x; y depends on x.', '2x+2y(dy/dx)=0, so dy/dx=−x/y.',family=fam)
        elif fam=='Logarithmic differentiation':
            f=(x**a)*sp.exp(b*x); q=f'Differentiate f(x)={sp.sstr(f)}.'; hint='Take logarithms or use the product rule.'
        elif fam=='Second derivatives':
            f=a*x**n+b*sp.sin(x); q=f'Find the SECOND derivative of f(x)={sp.sstr(f)}.'; hint='Differentiate twice.'
            return _item(q,sp.diff(f,x,2),hint,f'f′={sp.diff(f,x)}; f′′={sp.diff(f,x,2)}.',family=fam)
        elif fam=='Optimization':
            return _item(f'A rectangle has perimeter {4*b} meters. Find its MAXIMUM area in m².',b*b,'Use equal sides to maximize area for fixed perimeter.',f'Side lengths are {b} m and {b} m; maximum area={b*b} m².',family=fam)
        else:
            return _item(f'A circle expands at {a} cm/s. Find dA/dt when its radius is {b} cm.',2*sp.pi*a*b,'Differentiate A=πr² with respect to time.',f'dA/dt=2πr dr/dt=2π({b})({a})={2*a*b}π cm²/s.',family=fam)
        ans=sp.diff(f,x)
        return _item(q,ans,hint,f'Apply the appropriate differentiation rule: f′(x)={sp.sstr(ans)}.',family=fam)
    if subject=='Integral Calculus':
        if fam=='Power rule':
            f=a*x**n; hint='Increase the exponent by one, then divide.'
        elif fam=='Trigonometric antiderivatives':
            f=a*sp.cos(b*x); hint='Use the standard cosine antiderivative and chain-rule adjustment.'
        elif fam=='Exponential antiderivatives':
            f=a*sp.exp(b*x); hint='Divide by the coefficient of x in the exponent.'
        elif fam=='U-substitution':
            f=2*a*x*sp.cos(a*x*x+b); hint='Let u=ax²+b.'
        elif fam=='Integration by parts':
            f=x*sp.exp(a*x); hint='Use u=x, dv=exp(ax)dx.'
        elif fam=='Partial fractions':
            f=1/((x+a)*(x+b+a)); hint='Decompose into simple rational terms.'
        elif fam=='Definite integrals':
            f=a*x**2; val=sp.integrate(f,(x,0,b))
            return _item(f'Evaluate ∫₀^{b} {a}x² dx.',val,'Find an antiderivative, then evaluate at both bounds.',f'[{a}x³/3]₀^{b}={val}.',family=fam)
        elif fam=='Area between curves':
            val=sp.integrate(a*x,(x,0,b))
            return _item(f'Find the area between y={a}x and y=0 on [0,{b}].',val,'Integrate top minus bottom.',f'A=∫₀^{b} {a}x dx={val}.',family=fam)
        elif fam=='Riemann sums':
            width=sp.Rational(b,n); val=sum(a*(i*width)*width for i in range(1,n+1))
            return _item(f'Compute the RIGHT Riemann sum for f(x)={a}x on [0,{b}] using {n} rectangles.',val,'Compute Δx and sum right-endpoint heights times Δx.',f'Δx={width}; sum={sp.sstr(val)}.',family=fam)
        elif fam=='Improper integrals':
            val=sp.Rational(1,a)
            return _item(f'Evaluate ∫₀^∞ exp(-{a}x) dx.',val,'Evaluate the limit of the antiderivative as the upper bound grows.',f'[-exp(-{a}x)/{a}]₀^∞={val}.',family=fam)
        elif fam=='Volume by disks':
            val=sp.pi*a*a*b
            return _item(f'Revolve y={a} on [0,{b}] about the x-axis. Find the volume.',val,'Use V=π∫R²dx.',f'V=π({a}²)({b})={val}.',family=fam)
        else:
            val=sp.pi*((a+c)**2-a*a)*b
            return _item(f'Revolve the region between y={a+c} and y={a} on [0,{b}] about the x-axis. Find volume.',val,'Use π∫(R²−r²)dx.',f'V=π(({a+c})²−{a}²)({b})={val}.',family=fam)
        val=sp.integrate(f,x)
        return _item(f'Find an antiderivative of {sp.sstr(f)}. Omit +C.',val,hint,f'Integrate using {fam.lower()}: {sp.sstr(val)}+C.',kind='antiderivative',family=fam)
    if subject=='Differential Equations':
        if fam in ('Exponential growth','Separable equations','Initial conditions','Coupled growth interpretation'):
            val=b*sp.exp(a*x)
            prompt=f'Solve dy/dx={a}y with y(0)={b}. Enter y(x).'
            if fam=='Separable equations': prompt=f'Solve the separable initial-value equation y′/{a}=y, y(0)={b}. Enter y(x).'
            if fam=='Initial conditions': prompt=f'Find y(x) if y′−{a}y=0 and y(0)={b}.'
            if fam=='Coupled growth interpretation': prompt=f'A population starts at {b} hundred and follows dP/dt={a}P. Find P(t) in hundreds, using x as the time variable in your answer.'
            return _item(prompt,val,'Separate variables, then use the initial condition.',f'ln|y|={a}x+C; y(0)={b}; y={sp.sstr(val)}.',family=fam)
        if fam=='Direct integration':
            val=sp.Rational(a,2)*x*x+b
            return _item(f'Solve dy/dx={a}x, y(0)={b}.',val,'Integrate the right-hand side.',f'y={a}x²/2+C, C={b}.',family=fam)
        if fam=='First-order linear':
            val=b*sp.exp(-a*x)+sp.Rational(c,a)
            return _item(f'Solve y′+{a}y={c}, y(0)={b+sp.Rational(c,a)}. Enter y(x).',val,'Use the integrating factor exp(ax).',f'y={sp.sstr(val)}.',family=fam)
        if fam=='Bernoulli equations':
            val=1/(1+b*sp.exp(-a*x))
            return _item(f'Solve y′={a}y(1−y), y(0)=1/{1+b}. Enter y(x).',val,'Substitute v=1/y or separate variables.',f'Integrating the logistic equation gives y={sp.sstr(val)}.',family=fam)
        if fam in ('Second-order homogeneous','Repeated roots','Forced second-order'):
            if fam=='Repeated roots':
                val=(b+c*x)*sp.exp(-a*x)
                return _item(f'Solve y′′+{2*a}y′+{a*a}y=0, y(0)={b}, y′(0)={c-a*b}.',val,'Characteristic root r=−a is repeated.',f'y=(C1+C2x)e^(−{a}x); C1={b}, C2={c}.',family=fam)
            if fam=='Forced second-order':
                val=sp.Rational(c,a*a)
                return _item(f'Find a constant particular solution to y′′+{a*a}y={c}.',val,'Try a constant y=A.',f'{a*a}A={c}, so A={val}.',family=fam)
            val=b*sp.cos(a*x)
            return _item(f'Solve y′′+{a*a}y=0, y(0)={b}, y′(0)=0.',val,'Characteristic roots are ±ai.',f'y={b}cos({a}x).',family=fam)
        if fam=='Cooling models':
            val=b+c*sp.exp(-a*x)
            return _item(f'Newton cooling: ambient temperature {b}°C, initial temperature {b+c}°C, decay constant {a}. Find T(t) (use x for time).',val,'Temperature difference decays exponentially.',f'T={b}+{c}exp(-{a}x).',family=fam)
        if fam=='Euler numerical step':
            val=b+sp.Rational(1,10)*a*b
            return _item(f'Use ONE Euler step for y′={a}y, y(0)={b}, step size h=0.1. Find y(0.1) approximately.',val,'Use y_next=y_current+h f(x,y).',f'{b}+0.1({a})({b})={val}.',family=fam)
    raise ValueError('Unsupported exercise family')

def check_answer(parse, user, item):
    if not user.strip(): return False
    candidate=parse(user.strip()); target=parse(item['expected'])
    delta=sp.simplify(candidate-target)
    if item['kind']=='antiderivative': return sp.simplify(sp.diff(delta,x))==0
    return delta==0
