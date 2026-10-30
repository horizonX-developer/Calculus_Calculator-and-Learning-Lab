"""3D teaching visualizations for volumes of revolution (not a proof of geometry)."""
import numpy as np
import sympy as sp
import plotly.graph_objects as go

X = sp.Symbol('x', real=True)

def sampled(expr, a, b, count=45):
    fn = sp.lambdify(X, expr, modules='numpy')
    xs = np.linspace(float(a), float(b), count)
    with np.errstate(all='ignore'):
        vals = np.asarray(fn(xs), dtype=float)
    if vals.ndim == 0:
        vals = np.full(xs.shape, float(vals))
    if vals.shape != xs.shape or not np.all(np.isfinite(vals)) or np.max(np.abs(vals)) > 1e5:
        raise ValueError('Functions must be finite and reasonably sized throughout the interval.')
    return xs, vals

def create_volume_figure(kind, f, g, a, b, slices=14, show_solid=True):
    """Return a rotatable Plotly figure for disk/washer/shell examples.

    Disk and washer rotate around x; shells rotate vertical strips around y.
    """
    if not float(a) < float(b):
        raise ValueError('Upper bound must exceed lower bound.')
    xs, outer = sampled(f, a, b)
    inner = None
    if kind == 'Volume: washers':
        _, inner = sampled(g, a, b)
        if np.any(inner < -1e-8) or np.any(outer < inner-1e-8):
            raise ValueError('Washer visualization requires 0 ≤ inner radius ≤ outer radius.')
    elif kind == 'Volume: disks':
        if np.any(outer < -1e-8):
            raise ValueError('Disk visualization requires nonnegative radius.')
        inner = np.zeros_like(outer)
    elif kind == 'Volume: cylindrical shells':
        _, heights = sampled(g, a, b)
        if a < 0 or np.any(outer < -1e-8) or np.any(heights < -1e-8):
            raise ValueError('Shell visualization requires x ≥ 0, nonnegative radius and height.')
        # The existing application defines f as radius and g as height;
        # for a physically consistent x-axis shell model require f(x)=x.
        if np.max(np.abs(outer-xs)) > 1e-5:
            raise ValueError('For this shell visualizer enter f(x)=x (radius from the y-axis).')
    else:
        raise ValueError('Unsupported volume method.')
    theta=np.linspace(0,2*np.pi,52)
    fig=go.Figure()
    if kind in ('Volume: disks','Volume: washers'):
        if show_solid:
            for radii, name, opacity in ((outer,'Outer surface',0.65),(inner,'Inner surface',0.8)):
                if name=='Inner surface' and np.allclose(radii,0):continue
                xx=np.broadcast_to(xs[:,None],(len(xs),len(theta)))
                yy=radii[:,None]*np.cos(theta)[None,:]
                zz=radii[:,None]*np.sin(theta)[None,:]
                fig.add_trace(go.Surface(x=xx,y=yy,z=zz,opacity=opacity,showscale=False,name=name,showlegend=True))
        for ix in np.linspace(0,len(xs)-1,int(slices),dtype=int):
            ro=outer[ix]; ri=inner[ix]
            for rad in ([ro] if ri<1e-9 else [ro,ri]):
                fig.add_trace(go.Scatter3d(x=np.full(len(theta),xs[ix]),y=rad*np.cos(theta),z=rad*np.sin(theta),mode='lines',line=dict(width=3),showlegend=False))
        fig.update_layout(scene=dict(xaxis_title='x',yaxis_title='y',zaxis_title='z'))
    else:
        _, heights=sampled(g,a,b)
        chosen=np.linspace(0,len(xs)-1,int(slices),dtype=int)
        for ix in (range(len(xs)) if show_solid else chosen):
            if show_solid and ix not in chosen and ix%3:continue
            r=xs[ix]; h=heights[ix]
            tt=np.broadcast_to(theta[None,:],(2,len(theta)))
            yy=np.broadcast_to(np.array([0,h])[:,None],tt.shape)
            xx=r*np.cos(tt); zz=r*np.sin(tt)
            fig.add_trace(go.Surface(x=xx,y=yy,z=zz,showscale=False,opacity=.22 if show_solid else .5,showlegend=False))
        fig.update_layout(scene=dict(xaxis_title='x',yaxis_title='height (y)',zaxis_title='z'))
    fig.update_layout(height=530,margin=dict(l=0,r=0,t=20,b=0),scene_aspectmode='data')
    return fig
