import os

with open('oracle_files.txt','r') as oracle_files:
	for line in oracle_files:
		line=line.replace('\n','')
		run_cs_cmd="java -jar checkstyle-7.1.2-all.jar -c config.xml -o cs_op/"+line+'.txt '+ 'repo/store_here/'+line
		print(run_cs_cmd)
		os.system(run_cs_cmd)

