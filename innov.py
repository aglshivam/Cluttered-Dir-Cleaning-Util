"""
First part - identify the top 10 sized files in the file system. No input is required.
Second part - would clean the cluttered desktop 
"""

import os
from collections import defaultdict
from os.path import join, getsize

#get the current user path
current_user = os.path.expanduser('~')
result = []

"""
Walk through the directory recursively and scan the files
"""
for root, dirs, files in os.walk(current_user):
    for name in files:
    	#file should not be link
    	if(os.path.islink(join(root,name)) == False):
			if(len(result) < 10):
				result.append(((getsize(join(root,name))),join(root,name)))
			else :
				temp_size = getsize(join(root,name))
				result.sort()
				if(result[0][0] < temp_size):
					result.pop(0)
					result.insert(0,((getsize(join(root,name))),join(root,name)))

#print in descending oreder of file size
result.sort(reverse = True)
print "*****Top files*****"
print "-------------------------------------------------"
for a,b in result:
	print "size : %0.2f MB " % (a/(1024*1024.0))
	print "path : " ,b
	print "-------------------------------------------------"


print "Desktop Cleaning........"

d = defaultdict(list)
for root, dirs, files in os.walk(current_user +'/Desktop'):
	for name in files:
		tempfilename, file_extension = os.path.splitext(name)
		#get the filename and extension of the file
		while '.' in tempfilename:
			 tempfilename, tempfile_extension = os.path.splitext(tempfilename)
			 file_extension = tempfile_extension + file_extension
		if(file_extension != ".desktop"):
			#shortcuts should not be moved
			d[file_extension].append(tempfilename)
	break

#move the files from source to destionation
doc_path = current_user +'/Documents/'
current = current_user +'/Desktop/'
for a,b in d.items():
	#create a folder of extension name
	newpath = doc_path + a[1:].upper() +"/"
	#no need to create the folder if it is already present
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	for i in b:
		desk = current + i + a
		dest = newpath + i + a
		os.rename(desk, dest)

print "Desktop is cleaned"
