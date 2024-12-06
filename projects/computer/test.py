def binary_to_hex(binary_list):
    hex_list = [format(int(b, 2), '04x') for b in binary_list]
    return hex_list

def format_hex_list(hex_list):
    formatted_lines = ["v3.0 hex words addressed"]
    for i in range(0, len(hex_list), 8):
        address = format(i // 8 * 16, '02x')
        line = f"{address}: " + " ".join(hex_list[i:i+8])
        formatted_lines.append(line)
    return "\n".join(formatted_lines)

def write_to_file(formatted_string, filename):
    with open(filename, 'w') as file:
        file.write(formatted_string)

# Example usage
binary_list = [
    '0000000000000000', '0101001010000000', '0110000011000000', '0111010001000000',
    '1000011011000000', '1001001000000000', '1111000000000000', '0000000000000000',
    # Add more binary strings as needed
]

hex_list = binary_to_hex(binary_list)
formatted_string = format_hex_list(hex_list)
write_to_file(formatted_string, 'output.txt')