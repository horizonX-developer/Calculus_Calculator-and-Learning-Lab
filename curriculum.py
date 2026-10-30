"""Curriculum navigation and honest support indicators.

Listed topics are a roadmap, not claims of implemented solver coverage.
"""
SUBJECTS = {'Differential Calculus': {'Foundations': ['Functions and graphs',
                                           'Limits',
                                           'One-sided and infinite limits',
                                           'Continuity',
                                           'Derivative from first principles'],
                           'Differentiation': ['Power and sum rules',
                                               'Product and quotient rules',
                                               'Chain rule',
                                               'Trigonometric derivatives',
                                               'Inverse trigonometric derivatives',
                                               'Exponential and logarithmic derivatives',
                                               'Implicit differentiation',
                                               'Logarithmic differentiation',
                                               'Higher derivatives'],
                           'Applications': ['Tangent and normal lines',
                                            'Related rates',
                                            'Critical points and extrema',
                                            'Mean Value Theorem',
                                            'Optimization',
                                            'Curve sketching',
                                            'L’Hôpital’s rule',
                                            'Linear approximation and differentials'],
                           'Advanced': ['Parametric derivatives',
                                        'Polar derivatives',
                                        'Partial derivatives',
                                        'Directional derivatives',
                                        'Gradient and multivariable chain rule']},
 'Integral Calculus': {'Foundations': ['Antiderivatives',
                                       'Definite integrals',
                                       'Summation notation',
                                       'Left Riemann sums',
                                       'Right Riemann sums',
                                       'Midpoint Riemann sums',
                                       'Limits of Riemann sums',
                                       'Fundamental Theorem of Calculus'],
                       'Techniques': ['Power and substitution rules',
                                      'Integration by parts',
                                      'Trigonometric integrals',
                                      'Trigonometric substitution',
                                      'Partial fractions',
                                      'Improper integrals',
                                      'Numerical integration: trapezoidal',
                                      'Numerical integration: Simpson’s rule'],
                       'Applications': ['Area under a curve',
                                        'Area between curves',
                                        'Volumes: disks',
                                        'Volumes: washers',
                                        'Volumes: cylindrical shells',
                                        'Arc length',
                                        'Surface area of revolution',
                                        'Average value',
                                        'Work and fluid pressure',
                                        'Center of mass and moments'],
                       'Advanced': ['Polar area',
                                    'Parametric arc length',
                                    'Double integrals',
                                    'Triple integrals',
                                    'Line integrals',
                                    'Surface integrals']},
 'Differential Equations': {'Foundations': ['Order, degree, and classification',
                                            'Initial-value problems',
                                            'Slope fields',
                                            'Separable equations',
                                            'First-order linear equations',
                                            'Homogeneous first-order substitutions',
                                            'Exact equations',
                                            'Integrating factors',
                                            'Bernoulli equations'],
                            'Higher-order': ['Second-order constant coefficients',
                                             'Repeated and complex roots',
                                             'Nonhomogeneous equations',
                                             'Undetermined coefficients',
                                             'Variation of parameters',
                                             'Cauchy–Euler equations',
                                             'Higher-order linear equations'],
                            'Advanced': ['Laplace transforms',
                                         'Inverse Laplace transforms',
                                         'Systems of differential equations',
                                         'Power-series solutions',
                                         'Numerical Euler method',
                                         'Improved Euler method',
                                         'Runge–Kutta method',
                                         'Stability and phase portraits',
                                         'Introduction to PDEs'],
                            'Modeling': ['Population growth and decay',
                                         'Newton’s law of cooling',
                                         'Mixing problems',
                                         'Spring–mass systems',
                                         'Electrical circuits',
                                         'Logistic growth']}}
EXAMPLES = {'Differential Calculus': {'Power and sum rules': '3*x^2+4*x-5',
                           'Trigonometric derivatives': 'sin(x^2)',
                           'Chain rule': 'cos(x^3)',
                           'Exponential and logarithmic derivatives': 'log(x^2+1)',
                           'Product and quotient rules': 'x*exp(x)'},
 'Integral Calculus': {'Antiderivatives': '2*x',
                       'Power and substitution rules': '2*x*cos(x^2)',
                       'Integration by parts': 'x*exp(x)',
                       'Trigonometric integrals': 'sin(x)',
                       'Partial fractions': '1/(x^2-4)'},
 'Differential Equations': {'Separable equations': '2*x*y',
                            'First-order linear equations': 'x+y',
                            'Bernoulli equations': 'y+y^2'}}

