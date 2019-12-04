from cloudmesh.common.Shell import Shell

result = Shell.execute('pwd') # Printing working directory
print("result: ", result)

result1 = Shell.execute('ls',["-l"]) # Executing ls -l
print("result1: ", result1)

result2 = Shell.ls("-a","-u","-x") # build in functions of Shell
print("result2: ", result2)

