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

var max(heights)..sum(heights): plate_height = max([ heights[i]+y[i] | i in 1..num_circuits ]); %serve la seconda parte ??

% constraint assert(length(order)=num_circuits,"error");

constraint forall(c in ordered_c)(x[c] + widths[c] <= plate_width /\ y[c] + heights[c] <= plate_height);

constraint diffn(x,y,widths,heights);

constraint cumulative(x, widths, heights, plate_height) /\ cumulative(y, heights, widths, plate_width);


%dominance , non esiste una situazione in cui rettangoli non attaccati è meglio di attaccati (contigui)
constraint 
  forall(r in ordered_c)(
    member([0] ++ [x[s] + widths[s] | s in circuits where s != r], x[r]) /\
    member([0] ++ [y[s] + heights[s] | s in circuits where s != r], y[r])
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





