% Use this editor as a MiniZinc scratch book
include "globals.mzn";

int: plate_width;
int: num_circuits; % Number of total circuits to place
array[int] of int: widths; % widths of rectangles
array[int] of int: heights; % heights of rectangles


set of int: rectangle = index_set(heights);

array[int] of int : order = sort_by(rectangle, [-widths[r]*heights[r] | r in rectangle]);

array[rectangle] of var 0..plate_width: x;
array[rectangle] of var 0..sum(heights): y;

var max(heights)..sum(heights): plate_height;

constraint forall(r in rectangle)(x[r] + widths[r] <= plate_width /\ y[r] + heights[r] <= plate_height);

constraint diffn(x,y,widths,heights);

constraint cumulative(x, widths, heights, plate_height) /\ cumulative(y, heights, widths, plate_width);

constraint 
  forall(r in rectangle)(
    member([0] ++ [x[s] + widths[s] | s in rectangle where s != r], x[r]) /\
    member([0] ++ [y[s] + heights[s] | s in rectangle where s != r], y[r])
  );

constraint
  let {int: o1 = order[1], int: o2 = order[2]}
  in lex_less([y[o1],x[o1]], [y[o2],x[o2]]);
  
%constraint  forall(r in rectangle)(
%    let {array[int] of int: I = [i | i in rectangle where width[i]=width[r] /\ height[i]=height[r]]}
%    in if length(I)>1 /\ min(I)=r then
%  forall(i in index_set(I) where i>1)(lex_less( [y[I[i−1]],x[I[i−1]]], [y[I[i]],x[I[i]]]))
%     else true endif );

solve :: 
  int_search([plate_height], input_order, indomain_min, complete)
  :: seq_search([
      int_search([y[r] | r in order], input_order, indomain_min,complete),
      int_search([x[r] | r in order], input_order, indomain_min,complete),
      int_search([plate_height], input_order, indomain_min, complete),
      ])
  minimize plate_height;
  
  





