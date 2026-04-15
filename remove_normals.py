input_file = r'c:\Users\kydsh\OneDrive\Рабочий стол\3d_engine\Knight_ascii.ply'
output_file = r'c:\Users\kydsh\OneDrive\Рабочий стол\3d_engine\Knight_no_normals.ply'

with open(input_file, 'r') as f:
    lines = f.readlines()

# Find end_header
header_end = None
for i, line in enumerate(lines):
    if line.strip() == 'end_header':
        header_end = i
        break

# Modify header: remove normal properties
new_header = []
for line in lines[:header_end+1]:
    if 'nx' in line or 'ny' in line or 'nz' in line:
        continue
    new_header.append(line)

# Now, data starts after header_end
data_lines = lines[header_end+1:]

# Process vertices: take only first 3 numbers
vertices = []
faces = []
is_vertex = True
for line in data_lines:
    parts = line.strip().split()
    if len(parts) == 6:  # vertex with normals
        vertices.append(' '.join(parts[:3]) + '\n')
    elif len(parts) >= 5:  # face
        faces.append(line)
        is_vertex = False
    else:
        # empty or something
        pass

# Write new file
with open(output_file, 'w') as f:
    f.writelines(new_header)
    f.writelines(vertices)
    f.writelines(faces)

print("Normals removed. New file: Knight_no_normals.ply")