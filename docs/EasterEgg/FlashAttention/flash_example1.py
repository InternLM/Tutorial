import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule
import numpy as np
import torch

cuda_code = """
__global__
void forward_kernel(const float* Q, const float* K, const float* V, const int N, const int d,
                    const int Tc, const int Tr, const int Bc, const int Br, const float softmax_scale,
                    float* l, float *m, float* O) {
    int tx = threadIdx.x;
    int bx = blockIdx.x; int by = blockIdx.y;  // batch and head index

    // Offset into Q,K,V,O,l,m - different for each batch and head
    int qkv_offset = (bx * gridDim.y * N * d) + (by * N * d);  // gridDim.y = nh
    int lm_offset = (bx * gridDim.y * N) + (by * N);  // offset for l and m

    // Define SRAM for Q,K,V,S
    extern __shared__ float sram[];
    int tile_size = Bc * d;  // size of Qi, Kj, Vj
    float* Qi = sram;
    float* Kj = &sram[tile_size];
    float* Vj = &sram[tile_size * 2];
    float* S = &sram[tile_size * 3];

    for (int j = 0; j < Tc; j++) {

        // Load Kj, Vj to SRAM
        for (int x = 0; x < d; x++) {
            Kj[(tx * d) + x] = K[qkv_offset + (tile_size * j) + (tx * d) + x];
            Vj[(tx * d) + x] = V[qkv_offset + (tile_size * j) + (tx * d) + x];
        }
        __syncthreads();  // such that the inner loop can use the correct Kj, Vj

        for (int i = 0; i < Tr; i++)  {

            // Load Qi to SRAM, l and m to registers
            for (int x = 0; x < d; x++) {
                Qi[(tx * d) + x] = Q[qkv_offset + (tile_size * i) + (tx * d) + x];
            }
            float row_m_prev = m[lm_offset + (Br * i) + tx];
            float row_l_prev = l[lm_offset + (Br * i) + tx];

            // S = QK^T, row_m = rowmax(S)
            float row_m = -INFINITY;
            for (int y = 0; y < Bc; y++) {
                float sum = 0;
                for (int x = 0; x < d; x++) {
                    sum += Qi[(tx * d) + x] * Kj[(y * d) + x];
                }
                sum *= softmax_scale;
                S[(Bc * tx) + y] = sum;

                if (sum > row_m)
                    row_m = sum;
            }

            // P = exp(S - row_m), row_l = rowsum(P)
            float row_l = 0;
            for (int y = 0; y < Bc; y++) {
                S[(Bc * tx) + y] = __expf(S[(Bc * tx) + y] - row_m);
                row_l += S[(Bc * tx) + y];
            }

            // Compute new m and l
            float row_m_new = max(row_m_prev, row_m);
            float row_l_new = (__expf(row_m_prev - row_m_new) * row_l_prev) + (__expf(row_m - row_m_new) * row_l);

            // Write O, l, m to HBM
            for (int x = 0; x < d; x++) {
                float pv = 0;  // Pij * Vj
                for (int y = 0; y < Bc; y++) {
                    pv += S[(Bc * tx) + y] * Vj[(y * d) + x];
                }
                O[qkv_offset + (tile_size * i) + (tx * d) + x] = (1 / row_l_new) \
                    * ((row_l_prev * __expf(row_m_prev - row_m_new) * O[qkv_offset + (tile_size * i) + (tx * d) + x]) \
                    + (__expf(row_m - row_m_new) * pv));
            }
            m[lm_offset + (Br * i) + tx] = row_m_new;
            l[lm_offset + (Br * i) + tx] = row_l_new;
        }
        __syncthreads();  // otherwise, thread can use the wrong Kj, Vj in inner loop
    }
}
"""

mod = SourceModule(cuda_code)
forward_kernel = mod.get_function("forward_kernel")

def forward(Q, K, V):
    # TODO: determine Bc, Br dynamically
    Bc, Br = 32, 32

    B, nh, N, d = Q.shape

    Tc = int(np.ceil(N / Bc))
    Tr = int(np.ceil(N / Br))
    softmax_scale = 1.0 / np.sqrt(d)

    # Initialize O, l, m
    O = torch.zeros_like(Q)
    l = torch.zeros((B, nh, N), device='cuda')
    m = torch.full((B, nh, N), -np.inf, device='cuda')

    # Calculate SRAM size needed per block
    sram_size = (3 * Bc * d * 4) + (Bc * Br * 4)  # in bytes
    max_sram_size = drv.Device(0).get_attribute(drv.device_attribute.MAX_SHARED_MEMORY_PER_BLOCK)
    print(f"Max shared memory: {max_sram_size}, requested shared memory: {sram_size}")

    grid_dim = (B, nh)
    block_dim = (Bc, 1, 1)

    forward_kernel(
        drv.In(Q), drv.In(K), drv.In(V),
        np.int32(N), np.int32(d), np.int32(Tc), np.int32(Tr), np.int32(Bc), np.int32(Br), np.float32(softmax_scale),
        drv.InOut(l), drv.InOut(m), drv.Out(O),
        block=block_dim, grid=grid_dim, shared=sram_size
    )

    return O

# 使用示例
B, nh, N, d = 1, 1, 1024, 64
Q = torch.randn(B, nh, N, d, device='cuda')
K = torch.randn(B, nh, N, d, device='cuda')
V = torch.randn(B, nh, N, d, device='cuda')

result = forward(Q, K, V)
print(result.shape)
