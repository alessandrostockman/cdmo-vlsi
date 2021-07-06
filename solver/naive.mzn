include "globals.mzn";
include "cumulative.mzn";
include "alldifferent.mzn";

int: num_circuits;
int: plate_width;
array[1..num_circuits] of int: widths;
array[1..num_circuits] of int: heights;

int: upper_bound = sum(heights);

array[1..num_circuits] of var 0..plate_width-1: x;
array[1..num_circuits] of var 0..upper_bound-1: y;


constraint forall(i in 1..num_circuits) (x[i] >= 0 /\ x[i] + widths[i] <= plate_width);
constraint forall(i in 1..num_circuits) (y[i] >= 0);

constraint forall(i in 0..(upper_bound-1)) (sum([ if ((i <= y[j] + heights[j] - 1) /\ (i >= y[j])) then widths[j] else 0 endif | j in 1..num_circuits]) <= plate_width);
constraint forall(i in 0..(plate_width-1)) (sum([ if ((i <= x[j] + widths[j] - 1) /\ (i >= x[j])) then heights[j] else 0 endif | j in 1..num_circuits]) <= max_y);


constraint diffn(y,x,heights,widths);
constraint cumulative(x, widths, heights, upper_bound);
constraint cumulative(y, heights, widths, plate_width);

/*
constraint forall(i in 1..num_circuits, j in 1..num_circuits) 
    (
        (
          (y[i] <= y[j] + heights[j] /\ y[i] >= y[j]) 
           / (y[i] + heights[i] <= y[j] + heights[j] /\ y[i] + heights[i] >= y[j])
        ) /\ i != j
        -> x[i] + widths[i] < x[j] / x[i] > x[j] + widths[j]
    );
*/

var int: max_y = max([ heights[i]+y[i] | i in 1..num_circuits ]);
solve minimize max_y;

output ["Max Y: " ++ show(max_y) ++ "\nX: "++ show(x) ++ "\nY:" ++ show(y)];