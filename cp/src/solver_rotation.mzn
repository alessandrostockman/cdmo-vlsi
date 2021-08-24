include "globals.mzn";

% ==== Input variables ==== 

int: plate_width;
int: num_circuits; % Number of total circuits to place
set of int: circuits = 1..num_circuits;

array[circuits] of int: widths;  % Array of widths of the circuits
array[circuits] of int: heights; % Array of heights of the circuits

% ==== Output variables ==== 

array[circuits] of var 0..plate_width-1: x;  
array[circuits] of var 0..sum(heights)-1: y;  
array[circuits] of var bool : r; 

var lower_bound..upper_bound: plate_height;

% ==== Support variables ==== 

int: upper_bound = sum([max(heights[i], widths[i]) | i in circuits]);
int: lower_bound = max(heights ++ widths);

array[circuits] of int : ordered_c = sort_by(circuits, [-heights[c]*widths[c] | c in circuits]); % solo heights, max , oppure area ??

array[circuits] of var int: actual_widths = [(widths[c]*(1-r[c]))+(heights[c]*r[c]) | c in circuits];
array[circuits] of var int: actual_heights = [(heights[c]*(1-r[c]))+(widths[c]*r[c]) | c in circuits];

% ==== Domain reduction ==== 

constraint forall(c in circuits) (x[c]<=plate_width-actual_widths[c])::domain;
constraint forall(c in circuits) (y[c]<=plate_height-actual_heights[c])::domain;

% ==== Constraints ==== 

constraint forall(c in circuits)(x[c] + actual_widths[c] <= plate_width /\ y[c] + actual_heights[c] <= plate_height);

% ==== Global constraints ==== 

constraint diffn(x, y, actual_widths, actual_heights);
constraint cumulative(x, actual_widths, actual_heights, plate_height);
constraint cumulative(y, actual_heights, actual_widths, plate_width);

% ==== Symmetry breaking constraints ====

% Dominance constraint, adjacent circuits are always better
constraint 
  forall(c in circuits)(
    member([0] ++ [x[o] + actual_widths[o] | o in circuits where o != c], x[c]) /\
    member([0] ++ [y[o] + actual_heights[o] | o in circuits where o != c], y[c])
  );

% Precedence constraint between same sized circuits
constraint symmetry_breaking_constraint(
  forall (c in circuits) (
    let {
      array[int] of int: equals = [i | i in c+1..num_circuits where widths[i] = widths[c] /\ heights[i] = heights[c]]
    } in 
      forall (i in 1..length(equals)-1) (lex_less([ y[equals[i-1]], x[equals[i-1]] ], [ y[equals[i]],x[equals[i]] ]))
  )
);

% The biggest circuit is always placed under and on the left wrt the second biggest
constraint symmetry_breaking_constraint(
  let {
    int: c1 = ordered_c[1], int: c2 = ordered_c[2]
  } in lex_less([y[c1],x[c1]], [y[c2],x[c2]])
);

% Square circuits should not be rotated
constraint symmetry_breaking_constraint(
  forall (c in circuits) (heights[c] = widths[c] -> r[c] = 0)
);

solve 
  :: seq_search([
      int_search([plate_height], first_fail, indomain_min, complete),
      bool_search(r,input_order, indomain_min,complete)
  ])
  minimize plate_height;