import struct

input_file = r'c:\Users\kydsh\OneDrive\Рабочий стол\3d_engine\Knight.ply'
output_file = r'c:\Users\kydsh\OneDrive\Рабочий стол\3d_engine\Knight_ascii.ply'

with open(input_file, 'rb') as f:
    # Read header
    header = []
    line = f.readline().decode('ascii').strip()
    while line != 'end_header':
        header.append(line)
        line = f.readline().decode('ascii').strip()
    header.append('end_header')
    
    # Change format to ascii
    for i, line in enumerate(header):
        if line.startswith('format'):
            header[i] = 'format ascii 1.0'
    
    # Read vertices
    vertices = []
    for _ in range(236873):
        data = f.read(24)  # 6 floats * 4 bytes
        x, y, z, nx, ny, nz = struct.unpack('<6f', data)
        vertices.append(f'{x} {y} {z} {nx} {ny} {nz}')
    
    # Read faces
    faces = []
    for _ in range(441294):
        # Read colors: red, green, blue, alpha (4 uchars)
        red = struct.unpack('<B', f.read(1))[0]
        green = struct.unpack('<B', f.read(1))[0]
        blue = struct.unpack('<B', f.read(1))[0]
        alpha = struct.unpack('<B', f.read(1))[0]
        # Read count
        count = struct.unpack('<B', f.read(1))[0]
        # Read indices
        indices = struct.unpack('<' + 'I' * count, f.read(4 * count))
        faces.append(f'{red} {green} {blue} {alpha} {count} ' + ' '.join(map(str, indices)))

# Write ASCII file
with open(output_file, 'w') as f:
    for line in header:
        f.write(line + '\n')
    for v in vertices:
        f.write(v + '\n')
    for face in faces:
        f.write(face + '\n')

print("Conversion complete.")