"""Curated beginner-oriented teaching lessons. Session-only quiz progress."""
import streamlit as st

# Each record: title, objective, concept, formula (LaTeX), example, steps, pitfall, quiz, options, correct, explanation.
COURSES = {
"Differential Calculus": [
("Functions and notation","Identify inputs, outputs, and function values.","A function assigns one output to each allowed input. f(2) means substitute x=2 into the rule.",r"f(x)=x^2+1",r"f(2)=2^2+1=5",["Replace x with 2.","Square 2 to obtain 4.","Add 1 to obtain 5."],"f(x+1) is not always f(x)+1.","If f(x)=x²+1, what is f(3)?",["7","10","12"],1,"3²+1=10."),
("Limits","Interpret what a function approaches near a point.","A limit describes the value approached as x gets close to a number, even when the function is undefined there.",r"\lim_{x\to 2}(x+3)=5",r"\lim_{x\to 2}(x^2-4)/(x-2)=4",["Factor x²−4=(x−2)(x+2).","For x≠2, cancel the common factor.","As x approaches 2, x+2 approaches 4."],"Do not substitute into a 0/0 expression and conclude the limit is zero.","What is the limit of x+3 as x approaches 2?",["3","5","Undefined"],1,"A continuous expression can be evaluated directly."),
("Continuity","Recognize continuity at a point.","A function is continuous at a when its value exists, its limit exists, and the two are equal.",r"\lim_{x\to a}f(x)=f(a)",r"f(x)=x^2\text{ is continuous at }x=1",["Find f(1)=1.","Find the limit as x approaches 1; it is 1.","Since they match, f is continuous at 1."],"A limit existing does not alone guarantee continuity.","Which condition is needed for continuity at a?",["The limit equals f(a)","The slope is positive","The graph is a line"],0,"The limit and function value must agree."),
("Derivative as slope","Explain instantaneous rate of change.","A derivative is the slope of a tangent line, obtained from the limit of average rates of change.",r"f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}",r"f(x)=x^2\Rightarrow f'(x)=2x",["Expand (x+h)²−x²=2xh+h².","Divide by h to obtain 2x+h.","Take h→0 to get 2x."],"A derivative is not simply f(x)/x.","For f(x)=x², what is the slope at x=3?",["3","6","9"],1,"f′(3)=2(3)=6."),
("Power rule","Differentiate powers of x.","Multiply by the exponent, then subtract one from the exponent.",r"\frac{d}{dx}x^n=nx^{n-1}",r"\frac{d}{dx}(3x^2+2x)=6x+2",["Differentiate 3x² to get 6x.","Differentiate 2x to get 2.","Add the derivatives."],"Remember that the derivative of a constant is zero.","What is d(x⁴)/dx?",["4x³","x³","4x⁴"],0,"Bring down 4 and reduce the exponent to 3."),
("Product and quotient rules","Differentiate products and ratios.","When two changing functions are multiplied or divided, ordinary term-by-term differentiation does not apply.",r"(uv)'=u'v+uv'",r"\frac{d}{dx}(x^2\sin x)=2x\sin x+x^2\cos x",["Let u=x² and v=sin x.","Compute u′=2x and v′=cos x.","Use u′v+uv′."],"The derivative of uv is not u′v′.","Which is the product rule?",["u′v+uv′","u′v′","u+v"],0,"Differentiate each factor in turn."),
("Chain rule","Differentiate composite functions.","Differentiate the outside function, keeping the inside, then multiply by the inside derivative.",r"\frac{d}{dx}f(g(x))=f'(g(x))g'(x)",r"\frac{d}{dx}\sin(x^2)=2x\cos(x^2)",["Outside function: sin(u) becomes cos(u).","Inside function: u=x² gives u′=2x.","Multiply to obtain 2x cos(x²)."],"Do not forget the derivative of the inside function.","What is d(sin(3x))/dx?",["cos(3x)","3cos(3x)","3sin(3x)"],1,"The inner derivative of 3x is 3."),
("Optimization","Find maxima or minima from derivatives.","Critical points are candidates for extrema. Check endpoints or use derivative tests before deciding.",r"f'(c)=0",r"f(x)=-(x-2)^2+4\text{ has maximum }4",["Differentiate: f′(x)=−2(x−2).","Set f′=0 to get x=2.","Evaluate f(2)=4; the parabola opens downward."],"A critical point is not automatically a maximum.","For f(x)=−(x−2)²+4, where is the maximum?",["x=0","x=2","x=4"],1,"The vertex is at x=2.")
],
"Integral Calculus": [
("Antiderivatives","Reverse differentiation.","An antiderivative F has derivative f. Add an arbitrary constant because constants disappear under differentiation.",r"\int x^n\,dx=\frac{x^{n+1}}{n+1}+C\quad(n\ne-1)",r"\int 2x\,dx=x^2+C",["Increase the exponent of x from 1 to 2.","Divide the coefficient by 2.","Add C for an indefinite integral."],"Do not omit +C in a general indefinite integral.","What is ∫2x dx?",["2x²+C","x²+C","2+C"],1,"Differentiate x²+C to recover 2x."),
("Definite integrals","Understand signed accumulation over an interval.","A definite integral computes signed area or accumulated change. Regions below the x-axis contribute negatively.",r"\int_a^b f(x)\,dx",r"\int_0^2 x\,dx=2",["Find F(x)=x²/2.","Evaluate F(2)=2.","Subtract F(0)=0."],"A definite integral can be negative; it is not always geometric area.","What is ∫₀² x dx?",["1","2","4"],1,"The area of the triangle is ½·2·2=2."),
("Fundamental Theorem of Calculus","Connect differentiation and integration.","If F′=f, the definite integral from a to b equals F(b)−F(a).",r"\int_a^b f(x)\,dx=F(b)-F(a)",r"\int_0^1 3x^2\,dx=1",["Antiderivative of 3x² is x³.","At x=1, F=1.","At x=0, F=0; subtract to obtain 1."],"Remember to subtract the lower-bound value.","For F(3)=8 and F(1)=2, what is ∫₁³ F′(x) dx?",["10","6","4"],1,"F(3)−F(1)=8−2=6."),
("Substitution","Recognize a composite integrand.","Substitution reverses the chain rule: choose an inner expression u and rewrite its differential.",r"u=g(x),\quad du=g'(x)\,dx",r"\int 2x\cos(x^2)\,dx=\sin(x^2)+C",["Choose u=x².","Then du=2x dx.","Integrate cos(u) to sin(u), then substitute back."],"Check that the differential matches the integrand.","Which substitution fits ∫2x cos(x²) dx?",["u=2x","u=x²","u=cos x"],1,"The derivative of x² is 2x."),
("Integration by parts","Integrate products using the product rule.","Choose u to simplify when differentiated and dv to integrate easily.",r"\int u\,dv=uv-\int v\,du",r"\int x e^x\,dx=xe^x-e^x+C",["Choose u=x and dv=eˣ dx.","Then du=dx and v=eˣ.","Use uv−∫v du to get xeˣ−eˣ+C."],"The formula includes a minus sign.","What is ∫u dv?",["uv+∫v du","uv−∫v du","u′v′"],1,"This is the integration-by-parts identity."),
("Partial fractions","Break rational functions into simpler terms.","For suitable rational functions, factor the denominator and decompose into easier fractions before integrating.",r"\frac{1}{x(x+1)}=\frac1x-\frac1{x+1}",r"\int\frac{1}{x(x+1)}dx=\ln|x|-\ln|x+1|+C",["Write 1/[x(x+1)]=A/x+B/(x+1).","Solve A=1, B=−1.","Integrate each logarithmic term."],"Factor and check polynomial division first when needed.","What is A in 1/[x(x+1)]=A/x+B/(x+1)?",["1","−1","0"],0,"Set x=0 to obtain A=1."),
("Improper integrals","Evaluate integrals with infinite bounds.","Replace an infinite bound or singular endpoint with a limit; the integral converges only if that limit is finite.",r"\int_1^\infty x^{-2}dx=1",r"\lim_{b\to\infty}[-1/x]_1^b=1",["Integrate x⁻² to −x⁻¹.","Evaluate from 1 to b.","Let b approach infinity to obtain 1."],"An infinite interval does not automatically mean divergence.","Does ∫₁∞ 1/x² dx converge?",["Yes, to 1","No","Yes, to 0"],0,"The limit is finite and equals 1."),
("Applications of integration","Model area and accumulated quantities.","Integrals can model area between curves, displacement from velocity, and other accumulated changes.",r"A=\int_a^b(\text{top}-\text{bottom})\,dx",r"A=\int_0^1(x-x^2)dx=\frac16",["On [0,1], x is above x².","Integrate x−x².","Evaluate x²/2−x³/3 at 1 and 0 to get 1/6."],"Check which curve is on top over the interval.","What is the area between y=x and y=x² on [0,1]?",["1/6","1/2","1"],0,"Integrate x−x² over [0,1].")
],
"Differential Equations": [
("What is a differential equation?","Recognize equations involving derivatives.","A differential equation relates an unknown function to one or more of its derivatives.",r"\frac{dy}{dx}=2x",r"y=x^2+C",["Recognize that y′=2x specifies a derivative.","Integrate both sides with respect to x.","The family y=x²+C satisfies the equation."],"The unknown is a function, not just a number.","Which is a differential equation?",["y=2","y′=2x","x=2"],1,"It contains a derivative."),
("Separable equations","Solve equations by separating variables.","If y′=g(x)h(y), rearrange into dy/h(y)=g(x)dx where division is valid.",r"\frac{dy}{dx}=xy",r"y=Ce^{x^2/2}",["For y≠0, divide by y: dy/y=x dx.","Integrate: ln|y|=x²/2+C.","Exponentiate; include y=0 through C=0."],"Division by y may discard the zero solution unless checked.","Which form is separable?",["y′=xy","y′+y=x","y′′+y=0"],0,"xy is a product of a function of x and a function of y."),
("First-order linear equations","Use an integrating factor.","A linear first-order ODE has form y′+P(x)y=Q(x). Multiply by μ=e^(∫P dx).",r"y'+P(x)y=Q(x)",r"y'+y=0\Rightarrow y=Ce^{-x}",["Here P=1, Q=0.","Integrating factor μ=eˣ.","Then (eˣy)′=0, so y=Ce⁻ˣ."],"The integrating factor multiplies the entire equation.","What is the integrating factor for y′+2y=x?",["eˣ","e²ˣ","2x"],1,"μ=e^(∫2 dx)=e²ˣ."),
("Exponential growth and decay","Interpret proportional rates of change.","When y′=ky, solutions are exponential; positive k means growth and negative k means decay.",r"y(t)=y_0e^{kt}",r"y'=2y,\ y(0)=3\Rightarrow y=3e^{2t}",["Write the general solution y=Ce²ᵗ.","Use y(0)=3 to find C=3.","The positive rate 2 means growth."],"The initial value sets the multiplier, not the exponent.","For y′=−y, does y grow or decay?",["Grow","Decay","Remain constant"],1,"A negative rate gives exponential decay."),
("Second-order linear equations","Solve constant-coefficient homogeneous equations.","Try y=e^(rx) to turn ay′′+by′+cy=0 into a polynomial equation in r.",r"ar^2+br+c=0",r"y''-3y'+2y=0\Rightarrow y=C_1e^x+C_2e^{2x}",["Form r²−3r+2=0.","Factor (r−1)(r−2)=0.","Combine the two exponential solutions."],"A second-order equation generally needs two initial conditions for a unique solution.","What are the roots of r²−3r+2=0?",["1 and 2","−1 and −2","0 and 3"],0,"(r−1)(r−2)=0."),
("Initial-value problems","Use initial conditions to choose a solution.","A general solution includes constants; initial values determine them when a unique solution exists.",r"y'=y,\quad y(0)=2",r"y=2e^x",["Solve y′=y to obtain y=Ceˣ.","At x=0, y=C.","Use y(0)=2 to get C=2."],"Do not forget to apply the given initial condition.","If y=Ceˣ and y(0)=5, what is C?",["1","5","e"],1,"e⁰=1, so y(0)=C.")
]
}


