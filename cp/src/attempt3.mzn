% Use this editor as a MiniZinc scratch book
include "globals.mzn";

int: plate_width;
int: num_circuits; % Number of total circuits to place
set of int: circuits = 1..num_circuits;


array[circuits] of int: widths;  % Array of widths of the circuits
array[circuits] of int: heights; % Array of heights of the circuits


array[circuits] of int : ordered_c = sort_by(circuits, [-widths[c]*heights[c] | c in circuits]); 

array[circuits] of var 0..plate_width-1: x;   %-1 ??
array[circuits] of var 0..sum(heights)-1: y;  %-1 ??

var max(heights)..sum(heights): plate_height;

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

constraint
  let {int: o1 = ordered_c[1], int: o2 = ordered_c[2]}
  in lex_less([y[o1],x[o1]], [y[o2],x[o2]]);
  
% constraint  forall(r in rectangle)(
%    let {array[int] of int: I = [i | i in rectangle where width[i]=width[r] /\ height[i]=height[r]]}
%    in if length(I)>1 /\ min(I)=r then
%  forall(i in index_set(I) where i>1)(lex_less( [y[I[i−1]],x[I[i−1]]], [y[I[i]],x[I[i]]]))
%     else true endif );

constraint  forall(r in circuits)(
   let {array[int] of int: I = [i | i in circuits where widths[i]=widths[r] /\ heights[i]=heights[r]]}
   in (
     if (length(I)>1 /\ min(I)=r) then
       forall (i in index_set(I) where i>1) (lex_less([y[I[i-1]],x[I[i-1]]],[y[I[i]],x[I[i]]]))
     else true 
     endif ));

% solve :: 
%   int_search([plate_height], first_fail, indomain_min, complete)
%   :: seq_search([
%       int_search([y[r] | r in ordered_c], input_order, indomain_min,complete),
%       int_search([x[r] | r in ordered_c], input_order, indomain_min,complete),
%       int_search([plate_height], input_order, indomain_min, complete),
%       ])
%   minimize plate_height;

% solve :: 
%   int_search([y[r] | r in ordered_c] ++ [x[r] | r in ordered_c] ++ [plate_height], first_fail, indomain_min, complete)     
%   minimize plate_height;

solve :: 
  int_search([plate_height], first_fail, indomain_min, complete)
  minimize plate_height;
  
  





