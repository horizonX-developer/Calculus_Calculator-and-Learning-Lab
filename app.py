from foundations import render_foundations
from curriculum_audit import render_audit
import ast
from math_input import normalize_math
from applications import render_applications
from ode_methods import render_ode_methods
from guarded_compute import guarded_compute, ComputationLimitError
import streamlit as st
import sympy as s
import numpy as np
import matplotlib.pyplot as plt
from practice import render_practice
from curriculum import render_curriculum, render_input_assistant

x,y=s.symbols('x y', real=True)
FUNCS={'sin':s.sin,'cos':s.cos,'tan':s.tan,'asin':s.asin,'acos':s.acos,'atan':s.atan,'exp':s.exp,'log':s.log,'sqrt':s.sqrt,'sinh':s.sinh,'cosh':s.cosh}
VARS={'x':x,'y':y,'pi':s.pi,'E':s.E,'e':s.E}

def parse(text):
    if not isinstance(text,str): raise ValueError('Expression must be text.')
    if len(text)>160: raise ValueError('Expression too long (maximum 160 characters).')
    normalized=normalize_math(text)
    if len(normalized)>240: raise ValueError('Normalized expression too long.')
    try:
        tree=ast.parse(normalized.replace('^','**'),mode='eval')
    except (SyntaxError,RecursionError) as exc:
        raise ValueError('Invalid expression syntax. Check parentheses and operators.') from exc
    nodes=list(ast.walk(tree))
    if len(nodes)>65: raise ValueError('Expression too complex.')
    def depth(node):
        children=list(ast.iter_child_nodes(node))
        return 1+max((depth(child) for child in children),default=0)
    if depth(tree)>20: raise ValueError('Expression nesting is too deep.')
    if sum(isinstance(n, ast.Pow) for n in nodes)>5: raise ValueError('Too many exponent operations.')
    def walk(n):
        if isinstance(n,ast.Expression): return walk(n.body)
        if isinstance(n,ast.Constant) and type(n.value) in (int,float):
            if abs(n.value)>1e8: raise ValueError('Numeric value too large.')
            return s.sympify(n.value)
        if isinstance(n,ast.Name) and n.id in VARS: return VARS[n.id]
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.UAdd,ast.USub)):
            v=walk(n.operand); return v if isinstance(n.op,ast.UAdd) else -v
        if isinstance(n,ast.BinOp) and isinstance(n.op,(ast.Add,ast.Sub,ast.Mult,ast.Div,ast.Pow)):
            a,b=walk(n.left),walk(n.right)
            if isinstance(n.op,ast.Pow):
                if b.is_number:
                    if b.is_finite is not True or abs(float(b))>12: raise ValueError('Exponent too large.')
                elif b.has(x,y) and a != s.E:
                    raise ValueError('Variable exponents are not supported in this prototype; use exp(x) for exponentials.')
                if a.is_zero and b.is_number and b.is_nonpositive:
                    raise ValueError('Zero cannot be raised to a nonpositive power.')
                return a**b
            if isinstance(n.op,ast.Add):return a+b
            if isinstance(n.op,ast.Sub):return a-b
            if isinstance(n.op,ast.Mult):return a*b
            if b.is_zero: raise ValueError('Division by zero is not allowed.')
            return a/b
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in FUNCS and len(n.args)==1 and not n.keywords:
            return FUNCS[n.func.id](walk(n.args[0]))
        raise ValueError('Unsupported input. Use x, y, +, -, *, /, ^ and supported functions such as sin(x).')
    result=walk(tree)
    if result.has(s.zoo,s.nan,s.oo,-s.oo):
        raise ValueError('Expression has an undefined or infinite value.')
    if s.count_ops(result)>65: raise ValueError('Expression too complex.')
    return result

