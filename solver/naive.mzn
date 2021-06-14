
int: n;
int: max_w;
int: upper_bound = 50;
array[1..n] of int: w;
array[1..n] of int: h;
% 12
% x:                     4, 7, 7, 4, 0
% y:                     0, 0, 4, 3, 0

array[1..n] of var int: x;
array[1..n] of var int: y;

constraint forall(i in 1..n) (x[i] >= 0 /\ x[i] + w[i] <= max_w);
constraint forall(i in 1..n) (y[i] >= 0);

constraint forall(i in 0..(upper_bound-1)) (sum([ if ((i <= y[j] + h[j] - 1) /\ (i >= y[j])) then w[j] else 0 endif | j in 1..n]) <= max_w);
constraint forall(i in 0..(max_w-1)) (sum([ if ((i <= x[j] + w[j] - 1) /\ (i >= x[j])) then h[j] else 0 endif | j in 1..n]) <= max_y);

var int: max_y = max([ h[i]+y[i] | i in 1..n ]);
solve minimize max_y;

output ["Max Y: " ++ show(max_y) ++ "\nX: "++ show(x) ++ "\nY:" ++ show(y)];