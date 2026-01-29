file_path = 'examples.txt'



with open(file_path, 'r') as file:
    file.seek(0)
    lines = file.readlines()

print(lines)

for line in lines:
    print(line.strip())