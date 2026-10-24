"""MCP Server for GenPark Reservoir Sampling Stream Auditor.
100% Python Standard Library.
"""

import json
import sys
from client import ReservoirSamplingStreamAuditor

auditor = ReservoirSamplingStreamAuditor(capacity=100)

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "feed_stream",
                        "description": "Feed a batch of numeric values into the streaming reservoir",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "values": {"type": "array", "items": {"type": "number"}}
                            },
                            "required": ["values"]
                        }
                    },
                    {
                        "name": "get_stream_summary",
                        "description": "Retrieve unbiased summary statistics and quantiles (P50, P90, P95, P99)",
                        "inputSchema": {"type": "object"}
                    },
                    {
                        "name": "get_reservoir_sample",
                        "description": "Retrieve current uniform reservoir sample items",
                        "inputSchema": {"type": "object"}
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "feed_stream":
            vals = args.get("values", [])
            for v in vals:
                auditor.feed(float(v))
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": f"Ingested {len(vals)} metrics into reservoir."}]}
            }
        elif name == "get_stream_summary":
            summ = auditor.get_summary()
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(summ, indent=2)}]}
            }
        elif name == "get_reservoir_sample":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(auditor.reservoir, indent=2)}]}
            }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
