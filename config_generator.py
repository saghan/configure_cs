all_non_treewalker_checks=['UniqueProperties','JavadocPackage','Translation','FileTabCharacter','FileLength','NewlineAtEndOfFile','RegexpSingleline']
non_treewalker_checks=[]
treewalker_checks=[]
with open('warning_result.txt') as ip:
	for line in ip:
		line=line.replace('\n','')
		if line=='not_related_to_checkstyle' or line=='':
			continue
		if line in all_non_treewalker_checks:
			non_treewalker_checks.append(line)
		else:
			treewalker_checks.append(line)

opstring="<?xml version=\"1.0\"?>\n"

opstring+="""<!DOCTYPE module PUBLIC
          \"-//Puppy Crawl//DTD Check Configuration 1.3//EN\"
          \"http://www.puppycrawl.com/dtds/configuration_1_3.dtd\">\n"""
opstring+="<module name=\"Checker\">\n"
for x in non_treewalker_checks:
	opstring+= "<module name="+"\""+x+"\"/>"
	opstring+= "\n"

opstring+="<module name=\"TreeWalker\">\n"

for x in treewalker_checks:
	opstring+= "<module name="+"\""+x+"\"/>"
	opstring+= "\n"

opstring+="</module>"
opstring+="</module>"

print(opstring)