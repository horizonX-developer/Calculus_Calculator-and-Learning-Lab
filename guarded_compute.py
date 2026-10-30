"""Preflight calculation in an isolated child process with a wall-clock timeout.

This is defense in depth, NOT a complete production sandbox: the UI still
performs symbolic derivations and graph generation in its own process.
"""
import multiprocessing as mp
import queue

class ComputationLimitError(ValueError):
    pass

def _run(q, expression, mode, a, b, ode_kind):
    try:
        import ast
        import sympy as s
        from math_input import normalize_math
        x,y=s.symbols('x y',real=True)
        FUNCS={'sin':s.sin,'cos':s.cos,'tan':s.tan,'asin':s.asin,'acos':s.acos,'atan':s.atan,'exp':s.exp,'log':s.log,'sqrt':s.sqrt,'sinh':s.sinh,'cosh':s.cosh}
        VARS={'x':x,'y':y,'pi':s.pi,'E':s.E,'e':s.E}
        # Extract and compile the exact parser function without importing Streamlit UI.
        from pathlib import Path
        source=Path(__file__).with_name('app.py').read_text(encoding='utf-8')
        tree=ast.parse(source)
        fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='parse')
        ns={'ast':ast,'s':s,'FUNCS':FUNCS,'VARS':VARS,'normalize_math':normalize_math}
        exec(compile(ast.Module(body=[fn],type_ignores=[]),'<parser>','exec'),ns)
        f=ns['parse'](expression)
        if mode=='Differential Calculus': s.diff(f,x)
        elif mode=='Integral Calculus': s.integrate(f,x)
        else:
            yy=s.Function('y')(x)
            if ode_kind and ode_kind.startswith('Second-order'):
                if f.has(y): raise ValueError('Forcing function must not contain y.')
                eq=s.Eq(s.diff(yy,x,2)+s.Rational(str(a))*s.diff(yy,x)+s.Rational(str(b))*yy,f)
            else: eq=s.Eq(s.diff(yy,x),f.subs(y,yy))
            s.dsolve(eq)
        q.put(('ok',''))
    except Exception as exc:
        q.put(('error',str(exc)[:250]))

def guarded_compute(action, expression, mode, a=None, b=None, ode_kind=None, timeout=6):
    if action!='preflight': raise ValueError('Unsupported action')
    if not isinstance(timeout,(int,float)) or not (0.1<=timeout<=30):
        raise ValueError('Timeout must be between 0.1 and 30 seconds.')
    if not isinstance(expression,str) or len(expression)>160:
        raise ValueError('Invalid expression length.')
    ctx=mp.get_context('spawn')
    q=ctx.Queue(maxsize=1)
    p=ctx.Process(target=_run,args=(q,expression,mode,a,b,ode_kind),daemon=True)
    try:
        p.start()
    except (OSError,RuntimeError) as exc:
        q.close()
        raise ComputationLimitError('Unable to start calculation worker.') from exc
    p.join(timeout)
    if p.is_alive():
        p.terminate();p.join(2)
        if p.is_alive():p.kill();p.join()
        q.close()
        raise ComputationLimitError('This calculation exceeded the time limit. Try a simpler expression.')
    try: status,detail=q.get(timeout=1)
    except queue.Empty: raise ComputationLimitError('Calculation worker did not return a result.')
    finally: q.close()
    if status!='ok': raise ComputationLimitError('Unable to calculate: '+detail)
    return True
