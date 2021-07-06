
int: num_circuits;
int: plate_width;
array[1..num_circuits] of int: widths;
array[1..num_circuits] of int: heights;
% 12
% x:                     4, 7, 7, 4, 0
% y:                     0, 0, 4, 3, 0

array[1..num_circuits] of var int: x;
array[1..num_circuits] of var int: y;
var int: upper_bound = sum(heights);

constraint forall(i in 1..num_circuits) (x[i] >= 0 /\ x[i] + widths[i] <= plate_width);
constraint forall(i in 1..num_circuits) (y[i] >= 0);

constraint forall(i in 0..(upper_bound-1)) (sum([ if ((i <= y[j] + heights[j] - 1) /\ (i >= y[j])) then widths[j] else 0 endif | j in 1..num_circuits]) <= plate_width);
constraint forall(i in 0..(plate_width-1)) (sum([ if ((i <= x[j] + widths[j] - 1) /\ (i >= x[j])) then heights[j] else 0 endif | j in 1..num_circuits]) <= max_y);

var int: max_y = max([ heights[i]+y[i] | i in 1..num_circuits ]);
solve minimize max_y;

output ["Max Y: " ++ show(max_y) ++ "\nX: "++ show(x) ++ "\nY:" ++ show(y)];