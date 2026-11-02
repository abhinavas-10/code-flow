from collections import deque
from typing import Literal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="CodeFlow API", version="1.0.0",
              description="Stateless algorithm endpoints for the CodeFlow DSA Visualizer.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class ArrayRequest(BaseModel):
    values: list[int] = Field(min_length=1, max_length=100)
    algorithm: Literal["bubble", "selection", "insertion", "merge", "quick"] = "bubble"

class SearchRequest(BaseModel):
    values: list[int] = Field(min_length=1, max_length=100)
    target: int

class DuplicatesRequest(BaseModel):
    values: list[int] = Field(max_length=500)

@app.get("/")
def root():
    return {"name": "CodeFlow API", "docs": "/docs", "health": "/api/health"}

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "codeflow-api"}

@app.post("/api/sort")
def sort_array(request: ArrayRequest):
    values = request.values[:]
    steps = [{"array": values[:], "message": "Initial array", "line": 1}]
    if request.algorithm == "bubble":
        n = len(values)
        for i in range(n):
            swapped = False
            for j in range(0, n-i-1):
                steps.append({"array": values[:], "message": f"Compare {values[j]} and {values[j+1]}", "line": 3})
                if values[j] > values[j+1]:
                    values[j], values[j+1] = values[j+1], values[j]
                    swapped = True
                    steps.append({"array": values[:], "message": f"Swap positions {j} and {j+1}", "line": 4})
            if not swapped:
                break
    elif request.algorithm == "selection":
        for i in range(len(values)):
            m = i
            for j in range(i+1, len(values)):
                steps.append({"array": values[:], "message": f"Compare {values[j]} with current minimum {values[m]}", "line": 3})
                if values[j] < values[m]:
                    m = j
            if m != i:
                values[i], values[m] = values[m], values[i]
                steps.append({"array": values[:], "message": f"Place minimum at index {i}", "line": 4})
    elif request.algorithm == "insertion":
        for i in range(1, len(values)):
            key, j = values[i], i-1
            while j >= 0 and values[j] > key:
                values[j+1] = values[j]
                steps.append({"array": values[:], "message": f"Shift {values[j]} one position right", "line": 4})
                j -= 1
            values[j+1] = key
            steps.append({"array": values[:], "message": f"Insert {key} at index {j+1}", "line": 5})
    elif request.algorithm == "merge":
        def merge_sort(lo, hi):
            if hi - lo <= 1:
                return
            mid = (lo + hi) // 2
            merge_sort(lo, mid)
            merge_sort(mid, hi)
            merged = sorted(values[lo:hi])
            values[lo:hi] = merged
            steps.append({"array": values[:], "message": f"Merge range [{lo}, {hi})", "line": 5})
        merge_sort(0, len(values))
    else:
        def quick_sort(lo, hi):
            if lo >= hi:
                return
            pivot = values[hi]
            i = lo
            for j in range(lo, hi):
                steps.append({"array": values[:], "message": f"Compare {values[j]} with pivot {pivot}", "line": 4})
                if values[j] <= pivot:
                    values[i], values[j] = values[j], values[i]
                    i += 1
            values[i], values[hi] = values[hi], values[i]
            steps.append({"array": values[:], "message": f"Place pivot at index {i}", "line": 6})
            quick_sort(lo, i-1)
            quick_sort(i+1, hi)
        quick_sort(0, len(values)-1)
    steps.append({"array": values[:], "message": "Sorting complete", "line": 7})
    return {"algorithm": request.algorithm, "result": values, "steps": steps,
            "time_complexity": {"bubble":"O(n²)", "selection":"O(n²)", "insertion":"O(n²)", "merge":"O(n log n)", "quick":"O(n log n) average"}[request.algorithm]}

@app.post("/api/binary-search")
def binary_search(request: SearchRequest):
    values = sorted(request.values)
    lo, hi = 0, len(values)-1
    steps = []
    found = None
    while lo <= hi:
        mid = (lo+hi)//2
        steps.append({"left":lo, "mid":mid, "right":hi, "value":values[mid],
                      "message":f"Compare target {request.target} with {values[mid]}"})
        if values[mid] == request.target:
            found = mid
            break
        if values[mid] < request.target:
            lo = mid+1
        else:
            hi = mid-1
    return {"sorted_values":values, "target":request.target, "index":found,
            "found":found is not None, "steps":steps, "time_complexity":"O(log n)"}

@app.post("/api/remove-duplicates")
def remove_duplicates(request: DuplicatesRequest):
    values = request.values
    result = []
    for value in values:
        if not result or result[-1] != value:
            result.append(value)
    return {"input":values, "result":result, "assumption":"Input is sorted",
            "time_complexity":"O(n)", "space_complexity":"O(n) for the returned list"}