def derivative_steps(f):
    steps=[]
    terms=s.Add.make_args(s.expand(f))
    if len(terms)>1 and len(terms)<=12 and all(t.is_polynomial(x) for t in terms):
        steps.append(('Sum rule',r'\frac{d}{dx}\left('+s.latex(f)+r'\right)='+ '+'.join(r'\frac{d}{dx}\left('+s.latex(t)+r'\right)' for t in terms)))
        for t in terms:
            steps.append(('Differentiate a term',r'\frac{d}{dx}\left('+s.latex(t)+r'\right)='+s.latex(s.diff(t,x))))
    elif f.func==s.sin and f.args[0].has(x):
        u=f.args[0];steps.append(('Chain rule',r'\frac{d}{dx}\sin(u)=\cos(u)\frac{du}{dx}'))
        steps.append(('Substitute the inner function',r'u='+s.latex(u)+r',\quad \frac{du}{dx}='+s.latex(s.diff(u,x))))
    elif f.func==s.cos and f.args[0].has(x):
        u=f.args[0];steps.append(('Chain rule',r'\frac{d}{dx}\cos(u)=-\sin(u)\frac{du}{dx}'))
        steps.append(('Differentiate the inner function',r'\frac{d}{dx}('+s.latex(u)+')='+s.latex(s.diff(u,x))))
    elif f.is_Mul and len(f.args)==2 and all(t.has(x) for t in f.args):
        a,b=f.args;steps.append(('Product rule',r'(uv)\prime=u\prime v+uv\prime'))
        steps.append(('Differentiate both factors',r'u\prime='+s.latex(s.diff(a,x))+r',\quad v\prime='+s.latex(s.diff(b,x))))
    else: steps.append(('Symbolic differentiation',r'\frac{d}{dx}\left('+s.latex(f)+r'\right)'))
    return steps

def integral_steps(f):
    """Return honest worked derivations for a deliberately limited set of integrands."""
    steps=[]
    if f.is_polynomial(x):
        terms=s.Add.make_args(s.expand(f))
        if len(terms)>1:
            steps.append(('Linearity of integration',r'\int('+s.latex(f)+r')\,dx='+ '+'.join(r'\int('+s.latex(t)+r')\,dx' for t in terms)))
        for term in terms:
            coefficient, power=term.as_coeff_exponent(x)
            if coefficient.is_number and power.is_number and power.is_integer and power>=0:
                steps.append(('Identify coefficient and exponent',r'\int '+s.latex(term)+r'\,dx='+s.latex(coefficient)+r'\int x^{'+s.latex(power)+r'}\,dx'))
                steps.append(('Apply power rule',s.latex(coefficient)+r'\frac{x^{'+s.latex(power+1)+r'}}{'+s.latex(power+1)+r'}'))
                steps.append(('Simplify term',s.latex(s.integrate(term,x))))
        steps.append(('Combine and add constant',s.latex(s.integrate(f,x))+r'+C'))
        return steps
    # u-substitution for u'(x)*g(u(x)) using SymPy's manual integral rule tree
    try:
        from sympy.integrals.manualintegrate import integral_steps as manual_steps, URule, PartsRule, RewriteRule, AddRule, ConstantTimesRule, PowerRule
        rule=manual_steps(f,x)
        def locate(r,cls,depth=0):
            if depth>10:return None
            if isinstance(r,cls):return r
            for attr in ('substep','substeps','alternatives','parts','rule'):
                obj=getattr(r,attr,None)
                if isinstance(obj,(tuple,list)):
                    for child in obj:
                        found=locate(child,cls,depth+1)
                        if found:return found
                elif obj is not None:
                    found=locate(obj,cls,depth+1)
                    if found:return found
            return None
        ur=locate(rule,URule)
        if ur is not None:
            u=ur.u_func
            v=ur.u_var
            steps.append(('Choose substitution',r'u='+s.latex(u)+r',\quad du=('+s.latex(s.diff(u,x))+r')\,dx'))
            transformed=s.simplify(f/s.diff(u,x))
            candidate=s.simplify(transformed.subs(u,v))
            if not candidate.has(x):
                steps.append(('Rewrite integral in u',r'\int '+s.latex(candidate)+r'\,d'+s.latex(v)))
                steps.append(('Integrate in u',s.latex(s.integrate(candidate,v))+r'+C'))
                steps.append(('Substitute back',s.latex(s.integrate(candidate,v).subs(v,u))+r'+C'))
                return steps
        pr=locate(rule,PartsRule)
        if pr is not None:
            u=pr.u; dv=pr.dv
            v=s.integrate(dv,x); du=s.diff(u,x)
            steps.append(('Choose u and dv',r'u='+s.latex(u)+r',\quad dv='+s.latex(dv)+r'\,dx'))
            steps.append(('Differentiate and integrate',r'du='+s.latex(du)+r'\,dx,\quad v='+s.latex(v)))
            steps.append(('Apply integration by parts',r'\int u\,dv=uv-\int v\,du'))
            steps.append(('Substitute',s.latex(u*v)+r'-\int '+s.latex(v*du)+r'\,dx'))
            remaining=s.integrate(v*du,x)
            if not remaining.has(s.Integral):
                steps.append(('Evaluate remaining integral',s.latex(s.simplify(u*v-remaining))+r'+C'))
                return steps
    except (ValueError,TypeError,AttributeError,NotImplementedError,RecursionError):
        pass
    # Rational functions with simple partial fraction decomposition
    if f.is_rational_function(x) and not f.is_polynomial(x):
        apart=s.apart(f,x)
        if apart!=f and s.count_ops(apart)<80:
            steps.append(('Decompose into partial fractions',s.latex(f)+'='+s.latex(apart)))
            parts=s.Add.make_args(apart)
            steps.append(('Integrate each term',r'\int('+s.latex(apart)+r')\,dx='+ '+'.join(r'\int('+s.latex(t)+r')\,dx' for t in parts)))
            if all(not s.integrate(t,x).has(s.Integral) for t in parts):
                steps.append(('Combine antiderivatives',s.latex(s.integrate(apart,x))+r'+C'))
                return steps
    if f.func in (s.sin,s.cos,s.exp) and f.args[0]==x:
        steps.append(('Apply standard antiderivative',r'\int '+s.latex(f)+r'\,dx='+s.latex(s.integrate(f,x))+r'+C'))
        return steps
    steps.append(('Method not yet supported','A complete rule-by-rule derivation is not yet supported for this expression. The symbolic result, if available, is calculated separately.'))
    return steps

