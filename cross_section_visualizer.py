"""Cross-sectional solids: base between y=0 and y=f(x), perpendicular to x."""
import numpy as np
import sympy as sp
import plotly.graph_objects as go
from volume_visualizer import sampled, X

SHAPES = ('Squares', 'Semicircles', 'Equilateral triangles')

def cross_section_area(f, a, b, shape):
    if shape not in SHAPES: raise ValueError('Unknown cross-section shape.')
    factor = {'Squares':sp.Integer(1), 'Semicircles':sp.pi/8, 'Equilateral triangles':sp.sqrt(3)/4}[shape]
    return factor*sp.integrate(f**2,(X,a,b))

def create_cross_section_figure(f,a,b,shape,slices=12,show_solid=True):
    if shape not in SHAPES: raise ValueError('Unknown cross-section shape.')
    if not float(a)<float(b): raise ValueError('Upper bound must exceed lower bound.')
    xs, widths = sampled(f,a,b,65)
    if np.any(widths < -1e-8): raise ValueError('The base width f(x) must be nonnegative throughout the interval.')
    widths=np.maximum(widths,0)
    t=np.linspace(0,1,42)
    if shape=='Squares':
        y=np.concatenate([t,np.ones_like(t),1-t,np.zeros_like(t)])
        z=np.concatenate([np.zeros_like(t),t,np.ones_like(t),1-t])
    elif shape=='Equilateral triangles':
        y=np.concatenate([t,1-t,np.zeros_like(t)])
        z=np.concatenate([np.zeros_like(t),np.sqrt(3)*t,np.sqrt(3)*(1-t)])/2
    else:
        theta=np.linspace(0,np.pi,100)
        y=(1+np.cos(theta))/2
        z=np.sin(theta)/2
    fig=go.Figure()
    if show_solid:
        xx=np.broadcast_to(xs[:,None],(len(xs),len(y)))
        yy=widths[:,None]*y[None,:]
        zz=widths[:,None]*z[None,:]
        fig.add_trace(go.Surface(x=xx,y=yy,z=zz,showscale=False,opacity=.65,name='Solid surface'))
    for ix in np.linspace(0,len(xs)-1,int(slices),dtype=int):
        fig.add_trace(go.Scatter3d(x=np.full(len(y),xs[ix]),y=widths[ix]*y,z=widths[ix]*z,mode='lines',line=dict(width=4),showlegend=False))
    fig.update_layout(height=530,margin=dict(l=0,r=0,t=15,b=0),scene=dict(xaxis_title='x',yaxis_title='Base width y',zaxis_title='Height z'),scene_aspectmode='data')
    return fig
