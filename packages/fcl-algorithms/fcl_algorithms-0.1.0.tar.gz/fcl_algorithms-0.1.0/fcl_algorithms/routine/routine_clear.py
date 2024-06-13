# This scripts clears the pdf files from completed requests.

import os

# 1) Remove all address request:
directory = "./pdf_contents_a"
files_in_directory = os.listdir(directory)
filtered_files = [file for file in files_in_directory if file.endswith(".pdf")]
for file in filtered_files:
	path_to_file = os.path.join(directory, file)
	os.remove(path_to_file)

# 1) Remove all community request:
directory = "./pdf_contents_c"
files_in_directory = os.listdir(directory)
filtered_files = [file for file in files_in_directory if file.endswith(".pdf")]
for file in filtered_files:
	path_to_file = os.path.join(directory, file)
	os.remove(path_to_file)

# 1) Remove all global request:
directory = "./pdf_contents_g"
files_in_directory = os.listdir(directory)
filtered_files = [file for file in files_in_directory if file.endswith(".pdf")]
for file in filtered_files:
	path_to_file = os.path.join(directory, file)
	os.remove(path_to_file)