import os
import subprocess


def run_gumtree(current_file,next_file):
	full_current_file="repo/store_here/"+current_file
	full_next_file="repo/store_here/"+next_file
	os.system("java -jar gumtree-spoon-ast-diff-10-SNAPSHOT-jar-with-dependencies.jar "+full_current_file+" "+ full_next_file+" >"+'gumtree_op/'+current_file.replace('.txt.java','.txt'))
	# subprocess.call(['java', '-jar', 'Blender.jar',full_current_file,full_next_file])


	



with open('file_list.txt') as ip:
	for line in ip:
#bundles/org.eclipse.e4.ui.progress/src/org/eclipse/e4/ui/progress/internal/FinishedJobs.java+refs-changes-12-90512-2
		splitted=line.split('/')
		file_n_ref=splitted[len(splitted)-1].replace('\n','')
		splitted_dash=file_n_ref.split('-')
		current_patch=splitted_dash[len(splitted_dash)-1].replace('\n','')
		next_patch=int(current_patch)+1
		splitted_file_n_ref= file_n_ref.split('-')

		file_n_ref_next='-'.join(splitted_file_n_ref[:-1])+'-'+str(next_patch)
		# print(file_n_ref)
		# print(file_n_ref_next)
		# print(file_n_ref+'.txt')
		# print(file_n_ref_next)

		run_gumtree(file_n_ref+'.java',file_n_ref_next+'.java')
