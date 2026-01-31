from agent import plan, execute
import json

print("🤖 Task Automation Agent")

goal = input("Enter your goal: ")

proposal = plan(goal)
print("\nAgent Plan:\n", proposal)

approve = input("\nApprove execution? (yes/no): ")

if approve.lower() == "yes":
    print("\nWaiting for tool call...")

    tool_name = input("Tool name: ")
    args = json.loads(input("Args as JSON: "))

    result = execute(tool_name, args)
    print("\nResult:", result)
else:
    print("❌ Execution cancelled.")
