#! /usr/bin/env python
import numpy as np
from cvxopt import matrix, sparse
from cvxopt.solvers import qp, options
from scipy.integrate import odeint
from math import *
import time

options['show_progress'] = False
options['reltol'] = 1e-2 # was e-2
options['feastol'] = 1e-2 # was e-4
options['maxiters'] = 50 # default is 100

def si_position_controller(xi, positions, x_velocity_gain=1, y_velocity_gain=1, velocity_magnitude_limit=1):
    _,N = np.shape(xi)
    dxi = np.zeros((2, N))

        # Calculate control input
    dxi[0][:] = (positions[0][:]-xi[0][:])
    dxi[1][:] = (positions[1][:]-xi[1][:])

        # Threshold magnitude
    # norms = np.linalg.norm(dxi, axis=0)
    # idxs = np.where(norms > velocity_magnitude_limit)
    # if norms[idxs].size != 0:
    #     dxi[:, idxs] *= velocity_magnitude_limit/norms[idxs]

    return dxi

def si_barrier_cert(dxi, x, safety_radius, show_time, barrier_gain=80, magnitude_limit=0.4):
    N = dxi.shape[1]
    num_constraints = int(comb(N, 2))
    A = np.zeros((num_constraints, 2*N))
    b = np.zeros(num_constraints)
    H = sparse(matrix(2*np.identity(2*N)))
    count = 0
    for i in range(N-1):
        for j in range(i+1, N):
            error = x[:, i] - x[:, j]
            h = (error[0]*error[0] + error[1]*error[1]) - np.power(safety_radius, 2)

            A[count, (2*i, (2*i+1))] = -2*error
            A[count, (2*j, (2*j+1))] = 2*error
            b[count] = barrier_gain*np.power(h, 3)

            count += 1

        # Threshold control inputs before QP
    norms = np.linalg.norm(dxi, 2, 0)
    idxs_to_normalize = (norms > magnitude_limit)
    dxi[:, idxs_to_normalize] *= magnitude_limit/norms[idxs_to_normalize]

    f = -2*np.reshape(dxi, 2*N, order='F')
    start_time = time.time()
    result = qp(H, matrix(f), matrix(A), matrix(b))['x']
    if show_time:
        print("--- %s seconds ---" % (time.time() - start_time))

    return np.reshape(result, (2, -1), order='F')

def barrier_certificates(new_coords, new_centroids, safety_radius, show_time=False):
    x_si = np.dstack(new_coords)[0]
    x_goal = np.dstack(new_centroids)[0]
    dxi = si_position_controller(x_si, x_goal)
    dxi = si_barrier_cert(dxi, x_si, safety_radius, show_time)
    x_si = np.add(x_si, dxi)
    x_si = np.dstack((x_si[0], x_si[1]))[0]
    new_coords = x_si
    return new_coords