def show_steps(steps):
    st.subheader('Mathematical steps')
    guided=st.toggle('Guided learning: reveal steps one at a time',key='guided_steps')
    visible=st.slider('Steps to reveal',1,len(steps),1,key='step_count') if guided and steps else len(steps)
    for i,(name,body) in enumerate(steps[:visible],1):
        with st.expander(f'Step {i}: {name}',expanded=True):
            if body.startswith('A complete'): st.info(body)
            else: st.latex(body)
    if guided and visible<len(steps):st.caption(f'{len(steps)-visible} more step(s) available. Move the slider to reveal them.')


def ode_worked_steps(f):
    """Conservative step derivations for selected first-order ODEs y'=F(x,y)."""
    Y=s.Function('y'); yy=Y(x)
    eq=s.Eq(s.diff(yy,x),f.subs(y,yy))
    if not f.has(y):
        return 'Direct integration', [('Integrate both sides',r'y=\int('+s.latex(f)+r')\,dx+C'),('Evaluate integral',r'y='+s.latex(s.integrate(f,x))+r'+C')]
    # Linear: f = a(x)*y + b(x); verify affine dependence.
    b=s.simplify(f.subs(y,0)); a=s.simplify(s.diff(f,y))
    if not a.has(y) and s.simplify(f-(a*y+b))==0:
        if b==0:
            A=s.integrate(a,x)
            return 'Separable / homogeneous linear', [('Separate variables (for y ≠ 0)',r'\frac{dy}{y}='+s.latex(a)+r'\,dx'),('Integrate both sides',r'\ln|y|='+s.latex(A)+r'+C'),('Exponentiate (including zero solution)',r'y=C_1e^{'+s.latex(A)+'}')]
        P=-a; Q=b; mu=s.exp(s.integrate(P,x))
        rhs=s.integrate(mu*Q,x)
        return 'First-order linear (integrating factor)', [('Standard form',r'y\prime +('+s.latex(P)+r')y='+s.latex(Q)),('Integrating factor',r'\mu(x)=e^{\int('+s.latex(P)+r')\,dx}='+s.latex(mu)),('Multiply through',r'\frac{d}{dx}(\mu y)=\mu Q'),('Integrate',r'\mu y=\int '+s.latex(s.simplify(mu*Q))+r'\,dx+C'),('Solve for y',r'y='+s.latex(s.simplify((rhs+s.Symbol('C'))/mu)))]
    # Bernoulli y'=a(x)*y+b(x)*y^n, with n !=0,1, and explicit structural check.
    terms=s.Add.make_args(s.expand(f))
    for t in terms:
        powers=t.as_powers_dict(); n=s.sympify(powers.get(y,0))
        if n not in (0,1) and n.is_number and n.is_integer and -5<=n<=5:
            bcoef=s.simplify(t/y**n)
            rem=s.simplify(f-t); acoef=s.simplify(rem/y)
            if not bcoef.has(y) and not acoef.has(y) and s.simplify(f-(acoef*y+bcoef*y**n))==0:
                P=-acoef; Q=bcoef
                return 'Bernoulli equation', [('Standard Bernoulli form',r'y\prime+('+s.latex(P)+r')y=('+s.latex(Q)+')y^{'+s.latex(n)+'}'),('Substitute',r'v=y^{1-n}=y^{'+s.latex(1-n)+'}'),('Transform to linear equation',r'v\prime+('+s.latex(s.simplify((1-n)*P))+r')v='+s.latex(s.simplify((1-n)*Q))),('Solve transformed linear equation','Use the integrating-factor method on the equation for v, then substitute back. Check separately for solutions excluded by dividing by powers of y.')]
    return 'General symbolic ODE', [('Derivation unavailable','A complete rule-by-rule derivation is not yet supported for this equation. The solver will attempt a symbolic solution separately.')]