# Only these lesson topics have matching generated exercises. Never imply that
# an unrelated question/graph tests the same mathematical concept.
PRACTICE_LINKS = {
    ("Differential Calculus","Power rule"): "Power rule",
    ("Differential Calculus","Chain rule"): "Chain rule",
    ("Integral Calculus","Definite integrals"): "Definite integral",
    ("Integral Calculus","Substitution"): "Substitution",
    ("Differential Equations","Exponential growth and decay"): "Exponential growth",
}
# Curated examples for conceptual graphing, not plots of a student's answer.
GRAPH_EXAMPLES = {
    ("Differential Calculus","Derivative as slope"): ("x**2","derivative",(-3,3)),
    ("Differential Calculus","Power rule"): ("3*x**2+2*x","derivative",(-3,3)),
    ("Differential Calculus","Chain rule"): ("sin(x**2)","derivative",(-3,3)),
    ("Differential Calculus","Optimization"): ("-(x-2)**2+4","derivative",(-1,5)),
    ("Integral Calculus","Definite integrals"): ("x","area",(0,2)),
    ("Integral Calculus","Substitution"): ("2*x*cos(x**2)","antiderivative",(-2,2)),
    ("Differential Equations","Exponential growth and decay"): ("3*exp(2*x)","solution",(0,1)),
    ("Differential Calculus","Functions and notation"): ("x**2+1","solution",(-3,3)),
    ("Differential Calculus","Limits"): ("x+3","solution",(-1,4)),
    ("Differential Calculus","Continuity"): ("x**2","solution",(-3,3)),
    ("Differential Calculus","Product and quotient rules"): ("x**2*sin(x)","derivative",(-3,3)),
    ("Integral Calculus","Antiderivatives"): ("2*x","antiderivative",(-3,3)),
    ("Integral Calculus","Fundamental Theorem of Calculus"): ("3*x**2","area",(0,1)),
    ("Integral Calculus","Integration by parts"): ("x*exp(x)","antiderivative",(-1,2)),
    ("Integral Calculus","Partial fractions"): ("1/(x*(x+1))","antiderivative",(0.3,3)),
    ("Integral Calculus","Improper integrals"): ("1/x**2","area",(1,6)),
    ("Integral Calculus","Applications of integration"): ("x-x**2","area",(0,1)),
    ("Differential Equations","What is a differential equation?"): ("x**2","derivative",(-2,2)),
    ("Differential Equations","Separable equations"): ("exp(x**2/2)","solution",(-2,2)),
    ("Differential Equations","First-order linear equations"): ("exp(-x)","solution",(0,4)),
    ("Differential Equations","Second-order linear equations"): ("exp(x)+exp(2*x)","solution",(-1,1)),
    ("Differential Equations","Initial-value problems"): ("2*exp(x)","solution",(-1,2)),
}

