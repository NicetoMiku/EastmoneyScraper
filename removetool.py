substring_to_remove = 'caifuhao'
input_file_path = 'eastmoneypageurl copy.txt'
output_file_path = 'eastmoneypageurl.txt'

# Read lines from the input file and filter out lines containing the substring
with open(input_file_path, 'r') as input_file:
    lines = input_file.readlines()
    filtered_lines = [line for line in lines if substring_to_remove not in line]

# Write the filtered lines back to the output file
with open(output_file_path, 'w') as output_file:
    output_file.writelines(filtered_lines)

print("Lines containing '{}' removed from the file.".format(substring_to_remove))
