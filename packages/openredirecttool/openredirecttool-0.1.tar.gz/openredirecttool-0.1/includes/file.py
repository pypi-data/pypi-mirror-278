import shutil

def reader(input_file, output_path):
    try:
        shutil.copyfile(input_file, output_path)
        print(f"File '{input_file}' read successfully and output written to '{output_path}'.")
    except FileNotFoundError:
        print(f"File '{input_file}' not found.")
    except IOError as e:
        print(f"An I/O error occurred: {e}")

# Example usage:
# reader('input.txt', 'output.txt')
