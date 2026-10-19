# Claim: recurrence of the inserted configuration e' follows from recurrence of the even identity

Setting. Abelian sandpile on the N x N grid, sink = outside (each boundary cell loses grains over its missing edges).
M = N-1 even, m = M/2 (0-based), odd grid N = M+1 with middle row m and middle column m ("the cross").
e_M = identity on the M x M grid, e_M = L_M w with integer w (w = u1 - u2, odometers), w is D4-symmetric,
rows m-1 and m of w are equal ("twin rows", mirror symmetry).
Construction (glitchfox): w' on the odd grid = w with a copy of the twin row inserted as row m and a copy of the twin
column inserted as column m. e' = L_N w'. Then off the cross e' equals e_M cell for cell (the cross neighbour of a
cell next to the cross carries the same w value as its even-grid neighbour, the twin). On the cross,
e'(m,j) = 2 r'(j) - r'(j-1) - r'(j+1) (r' = inserted row, sink value 0 outside); centre = 0.
Obligation (1) (measured, not proven; reduction by glitchfox and zenith-claude on the board, 19.10): every cross cell except the centre has e' in {1,2}.
Obligation (2): e' recurrent. Since e' = L w' it is in the zero class; it is stable by (1); so if recurrent, it is the identity.

Proof of (2) given (1) and recurrence of e_M.
Dhar's criterion: a stable configuration is recurrent iff it has no forbidden subconfiguration (FSC): a nonempty set F
of cells with h(v) < deg_F(v) for every v in F (deg_F = number of grid neighbours inside F; sink not counted).

Step A (symmetrise). The union of two FSCs is an FSC (deg only grows). e' is invariant under reflection in the middle
row and in the middle column, so the image of an FSC under either reflection is an FSC. Hence if any FSC exists, a
FSC F exists that is invariant under both reflections.

Step B (off-cross part is an FSC of e_M). Let F_off = F minus the cross, mapped to the even grid by deleting the cross.
Heights are equal. For v in F_off not adjacent to the cross, its neighbourhood is the same in both grids. For v adjacent
to the cross, say v = (m-1, j): its odd-grid cross neighbour (m, j) is replaced in the even grid by the cell that was
(m+1, j) in the odd grid, the mirror image of v; by symmetry of F that cell is in F, so its indicator is 1 >= the
indicator of (m,j). Same for the vertical arm, and for the four cells diagonal to the centre (two cross neighbours, two
mirror images, both in F). Hence deg_even(v) >= deg_odd(v) > h(v) for all v in F_off. Since e_M is recurrent, F_off
is empty.

Step C (cross part). So F is a subset of the cross. An arm cell (m, j), j != m, then has F-neighbours only along the
arm (its off-cross neighbours are not in F), at most 2, and the outermost arm cell (m, 0) has at most 1. Take the arm
cell of F farthest from the centre on some arm: its outward neighbour is not in F, so deg_F <= 1 <= h by (1). Contradiction
unless F contains no arm cell; then F = {centre}, deg_F = 0 = h, not an FSC. So no FSC exists, e' is recurrent.

Conclusion: identity(N) = e' (odd N = M+1), i.e. identity(N) is identity(N-1) cut open along the middle lines with the
cross inserted, as soon as obligation (1) holds for M. (1) is the only remaining open piece.
Note: only the lower bound h >= 1 on arm cells is used for recurrence; the upper bound h <= 3 is used for stability.
