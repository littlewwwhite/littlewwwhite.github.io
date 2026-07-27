"""Small, reproducible turbovec recall/compression experiment.

This is intentionally not a project-wide benchmark. It isolates one question:
how much recall is traded for 2, 3, and 4-bit vector representations?

Run:
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    RAYON_NUM_THREADS=1 python benchmark_turbovec.py
"""

from __future__ import annotations

import json
import os
import platform
import tempfile
import time
from pathlib import Path

import numpy as np
import turbovec
from turbovec import TurboQuantIndex


SEED = 20260727
N_VECTORS = 50_000
DIM = 384
N_QUERIES = 200
K = 10
BIT_WIDTHS = (2, 3, 4)
REPEATS = 7


def normalize(rows: np.ndarray) -> np.ndarray:
    return rows / np.linalg.norm(rows, axis=1, keepdims=True)


def exact_topk(queries: np.ndarray, vectors: np.ndarray, k: int) -> np.ndarray:
    scores = queries @ vectors.T
    candidates = np.argpartition(scores, -k, axis=1)[:, -k:]
    candidate_scores = np.take_along_axis(scores, candidates, axis=1)
    order = np.argsort(candidate_scores, axis=1)[:, ::-1]
    return np.take_along_axis(candidates, order, axis=1)


def median_runtime(fn, repeats: int = REPEATS) -> float:
    durations = []
    for _ in range(repeats):
        started = time.perf_counter()
        fn()
        durations.append(time.perf_counter() - started)
    return float(np.median(durations))


def recall_at_k(actual: np.ndarray, expected: np.ndarray) -> float:
    overlap = [
        len(set(actual_row.tolist()) & set(expected_row.tolist()))
        for actual_row, expected_row in zip(actual, expected, strict=True)
    ]
    return float(np.mean(overlap) / expected.shape[1])


def main() -> None:
    rng = np.random.default_rng(SEED)
    vectors = normalize(
        rng.standard_normal((N_VECTORS, DIM), dtype=np.float32)
    ).astype(np.float32, copy=False)
    queries = normalize(
        rng.standard_normal((N_QUERIES, DIM), dtype=np.float32)
    ).astype(np.float32, copy=False)

    ground_truth = exact_topk(queries, vectors, K)
    exact_seconds = median_runtime(lambda: exact_topk(queries, vectors, K))

    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        for bits in BIT_WIDTHS:
            started = time.perf_counter()
            index = TurboQuantIndex(dim=DIM, bit_width=bits)
            index.add(vectors)
            build_seconds = time.perf_counter() - started

            # Warm up dispatch and memory pages before timing.
            index.search(queries, k=K)
            search_seconds = median_runtime(lambda: index.search(queries, k=K))
            _, ids = index.search(queries, k=K)

            index_path = Path(tmp) / f"turbovec-{bits}bit.tv"
            index.write(str(index_path))
            index_bytes = index_path.stat().st_size

            rows.append(
                {
                    "bit_width": bits,
                    "index_mib": round(index_bytes / 1024**2, 3),
                    "compression_vs_float32": round(vectors.nbytes / index_bytes, 2),
                    "recall_at_10": round(recall_at_k(ids, ground_truth), 4),
                    "top1_hit_rate": round(float(np.mean(ids[:, 0] == ground_truth[:, 0])), 4),
                    "build_seconds": round(build_seconds, 4),
                    "search_200_queries_ms": round(search_seconds * 1000, 4),
                }
            )

    result = {
        "environment": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "numpy": np.__version__,
            "turbovec": getattr(turbovec, "__version__", "0.8.0"),
            "threads": {
                name: os.environ.get(name, "unset")
                for name in (
                    "OPENBLAS_NUM_THREADS",
                    "OMP_NUM_THREADS",
                    "MKL_NUM_THREADS",
                    "RAYON_NUM_THREADS",
                )
            },
        },
        "dataset": {
            "seed": SEED,
            "vectors": N_VECTORS,
            "queries": N_QUERIES,
            "dimensions": DIM,
            "top_k": K,
            "distribution": "independent random unit vectors",
            "float32_mib": round(vectors.nbytes / 1024**2, 3),
        },
        "exact_search_200_queries_ms": round(exact_seconds * 1000, 4),
        "results": rows,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
