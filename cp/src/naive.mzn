include "globals.mzn";
include "cumulative.mzn";
include "alldifferent.mzn";

% ==== Input variables ==== 

int: num_circuits; % Number of total circuits to place
int: plate_width; % Plate width
array[1..num_circuits] of int: widths; % Array of widths of the circuits
array[1..num_circuits] of int: heights; % Array of heights of the circuits

% ==== Output variables ==== 

array[1..num_circuits] of var 0..plate_width-1: x;
array[1..num_circuits] of var 0..upper_bound-1: y;

var int: plate_height = max([ heights[i]+y[i] | i in 1..num_circuits ]);

% ==== Support variables ==== 

int: upper_bound = sum(heights); % Plate height upper bound: circuits height sum
int: lower_bound = max(heights); % Plate height lower bound: max circuit height

% ==== Bounds constraints ==== 

constraint plate_height >= max(heights);
constraint forall(i in 1..num_circuits) (x[i] + widths[i] <= plate_width);
constraint forall(i in 1..num_circuits) (y[i] + heights[i] <= upper_bound);

% ==== Overlapping constraints (?) ==== 

constraint diffn(x,y,widths,heights);
constraint cumulative(x, widths, heights, plate_height);
constraint cumulative(y, heights, widths, plate_width);

solve minimize plate_height;
