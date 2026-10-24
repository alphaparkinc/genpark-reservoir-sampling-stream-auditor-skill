"""Example usage for GenPark Reservoir Sampling Stream Auditor.
100% Python Standard Library.
"""

from client import ReservoirSamplingStreamAuditor

def main():
    auditor = ReservoirSamplingStreamAuditor(capacity=50)
    
    # Simulate high-volume token generation latency measurements
    import random
    for i in range(1000):
        latency_ms = random.gauss(120.0, 25.0)
        auditor.feed(latency_ms, item_id=f"req_{i}")
        
    summary = auditor.get_summary()
    print("Stream Summary:")
    print("- Total Seen:", summary["total_seen"])
    print("- Sample Size:", summary["sample_size"])
    print("- Mean Latency:", summary["mean"], "ms")
    print("- StdDev:", summary["stddev"], "ms")
    print("- Quantiles (P50, P90, P95, P99):", summary["quantiles"])

if __name__ == "__main__":
    main()
