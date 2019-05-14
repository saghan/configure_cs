import os
os.system("ssh -p 29418 username@git.eclipse.org  gerrit query --format json   project:mylyn/org.eclipse.mylyn.reviews --patch-sets --current-patch-set --all-approvals --files --comments --commit-message --dependencies  --submit-records >comments_gerrit.txt")
i=0
iteration=1
j=1
with open("comments_gerrit.txt",'r') as ip:
	for line in ip:
		i+=1
		if(i!=500*iteration+j):
			continue
		if ('\"moreChanges\":true}' in line):
			start=str(500*iteration+1)
			cmd= "ssh -p 29418 username@git.eclipse.org  gerrit query --format json   project:mylyn/org.eclipse.mylyn.reviews --patch-sets --current-patch-set  --files --comments --commit-message --start {} >>comments_gerrit.txt".format(start)
			# cmd= "ssh -p 29418 smudbhari@dev.vaadin.com  gerrit query --format json   project:vaadin --patch-sets --current-patch-set  --files --comments --commit-message --after 2016-08-26 --start {} >>comments_gerrit_vaadin.txt".format(start)
			# cmd= "ssh -p 29418 smudbhari@review.motechproject.org  gerrit query --format json   project:motech --patch-sets --current-patch-set  --files --comments --commit-message --start {} >>comments_gerrit_vaadin.txt".format(start)

			print(cmd)
			os.system(cmd)
			iteration+=1
			j+=1

