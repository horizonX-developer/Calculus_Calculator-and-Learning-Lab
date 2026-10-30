def answer_guidance(subject, prompt, mode='Curated Exercises'):
    """Return exercise-specific instructions shown before answer entry."""
    p = prompt.lower()
    if 'without the arbitrary constant' in p or 'c1=1' in p or 'c2=0' in p:
        return ('Function y(x)', 'Enter only the requested particular solution. Example: exp(x^2). Do not add an arbitrary constant unless the question asks for one.', 'exp(x^2)')
    if subject == 'Differential Equations':
        if any(t in p for t in ('approximation', 'approximate', 'euler', 'value at', 'evaluate')):
            return ('Numerical result', 'Enter a number or exact expression, for example 2.5 or 5/2. Do not type units.', '2.5')
        return ('Solution function', 'Enter y as an expression using x. For example, 2*exp(x). If constants are requested, use C, C1, or C2 exactly as specified in the question.', '2*exp(x)')
    if subject == 'Integral Calculus':
        if any(t in p for t in ('area', 'volume', 'riemann', 'sum', 'approximation', 'simpson', 'trapezoid', 'surface', 'arc length', 'definite', 'converge')):
            return ('Number or exact expression', 'Enter only the mathematical value (no units). Fractions such as 3/4, pi, and expressions like 4*pi are accepted.', '4*pi')
        return ('Antiderivative', 'Enter the resulting function of x, for example x^3/3. You may omit +C because any constant of integration is accepted.', 'x^3/3')
    if any(t in p for t in ('slope', 'rate at', 'velocity at', 'at x=', 'at x =', 'at t=', 'at t =', 'maximum', 'minimum', 'dimensions')):
        return ('Value or expression', 'Enter the requested value without units. Use 3/2 for fractions, or an expression such as sqrt(2).', '3/2')
    return ('Derivative or requested value', 'Enter the derivative as an expression in x. For example, 6*x+4 or 6x+4. Do not include the label f(x)=.', '6*x+4')


