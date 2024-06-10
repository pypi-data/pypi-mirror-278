
diversipy has been tested with Python 3.11. Everything in this package is pure
Python. For a description of the contents see DESCRIPTION.rst.


Changes
=======

0.9
---
* Fixed a bug in sukharev_grid, where valid combinations of num_points and
  dimension raised an exception due to rounding error.
* Gave maximin_reconstruction an additional parameter for a custom sampling
  function. This can be used to restrict candidate points according to the
  user's criteria.

0.8
---
* Added a callback function argument to greedy subset selection functions.
* Refactored stratified sampling and added new options for latinized stratified
  sampling. Stratification is now separated from sampling. Also added a function
  for reconstructing strata from existing, arbitrary point sets.
* Added rank-1 lattices.
* Deleted edge_lhs, centered_lhs, and perturbed_lhs in favor of new functions
  transform_spread_out, transform_cell_centered, transform_perturbed, and
  transform_anchored, because the transformations are also applicable to other
  design matrices.
* Fixed bug in calc_euclidean_dist_matrix and calc_manhattan_dist_matrix that
  appeared when input points where of integer type.

0.7
---
* Made stratified_sampling the default algorithm for generating the initial
  sample in maximin_reconstruction and random_k_means.
* Implemented the quality index of Wahl, Mercadier, and Helbert
  (diversipy.indicator.wmh_index).

0.6
---
* Added covering radius and lower and upper bounds for it to diversity
  indicators. (This function requires SciPy.)
* Added generalized stratified sampling to diversipy.hycusampling.

0.5
---
* Made some sampling and subset selection functions more robust with regard to
  existing points (now also an empty 2-D array is recognized as being empty).

0.4
---
* Added function hausdorff_dist in module indicator.
* Removed __future__ imports.

0.3
---
* Bugfix in select_greedy_maxisum when supplying points as list instead of
  numpy array.
* Added function select_greedy_energy in module subset.
* Slightly refined choice of the first point in select_greedy_maximin and
  select_greedy_maxisum.

0.2
---
* psa_partition and psa_select now raise exceptions when num_clusters or
  num_selected_points are <= 0.
* Added functions select_greedy_maximin and select_greedy_maxisum in module
  subset.

0.1.1
-----
* Fixed bug in installation script.

0.1
---
* Initial version.
