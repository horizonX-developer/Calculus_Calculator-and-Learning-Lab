"""Practice mode with curated, verified exercises and safe symbolic answer checking."""
import streamlit as st
import sympy as sp
from math_input import normalize_math
from practice_generator import generate, check_answer, families
from practice_topics import TOPICS, generate_application
from scenario_generator import generate_scenario, SCENARIOS
import random
from answer_guidance import answer_guidance
from display_notation import readable_math
from practice_visuals import show_practice_visual

# Each entry is (prompt, expected expression, hint, worked explanation).
BANK = {
    'Differential Calculus': {
        'Beginner': [
            ('Differentiate f(x) = 3*x^2 + 4*x - 5', '6*x+4', 'Apply the power rule separately to each term.', 'd(3x²)/dx = 6x, d(4x)/dx = 4, and the derivative of -5 is 0.'),
            ('Differentiate f(x) = sin(x)', 'cos(x)', 'Recall the basic derivative of sine.', 'The derivative of sin(x) is cos(x).'),
        ],
        'Intermediate': [
            ('Differentiate f(x) = sin(x^2)', '2*x*cos(x^2)', 'Use the chain rule with u = x².', 'd(sin u)/dx = cos(u)u′; u′=2x, giving 2x cos(x²).'),
            ('Differentiate f(x) = x*exp(x)', 'exp(x)*(x+1)', 'Use the product rule.', 'f′ = (1)eˣ + x(eˣ) = eˣ(x+1).'),
        ],
        'Advanced': [
            ('Differentiate f(x) = log(x^2+1)', '2*x/(x^2+1)', 'Use the logarithmic chain rule.', 'd ln(u)/dx = u′/u, with u=x²+1.'),
        ],
    },
    'Integral Calculus': {
        'Beginner': [
            ('Find an antiderivative of 2*x', 'x^2', 'Increase the exponent by one and divide by the new exponent.', '∫2x dx = 2(x²/2)+C = x²+C.'),
            ('Find an antiderivative of cos(x)', 'sin(x)', 'Which function has cosine as its derivative?', '∫cos(x) dx = sin(x)+C.'),
        ],
        'Intermediate': [
            ('Find an antiderivative of 2*x*cos(x^2)', 'sin(x^2)', 'Let u=x², so du=2x dx.', '∫2x cos(x²) dx = ∫cos(u) du = sin(u)+C = sin(x²)+C.'),
            ('Find an antiderivative of x*exp(x)', 'exp(x)*(x-1)', 'Use integration by parts: u=x and dv=eˣ dx.', '∫xeˣ dx = xeˣ − ∫eˣ dx = eˣ(x−1)+C.'),
        ],
        'Advanced': [
            ('Find an antiderivative of 1/(x^2-1)', 'log(x-1)/2-log(x+1)/2', 'Decompose into partial fractions.', '1/(x²−1) = 1/[2(x−1)] − 1/[2(x+1)]. Integrate to obtain ½ln|x−1| − ½ln|x+1| + C, for |x|>1.'),
        ],
    },
    'Differential Equations': {
        'Beginner': [
            ('Solve dy/dx = 2*x*y. Enter y(x), without the arbitrary constant (set C=1).', 'exp(x^2)', 'Separate dy/y = 2x dx.', 'Integrating gives ln|y|=x²+C, hence y=Ce^(x²). For C=1, y=e^(x²).'),
        ],
        'Intermediate': [
            ('Solve dy/dx = y, y(0)=2. Enter y(x).', '2*exp(x)', 'Separate variables and use y(0)=2.', 'ln|y|=x+C, so y=Ceˣ; y(0)=2 gives C=2.'),
        ],
        'Advanced': [
            ('Solve y\'\' + 3*y\' + 2*y = 0. Enter one solution with C1=1 and C2=0.', 'exp(-x)', 'Find roots of r²+3r+2=0.', 'The roots are −1 and −2, so y=C1e^(−x)+C2e^(−2x). With C1=1, C2=0, y=e^(−x).'),
        ],
    },
}