def linked_practice(subject,topic):
    return PRACTICE_LINKS.get((subject,topic))

def lesson_graph(subject,topic):
    spec=GRAPH_EXAMPLES.get((subject,topic))
    if spec is None:return None
    import sympy as sp
    from guided_learning import lesson_plot,x
    expression,graph,domain=spec
    function=sp.sympify(expression,locals={"x":x})
    expected=sp.integrate(function,x) if graph=="antiderivative" else function
    return lesson_plot({"function":function,"expected":expected,"graph":graph,"domain":domain})

def open_linked_practice(subject,topic):
    import streamlit as st
    st.session_state["teaching_practice_target"]=(subject,topic)
    st.session_state["teaching_mode"]="Guided practice"

def advance_lesson(subject,topic):
    lessons=[item[0] for item in COURSES[subject]]
    index=lessons.index(topic)
    if index+1<len(lessons):
        st.session_state["teaching_topic"]=lessons[index+1]
    else:
        subjects=list(COURSES)
        next_subject=subjects[(subjects.index(subject)+1)%len(subjects)]
        st.session_state["teaching_subject"]=next_subject
        st.session_state["teaching_topic"]=COURSES[next_subject][0][0]

def checked_latex(expression):
    """Reject common accidental escape corruption before sending to Streamlit."""
    import re
    if not isinstance(expression,str) or not expression.strip():
        raise ValueError("Missing mathematical expression")
    if any(ch in expression for ch in ("\x08","\x09","\x0c","\x0d")):
        raise ValueError("LaTeX contains an escaped control character; use raw strings")
    if re.search(r"(?<![A-Za-z\\])(?:frac|int|lim|sin|cos|quad)(?=[{_\s]|$)",expression):
        raise ValueError("LaTeX command is missing its backslash")
    return expression


