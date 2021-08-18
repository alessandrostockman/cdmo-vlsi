% Use this editor as a MiniZinc scratch book
include "globals.mzn";

int: plate_width;
int: num_circuits; % Number of total circuits to place
set of int: circuits = 1..num_circuits;


array[circuits] of int: widths;  % Array of widths of the circuits
array[circuits] of int: heights; % Array of heights of the circuits


array[circuits] of int : ordered_c = sort_by(circuits, [-heights[c]*widths[c] | c in circuits]); % solo heights, max , oppure area ??

array[circuits] of var 0..plate_width-1: x;  
array[circuits] of var 0..sum(heights)-1: y;  

array[circuits] of var 0..1 : r; 

var max(heights)..sum(heights): plate_height; 


constraint forall(c in ordered_c)(x[c] + (widths[c]*(1-r[c]))+(heights[c]*r[c]) <= plate_width /\ y[c] + (heights[c]*(1-r[c]))+(widths[c]*r[c]) <= plate_height);

constraint diffn(x,y,[(widths[c]*(1-r[c]))+(heights[c]*r[c]) | c in circuits] ,[(heights[c]*(1-r[c]))+(widths[c]*r[c]) | c in circuits]);

constraint cumulative(x, [(widths[c]*(1-r[c]))+(heights[c]*r[c]) | c in circuits], [(heights[c]*(1-r[c]))+(widths[c]*r[c]) | c in circuits], plate_height) /\ cumulative(y, [(heights[c]*(1-r[c]))+(widths[c]*r[c]) | c in circuits], [(widths[c]*(1-r[c]))+(heights[c]*r[c]) | c in circuits], plate_width);


%dominance , non esiste una situazione in cui rettangoli non attaccati è meglio di attaccati (contigui)
constraint 
  forall(c in ordered_c)(
    member([0] ++ [x[s] + (widths[s]*(1-r[s]))+(heights[s]*r[s]) | s in circuits where s != c], x[c]) /\
    member([0] ++ [y[s] + (heights[s]*(1-r[s]))+(widths[s]*r[s]) | s in circuits where s != c], y[c])
  );

%symmetry breacking , il circuito più grande sempre in basso a sinistra  
constraint
  let {int: o1 = ordered_c[1], int: o2 = ordered_c[2]}
  in lex_less([y[o1],x[o1]], [y[o2],x[o2]]);
  

solve :: 
  seq_search([
      int_search([plate_height], first_fail, indomain_min, complete),
      %int_search([y[r] | r in ordered_c], input_order, indomain_min,complete),
      %int_search([x[r] | r in ordered_c], input_order, indomain_min,complete),
      ])
  minimize plate_height;

%output ["Height  : ", show(plate_height)]





