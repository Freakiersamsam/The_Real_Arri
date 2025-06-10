#!/usr/bin/env python3

import sys
import requests
from arri.crew import HierarchicalCrew

def check_ollama_connection():
    """Check if Ollama is running and accessible"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama is running with {len(models)} models available")
            
            # Check if required model exists
            llama_models = [m for m in models if 'llama3.1' in m.get('name', '')]
            if llama_models:
                print(f"✅ Found Llama model: {llama_models[0]['name']}")
                return True
            else:
                print("❌ Llama3.1:8b model not found")
                print("💡 Run: ollama pull llama3.1:8b")
                return False
        else:
            print(f"❌ Ollama responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama at http://localhost:11434")
        print("💡 Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error checking Ollama: {str(e)}")
        return False

def main():
    """
    Run the hierarchical crew with fallback options.
    """
    print("=== Hierarchical Project Management Crew ===")
    print("This system can research any topic using a coordinated team approach.\n")
    
    # Check Ollama connection first
    print("🔍 Checking Ollama connection...")
    if not check_ollama_connection():
        print("\n❌ Please fix Ollama setup before continuing.")
        sys.exit(1)
    
    # Get user input
    print("\nEnter a research topic (examples: 'weight loss', 'Python programming', 'solar energy', '2023 Honda Civic'):")
    topic = input("Research topic: ").strip()
    
    if not topic:
        print("❌ Please enter a valid topic!")
        return
    
    print(f"\n📝 You entered: '{topic}'")
    
    # Ask for execution mode
    print("\nChoose execution mode:")
    print("1. Hierarchical (recommended for complex projects)")
    print("2. Sequential (fallback option)")
    
    mode = input("Enter choice (1 or 2): ").strip()
    
    confirm = input(f"Continue with topic '{topic}'? (y/n): ").strip().lower()
    
    if confirm not in ['y', 'yes']:
        print("Operation cancelled.")
        return
    
    try:
        # Initialize the crew
        print("\n🔧 Initializing crew...")
        project_crew = HierarchicalCrew()
        
        # Run based on chosen mode
        if mode == "2":
            print(f"\n🔄 Starting sequential research project on: '{topic}'")
            result = project_crew.run_sequential_fallback(topic)
        else:
            print(f"\n🚀 Starting hierarchical research project on: '{topic}'")
            print("⚠️  Note: This may take several minutes for first-time execution...")
            try:
                result = project_crew.run_project(topic)
            except Exception as e:
                print(f"\n⚠️  Hierarchical execution failed: {str(e)}")
                print("🔄 Attempting sequential fallback...")
                result = project_crew.run_sequential_fallback(topic)
        
        # Display results
        print("\n" + "="*60)
        print("🎯 PROJECT COMPLETED SUCCESSFULLY")
        print("="*60)
        print(result)
        
        # Show output files
        print("\n📁 Output files created:")
        print("- project_plan.md")
        print("- research_report.md") 
        print("- analysis_report.md")
        print("- final_report.md")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Verify Ollama is running: ollama serve")
        print("2. Check model availability: ollama list")
        print("3. Pull required model: ollama pull llama3.1:8b")
        print("4. Restart Ollama: pkill ollama && ollama serve")
        print("5. Check system resources (RAM/CPU)")
        print("6. Try sequential mode instead of hierarchical")
        sys.exit(1)

def run():
    """Entry point for CrewAI"""
    main()

if __name__ == "__main__":
    main()