# Plain-language notation guide shown next to each lesson's formula.
NOTATION_GUIDES = {
("Differential Calculus","Functions and notation"): [
("Function", "A rule that assigns exactly one output to each allowed input."),
("f", "The name of the function. Other names such as g or h are also possible."),
("x", "The input (independent variable). You choose a value for x."),
("f(x)", "The output of function f when its input is x. It does NOT mean f multiplied by x."),
("x² + 1", "The rule: square the input, then add one."),
("f(2)", "The value of the function at x = 2; replace every x with 2."),
("Domain", "The set of input values the function allows."),
("Range", "The set of outputs the function produces."),
],
("Differential Calculus","Limits"): [
("lim", "The limit: the value a function approaches."),
("x → 2", "The input x gets closer and closer to 2."),
("f(x)", "The output of the function at input x."),
],
("Differential Calculus","Continuity"): [
("a", "The input where we are checking continuity."),
("f(a)", "The actual output at x = a."),
("lim x→a f(x)", "The value the outputs approach near a."),
],
("Differential Calculus","Derivative as slope"): [
("f′(x)", "The derivative: instantaneous rate of change of f."),
("h", "A small change in the input."),
("f(x+h)−f(x)", "The change in output."),
("d/dx", "An instruction to differentiate with respect to x."),
],
("Differential Calculus","Power rule"): [
("d/dx", "Differentiate with respect to x."),
("n", "The exponent (power) of x."),
("nxⁿ⁻¹", "Multiply by the old exponent, then reduce the exponent by one."),
],
("Differential Calculus","Product and quotient rules"): [
("u and v", "Two functions of x."),
("u′ and v′", "Their derivatives."),
("(uv)′", "Derivative of the product u times v."),
],
("Differential Calculus","Chain rule"): [
("f", "The outside function."),
("g", "The inside function."),
("f(g(x))", "A composite function: apply g first, then f."),
("g′(x)", "Derivative of the inside function."),
],
("Differential Calculus","Optimization"): [
("f′(c)=0", "The slope is zero at the candidate point c."),
("c", "A critical-point candidate; check whether it is a maximum or minimum."),
],
("Integral Calculus","Antiderivatives"): [
("∫", "The integral sign: find an antiderivative."),
("dx", "Integrate with respect to x."),
("n", "The exponent of x."),
("C", "An arbitrary constant of integration."),
],
("Integral Calculus","Definite integrals"): [
("∫ from a to b", "Accumulate signed change between the lower bound a and upper bound b."),
("f(x)", "The quantity being accumulated."),
("dx", "The variable of integration."),
],
("Integral Calculus","Fundamental Theorem of Calculus"): [
("F", "An antiderivative of f, meaning F′=f."),
("F(b)−F(a)", "Evaluate at the upper bound and subtract the lower-bound value."),
],
("Integral Calculus","Substitution"): [
("u", "A new variable representing the inner expression."),
("du", "Its differential, found by differentiating u."),
],
("Integral Calculus","Integration by parts"): [
("u", "A chosen function to differentiate."),
("dv", "The part chosen to integrate."),
("du", "The differential of u."),
("v", "An antiderivative of dv."),
],
("Integral Calculus","Partial fractions"): [
("x", "The variable."),
("1/x", "A simpler rational term whose antiderivative is ln|x|."),
],
("Integral Calculus","Improper integrals"): [
("∞", "An unbounded endpoint, handled using a limit."),
("Converges", "The limiting integral has a finite value."),
],
("Integral Calculus","Applications of integration"): [
("A", "Area between curves."),
("top − bottom", "Vertical distance between the upper and lower curves."),
],
("Differential Equations","What is a differential equation?"): [
("y", "The unknown function we want to find."),
("dy/dx", "How quickly y changes as x changes."),
("2x", "The specified rate of change at each x."),
("C", "An arbitrary constant in the family of solutions."),
],
("Differential Equations","Separable equations"): [
("dy/dx", "Rate of change of y with respect to x."),
("x and y", "The independent variable and unknown dependent function."),
],
("Differential Equations","First-order linear equations"): [
("y′", "The first derivative of the unknown function y."),
("P(x), Q(x)", "Known functions of x."),
],
("Differential Equations","Exponential growth and decay"): [
("y₀", "Initial amount at time zero."),
("k", "Growth/decay rate constant; positive means growth, negative decay."),
("t", "Time."),
],
("Differential Equations","Second-order linear equations"): [
("y′′", "Second derivative of y."),
("r", "A trial exponent used to find solutions."),
("a, b, c", "Constant coefficients of the differential equation."),
],
("Differential Equations","Initial-value problems"): [
("y(0)", "Value of the unknown function when x=0."),
("C", "Constant determined from the initial condition."),
],
}

