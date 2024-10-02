import os

class SparseMatrix:
    def __init__(self, file_path=None, num_rows=None, num_cols=None):
        """
        Initialize the SparseMatrix object. Either load from a file or create an empty matrix.

        :param file_path: Path to the file to load the matrix from.
        :param num_rows: Number of rows for the matrix if creating a new one.
        :param num_cols: Number of columns for the matrix if creating a new one.
        """
        if file_path:
            self.load_from_file(file_path)
        else:
            self.num_rows = num_rows
            self.num_cols = num_cols
            self.elements = {}

    def load_from_file(self, file_path):
        """
        Load matrix data from a file.

        :param file_path: Path to the file to load the matrix from.
        """
        self.elements = {}
        with open(file_path, 'r') as f:
            lines = f.readlines()
            self.num_rows = int(lines[0].split('=')[1].strip())
            self.num_cols = int(lines[1].split('=')[1].strip())
            for line in lines[2:]:
                line = line.strip()
                if line:
                    row, col, value = map(int, line.strip('()').split(','))
                    self.set_element(row, col, value)

    def get_element(self, row, col):
        """
        Get the value of an element in the matrix.

        :param row: Row index of the element.
        :param col: Column index of the element.
        :return: The value of the element at the given row and column, or 0 if it is not set.
        """
        return self.elements.get((row, col), 0)

    def set_element(self, row, col, value):
        """
        Set the value of an element in the matrix.

        :param row: Row index of the element.
        :param col: Column index of the element.
        :param value: The value to set for the element.
        """
        if value != 0:
            self.elements[(row, col)] = value
        elif (row, col) in self.elements:
            del self.elements[(row, col)]

    def add(self, other):
        """
        Add another matrix to this matrix.

        :param other: The other matrix to add.
        :return: A new SparseMatrix object that is the result of the addition.
        :raises ValueError: If the matrices have different dimensions.
        """
        print(f"Adding matrices with dimensions: {self.num_rows}x{self.num_cols} and {other.num_rows}x{other.num_cols}")
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices dimensions do not match for addition")
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value + other.get_element(row, col))
        for (row, col), value in other.elements.items():
            if (row, col) not in result.elements:
                result.set_element(row, col, value)
        return result

    def subtract(self, other):
        """
        Subtract another matrix from this matrix.

        :param other: The other matrix to subtract.
        :return: A new SparseMatrix object that is the result of the subtraction.
        :raises ValueError: If the matrices have different dimensions.
        """
        print(f"Subtracting matrices with dimensions: {self.num_rows}x{self.num_cols} and {other.num_rows}x{other.num_cols}")
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices dimensions do not match for subtraction")
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value - other.get_element(row, col))
        for (row, col), value in other.elements.items():
            if (row, col) not in result.elements:
                result.set_element(row, col, -value)
        return result

    def multiply(self, other):
        """
        Multiply this matrix with another matrix.

        :param other: The other matrix to multiply with.
        :return: A new SparseMatrix object that is the result of the multiplication.
        :raises ValueError: If the number of columns in this matrix does not match the number of rows in the other matrix.
        """
        print(f"Multiplying matrices with dimensions: {self.num_rows}x{self.num_cols} and {other.num_rows}x{other.num_cols}")
        if self.num_cols != other.num_rows:
            raise ValueError("Matrices dimensions do not match for multiplication")
        result = SparseMatrix(num_rows=self.num_rows, num_cols=other.num_cols)
        for (row1, col1), value1 in self.elements.items():
            for col2 in range(other.num_cols):
                value2 = other.get_element(col1, col2)
                if value2 != 0:
                    result.set_element(row1, col2, result.get_element(row1, col2) + value1 * value2)
        return result

    def save_to_file(self, file_path):
        """
        Save the matrix data to a file.

        :param file_path: Path to the file to save the matrix to.
        """
        with open(file_path, 'w') as f:
            f.write(f"rows={self.num_rows}\n")
            f.write(f"cols={self.num_cols}\n")
            for (row, col), value in self.elements.items():
                f.write(f"({row}, {col}, {value})\n")

def list_files(directory):
    """
    List all files in a directory.

    :param directory: The directory to list files from.
    :return: A sorted list of filenames.
    """
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return sorted(files)  # Return sorted list of files

def generate_unique_filename(directory, filename):
    """
    Generate a unique filename by appending a counter to the base name if a file with the given name already exists.

    :param directory: The directory to check for existing files.
    :param filename: The desired filename.
    :return: A unique filename that does not exist in the directory.
    """
    base, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    while os.path.exists(os.path.join(directory, unique_filename)):
        unique_filename = f"{base}_{counter}{ext}"
        counter += 1
    return unique_filename

def main():
    """
    Main function to perform matrix operations based on user input.
    """
    input_dir = '/dsa/Sparse-Matrix/sample_inputs'
    output_dir = '/dsa/Sparse-Matrix/output'
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    files = list_files(input_dir)

    print("Available files:")
    for idx, file in enumerate(files):
        print(f"{idx + 1}. {file}")

    file1_idx = int(input("Select the first file to make first matrix (by number): ")) - 1
    file2_idx = int(input("Select the second file to make second matrix (by number): ")) - 1

    file1 = os.path.join(input_dir, files[file1_idx])
    file2 = os.path.join(input_dir, files[file2_idx])

    matrix1 = SparseMatrix(file1)
    matrix2 = SparseMatrix(file2)

    print("Select operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    choice = input("Enter choice: ")

    if choice == '1':
        try:
            result = matrix1.add(matrix2)
        except ValueError as e:
            print(e)
            return
    elif choice == '2':
        try:
            result = matrix1.subtract(matrix2)
        except ValueError as e:
            print(e)
            return
    elif choice == '3':
        try:
            result = matrix1.multiply(matrix2)
        except ValueError as e:
            print(e)
            return
    else:
        print("Invalid choice")
        return

    base_file_name = os.path.splitext(os.path.basename(file1))[0]
    output_filename = generate_unique_filename(output_dir, f"{base_file_name}_result.txt")
    output_file_path = os.path.join(output_dir, output_filename)
    result.save_to_file(output_file_path)
    print(f"Result written to {output_file_path}")

if __name__ == '__main__':
    main()

