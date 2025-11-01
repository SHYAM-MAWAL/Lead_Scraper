"""
Test to figure out the correct browser-use-sdk usage
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Try different import approaches
print("Testing browser-use-sdk imports...")

try:
    from browser_use_sdk import BrowserUse
    print("✅ BrowserUse imported successfully")
    
    api_key = os.getenv('BROWSER_USE_API_KEY')
    print(f"API Key found: {api_key[:10]}..." if api_key else "No API key")
    
    # Check the BrowserUse class
    print("\nBrowserUse attributes:")
    print([x for x in dir(BrowserUse) if not x.startswith('_')])
    
    # Try to instantiate
    print("\nTrying to create BrowserUse instance...")
    client = BrowserUse(api_key=api_key)
    print("✅ BrowserUse instance created")
    
    print("\nClient attributes:")
    print([x for x in dir(client) if not x.startswith('_')])
    
    # Check tasks
    print("\nTasks attributes:")
    print([x for x in dir(client.tasks) if not x.startswith('_')])
    
    # Try to create a simple task
    print("\n\nCreating a test task...")
    task = client.tasks.create_task(
        task="Go to google.com and tell me the page title"
    )
    print(f"✅ Task created: {task}")
    print(f"Task ID: {task.id}")
    
    # Wait for completion
    print("\nWaiting for task to complete...")
    result = task.complete()
    print(f"✅ Task completed!")
    print(f"Result type: {type(result)}")
    print(f"Result attributes: {[x for x in dir(result) if not x.startswith('_')]}")
    print(f"\nOutput: {result.output if hasattr(result, 'output') else result}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
