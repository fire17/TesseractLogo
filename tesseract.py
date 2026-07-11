import math, itertools

# Tesseract Petrie projection: 4D hypercube -> octagonal star lattice.
# Basis angles offset 22.5deg so octagon vertices land at N/E/S/W like the original.
TH = [math.pi/8 + i*math.pi/4 for i in range(4)]
U = [(math.cos(t), math.sin(t)) for t in TH]

def proj(v):
    x = sum(c*U[i][0] for i, c in enumerate(v))
    y = sum(c*U[i][1] for i, c in enumerate(v))
    return x, y

verts = list(itertools.product((-1, 1), repeat=4))
R = max(math.hypot(*proj(v)) for v in verts)
S, C = 460/R, 500  # fit radius 460 in 1000x1000, centered

def pt(v):
    x, y = proj(v)
    return (C + x*S, C - y*S)

edges = [(a, b) for a, b in itertools.combinations(verts, 2)
         if sum(i != j for i, j in zip(a, b)) == 1]
assert len(verts) == 16 and len(edges) == 32

def lines(w, color):
    return "\n".join(
        f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" '
        f'stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
        for (x1, y1), (x2, y2) in (map(pt, e) for e in edges))

def emit(name, w_out, w_in, bg, outer, inner):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">
<rect width="1000" height="1000" fill="{bg}"/>
{lines(w_out, outer)}
{lines(w_in, inner)}
</svg>'''
    open(name, "w").write(svg)

for tag, w_out, w_in in [("", 15, 9), ("thin-", 7, 3.5)]:
    emit(f"tesseract-{tag}outlined.svg", w_out, w_in, "white", "black", "white")
    emit(f"tesseract-{tag}solid.svg",    w_out, w_in, "white", "black", "black")
    emit(f"tesseract-{tag}outlined-inverted.svg", w_out, w_in, "black", "white", "black")
    emit(f"tesseract-{tag}solid-inverted.svg",    w_out, w_in, "black", "white", "white")
print("ok", len(edges), "edges, outer radius", round(R, 3))
