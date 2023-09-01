input_file_path = "eastmoneypageurl.txt"
output_file_path = "eastmoneypageurl.txt"
# Read lines from the input file and store them in a list
with open(input_file_path, 'r') as input_file:
    lines = input_file.readlines()

# Sort the lines in the list
lines.sort()

# Write the sorted lines back to the output file
with open(output_file_path, 'w') as output_file:
    output_file.writelines(lines)

print("File sorted and saved to", output_file_path)
