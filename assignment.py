import os
import sys
import numpy as np
from scipy.optimize import linear_sum_assignment
import time


def create_cost_matrix(n_workers, n_jobs, low, high):
	"""
	This function creates a cost matrix for specific numbers of workers and jobs with random integer values from the [low, high) interval.
	If the number of jobs is greater than the number of workers, then the rows of the matrix are cloned to get a new augmented square matrix.

	:param n_workers: the number of workers
	:type: int
	:param n_jobs: the number of jobs
	:type: int
	:param low: the lower bound of the interval from which the random integer values are drawn
	:type: int
	:param high: the upper bound of the interval from which the random integer values are drawn
	:type: int
	:return: the initial cost matrix (square or rectangular)
	:rtype: numpy.ndarray
	:return: the final (augmented) cost matrix (square)
	:rtype: numpy.ndarray
	:return: the matching between indexes of initial with indexes of the final cost matrix
	:rtype: dict

	"""
	C_ind = {}
	if n_workers >= n_jobs:
		C = np.random.randint(low, high, size=(n_workers, n_jobs))
		for i in range(n_workers):
			C_ind[i] = i
		return C, C, C_ind
	elif n_workers < n_jobs:	#	more jobs than workers
		C = np.random.randint(low, high, size=(n_workers, n_jobs))
		for i in range(n_workers):
			C_ind[i] = i
		multiples = int(n_jobs / n_workers) 
		n_stacks = multiples - 1
		C_init = C.copy()
		for i in range(n_stacks):
			C = np.vstack((C, C_init))
			for ii in range(n_workers):
				C_ind[(i + 1) * n_workers + ii] = ii
		remaining_rows = n_jobs - (multiples * n_workers)
		for i in range(remaining_rows):
			rand_worker_id = np.random.randint(0, n_workers)
			row_to_stack = C_init[rand_worker_id, :]
			C = np.vstack((C, row_to_stack))
			C_ind[C.shape[0] - 1] = rand_worker_id
		return C_init, C, C_ind


def main():
	# Initial seed with specific number for results reproducibility
	np.random.seed(42)
	
	if (len(sys.argv) == 1):
		print('4 command line arguments are required:')
		print('n_workers: the number of workers')
		print('n_jobs: the number of jobs')
		print('low: the lower bound of the interval from which the random integer values are drawn')
		print('high: the upper bound of the interval from which the random integer values are drawn')
	else:
		# Read command line arguments
		n_workers = int(sys.argv[1])
		n_jobs = int(sys.argv[2])
		low = int(sys.argv[3])
		high = int(sys.argv[4])

		screen_height, screen_width = os.popen('stty size', 'r').read().split()
		screen_width = int(screen_width)
		
		# Create cost matrix
		C_init, C, C_ind = create_cost_matrix(n_workers, n_jobs, low, high)

		# Print initial and augmented (if applied) cost matrix
		print('Initial cost matrix: \n', C_init)
		print('<' + (screen_width - 2) * '-' + '>')
		print('Final cost matrix: \n', C)
		print('<' + (screen_width - 2) * '-' + '>')

		# Hungarian algorithm
		start_time = time.time()
		workers, jobs = linear_sum_assignment(C)	
		elapsed_time = time.time() - start_time

		# Create final assignment
		final_assignment = {}
		for i in range(n_workers):
			final_assignment[i] = []

		for k in range(len(workers)):
			worker_id = C_ind[workers[k]]
			if jobs[k] not in final_assignment[worker_id]:
				final_assignment[worker_id].append(jobs[k])

		# Calculate minimum assignment cost
		minimum_assignment_cost = 0
		for i in range(n_workers):
			assigned_jobs = final_assignment[i]
			for j in assigned_jobs:
				minimum_assignment_cost += np.sum(C_init[:, j])

		# Print final assignment
		print('Final assignment:')
		for i in range(n_workers):
			print('{}:'.format(i), end=' ')
			assigned_jobs = final_assignment[i]
			k  = 0
			for j in assigned_jobs:
				print(j, end='')
				if (len(assigned_jobs) > 1) and (k != (len(assigned_jobs) - 1)):
					print(',', end='')
				k += 1
			print('')

		print('<' + (screen_width - 2) * '-' + '>')
		print('Minimum assignment cost: ', minimum_assignment_cost)
		print('Elapsed time (sec.): ', round(elapsed_time, 3))


if __name__ == '__main__':
	main()