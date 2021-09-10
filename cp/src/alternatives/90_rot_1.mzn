% Use this editor as a MiniZinc scratch book
include "globals.mzn";
include "table.mzn";

int: plate_width;
int: num_circuits; % Number of total circuits to place
set of int: circuits = 1..num_circuits;


array[circuits] of int: widths;  % Array of widths of the circuits
array[circuits] of int: heights; % Array of heights of the circuits

array[circuits] of int : ordered_c = sort_by(circuits, [-widths[c]*heights[c] | c in circuits]); % solo heights, max , oppure area

array[circuits] of var 0..plate_width-1: x;  
array[circuits] of var 0..sum(heights)-1: y; 

array[circuits] of var 0..1 : r; 
array[circuits] of var int: actual_widths;
array[circuits] of var int: actual_heights;
array[1..num_circuits*2,1..3] of int : t;


var max(heights)..sum(heights) : plate_height; %= max([ heights[i]+y[i] | i in 1..num_circuits ]) ;  % seconda parte o no ???

%constraint forall(c in circuits) (t[c,1..3]=[0,widths[c],heights[c]] /\ t[c+num_circuits,1..3]=[1,heights[c],widths[c]]);

constraint forall(c in circuits) (table([r[c],actual_widths[c],actual_heights[c]],t));

constraint forall(c in ordered_c)(x[c] + actual_widths[c] <= plate_width /\ y[c] + actual_heights[c] <= plate_height);

constraint diffn(x,y,actual_widths,actual_heights);

constraint cumulative(x, actual_widths, actual_heights, plate_height) /\ cumulative(y, actual_heights, actual_widths, plate_width);


%dominance , non esiste una situazione in cui rettangoli non attaccati è meglio di attaccati (contigui)
constraint 
  forall(r in ordered_c)(
    member([0] ++ [x[s] + actual_widths[s] | s in circuits where s != r], x[r]) /\
    member([0] ++ [y[s] + actual_heights[s] | s in circuits where s != r], y[r])
  );

%symmetry breacking , il circuito più grande sempre in basso a sinistra  
constraint
  let {int: o1 = ordered_c[1], int: o2 = ordered_c[2]}
  in lex_less([y[o1],x[o1]], [y[o2],x[o2]]);


solve 
  :: int_search([plate_height],input_order,indomain_min, complete)
  minimize plate_height;
 
  