def show_ode_steps(steps):
    show_steps(steps)

def plot_expression(expr, title, bounds=(-5,5), shade=None):
    """Plot real-valued, finite samples; never plot untrusted lambdified Python."""
    if expr.free_symbols-{x}:return
    if s.count_ops(expr)>65:return
    try:
        fun=s.lambdify(x,expr,modules=['numpy'])
        xx=np.linspace(bounds[0],bounds[1],500)
        with np.errstate(all='ignore'):
            yy=np.asarray(fun(xx),dtype=float)
        if yy.ndim==0:yy=np.full_like(xx,float(yy))
        if yy.shape!=xx.shape:return
        yy[~np.isfinite(yy)]=np.nan
        yy[np.abs(yy)>1e5]=np.nan
        fig,ax=plt.subplots(figsize=(8,3.6))
        ax.plot(xx,yy,label=title)
        if shade is not None:
            a,b=shade
            ax.fill_between(xx,yy,0,where=(xx>=min(a,b))&(xx<=max(a,b)),alpha=.18)
        ax.axhline(0,color='gray',linewidth=.7);ax.axvline(0,color='gray',linewidth=.7)
        ax.grid(alpha=.2);ax.set_xlabel('x');ax.set_ylabel('y');ax.legend()
        st.pyplot(fig);plt.close(fig)
    except (ValueError,TypeError,OverflowError,ZeroDivisionError):
        st.info('Graph unavailable for this expression or selected interval.')

def plot_ode_solution(sol):
    if not isinstance(sol,s.Equality):return
    constants=sorted([z for z in sol.rhs.free_symbols if z!=x],key=str)
    if not constants or len(constants)>2:return
    st.subheader('Solution curves')
    st.caption('Illustrative solution family; values are not fitted to initial conditions.')
    limit=st.slider('Graph range (−x to +x)',0.5,3.0,1.5,0.25,key='ode_graph_range')
    xx=np.linspace(-limit,limit,400)
    fig,ax=plt.subplots(figsize=(8,3.8))
    shown=0
    for k in (-1,0,1):
        values={c:(k if i==0 else 1) for i,c in enumerate(constants)}
        expr=sol.rhs.subs(values)
        if s.count_ops(expr)>65:continue
        try:
            fun=s.lambdify(x,expr,modules=['numpy'])
            with np.errstate(all='ignore'):
                yy=np.asarray(fun(xx),dtype=float)
            if yy.ndim==0:yy=np.full_like(xx,float(yy))
            if yy.shape!=xx.shape:continue
            yy=np.where(np.isfinite(yy)&(np.abs(yy)<1e6),yy,np.nan)
            ax.plot(xx,yy,label=', '.join(f'{c}={values[c]}' for c in constants))
            shown+=1
        except (ValueError,TypeError,OverflowError,ZeroDivisionError):continue
    if shown:
        ax.axhline(0,color='gray',linewidth=.7)
        ax.axvline(0,color='gray',linewidth=.7)
        ax.grid(alpha=.2)
        ax.set_xlabel('x');ax.set_ylabel('y');ax.legend()
        st.pyplot(fig)
    else:st.info('Graph unavailable for this solution.')
    plt.close(fig)


