"""Guided learning paths: lesson -> worked example -> practice -> graph."""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

x=sp.Symbol("x",real=True)
LESSONS={
 "Differential Calculus": {
  "Power rule": {"function":x**3-3*x,"expected":3*x**2-3,"question":"Differentiate f(x) = x^3 - 3*x","hint":"Differentiate each term with the power rule.","steps":["d(x^3)/dx = 3*x^2","d(-3*x)/dx = -3"],"domain":(-3,3),"graph":"derivative"},
  "Chain rule": {"function":sp.sin(x**2),"expected":2*x*sp.cos(x**2),"question":"Differentiate sin(x^2)","hint":"Let u=x²; apply d sin(u)/dx = cos(u)u'.","steps":["u=x², so u'=2*x","f'=cos(u)*u'=2*x*cos(x²)"],"domain":(-3,3),"graph":"derivative"}
 },
 "Integral Calculus": {
  "Definite integral": {"function":x**2,"expected":sp.Rational(8,3),"question":"Evaluate the integral of x^2 from 0 to 2","hint":"Use the power rule and evaluate the antiderivative at the bounds.","steps":["Antiderivative: F(x)=x³/3","F(2)-F(0)=8/3"],"domain":(0,2),"graph":"area"},
  "Substitution": {"function":2*x*sp.cos(x**2),"expected":sp.sin(x**2),"question":"Find an antiderivative of 2*x*cos(x^2)","hint":"Substitute u=x², du=2x dx.","steps":["u=x² and du=2x dx","∫cos(u)du=sin(u)+C","Return to x: sin(x²)+C"],"domain":(-2,2),"graph":"antiderivative"}
 },
 "Differential Equations": {
  "Exponential growth": {"function":2*sp.exp(x),"expected":2*sp.exp(x),"question":"Solve y'=y with y(0)=2. Enter y(x).","hint":"The general solution is Ce^x; use y(0)=2.","steps":["Separate: dy/y=dx","ln|y|=x+C","y(0)=2 gives y=2e^x"],"domain":(0,3),"graph":"solution"},
  "Exponential decay": {"function":3*sp.exp(-x),"expected":3*sp.exp(-x),"question":"Solve y'=-y with y(0)=3. Enter y(x).","hint":"Separate dy/y=-dx, then apply the initial condition.","steps":["ln|y|=-x+C","y=Ce^(-x)","y(0)=3 gives y=3e^(-x)"],"domain":(0,4),"graph":"solution"}
 }
}


import random

def generated_exercise(subject, topic, seed):
    """Build a reproducible exercise with topic-specific structure and its own graph."""
    rng=random.Random(seed)
    a=rng.randint(2,7)
    b=rng.randint(1,5)
    if subject=="Differential Calculus":
        if topic=="Power rule":
            n=rng.randint(2,5)
            f=a*x**n-b*x
            return {"function":f,"expected":sp.diff(f,x),
                    "question":f"Differentiate f(x) = {sp.sstr(f)}",
                    "hint":"Apply the power rule to each term.",
                    "steps":[f"Differentiate {a}*x^{n} to obtain {a*n}*x^{n-1}.",f"Differentiate {-b}*x to obtain {-b}."],
                    "domain":(-2,2),"graph":"derivative"}
        f=sp.sin(a*x**2+b)
        return {"function":f,"expected":sp.diff(f,x),
                "question":f"Differentiate f(x) = {sp.sstr(f)}",
                "hint":"Differentiate the inside first, then multiply by cos(inside).",
                "steps":[f"Let u={a}*x^2+{b}.",f"Then u'={2*a}*x and f'=u'*cos(u)."],
                "domain":(-2,2),"graph":"derivative"}
    if subject=="Integral Calculus":
        if topic=="Definite integral":
            n=rng.randint(1,4)
            f=a*x**n
            upper=sp.Integer(rng.randint(1,3))
            answer=sp.integrate(f,(x,0,upper))
            return {"function":f,"expected":answer,
                    "question":f"Evaluate ∫ from 0 to {upper} of ({sp.sstr(f)}) dx",
                    "hint":"Find an antiderivative, then subtract the lower-endpoint value.",
                    "steps":[f"F(x)={sp.sstr(sp.integrate(f,x))}.",f"Evaluate F({upper})-F(0)."],
                    "domain":(0,float(upper)),"graph":"area"}
        f=2*a*x*sp.cos(a*x**2+b)
        return {"function":f,"expected":sp.sin(a*x**2+b),
                "question":f"Find an antiderivative of {sp.sstr(f)}",
                "hint":"Use u=a*x²+b and du=2*a*x dx.",
                "steps":[f"Set u={a}*x²+{b}.","Integrate cos(u) du to get sin(u)+C.","Substitute back into x."],
                "domain":(-2,2),"graph":"antiderivative"}
    if topic=="Exponential growth":
        f=a*sp.exp(b*x)
        return {"function":f,"expected":f,
                "question":f"Solve y'={b}*y with y(0)={a}. Enter y(x).",
                "hint":"The solution is C*exp(k*x); apply y(0).",
                "steps":[f"General solution: y=C*exp({b}*x).",f"Initial condition gives C={a}."],
                "domain":(0,1),"graph":"solution"}
    f=a*sp.exp(-b*x)
    return {"function":f,"expected":f,
            "question":f"Solve y'=-{b}*y with y(0)={a}. Enter y(x).",
            "hint":"The solution is C*exp(-k*x); apply y(0).",
            "steps":[f"General solution: y=C*exp(-{b}*x).",f"Initial condition gives C={a}."],
            "domain":(0,2),"graph":"solution"}

