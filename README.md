Hungarian-algorithm

This module is an implementation of the Hungarian algorithm (i.e. Munkres or Kuhn-Munkres algorithm)

https://en.wikipedia.org/wiki/Hungarian_algorithm

for solving the assignment problem

https://en.wikipedia.org/wiki/Assignment_problem

even in the case in which the number of jobs is greater than the number of workers (i.e. the cost matrix is rectangular).

The cost matrix is generated using dimensions provided by the user, and contains random integer values drawn from an interval whose bounds are provided by the user.

When the number of jobs is greater than the number of workers, the cloning trick is used, namely the rows of the original cost matrix are duplicate in order to reach the number of columns. In this way, the cost matrix becomes square from rectangular. Each row in the original cost matrix is duplicated/cloned the same number of times.

The Hungarian algorithm gets the final cost matrix, and returns the assignment of jobs to workers. For the implementation of Hungarian algorithm, the Python implementation in scipy package was used.

https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.linear_sum_assignment.html