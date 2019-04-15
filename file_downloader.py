repo_loc="git fetch https://git.eclipse.org/r/mylyn/org.eclipse.mylyn.reviews refs/changes/04/91104/4 && git checkout FETCH_HEAD"
repo_loc="https://git.eclipse.org/r/mylyn/org.eclipse.mylyn.reviews"
#I see. I guess it's fine to add them.	12	org.eclipse.mylyn.gerrit.releng/modules/gerrit/manifests/init.pp	refs/changes/25/83625/1


#Test_Project	Renamed method to openCompareEditor and added a null check.	NA	org.eclipse.mylyn.gerrit.ui/src/org/eclipse/mylyn/internal/gerrit/ui/GerritUrlHandler.java+refs-changes-40-47940-1	124

import os
import urllib
import glob #for regex


download_list=[]

os.chdir("/home/saghan/Documents/thesis/final_software/repo/store_here/")
with open("/home/saghan/Documents/thesis/final_software/comments.txt") as ip:
	for line in ip:

		if (not ".java" in line):
			continue
		
		try:
			splitted=line.split('\t')
			full_file_name_split=splitted[3].split('/')
			splitted_plus=splitted[3].split('+')
			only_file_name=full_file_name_split[len(full_file_name_split)-1].split('+')[0]
			ref=splitted_plus[1]
			# update_cmd="git fetch "+repo_loc+" && git checkout FETCH_HEAD"
			# os.system(update_cmd)
			# mv_cmd="mv "+splitted[2]+ " "+splitted[2]+ref.replace('/','-')
			# os.system(mv_cmd)
			# print(mv_cmd)
			# os.system("git reset --merge")

			ref_splitted=ref.split('-')
			patch_num=ref_splitted[len(ref_splitted)-1]
			ref_num=ref_splitted[len(ref_splitted)-2]
			print(patch_num+'^')
			# continue
			download_link="https://git.eclipse.org/r/cat/"+ref_num+"%2C"+str(int(patch_num.replace('\n','')))+"%2C"+splitted[3].split('+')[0]+"%5E0"
			download_link2="https://git.eclipse.org/r/cat/"+ref_num+"%2C"+str(int(patch_num.replace('\n',''))+1)+"%2C"+splitted[3].split('+')[0]+"%5E0"
		


			print(download_link)
			print(download_link2)
			
			op_loc=only_file_name+'+'+ref.replace('/','-')+'.zip'

			op_loc_2=only_file_name+'+'+'-'.join(ref_splitted[:len(ref_splitted)-1])+'-'+str(int(patch_num)+1)+'.zip'
			print(op_loc)
			print(op_loc_2)

			# if (not os.path.exists(os.path.dirname(op_loc))):
			# 	os.makedirs(os.path.dirname(op_loc))
	    	# if [download_link2,op_loc_2] not in download_list:
			download_list.append((download_link2,op_loc_2))
	    	# if [download_link,op_loc] not in download_list:
			# download_list.append((download_link,op_loc))



			# urllib.urlretrieve(download_link2,filename=op_loc_2)
			# urllib.urlretrieve(download_link,filename=op_loc)
	        # unzip_cmd="find . -name \"*.java*\" | while read filename; do unzip -o -d \"`dirname \"$filename\" \"filename $filename\" ; done;"
	        # dirname='/'.join(op_loc_2.split('/')[:-1])
			# print(xx)
	        # unzip_cmd2="unzip -o -d "+ dirname+  " "+op_loc_2 #+ " "+only_file_name
	        # unzip_cmd="unzip -o -d "+ dirname+  " "+op_loc
			# print(unzip_cmd)
			# os.system(unzip_cmd)
			# os.system(unzip_cmd2)
	        # name_n_ref2=('/'.join(op_loc_2.split('/')[-1:]).replace('.zip',''))
	        # name_n_ref=('/'.join(op_loc.split('/')[-1:]).replace('.zip',''))
				# mv_cmd="rename "+only_file_name+"* " + ('/'.join(op_loc_2.split('/')[-1:]).replace('.zip',''))
			# mv_cmd="rename "+ "\'s/"+only_file_name+"* "+"/"+name_n_ref+"/igm\'"
			# print('rename cmd',mv_cmd)
			# os.chdir(dirname)
			# print(os.getcwd())
			# only_file_name=only_file_name.replace('.java','')
		except:
			pass
download_list=list(set(download_list))
oracle_file_handler=open('../../oracle_files.txt','w')
for x in download_list:
	print(x[1])
	# oracle_file_handler.write(x[1].replace('.zip','.java')+'\n')
	urllib.urlretrieve(x[0],filename=x[1])	
oracle_file_handler.close()
# unzip_rename_cmd="find . -name '*.zip'| while read f;do unzip \"$f\" -o -d tmp && mv tmp/* \"${f%.zip}\"; done"

# os.system(unzip_rename_cmd)
		# for filename in glob.glob(only_file_name+'*'):
		# 	# print('search',only_file_name)
		# 	# print('found',filename)
		# 	if not '.zip' in filename:
		# 		os.rename(filename,name_n_ref+'.java')
		# os.rename(mv_cmd)
		
		
#https://git.eclipse.org/r/#/c/91104/3..4/org.eclipse.mylyn.reviews.ui/src/org/eclipse/mylyn/reviews/ui/spi/editor/ReviewDetailSection.java
# update_cmd="git fetch "+repo_loc+

#urllib.urlretrieve("https://dev.vaadin.com/review/cat/14599%2C3%2Cserver/src/main/java/com/vaadin/data/fieldgroup/FieldGroup.java^0", filename="op.zip")
#https://git.eclipse.org/r/#/c/99671/1..2/org.eclipse.mylyn.reviews.ui/src/org/eclipse/mylyn/reviews/ui/spi/editor/ReviewDetailSection.java
#https://git.eclipse.org/r/#/c/8592/2..3/org.eclipse.mylyn.gerrit.ui/src/org/eclipse/mylyn/internal/gerrit/ui/operations/RebaseDialog.java