def exercise_is_valid(subject,topic,exercise):
    f=exercise["function"]
    expected=exercise["expected"]
    if subject=="Differential Calculus":
        return sp.simplify(sp.diff(f,x)-expected)==0
    if subject=="Integral Calculus":
        if topic=="Definite integral":
            lo,hi=exercise["domain"]
            return sp.simplify(sp.integrate(f,(x,lo,sp.Rational(str(hi))))-expected)==0
        return sp.simplify(sp.diff(expected,x)-f)==0
    coefficient=sp.simplify(sp.diff(f,x)/f)
    if topic=="Exponential growth":
        return coefficient.is_positive is True and sp.simplify(sp.diff(f,x)-coefficient*f)==0
    return coefficient.is_negative is True and sp.simplify(sp.diff(f,x)-coefficient*f)==0

def equivalent(expected,actual,indefinite=False):
    actual=sp.sympify(actual)
    if actual.free_symbols-{x}:
        return False
    delta=sp.simplify(actual-expected)
    if delta==0:return True
    if indefinite:return sp.simplify(sp.diff(delta,x))==0
    return False

def lesson_plot(lesson):
    f=lesson["function"];lo,hi=lesson["domain"]
    xs=np.linspace(lo,hi,350)
    ys=np.broadcast_to(np.asarray(sp.lambdify(x,f,"numpy")(xs),dtype=float),xs.shape)
    if not np.all(np.isfinite(ys)):raise ValueError("Graph contains nonfinite values.")
    fig,ax=plt.subplots()
    ax.plot(xs,ys,label="f(x)" if lesson["graph"] not in ("solution",) else "y(x)")
    if lesson["graph"]=="derivative":
        df=sp.diff(f,x)
        dys=np.broadcast_to(np.asarray(sp.lambdify(x,df,"numpy")(xs),dtype=float),xs.shape)
        ax.plot(xs,dys,label="f'(x)")
    elif lesson["graph"]=="area":
        ax.fill_between(xs,0,ys,alpha=.25,label="Definite integral area")
    elif lesson["graph"]=="antiderivative":
        antiderivative=lesson["expected"]
        dys=np.broadcast_to(np.asarray(sp.lambdify(x,antiderivative,"numpy")(xs),dtype=float),xs.shape)
        ax.plot(xs,dys,label="Antiderivative F(x)")
    ax.axhline(0,linewidth=.6);ax.legend();ax.set_xlabel("x");ax.set_ylabel("Value")
    return fig

def question_latex(subject, topic, lesson):
    """Render questions from symbolic expressions, not Python source strings."""
    f=sp.latex(lesson["function"])
    if subject=="Differential Calculus":
        return r"\text{Differentiate:}\quad f(x)="+f
    if subject=="Integral Calculus":
        if topic=="Definite integral":
            lo,hi=lesson["domain"]
            return r"\text{Evaluate:}\quad \int_{"+sp.latex(sp.sympify(lo))+"}^{"+sp.latex(sp.sympify(hi))+"} "+f+r"\,dx"
        return r"\text{Find an antiderivative:}\quad \int "+f+r"\,dx"
    initial=sp.simplify(lesson["function"].subs(x,0))
    rate=sp.simplify(sp.diff(lesson["function"],x)/lesson["function"])
    return r"\text{Solve:}\quad \frac{dy}{dx}="+sp.latex(rate)+r"y,\quad y(0)="+sp.latex(initial)


