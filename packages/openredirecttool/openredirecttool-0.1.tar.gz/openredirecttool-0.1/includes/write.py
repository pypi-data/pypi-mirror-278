def write_to_file(output_file, data):
    """
    Append the given data to the specified output file.
    
    Parameters:
    output_file (str): The path to the output file.
    data (str): The data to be written to the file.
    """
    try:
        with open(output_file, 'a') as file:
            file.write(data)
        print(f"Data successfully appended to '{output_file}'.")
    except IOError as e:
        print(f"An I/O error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    output_file = 'output.txt'
    data = 'This is a sample line of data.\n'
    write_to_file(output_file, data)
    