st.set_page_config(page_title='Calculus Learning Lab v3.0 RC1',page_icon='📘',layout='centered')
st.title('📘 Calculus Learning Lab')
st.caption('v3.0 RC1 · Deployment validation candidate · Not cleared for public access')
WORKSPACES = ['Student Home', 'Calculators', 'Student Practice', 'Curriculum Explorer', 'Curriculum Audit', 'Differential Foundations', 'Derivative Applications', 'Integral Techniques', 'Integral Applications', 'Integral Applications Expanded', 'ODE Methods', 'First-Order ODE Lessons', 'Higher-Order ODE Lessons', 'Guided Learning Paths']
WORKSPACE_GROUPS = {
    'Start here': ['Guided Learning Paths', 'Student Practice', 'Curriculum Explorer'],
    'Differential Calculus': ['Differential Foundations', 'Derivative Applications'],
    'Integral Calculus': ['Integral Techniques', 'Integral Applications', 'Integral Applications Expanded'],
    'Differential Equations': ['ODE Methods', 'First-Order ODE Lessons', 'Higher-Order ODE Lessons'],
    'Tools & review': ['Calculators', 'Curriculum Audit'],
}
HOME_ACTIONS = {
    'Learn a Topic': 'Guided Learning Paths',
    'Practice Problems': 'Student Practice',
    'Solve My Problem': 'Calculators',
}
if st.session_state.get('workspace_choice') not in WORKSPACES:
    st.session_state['workspace_choice'] = 'Student Home'

def navigate(destination):
    st.session_state['workspace_choice'] = destination
    st.rerun()

with st.sidebar:
    st.header('📚 Your study space')
    if st.button('🏠 Home',use_container_width=True):
        navigate('Student Home')
    st.caption('Choose a task on Home. You can explore the specialist tools below.')
    advanced = st.toggle('Show advanced tools',value=False,key='v228_advanced')
    if advanced:
        group = st.selectbox('Subject area',list(WORKSPACE_GROUPS),key='v228_area')
        chosen = st.selectbox('Specialist workspace',WORKSPACE_GROUPS[group],key='v228_workspace')
        if st.button('Open selected workspace',use_container_width=True):
            navigate(chosen)
    with st.expander('⌨️ How to type mathematics'):
        st.markdown('Use `*` for multiplication, `^` for powers, and parentheses for functions.')
        st.code('3*x^2 - 4*x + 1\nsin(x^2)\nexp(x)\n1/(x+2)',language=None)
        st.caption('Enter an expression, not an equation containing =, unless a lesson explicitly requests one.')
    st.caption('Local prototype · Check results before high-stakes use.')
workspace = st.session_state['workspace_choice']
if workspace == 'Student Home':
    st.subheader('What would you like to do today?')
    st.write('No programming experience needed. Pick one option to begin.')
    options = [
        ('📖 Learn a Topic','Learn calculus with examples, hints, and graphs.','Learn a Topic'),
        ('✏️ Practice Problems','Choose a topic, try questions, and check your work.','Practice Problems'),
        ('🧮 Solve My Problem','Enter your own problem and explore its solution.','Solve My Problem'),
    ]
    for title,description,action in options:
        with st.container(border=True):
            st.markdown('**'+title+'**')
            st.caption(description)
            if st.button('Start '+action,key='v228_'+action.replace(' ','_'),use_container_width=True):
                navigate(HOME_ACTIONS[action])
    st.info('New to calculus? Start with **Learn a Topic**. You can switch activities using Home at any time.')
    st.stop()
if workspace in HOME_ACTIONS.values():
    if st.button('← Back to Home',key='v228_back'):
        navigate('Student Home')
    friendly = {'Guided Learning Paths':'Learn a Topic','Student Practice':'Practice Problems','Calculators':'Solve My Problem'}
    st.caption('**You are here:** '+friendly[workspace])
else:
    if st.button('← Back to Home',key='v228_back_advanced'):
        navigate('Student Home')
    st.caption('**Advanced workspace:** '+workspace)
if workspace == 'Guided Learning Paths':
    st.info('Pick a topic, read an example, try a question, then see a graph.')