def insert_math_token(token):
    """Streamlit button callback: executes before text_input is instantiated on rerun."""
    old = st.session_state.get('practice_answer', '')
    st.session_state['practice_answer'] = (
        '' if token == 'Clear' else old[:-1] if token == 'Backspace' else old + token
    )
    st.session_state['practice_feedback'] = None


def render_practice(parse):
    st.header('📝 Student Practice Mode')
    st.caption('Try the question first. Use hints when needed, then check your answer. All exercises are curated examples.')
    mode = st.radio('Question source', ['Curated Exercises', 'Generate New Exercise', 'Real-World Scenario'], horizontal=True, key='practice_mode')
    subject = st.selectbox('Practice subject', list(BANK), key='practice_subject')
    difficulty = st.selectbox('Difficulty', ['Beginner', 'Intermediate', 'Advanced'], key='practice_difficulty')
    topic = None
    if mode != 'Curated Exercises':
        choices = ['Random topics', *(SCENARIOS[subject][difficulty] if mode == 'Real-World Scenario' else families(subject, difficulty))]
        if subject == 'Integral Calculus' and mode == 'Generate New Exercise':
            choices += [t for t in TOPICS if t not in choices]
        topic = st.selectbox('Practice topic', choices, key='practice_topic')
    if mode != 'Curated Exercises':
        identity_base = (subject, difficulty, mode, topic)
        def create_item():
            if mode == 'Real-World Scenario':
                return generate_scenario(subject, difficulty, random.Random(), topic if topic in SCENARIOS[subject][difficulty] else None)
            if topic in TOPICS: return generate_application(topic, random.Random())
            return generate(subject, difficulty, False, random.Random(), family=topic if topic in families(subject, difficulty) else None)
        if st.session_state.get('generated_base') != identity_base:
            st.session_state['generated_base'] = identity_base
            st.session_state['generated_number'] = 0
            st.session_state['generated_item'] = create_item()
            st.session_state['practice_answer'] = ''
            st.session_state['practice_feedback'] = None
        if st.button('🎲 Generate New Exercise', key='generate_exercise'):
            st.session_state['generated_number'] += 1
            st.session_state['generated_item'] = create_item()
            st.session_state['practice_answer'] = ''
            st.session_state['practice_feedback'] = None
        item = st.session_state['generated_item']
        prompt, expected, hint, explanation = item['prompt'], item['expected'], item['hint'], item['steps']
        identity = ('generated', subject, difficulty, mode, topic, st.session_state['generated_number'])
        index = None
    else:
        questions = BANK[subject][difficulty]
        index = st.selectbox('Exercise', range(len(questions)), format_func=lambda i: f'Exercise {i+1}', key='practice_index')
        prompt, expected, hint, explanation = questions[index]
        identity = (subject, difficulty, index)

    if st.session_state.get('practice_identity') != identity:
        st.session_state['practice_identity'] = identity
        st.session_state['practice_feedback'] = None
        st.session_state['practice_answer'] = ''
    if mode != 'Curated Exercises':
        st.caption('Method: ' + item.get('family', item.get('topic','Application')))
    st.info(readable_math(prompt))
    if st.button('Show hint', key='practice_hint'):
        st.session_state['practice_hint_for'] = identity
    if st.session_state.get('practice_hint_for') == identity:
        st.write('**Hint:**', hint)
    answer_type, answer_note, answer_example = answer_guidance(subject, prompt, mode)
    st.markdown(f'**What should I enter? — {answer_type}**')
    st.info(answer_note)
    with st.expander('⌨️ How to type mathematical answers (examples)'):
        st.markdown('''- **Powers:** `x^2`, `x²`, `e^(x^2)`
- **Multiplication:** `2*x` or `2x`
- **Fractions:** `3/4`, `(x+1)/(x-1)`
- **Roots and constants:** `sqrt(x)`, `√(x)`, `pi`, `π`
- **Functions:** `sin(x)`, `cos(x)`, `ln(x)`, `exp(x)`
- **Antiderivatives:** enter the function; `+C` is optional
- **Word problems:** enter the requested value or function, **not a sentence**; omit units
- **Differential equations:** enter `y(x)` as an expression, following the constant instructions in the question.

Use **x** as the independent variable when the question says so. Some scenario templates also require **x** even when the story refers to time `t`; follow the question's wording.''')
    answer = st.text_input('Your mathematical answer', key='practice_answer', placeholder=f'Example: {answer_example}', help=answer_note)
    cols = st.columns(6)
    buttons = ['x','²','^','e^(', '√(', 'π', '+','−','×','/','(',')','sin(','cos(','tan(','ln(','Backspace','Clear']
    for i, token in enumerate(buttons):
        cols[i % 6].button(
            token, key=f'math_key_{i}', use_container_width=True,
            on_click=insert_math_token, args=(token,)
        )
    if answer.strip():
        try:
            preview = parse(answer)
            st.latex(sp.latex(preview))
        except (ValueError, SyntaxError, TypeError, OverflowError):
            st.caption('Complete the expression to see its mathematical preview.')
    submitted = st.button('Check my answer', key='practice_check')
    if submitted:
        try:
            user_expr = parse(answer.strip())
            expected_expr = parse(expected)
            if mode != 'Curated Exercises':
                correct = check_answer(parse, answer, item)
            elif subject == 'Integral Calculus':
                # Antiderivatives may differ by a constant.
                correct = sp.simplify(sp.diff(user_expr-expected_expr, sp.Symbol('x', real=True))) == 0
            else:
                correct = sp.simplify(user_expr-expected_expr) == 0
            st.session_state['practice_feedback'] = ('correct' if correct else 'retry', identity)
            if correct:
                solved = st.session_state.setdefault('practice_solved', set())
                solved.add(identity)
        except Exception as exc:
            st.session_state['practice_feedback'] = ('invalid', identity)
    feedback = st.session_state.get('practice_feedback')
    if feedback and feedback[1] == identity:
        if feedback[0] == 'correct': st.success('Correct! Your answer is symbolically equivalent to the expected result.')
        elif feedback[0] == 'retry': st.warning('Not equivalent to the expected answer. Try again or use the hint.')
        else: st.error('I could not interpret this expression. Try e^(x²), 2x, sin(x), or use the math keyboard.')
    with st.expander('Explore a graph of this exercise'):
        st.caption('A graph can help you check the shape or behavior of the mathematical result. Not every word problem has a meaningful graph.')
        show_practice_visual(subject, prompt, expected, parse, item if mode != 'Curated Exercises' else None)
    with st.expander('Reveal worked solution'):
        st.write(readable_math(explanation))
        st.caption('Reveal this after attempting the question for the best learning experience.')
    curated_total = sum(len(q) for sub in BANK.values() for q in sub.values())
    curated_done = sum(1 for ident in st.session_state.get('practice_solved', set()) if len(ident)==3 and ident[0] != 'generated')
    st.metric('Curated exercises solved', f'{curated_done}/{curated_total}')
    generated_done = sum(1 for ident in st.session_state.get('practice_solved', set()) if ident[0] == 'generated')
    st.caption(f'Generated exercises solved this session: {generated_done}')
    if mode != 'Curated Exercises':
        solved_topics = sorted({i[4] for i in st.session_state.get('practice_solved', set())
                                if len(i) >= 6 and i[0] == 'generated' and i[1] == subject})
        if solved_topics:
            with st.expander('Topics practiced successfully this session'):
                st.write(', '.join(str(t) for t in solved_topics if t is not None) or 'Random topics')
    st.caption('Progress is stored in this browser session only and resets when the session ends.')
