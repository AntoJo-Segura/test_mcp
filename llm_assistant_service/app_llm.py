import asyncio
import csv
import os
from typing import List, Dict, Any
# Assuming the library provides FastMCP like in the example
# The exact import path might need adjustment if 'mcp.server.fastmcp' is incorrect
# based on the actual 'mcp' package structure.
from mcp.server.fastmcp import FastMCP 
from mcp.server.transports.stdio import serve_stdio

# Initialize FastMCP server
mcp_server = FastMCP(
    name="LLMAssistantService",
    version="1.0.0",
    description="Provides tools to get participant lists for birthday planning."
)

LEADS_CSV_PATH = '/csv_data/leads.csv' # For Docker volume mount

def read_leads() -> List[Dict[str, str]]:
    """Reads data from the leads.csv file."""
    leads = []
    if not os.path.exists(LEADS_CSV_PATH):
        # In a real scenario, better logging or error handling for MCP might be needed
        print(f"Warning: CSV file not found at {LEADS_CSV_PATH}")
        return leads
    
    try:
        with open(LEADS_CSV_PATH, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                leads.append(row)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []
    return leads

@mcp_server.tool()
def get_non_volunteers() -> List[Dict[str, str]]:
    """Gets a list of participants who are NOT volunteer organizers."""
    leads_data = read_leads()
    non_volunteers = [
        {"nombre": lead["Nombre"], "email": lead["Email"]}
        for lead in leads_data
        if lead.get("Voluntario Organizador", "").strip().lower() == "no"
    ]
    return non_volunteers

@mcp_server.tool()
def get_volunteers() -> List[Dict[str, str]]:
    """Gets a list of participants who ARE volunteer organizers."""
    leads_data = read_leads()
    volunteers = [
        {"nombre": lead["Nombre"], "email": lead["Email"]}
        for lead in leads_data
        if lead.get("Voluntario Organizador", "").strip().lower() == "sí"
    ]
    return volunteers

@mcp_server.tool()
def get_participant_count() -> Dict[str, Any]:
    """Gets the total number of unique participants plus one."""
    leads_data = read_leads()
    if not leads_data:
        # Consider how MCP tools signal errors or empty states.
        # Returning a specific structure might be better.
        return {"count": 1, "message": "No participant data found or error reading CSV."}

    unique_emails = set()
    for lead in leads_data:
        if lead.get("Email"):
            unique_emails.add(lead["Email"])
    
    return {"count": len(unique_emails) + 1}

if __name__ == "__main__":
    # Check if the CSV path exists just for a warning during direct execution,
    # though in MCP context, the tool invoker handles data flow.
    if not os.path.exists(LEADS_CSV_PATH):
        print(f"Warning: {LEADS_CSV_PATH} not found. Tools might return empty data.")
        # For local testing without Docker, you might want to create a dummy leads.csv
        # in the expected location if you were to run this script directly.
        # However, it's typically invoked by an MCP client.

    # Start the server with stdio transport
    # This will listen for MCP requests on stdin and send responses to stdout.
    print("LLM Assistant MCP Service starting with stdio transport...")
    asyncio.run(serve_stdio(mcp_server))