def notation_guide(subject, topic):
    return NOTATION_GUIDES.get((subject,topic), [])

def render_teaching_library():
    st.subheader("Full Lessons · Start from the Basics")
    st.caption("Read the concept, follow the example, then answer a short understanding check. Progress is stored only in this browser session.")
    subject=st.selectbox("Choose a subject",list(COURSES),key="teaching_subject")
    names=[item[0] for item in COURSES[subject]]
    if st.session_state.get("teaching_topic") not in names:
        st.session_state["teaching_topic"]=names[0]
    topic=st.selectbox("Choose a lesson",names,key="teaching_topic")
    lesson=next(item for item in COURSES[subject] if item[0]==topic)
    title,objective,concept,formula,example,steps,pitfall,question,options,correct,explanation=lesson
    completed=st.session_state.setdefault("teaching_completed",set())
    done=sum((s,t) in completed for s,lessons in COURSES.items() for t,*_ in lessons)
    total=sum(len(v) for v in COURSES.values())
    st.progress(done/total,text=f"Understanding checks completed: {done}/{total} (this session)")
    st.markdown("#### 1. What you'll learn")
    st.write(objective)
    st.markdown("#### 2. Understand the idea")
    st.write(concept)
    st.markdown("#### 3. Formula and meaning")
    st.latex(checked_latex(formula))
    st.markdown("**What do the symbols mean?**")
    for symbol, meaning in notation_guide(subject, topic):
        st.markdown(f"- **{symbol}** — {meaning}")
    st.markdown("#### 4. Worked example")
    st.latex(checked_latex(example))
    for index,step in enumerate(steps,1): st.write(f"{index}. {step}")
    with st.expander("Common mistake to avoid"):st.warning(pitfall)
    st.markdown("#### 5. Explore a graph")
    if (subject,topic) in GRAPH_EXAMPLES:
        if st.checkbox("Show an illustrative graph for this concept",key="teaching_graph_"+subject+"_"+topic):
            try:
                import matplotlib.pyplot as plt
                fig=lesson_graph(subject,topic)
                st.pyplot(fig)
                plt.close(fig)
                st.caption("Illustrative example only; it does not represent your quiz answer.")
            except (ValueError,TypeError,OverflowError,RuntimeError) as exc:
                st.info("Graph unavailable for this example.")
    else:
        st.caption("A topic-specific graph is not yet available for this lesson.")
    st.markdown("#### 6. Check your understanding")
    st.write(question)
    choice=st.radio("Select your answer",options,index=None,key="quiz_"+subject+"_"+topic)
    if st.button("Check understanding",key="check_"+subject+"_"+topic):
        if choice is None:st.info("Choose an answer first.")
        elif options.index(choice)==correct:
            completed.add((subject,topic))
            st.success("Correct! "+explanation)
        else:st.warning("Not yet. "+explanation)
    if (subject,topic) in completed:
        st.success("Understanding check completed for this lesson (current session).")
    st.button("Next lesson",key="next_lesson_"+subject+"_"+topic,
              on_click=advance_lesson,args=(subject,topic))
    st.markdown("#### 7. Practice independently")
    match=linked_practice(subject,topic)
    if match:
        st.write("A matching randomized practice activity is available for this lesson.")
        st.button("Open matching guided practice",key="open_practice_"+subject+"_"+topic,
                  on_click=open_linked_practice,args=(subject,match))
    else:
        st.caption("A matching generated practice set is not yet available. You can still explore the separate Guided practice activity.")
    st.caption("Completion is saved only for this browser session; it is not a permanent student record.")
