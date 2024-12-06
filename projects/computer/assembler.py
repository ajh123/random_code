import argparse

def binary_to_hex(binary_str):
    # Convert binary string to integer
    decimal_value = int(binary_str, 2)
    # Convert integer to hexadecimal string
    hex_value = hex(decimal_value)
    # Remove the '0x' prefix
    return hex_value[2:]


def binary_to_hex_list(binary_list):
    hex_list = [format(int(b, 2), '04x') for b in binary_list]
    return hex_list


def format_hex_list(hex_list):
    formatted_lines = ["v3.0 hex words addressed"]
    for i in range(0, len(hex_list), 8):
        address = format(i // 8 * 16, '02x')
        line = f"{address}: " + " ".join(hex_list[i:i+8])
        formatted_lines.append(line)
    return "\n".join(formatted_lines)


class OperandType:
    """
    Base class for operand types.
    Subclasses must implement the `parse` method to define custom parsing and validation logic.
    """
    @staticmethod
    def parse(value):
        """
        Parses and validates the operand.

        :param value: The operand as a string.
        :return: Parsed operand in the correct format.
        """
        raise NotImplementedError("Subclasses must implement this method.")


class RegisterOperand(OperandType):
    """
    Operand type for register identifiers (e.g., R0, R1, R2).
    """
    @staticmethod
    def parse(value):
        if not value.upper().startswith("R") or not value[1:].isdigit():
            raise ValueError(f"Invalid register identifier: {value}")
        register_number = int(value[1:])
        if register_number < 0 or register_number > 7:
            raise ValueError(f"Register out of range: {value}")
        return register_number


class Instruction:
    """
    Represents a single instruction in the instruction set.
    """
    def __init__(self, name, opcode, operand_format=None):
        self.name = name
        self.opcode = opcode
        self.operand_format = operand_format or []

    def encode(self, operands):
        """
        Encodes the instruction into its binary representation.

        :param operands: List of operand values.
        :return: 16-bit binary string.
        """
        # Validate operand count
        if len(operands) != len(self.operand_format):
            raise ValueError(f"Instruction {self.name} expects {len(self.operand_format)} operands, got {len(operands)}.")

        # Encode the opcode
        binary_instruction = f"{self.opcode:04b}"

        # Encode the operands
        for operand, bit_range in zip(operands, self.operand_format):
            start, end = bit_range
            operand_bits = f"{operand:0{end - start + 1}b}"
            binary_instruction += operand_bits

        # Pad the rest of the instruction to 16 bits
        return binary_instruction.ljust(16, '0')


class Assembler:
    """
    Assembler that converts assembly instructions into binary code.
    """
    def __init__(self):
        self.instructions = {}

    def add_instruction(self, name, opcode, operand_format=None, operand_types=None):
        """
        Adds a new instruction to the assembler's instruction set.

        :param name: Name of the instruction.
        :param opcode: 4-bit opcode of the instruction.
        :param operand_format: List of (start, end) bit ranges for operands.
        :param operand_types: List of operand types (subclasses of OperandType).
        """
        operand_types = operand_types or []
        if len(operand_format or []) != len(operand_types):
            raise ValueError("Operand format and operand types must have the same length.")
        self.instructions[name.upper()] = (Instruction(name, opcode, operand_format), operand_types)

    def assemble(self, input_file, output_file, otput_format):
        """
        Assembles a program from an input file and writes the binary code to an output file.

        :param input_file: Path to the file containing assembly instructions.
        :param output_file: Path to the file to save machine code.
        """
        machine_code = []
        with open(input_file, 'r') as infile:
            for line in infile:
                line = line.strip()
                if not line or line.startswith("#"):  # Skip empty lines and comments
                    continue

                parts = line.split()
                instruction_name = parts[0].upper()
                raw_operands = parts[1:] if len(parts) > 1 else []

                if instruction_name not in self.instructions:
                    raise ValueError(f"Unknown instruction: {instruction_name}")

                instruction, operand_types = self.instructions[instruction_name]

                # Validate operand count
                if len(raw_operands) > len(operand_types):
                    raise ValueError(
                        f"Instruction {instruction_name} expects at most {len(operand_types)} operands, "
                        f"but {len(raw_operands)} were provided."
                    )

                # Parse operands using the defined types
                operands = []
                for raw_operand, operand_type in zip(raw_operands, operand_types):
                    operands.append(operand_type.parse(raw_operand))

                # Encode instruction
                binary_code = instruction.encode(operands)
                machine_code.append(binary_code)

        with open(output_file, 'w') as outfile:
            if otput_format == "raw":
                for i in range(0, len(machine_code)):
                    binary_line = machine_code[i]
                    if i < len(machine_code) - 1:
                        outfile.write(binary_line + "\n")
                    else:
                        outfile.write(binary_line)
            elif otput_format == "logisim_v3_hex":
                hex_list = binary_to_hex_list(machine_code)
                formatted_string = format_hex_list(hex_list)
                outfile.write(formatted_string)


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="My assembler.")
    parser.add_argument("input_file", help="Path to the input assembly file.")
    parser.add_argument("output_file", help="Path to the output binary file.")
    parser.add_argument("-f", "--format", choices=["logisim_v3_hex", "raw"], default="raw")
    args = parser.parse_args()

    # Create the assembler and define the instruction set
    assembler = Assembler()
    assembler.add_instruction("NOP", 0b0000)
    assembler.add_instruction("ADD", 0b0101, [(0, 2), (3, 5)], [RegisterOperand, RegisterOperand])
    assembler.add_instruction("SUB", 0b0110, [(0, 2), (3, 5)], [RegisterOperand, RegisterOperand])
    assembler.add_instruction("AND", 0b0111, [(0, 2), (3, 5)], [RegisterOperand, RegisterOperand])
    assembler.add_instruction("OR", 0b1000, [(0, 2), (3, 5)], [RegisterOperand, RegisterOperand])
    assembler.add_instruction("XOR", 0b1001, [(0, 2), (3, 5)], [RegisterOperand, RegisterOperand])
    assembler.add_instruction("NOT", 0b1010, [(0, 2)], [RegisterOperand])
    assembler.add_instruction("HLT", 0b1111)  # Halt

    # Assemble the program
    assembler.assemble(args.input_file, args.output_file, args.format)
    print(f"Assembly complete. Machine code saved to {args.output_file}.")


if __name__ == "__main__":
    main()
