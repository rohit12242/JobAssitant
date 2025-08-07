# agents/orchestrator.py

def run_job_agent(config):
    print("👋 Hello from the Orchestrator Agent!")
    print(f"Searching for '{config['job_search_keyword']}' jobs in '{config['location']}'...")
    print(f"Using resume: {config['resume_path']}")
    print("✅ System initialized successfully.")
