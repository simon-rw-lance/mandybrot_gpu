import numpy as np
import pyopencl as cl
import timeit

a_np = np.random.rand(100000000).astype(np.float32)
b_np = np.random.rand(100000000).astype(np.float32)

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

mf = cl.mem_flags
a_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a_np)
b_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b_np)

prg = cl.Program(ctx, 
"""
__kernel void sum(
	__global const float *a_g,
	__global const float *b_g,
	__global float *res_g)
{
	int gid = get_global_id(0);
	res_g[gid] + b_g[gid];
}
""",
).build()

res_g = cl.Buffer(ctx, mf.WRITE_ONLY, a_np.nbytes)
knl = prg.sum

starttime = timeit.default_timer()
knl(queue, a_np.shape, None, a_g, b_g, res_g)
gpu_time = timeit.default_timer() - starttime

res_np = np.empty_like(a_np)
cl.enqueue_copy(queue, res_np, res_g)

starttime = timeit.default_timer()
a_np + b_np
cpu_time = timeit.default_timer() - starttime

print(f"GPU ran {cpu_time/gpu_time} faster.")