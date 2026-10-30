"""Real-world scenario questions with deterministic, checked mathematical answers."""
import random
import sympy as sp
x=sp.Symbol('x',real=True)
SCENARIOS={
'Differential Calculus':{
'Beginner':('Velocity from position','Slope of a road'),
'Intermediate':('Expanding circular area','Projectile maximum height'),
'Advanced':('Maximum fenced area','Acceleration from position')},
'Integral Calculus':{
'Beginner':('Distance from velocity','Accumulated water flow'),
'Intermediate':('Channel cross-sectional area','Area of a triangular plot'),
'Advanced':('Storage tank volume','Rotating a profile')},
'Differential Equations':{
'Beginner':('Population growth','Continuous cooling'),
'Intermediate':('Bacterial growth','Radioactive decay model'),
'Advanced':('Damped displacement','Numerical population prediction')}}

def generate_scenario(subject,difficulty,rng=None,family=None):
 r=rng or random.Random(); a=r.randint(1,4);b=r.randint(2,6);c=r.randint(2,5)
 options=SCENARIOS[subject][difficulty]; fam=family or r.choice(options)
 if fam not in options:raise ValueError('Invalid scenario category')
 def item(prompt,expected,hint,steps):return dict(prompt=prompt,expected=sp.sstr(expected),hint=hint,steps=steps,kind='exact',family=fam,topic=fam)
 if fam=='Velocity from position':return item(f'A vehicle has s(t)={a}t²+{b}t meters. Find velocity at t={c} s.',2*a*c+b,'Differentiate displacement with respect to time.',f'v(t)={2*a}t+{b}; v({c})={2*a*c+b} m/s.')
 if fam=='Slope of a road':return item(f'A road elevation profile is h(x)={a}x²+{b}x meters. Find dh/dx at x={c}.',2*a*c+b,'Differentiate elevation to obtain the slope.',f'h′(x)={2*a}x+{b}; slope={2*a*c+b}.')
 if fam=='Expanding circular area':return item(f'A circular pond expands with dr/dt={a} m/min. Find dA/dt at radius {b} m.',2*sp.pi*a*b,'Differentiate A=πr² with respect to time.',f'dA/dt=2π({b})({a})={2*a*b}π m²/min.')
 if fam=='Projectile maximum height':return item(f'A model projectile has h(t)={b}t−{a}t² meters. Find its maximum height.',sp.Rational(b*b,4*a),'Set dh/dt to zero and substitute the time.',f't={b}/({2*a}); hmax={sp.Rational(b*b,4*a)} m.')
 if fam=='Maximum fenced area':return item(f'A rectangular garden has {4*b} m of fencing. Find its maximum enclosed area.',b*b,'For fixed perimeter, a square maximizes area.',f'Side={b} m; area={b*b} m².')
 if fam=='Acceleration from position':return item(f'A survey vehicle moves with s(t)={a}t³+{b}t² meters. Find acceleration at t={c} s.',6*a*c+2*b,'Acceleration is the second derivative of position.',f'a(t)={6*a}t+{2*b}; a({c})={6*a*c+2*b} m/s².')
 if fam=='Distance from velocity':return item(f'A cart travels with v(t)={a}t m/s. Find distance from t=0 to t={b} s.',sp.Rational(a*b*b,2),'Integrate nonnegative velocity over time.',f'∫₀^{b}{a}t dt={sp.Rational(a*b*b,2)} m.')
 if fam=='Accumulated water flow':return item(f'Water flows at Q(t)={a}t+{b} liters/min. How many liters pass in the first {c} minutes?',sp.Rational(a*c*c,2)+b*c,'Integrate flow rate over the time interval.',f'∫₀^{c}({a}t+{b})dt={sp.Rational(a*c*c,2)+b*c} L.')
 if fam=='Channel cross-sectional area':return item(f'A triangular drainage channel has depth d(x)={a}x/{b} meters for 0≤x≤{b} m. Find cross-sectional area.',sp.Rational(a*b,2),'Integrate depth over the horizontal width.',f'∫₀^{b}({a}/{b})x dx={sp.Rational(a*b,2)} m².')
 if fam=='Area of a triangular plot':return item(f'A plot has upper boundary y={a}x and lower boundary y=0, for 0≤x≤{b}. Find its area.',sp.Rational(a*b*b,2),'Integrate upper minus lower.',f'∫₀^{b}{a}x dx={sp.Rational(a*b*b,2)} square units.')
 if fam=='Storage tank volume':return item(f'A cylindrical storage tank has radius {a} m and length {b} m. Calculate its volume using the disk method.',sp.pi*a*a*b,'Integrate πr² over the length.',f'V=π∫₀^{b}{a}²dx={a*a*b}π m³.')
 if fam=='Rotating a profile':return item(f'Rotate y={a}x for 0≤x≤{b} about the x-axis. Find the volume of the resulting cone.',sp.pi*sp.Rational(a*a*b**3,3),'Use V=π∫y²dx.',f'V=π∫₀^{b}({a}x)²dx={sp.Rational(a*a*b**3,3)}π cubic units.')
 if fam=='Population growth':return item(f'A population starts at {b*100} and obeys dP/dt={a}P. Find P(t), using x for time.',b*100*sp.exp(a*x),'Solve the separable exponential-growth equation.',f'P(x)={b*100}exp({a}x).')
 if fam=='Continuous cooling':return item(f'A body is initially {b+c}°C in a {b}°C room and obeys dT/dt=−{a}(T−{b}). Find T(t), using x for time.',b+c*sp.exp(-a*x),'Solve for the temperature difference.',f'T(x)={b}+{c}exp(−{a}x).')
 if fam=='Bacterial growth':return item(f'A bacterial culture begins with {b*100} cells and grows at proportional rate {a}. Find P(t), using x for time.',b*100*sp.exp(a*x),'Separate dP/P=a dt.',f'P(x)={b*100}exp({a}x).')
 if fam=='Radioactive decay model':return item(f'A sample begins with {b*100} units and follows dM/dt=−{a}M. Find M(t), using x for time.',b*100*sp.exp(-a*x),'Use exponential decay.',f'M(x)={b*100}exp(−{a}x).')
 if fam=='Damped displacement':return item(f'A damped oscillator satisfies y′′+{2*a}y′+{a*a}y=0 with y(0)={b}, y′(0)=−{a*b}. Find y(t), using x for time.',b*sp.exp(-a*x),'Repeated characteristic root; apply initial values.',f'y(x)={b}exp(−{a}x).')
 if fam=='Numerical population prediction':return item(f'A population follows dP/dt={a}P and P(0)={b*100}. Use ONE Euler step h=0.1 to approximate P(0.1).',b*100+sp.Rational(a*b*100,10),'Use Pnext=P+h(aP).',f'{b*100}+0.1({a})({b*100})={b*100+sp.Rational(a*b*100,10)}.')
 raise ValueError('Unknown scenario')
