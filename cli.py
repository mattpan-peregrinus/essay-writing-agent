"""Command-line interface for the essay writer."""

import os
from graph import create_essay_graph


def run_essay_writer(task: str, max_revisions: int = 2):
    """Run the essay writer with a given task."""
    graph = create_essay_graph()
    thread = {"configurable": {"thread_id": "1"}}
    
    print(f"Starting essay writing for: {task}")
    print("=" * 50)
    
    final_state = None
    for step, state in enumerate(graph.stream({
        'task': task,
        "max_revisions": max_revisions,
        "revision_number": 0,
    }, thread)):
        print(f"\nStep {step + 1}: {list(state.keys())[0]}")
        # Update final_state with all values
        if final_state is None:
            final_state = state.copy()
        else:
            final_state.update(state)
        
        # Print relevant information for each step
        for key, value in state.items():
            if key == 'plan' and value:
                print(f"Plan created: {str(value)[:100]}...")
            elif key == 'draft' and value:
                print(f"Draft generated ({len(str(value))} characters)")
            elif key == 'critique' and value:
                print(f"Critique: {str(value)[:100]}...")
            elif key == 'content' and value:
                print(f"Research content added: {len(value)} sources")
    
    return final_state


def main():
    """Simple CLI interface for the essay writer."""
    import os
    
    print("Essay Writer Agent")
    print("=" * 20)
    
    # Check for required API keys
    if not os.environ.get("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY environment variable is required")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-openai-api-key'")
        return
    
    if not os.environ.get("TAVILY_API_KEY"):
        print("ERROR: TAVILY_API_KEY environment variable is required")
        print("Please set your Tavily API key:")
        print("export TAVILY_API_KEY='your-tavily-api-key'")
        return
    
    print("API keys found - ready to write essays!")
    print()
    
    task = input("Enter your essay topic: ")
    max_revisions_input = input("Maximum revisions (default 2): ")
    max_revisions = int(max_revisions_input) if max_revisions_input else 2
    
    try:
        final_state = run_essay_writer(task, max_revisions)
        
        if final_state and 'draft' in final_state:
            print("\n" + "=" * 50)
            print("FINAL ESSAY:")
            print("=" * 50)
            print(final_state['draft'])
        else:
            print("\nError: No final draft was generated")
            
    except Exception as e:
        print(f"\nError running essay writer: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()