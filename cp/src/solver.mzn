include "globals.mzn";
include "gecode.mzn"; % enabling LNS

% ==== Input variables ==== 

int: plate_width;
int: num_circuits; % Number of total circuits to place
set of int: circuits = 1..num_circuits;

array[circuits] of int: widths;  % Array of widths of the circuits
array[circuits] of int: heights; % Array of heights of the circuits

% ==== Output variables ==== 

array[circuits] of var 0..plate_width-min(widths): x;  
array[circuits] of var 0..upper_bound-min(heights): y;  

var lower_bound..upper_bound: plate_height;

% ==== Support variables ==== 

int: upper_bound = sum(heights); % Plate height upper bound: circuits height sum
int: lower_bound = max(heights); % Plate height lower bound: max circuit height

array[circuits] of int : ordered_c = sort_by(circuits, [-heights[c]*widths[c] | c in circuits]);

% ==== Domain reduction ==== 

constraint forall(c in circuits) (x[c]<=plate_width-widths[c])::domain;
constraint forall(c in circuits) (y[c]<=plate_height-heights[c])::domain;

% ==== Main constraint ==== 
constraint forall(c in circuits)(x[c] + widths[c] <= plate_width /\ y[c] + heights[c] <= plate_height);    %TODO: inutile 

% ==== Global constraints ==== 

constraint diffn(x,y,widths,heights);
constraint cumulative(x, widths, heights, plate_height);
constraint cumulative(y, heights, widths, plate_width);

% ==== Symmetry breaking constraints ====

% Dominance constraint, adjacent circuits are always better
constraint 
  forall(c in circuits)(
    member([0] ++ [x[o] + widths[o] | o in circuits where o != c], x[c]) /\
    member([0] ++ [y[o] + heights[o] | o in circuits where o != c], y[c])
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

% === Search ===
solve 
  :: int_search([plate_height], first_fail, indomain_min, complete)
  :: relax_and_reconstruct([plate_height], 70) 
  minimize plate_height;
