import numpy as np
from scipy.optimize import linear_sum_assignment


def create_cost_matrix(n_workers, n_jobs, low, high):
	C_ind = {}
	if n_workers == n_jobs:
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
	else:	#	more workers than jobs, TODO: implement C_ind dictionary generation
		C = np.random.randint(low, high, size=(n_workers, n_jobs))
		multiples = int(n_workers / n_jobs)
		n_stacks = multiples - 1
		C_init = C.copy()
		for j in range(n_stacks):
			C = np.hstack((C, C_init))
		remaining_cols = n_workers - (multiples * n_jobs)
		for j in range(remaining_cols):
			rand_job_id = np.random.randint(0, n_jobs)
			col_to_stack = C_init[:, rand_job_id].reshape((C_init[:, rand_job_id].shape[0], 1))
			C = np.hstack((C, col_to_stack))
		return C_init, C, C_ind


def main():
	np.random.seed(42)
	low = 1
	high = 100
	n_workers = 4
	n_jobs = 10
	C_init, C, C_ind = create_cost_matrix(n_workers, n_jobs, low, high)

	print('Initial cost matrix: \n', C_init)
	print('<--------------------->\n')
	print('Cost matrix with cloned workers: \n', C)
	print('<--------------------->\n')

	workers, jobs = linear_sum_assignment(C)	#	Hungarian algorithm
	final_assignment = {}
	for i in range(n_workers):
		final_assignment[i] = []

	for k in range(len(workers)):
		worker_id = C_ind[workers[k]]
		if jobs[k] not in final_assignment[worker_id]:
			final_assignment[worker_id].append(jobs[k])

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


if __name__ == '__main__':
	main()