"""Small, verified parameterized integral-application practice bank."""
import random
import sympy as sp

x = sp.Symbol('x', real=True)
TOPICS = ('Riemann sums', 'Area between curves', 'Volume by disks', 'Volume by washers', 'Volume by shells')

def generate_application(topic, rng=None):
    r = rng if rng is not None else random.Random()
    a = r.randint(1, 5)
    b = r.randint(2, 5)
    n = r.choice((4, 6, 8))
    if topic == 'Riemann sums':
        # Right-endpoint sum of ax on [0,b].
        width = sp.Rational(b, n)
        value = sp.simplify(sum(a*(i*width)*width for i in range(1, n+1)))
        return dict(prompt=f'Find the RIGHT Riemann sum of f(x)={a}x on [0,{b}] using n={n} equal rectangles. Enter the numerical sum.', expected=str(value), kind='exact', hint='Compute Δx=(b−a)/n, then add f(xᵢ)Δx at each right endpoint.', steps=f'Δx={b}/{n}. Right endpoints xᵢ=iΔx. Rₙ=Σ({a}xᵢ)Δx={value}.')
    if topic == 'Area between curves':
        value = sp.integrate(a*x, (x,0,b))
        return dict(prompt=f'Find the area between y={a}x and y=0 for 0≤x≤{b}. Enter the numerical area.', expected=str(value), kind='exact', hint='Integrate upper curve minus lower curve over the interval.', steps=f'A=∫₀^{b} ({a}x−0)dx=[{a}x²/2]₀^{b}={value}.')
    if topic == 'Volume by disks':
        value = sp.pi*a*a*b
        return dict(prompt=f'Revolve y={a} (a horizontal line) over 0≤x≤{b} about the x-axis. Find the volume. Include pi in your answer.', expected=sp.sstr(value), kind='exact', hint='Use V=π∫R(x)² dx.', steps=f'V=π∫₀^{b}({a})²dx={a*a*b}π.')
    if topic == 'Volume by washers':
        outer = a+2
        value = sp.pi*(outer*outer-a*a)*b
        return dict(prompt=f'Revolve the region between y={outer} and y={a} over 0≤x≤{b} about the x-axis. Find the volume.', expected=sp.sstr(value), kind='exact', hint='Washer volume is π∫(R²−r²)dx.', steps=f'V=π∫₀^{b}({outer}²−{a}²)dx={sp.expand(value/sp.pi)}π.')
    if topic == 'Volume by shells':
        value = sp.pi*a*b*b
        return dict(prompt=f'Revolve the rectangle 0≤x≤{b}, 0≤y≤{a} about the y-axis. Find its volume using cylindrical shells.', expected=sp.sstr(value), kind='exact', hint='Use V=2π∫ radius×height dx.', steps=f'V=2π∫₀^{b}x({a})dx={a*b*b}π.')
    raise ValueError('Unknown practice topic')