# Topic-to-workspace links are conservative: a link means selected cases, not full coverage.
TOPIC_WORKSPACES = {
 'Differential Calculus': {
  'Limits':'Differential Foundations', 'One-sided and infinite limits':'Differential Foundations',
  'Continuity':'Differential Foundations','Derivative from first principles':'Differential Foundations',
  'Power and sum rules':'Guided Learning Paths','Chain rule':'Guided Learning Paths',
  'Higher derivatives':'Derivative Applications', 'Tangent and normal lines':'Derivative Applications',
  'Related rates':'Derivative Applications','Critical points and extrema':'Derivative Applications',
  'Optimization':'Derivative Applications',
  'Product and quotient rules':'Calculators','Trigonometric derivatives':'Calculators',
  'Inverse trigonometric derivatives':'Calculators','Exponential and logarithmic derivatives':'Calculators',
  'Implicit differentiation':'Calculators',
 },
 'Integral Calculus': {
  'Antiderivatives':'Calculators','Definite integrals':'Calculators',
  'Power and substitution rules':'Integral Techniques','Integration by parts':'Integral Techniques',
  'Trigonometric integrals':'Integral Techniques','Partial fractions':'Integral Techniques',
  'Improper integrals':'Calculators',
  'Left Riemann sums':'Integral Applications','Right Riemann sums':'Integral Applications',
  'Midpoint Riemann sums':'Integral Techniques',
  'Numerical integration: trapezoidal':'Integral Applications',
  'Numerical integration: Simpson’s rule':'Integral Techniques',
  'Area between curves':'Integral Applications','Volumes: disks':'Integral Applications',
  'Volumes: washers':'Integral Applications','Volumes: cylindrical shells':'Integral Applications',
  'Arc length':'Integral Applications','Surface area of revolution':'Integral Applications',
  'Average value':'Integral Applications Expanded','Work and fluid pressure':'Integral Applications Expanded',
  'Center of mass and moments':'Integral Applications Expanded',
 },
 'Differential Equations': {
  'Separable equations':'First-Order ODE Lessons','First-order linear equations':'First-Order ODE Lessons',
  'Homogeneous first-order substitutions':'ODE Methods','Exact equations':'ODE Methods',
  'Integrating factors':'First-Order ODE Lessons','Bernoulli equations':'First-Order ODE Lessons',
  'Second-order constant coefficients':'Higher-Order ODE Lessons',
  'Repeated and complex roots':'Higher-Order ODE Lessons',
  'Nonhomogeneous equations':'Higher-Order ODE Lessons',
  'Undetermined coefficients':'Higher-Order ODE Lessons',
  'Laplace transforms':'Higher-Order ODE Lessons',
  'Numerical Euler method':'ODE Methods',
  'Population growth and decay':'First-Order ODE Lessons',
  'Newton’s law of cooling':'First-Order ODE Lessons',
 }
}

def topic_status(subject,topic):
    if topic in TOPIC_WORKSPACES.get(subject,{}):
        return 'Partially available — selected examples or methods'
    return 'Planned — dedicated lesson not yet available'

def topic_workspace(subject,topic):
    return TOPIC_WORKSPACES.get(subject,{}).get(topic)

def render_curriculum(st):
    st.header('Curriculum explorer')
    st.info('Available links lead to supported introductory cases, not complete coverage of the named topic.')
    subject=st.selectbox('Subject',list(SUBJECTS),key='curriculum_subject')
    topics=[t for chapter in SUBJECTS[subject].values() for t in chapter]
    supported=sum(topic_workspace(subject,t) is not None for t in topics)
    st.caption(f'{supported} of {len(topics)} topics have a linked introductory workspace. This is not a curriculum completion score.')
    for chapter,chapter_topics in SUBJECTS[subject].items():
        with st.expander(chapter,expanded=False):
            for topic in chapter_topics:
                destination=topic_workspace(subject,topic)
                st.write(('🟡 ' if destination else '🕒 ')+topic+' — '+topic_status(subject,topic))
                if destination:
                    st.caption('Workspace: '+destination)
                    if st.button('Open '+topic,key='curriculum_open_'+subject+'_'+topic):
                        st.session_state['workspace_choice']=destination
                        # Sidebar area is derived from destination on the next rerun.
                        st.session_state.pop('learning_area', None)
                        st.rerun()
                if topic in EXAMPLES.get(subject,{}):
                    st.code(EXAMPLES[subject][topic],language=None)

def render_input_assistant(st,mode):
    st.subheader("Math input assistant")
    st.caption("Select an example to see valid input syntax. Copy it into the calculator below. Examples do not guarantee a complete derivation for every expression.")
    choices=EXAMPLES[mode]
    topic=st.selectbox("Example method",list(choices),key="input_method_"+mode)
    st.code(choices[topic],language=None)
    st.caption("Use * for multiplication, ^ for powers, parentheses for grouping, and sin(x), cos(x), tan(x), log(x), sqrt(x), exp(x). Angles are in radians. For first-order ODEs enter only the right side of dy/dx = F(x,y).")
