from tool import Tool

tool = Tool(command="apt")
apt = tool.resource("apt")
result = apt.install("vim")

print(result)
