import json
num_comments=0
op=open("comments.txt",'w')
new_oracle=open("new_oracle.txt",'w')
file_handle=open("file_list.txt",'w')
with open('comments_gerrit.txt') as ip_file:
	for line in ip_file:
		
		try:
			parsed_json = json.loads(line)
			# currentPatchSet=parsed_json['currentPatchSet']
			# # comments_arr=json.loads(currentPatchSet)
			# currentPatchSet=str(currentPatchSet).replace('u\'','\'').replace('\'','\"').replace("False","\"False\"")
			# currentPatchSet=json.loads(currentPatchSet)
			# comments=currentPatchSet['comments']
			# ref=currentPatchSet['parents']

			# print(str(currentPatchSet).replace('u\'','\'').replace('\'','\"'))
			# op.Write(str(currentPatchSet))
			# for x in comments:
			# 	op_str=str(x['line'])+'\t'+x['message']+'\t'+x['file']
			# 	# print(op_str)
			# 	# print(ref)
			# 	# op.Write(op_str)

			patchSets=parsed_json['patchSets']
			# print(patchSets)
			for patches in patchSets:
				# patch=str(patches).replace('u\'','\'').replace('\'','\"').replace("False","\"False\"").replace(": u\"",": \"")
				# print(patch)
				parents=patches['parents']
				# print(parents)
				# print(parents)
				# ref=parents['ref']
				comments=patches['comments']
				# print(comments)
				ref=patches['ref']
				ref=ref.replace('/','-')
				# print(ref)
				# print(str(comments))	
				
				for comment in comments:
					if comment['message']=='\n':
						continue
					xx=comment['message'].replace('\r\n',' ')+'\t'+'NA'+'\t'+comment['file']+'+'+ref+'\t'+str(comment['line'])
					# if('\n' in xx):
					file_handle.write(comment['file']+'+'+ref+'\n')
					xx=xx.replace('\n',' ').replace('\r\n',' ')
					print(xx)
					op.write('Test_Project\t'+xx+'\n')
					new_oracle.write('Test_Project\t'+xx+'\n')
					num_comments+=1
				# 	# print()
				# 	pass
		except :
			continue
globalfile=open("num_comments.txt",'w')
globalfile.write(str(num_comments))
globalfile.close()

with open('oracle.txt','r')as old_oracle:
	for line in old_oracle:
		new_oracle.write(line)
new_oracle.close()
file_handle.close()


op.close()
		
