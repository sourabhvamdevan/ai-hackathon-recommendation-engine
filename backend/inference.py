
import json
import argparse
import time
from src.rag_engine import BISRagEngine

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to input JSON")
    parser.add_argument("--output", required=True, help="Path to output JSON")
    args = parser.parse_args()

    # Initialize your engine
    engine = BISRagEngine()
    
    with open(args.input, 'r') as f:
        data = json.load(f)

    results = []

    for entry in data:
        query_id = entry.get('id')
        query_text = entry.get('query')

        start_time = time.time()
        
        # Get response from your RAG
        # Note: Ensure get_recommendations returns a list of standard IDs for the eval script
        raw_response = engine.get_recommendations(query_text)
        
        # LOGIC: You need to extract just the IDs (e.g., ["IS 456", "IS 1786"]) 
        # from the LLM string for the automated Hit Rate @3 check.
        # This is a placeholder; adjust based on your LLM output format.
        retrieved_ids = engine.extract_ids_from_text(raw_response["result"]) 

        end_time = time.time()
        latency = end_time - start_time

        results.append({
            "id": query_id,
            "retrieved_standards": retrieved_ids, # List of strings
            "latency_seconds": latency
        })

    with open(args.output, 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    main()