def worked_solution_latex(subject, topic, lesson):
    """A mathematically formatted solution for each guided exercise."""
    f=lesson["function"]
    answer=lesson["expected"]
    if subject=="Differential Calculus":
        return [r"f(x)="+sp.latex(f),r"f'(x)="+sp.latex(answer)]
    if subject=="Integral Calculus":
        if topic=="Definite integral":
            lo,hi=map(sp.sympify,lesson["domain"])
            antiderivative=sp.integrate(f,x)
            return [r"F(x)="+sp.latex(antiderivative),r"\int_{"+sp.latex(lo)+"}^{"+sp.latex(hi)+"}"+sp.latex(f)+r"\,dx=\left["+sp.latex(antiderivative)+r"\right]_{"+sp.latex(lo)+"}^{"+sp.latex(hi)+"}="+sp.latex(answer)]
        return [r"\int "+sp.latex(f)+r"\,dx="+sp.latex(answer)+"+C"]
    return [r"y(x)="+sp.latex(answer)]

def render_guided_learning(parse):
    import streamlit as st
    st.header("Learn a Topic")
    mode=st.radio("Learning activity",["Full lessons (start here)","Guided practice"],horizontal=True,key="teaching_mode")
    if mode=="Full lessons (start here)":
        from teaching_curriculum import render_teaching_library
        render_teaching_library()
        return

    st.caption("Guided practice · Student-friendly mathematical notation.")
    target=st.session_state.pop("teaching_practice_target",None)
    if target and target[0] in LESSONS and target[1] in LESSONS[target[0]]:
        st.session_state["v218_subject"]=target[0]
        st.session_state["v218_topic"]=target[1]
    subject=st.selectbox("Subject",list(LESSONS),key="v218_subject")
    # A keyed selectbox can retain a value from a previous subject.
    # Reset it before constructing the topic widget if its options changed.
    if st.session_state.get("v218_topic") not in LESSONS[subject]:
        st.session_state["v218_topic"]=next(iter(LESSONS[subject]))
    topic=st.selectbox("Topic",list(LESSONS[subject]),key="v218_topic")
    identity=(subject,topic)
    seed_key="v219_seed"
    if st.session_state.get("v219_topic")!=identity:
        st.session_state["v219_topic"]=identity
        st.session_state[seed_key]=0
    st.toggle("Generate varied questions",value=True,key="v219_randomized")
    if st.session_state["v219_randomized"]:
        if st.button("New question",key="v219_next"):
            st.session_state[seed_key]+=1
            st.session_state["v218_answer"]=""
            st.session_state["v218_feedback"]=None
        lesson=generated_exercise(subject,topic,st.session_state[seed_key]+173)
    else:
        lesson=LESSONS[subject][topic]
    identity=(subject,topic,st.session_state["v219_randomized"],st.session_state[seed_key])
    if st.session_state.get("v218_identity")!=identity:
        st.session_state["v218_identity"]=identity
        st.session_state["v218_answer"]=""
        st.session_state["v218_feedback"]=None
    st.subheader("1. Learn")
    st.write("**Method:**",topic)
    with st.expander("Show a worked example",expanded=False):
        for i,step in enumerate(lesson["steps"],1):st.write(f"{i}. {step}")
        for expression in worked_solution_latex(subject,topic,lesson):st.latex(expression)
    st.subheader("2. Practice")
    st.latex(question_latex(subject,topic,lesson))
    with st.expander("How do I enter my answer?"):
        st.write("Type expressions such as `3*x^2-3`, `sin(x^2)`, `2*exp(x)`, or `8/3`. Use `*` for multiplication and `^` for powers. For indefinite integrals, omit `+C`; any constant difference is accepted.")
    st.text_input("Your answer",key="v218_answer")
    if st.button("Check my answer",key="v218_check"):
        try:
            user=parse(st.session_state["v218_answer"])
            is_indefinite=subject=="Integral Calculus" and topic=="Substitution"
            correct=equivalent(lesson["expected"],user,is_indefinite)
            st.session_state["v218_feedback"]=correct
        except Exception as exc:
            st.session_state["v218_feedback"]=None
            st.error(f"Check your expression: {exc}")
    if st.session_state.get("v218_feedback") is True:
        st.success("Correct! Your expression matches the expected result.")
    elif st.session_state.get("v218_feedback") is False:
        st.warning("Not quite. Review the hint and try again.")
    with st.expander("Hint"):
        st.write(lesson["hint"])
    with st.expander("Reveal the worked solution"):
        for step in lesson["steps"]:st.write("• "+step)
        for expression in worked_solution_latex(subject,topic,lesson):st.latex(expression)
    st.subheader("3. Visualize")
    try:
        fig=lesson_plot(lesson)
        st.pyplot(fig)
        plt.close(fig)
    except Exception as exc:
        st.info(f"Graph unavailable: {exc}")
    st.caption("Each guided exercise has its own matching graph. The separate Student Practice workspace is not yet fully integrated.")
