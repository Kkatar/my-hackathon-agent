import os
import pandas as pd
from utils import load_csv, save_csv, logger
from agent import SupportAgent

def main():
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, "support_tickets", "support_tickets.csv")
    output_path = os.path.join(base_dir, "support_tickets", "output.csv")
    data_dir = os.path.join(base_dir, "data")
    
    # Initialize
    logger.info("Initializing Agent System...")
    agent = SupportAgent(data_dir=data_dir)
    
    # Load Data
    logger.info(f"Loading tickets from {input_path}")
    df = load_csv(input_path)
    if df.empty:
        logger.error("No data found to process.")
        return

    results = []
    total = len(df)
    
    logger.info(f"Processing {total} tickets...")
    
    # Process
    for idx, row in df.iterrows():
        # Terminal progress bar
        progress = int((idx + 1) / total * 20)
        print(f"\rProgress: [{'#' * progress}{'.' * (20 - progress)}] {idx + 1}/{total}", end="")
        
        ticket_id = row.get("ticket_id", str(idx))
        query = row.get("Issue", "")
        
        if pd.isna(query) or not str(query).strip():
            query = row.get("Subject", "") # Fallback column name
            
        result = agent.process_ticket(ticket_id, str(query))
        
        results.append({
            "status": result["status"],
            "product_area": result["product_area"],
            "response": result["response"],
            "justification": result["justification"],
            "request_type": result["request_type"]
        })
        
    print() # Newline after progress bar
    logger.info("Processing complete.")
    
    # Save Output
    out_df = pd.DataFrame(results)
    
    # Ensure columns match strict requirements
    cols = ["status", "product_area", "response", "justification", "request_type"]
    save_csv(out_df[cols], output_path)

if __name__ == "__main__":
    main()
