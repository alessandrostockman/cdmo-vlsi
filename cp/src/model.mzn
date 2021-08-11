include "globals.mzn";
include "alldifferent.mzn";

int: num_circuits = 5;
int: plate_width = 9;
array[1..num_circuits] of int: widths = [3,2,2,3,4];
array[1..num_circuits] of int: heights = [3,4,8,9,12];


int: max_plate_length = sum(heights);

set of int : X_coord = 0..plate_width-1;
set of int : Y_coord = 0..max_plate_length-1;

array[Y_coord,X_coord] of var 0..num_circuits : plate;

array[1..num_circuits] of var int: x;
array[1..num_circuits] of var int: y;


constraint forall(i in Y_coord,j in X_coord) (if plate[i,j]!=0 then ((heights[plate[i,j]]+i<max_plate_length) /\ (widths[plate[i,j]]+j<plate_width)) endif);

constraint alldifferent_except_0([plate[i,j] | i in Y_coord, j in X_coord]);


constraint forall(n in 0..num_circuits) (exists(i in Y_coord, j in X_coord)(plate[i,j]==n));

%constraint nvalue([plate[i,j] | i in Y_coord, j in X_coord])==num_circuits+1; 

constraint forall(i in Y_coord,j in X_coord) (if plate[i,j]!=0 then((y[plate[i,j]]=i) /\ (x[plate[i,j]]=j)) endif);     

constraint diffn_nonstrict(y,x,widths,heights);

var int : max_y = max([heights[i]+y[i] | i in 1..num_circuits]);

solve minimize max_y;

output ["Max Y: " ++ show(max_y) ++ "\nX: "++ show(x) ++ "\nY:" ++ show(y)];









