import uvicorn
import os
import sys

# Add the backend directory to sys.path so 'app' is recognized
sys.path.append(os.path.join(os.getcwd(), 'backend'))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    print(f"[*] Launching Advanced AI IDS on port {args.port}...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=args.port, reload=True)