elif workspace == 'Student Practice':
    st.info('Choose your subject and difficulty. Use the input examples if you get stuck.')
elif workspace == 'Calculators':
    st.info('Enter an expression to solve. For example, type `3*x^2` to mean 3x².')
if workspace == 'Integral Applications Expanded':
    from integral_expansion import render_integral_expansion
    render_integral_expansion(parse)
    st.stop()
if workspace == 'Integral Techniques':
    from integral_techniques import render_integral_techniques
    render_integral_techniques(parse)
    st.stop()
if workspace == 'Derivative Applications':
    from derivative_applications import render_derivative_applications
    render_derivative_applications(parse)
    st.stop()
if workspace == 'Differential Foundations':
    render_foundations(parse)
    st.stop()
if workspace == 'Guided Learning Paths':
    from guided_learning import render_guided_learning
    render_guided_learning(parse)
    st.stop()
if workspace == 'Higher-Order ODE Lessons':
    from higher_order_ode import render_higher_order_ode
    render_higher_order_ode(parse)
    st.stop()
if workspace == 'First-Order ODE Lessons':
    from first_order_ode import render_first_order_ode
    render_first_order_ode(parse)
    st.stop()
if workspace == 'ODE Methods':
    render_ode_methods(parse)
    st.stop()
if workspace == 'Integral Applications':
    render_applications(parse)
    st.stop()
if workspace == 'Student Practice':
    render_practice(parse)
    st.stop()
if workspace == 'Curriculum Audit':
    render_audit(st)
    st.stop()
if workspace == 'Curriculum Explorer':
    render_curriculum(st)
    st.stop()
st.warning('Pre-release candidate for local testing only. Core calculations have a subprocess timeout; step generation, plotting and practice checking still need production-grade isolation and load testing. Do not deploy publicly.')
mode=st.selectbox('Choose a calculator',['Differential Calculus','Integral Calculus','Differential Equations'])
with st.expander('How do I enter an expression?', expanded=False):
    render_input_assistant(st, mode)
examples={'Differential Calculus':'3*x^2+4*x-5','Integral Calculus':'2*x','Differential Equations':'2*x*y'}
with st.form('solve'):
    ode_kind=st.selectbox('Differential equation type',['First-order: dy/dx = F(x,y)','Second-order: y\"\" + a*y\" + b*y = g(x)']) if mode=='Differential Equations' else None
    if ode_kind and ode_kind.startswith('Second-order'):
        st.caption('Equation: y\"\" + a y\" + b y = g(x). Enter constant coefficients and the forcing function.')
        a2=st.number_input('Coefficient a (of y prime)',value=3.0)
        b2=st.number_input('Coefficient b (of y)',value=2.0)
        raw=st.text_input('Forcing function g(x)',value='0')
    else:
        raw=st.text_input('Enter expression',value=examples[mode],help='Use * for multiplication and ^ for powers. For first-order equations enter the right side of dy/dx = ...')
    definite=st.checkbox('Definite integral',disabled=mode!='Integral Calculus') if mode=='Integral Calculus' else False
    if definite:
        lower=st.number_input('Lower bound',value=0.0)
        upper=st.number_input('Upper bound',value=1.0)
    from math_preview import render_preview
    render_preview(st, parse, raw, allowed=('x','y') if mode=='Differential Equations' and not (ode_kind and ode_kind.startswith('Second-order')) else ('x',), label='Expression preview')
    submitted=st.form_submit_button('Solve',type='primary')
if submitted:
    st.session_state['last_calculation']={
        'mode':mode,'ode_kind':ode_kind,'raw':raw,'definite':definite,
        'lower':lower if definite else None,'upper':upper if definite else None,
        'a2':a2 if ode_kind and ode_kind.startswith('Second-order') else None,
        'b2':b2 if ode_kind and ode_kind.startswith('Second-order') else None,
    }
    # A new calculation should begin at the first guided step.
    st.session_state.pop('step_count',None)

