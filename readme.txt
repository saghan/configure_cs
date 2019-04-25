1. Run gerrit_downloader.py 
This downloads the data from gerrit. Make sure to edit the file in line #2 to add your gerrit credentials.

2. Run comment_extractor.py
This extracts the comment from downloaded gerrit data. It creates th following files:
	a. comments.txt with comment data
	b. file_list.txt with names of files where the comments were made.
	c. num_comments.txt with the number of comments downloaded

3. Run cs_runner.py
This runs CheckStyle on the files where the comments were made.

4. Run run_gumtree.py
This runs Gumtree on the files where the comments were made and the next patch.

5. Run classifier.py
This is the classifier. It generates the file warning_result.txt

6. Run config_generator.py. This displays the configuration file in the Python console.

