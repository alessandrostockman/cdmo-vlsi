include "globals.mzn";

% ==== Input variables ==== 

int: plate_width;
int: num_circuits; % Number of total circuits to place
set of int: circuits = 1..num_circuits;

array[circuits] of int: widths;  % Array of widths of the circuits
array[circuits] of int: heights; % Array of heights of the circuits

% ==== Output variables ==== 

array[circuits] of var 0..plate_width-1: x;  
array[circuits] of var 0..upper_bound-1: y;  

var lower_bound..upper_bound: plate_height;

% ==== Support variables ==== 

int: upper_bound = sum(heights); % Plate height upper bound: circuits height sum
int: lower_bound = max(heights); % Plate height lower bound: max circuit height

array[circuits] of int : ordered_c = sort_by(circuits, [-heights[c]*widths[c] | c in circuits]); % solo heights, max , oppure area ??

% ==== Global constraints ==== 

constraint forall(c in ordered_c)(x[c] + widths[c] <= plate_width /\ y[c] + heights[c] <= plate_height);

constraint diffn(x,y,widths,heights);
constraint cumulative(x, widths, heights, plate_height) /\ cumulative(y, heights, widths, plate_width);

% Dominance constraint, adjacent circuits are always better
constraint 
  forall(r in ordered_c)(
    member([0] ++ [x[s] + widths[s] | s in circuits where s != r], x[r]) /\
    member([0] ++ [y[s] + heights[s] | s in circuits where s != r], y[r])
  );

% ==== Symmetry breaking constraints ====

% The biggest circuit is always placed under and on the left wrt the second biggest
constraint symmetry_breaking_constraint(
  let {
    int: o1 = ordered_c[1], int: o2 = ordered_c[2]
  } in lex_less([y[o1],x[o1]], [y[o2],x[o2]])
);

% Precedence constraint between same sized circuits
constraint forall(i in circuits, j in i+1..num_circuits) ( (widths[i] = widths[j] /\ heights[i] = heights[j]) -> (x[i] <= x[j] /\ y[i] <= y[j]) );

solve :: 
  seq_search([
    int_search([plate_height], first_fail, indomain_min, complete),
  ]) minimize plate_height;