saved=st.session_state.get('last_calculation')
if saved and saved['mode']==mode:
    raw=saved['raw'];ode_kind=saved['ode_kind'];definite=saved['definite']
    lower=saved['lower'];upper=saved['upper'];a2=saved['a2'];b2=saved['b2']
    try:
        guarded_compute('preflight', raw, mode, a2 if mode=='Differential Equations' and ode_kind.startswith('Second-order') else None, b2 if mode=='Differential Equations' and ode_kind.startswith('Second-order') else None, ode_kind, timeout=6)
        f=parse(raw)
        if mode!='Differential Equations' and f.has(y):raise ValueError('This calculator expects an expression in x only.')
        if mode=='Differential Calculus':
            answer=s.diff(f,x)
            st.subheader('Derivative');st.latex(r'\frac{d}{dx}\left('+s.latex(f)+r'\right)='+s.latex(answer))
            show_steps(derivative_steps(f))
            st.success('Derivative calculated symbolically.')
            with st.expander('Visualize function and derivative'):
                plot_expression(f,'Original function')
                plot_expression(answer,'Derivative')
        elif mode=='Integral Calculus':
            answer=s.integrate(f,x)
            if isinstance(answer,s.Integral):
                st.warning('An elementary symbolic antiderivative was not found. No unsupported steps will be invented.')
                st.latex(s.latex(answer))
            elif definite:
                val=s.integrate(f,(x,lower,upper));st.subheader('Definite integral')
                st.latex(r'\int_{'+s.latex(s.Float(lower))+r'}^{'+s.latex(s.Float(upper))+r'}'+s.latex(f)+r'\,dx='+s.latex(val))
                show_steps(integral_steps(f)+[('Evaluate at bounds',r'F(b)-F(a)='+s.latex(val))])
                with st.expander('Visualize signed area'):
                    plot_expression(f,'Integrand', (min(lower,upper)-2,max(lower,upper)+2), (lower,upper))
            else:
                st.subheader('Antiderivative');st.latex(r'\int '+s.latex(f)+r'\,dx='+s.latex(answer)+r'+C')
                show_steps(integral_steps(f))
                with st.expander('Visualize integrand and antiderivative'):
                    plot_expression(f,'Integrand')
                    plot_expression(answer,'Antiderivative (C=0)')
            if not isinstance(answer,s.Integral):
                if s.simplify(s.diff(answer,x)-f)==0:st.success('Antiderivative verified by differentiation.')
        else:
            Y=s.Function('y'); yy=Y(x)
            if ode_kind.startswith('Second-order'):
                if f.has(y):raise ValueError('The forcing function g(x) must depend only on x.')
                aa=s.Rational(str(a2));bb=s.Rational(str(b2))
                eq=s.Eq(s.diff(yy,x,2)+aa*s.diff(yy,x)+bb*yy,f)
                st.subheader('Detected method');st.write('Second-order linear ODE with constant coefficients')
                st.latex(s.latex(eq))
                st.subheader('Mathematical steps')
                show_ode_steps([('Solve homogeneous characteristic equation',r'r^2+('+s.latex(aa)+r')r+('+s.latex(bb)+r')=0'),('Find characteristic roots',s.latex(s.solve(s.Symbol('r')**2+aa*s.Symbol('r')+bb,s.Symbol('r'))))])
                if f!=0:st.info('A forcing term is present. The particular-solution derivation is not yet implemented; SymPy will attempt to solve it.')
            else:
                eq=s.Eq(s.diff(yy,x),f.subs(y,yy))
                method,steps=ode_worked_steps(f)
                st.subheader('Detected method');st.write(method)
                show_ode_steps(steps)
            sol=s.dsolve(eq)
            st.subheader('Symbolic solution');st.latex(s.latex(sol))
            with st.expander('Visualize example solution curves'):
                plot_ode_solution(sol)
            try:
                residual=s.simplify((eq.lhs-eq.rhs).subs({s.diff(yy,x,2):s.diff(sol.rhs,x,2),s.diff(yy,x):s.diff(sol.rhs,x),yy:sol.rhs}).doit())
                if residual==0:st.success('Solution verified by substitution.')
                else:st.warning('Symbolic verification was inconclusive; review the result.')
            except Exception:st.info('Automatic verification unavailable for this result.')
    except (ValueError,SyntaxError,TypeError,ZeroDivisionError,s.SympifyError,NotImplementedError,ComputationLimitError) as e:st.error(str(e))
    except Exception:st.error('Unable to solve this expression with the current prototype. Try a simpler supported problem.')
st.divider()
st.caption('Supports selected derivations only. Mathematical method labels are not a guarantee that every intermediate transformation is implemented.')
