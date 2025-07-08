import os

class SparseMatrix:
    # A sparse matrix implementing the use of coordinates.
    
    def __init__(self, matrix_file_path=None, num_rows=0, num_cols=0):
        # Initializing matrix from file
        self.rows = num_rows
        self.cols = num_cols
        self.elements = []  # List of tuples (row, col, value)
        
        if matrix_file_path:
            self._load_matrix(matrix_file_path)

    def _load_matrix(self, file_path):
        """Read the data on the load matrix file.
        Supposes 0 based indexing of row and 0/1 based indexing of column in the input file,
        in which a column number corresponding to the value of self.cols is treated as self.cols - 1 (0-based)."""
        try:
            with open(file_path, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
                
            if len(lines) < 2:
                raise ValueError("File must contain at least rows and columns")
                
            # Parse dimensions
            try:
                self.rows = int(lines[0].split('=')[1].strip())
                self.cols = int(lines[1].split('=')[1].strip())
            except (IndexError, ValueError):
                raise ValueError("Invalid rows/cols format. Expected 'rows=N' and 'cols=M'")
            
            if self.rows <= 0 or self.cols <= 0:
                raise ValueError("Matrix dimensions must be positive integers")
            
            # Parse elements
            for line in lines[2:]:
                line = line.replace(" ", "")
                if not (line.startswith("(") and line.endswith(")")):
                    raise ValueError(f"Invalid entry format: {line}")
                
                content = line[1:-1].split(',')
                if len(content) != 3:
                    raise ValueError(f"Entry must have exactly 3 values: {line}")
                
                try:
                    row = int(content[0])
                    col = int(content[1])
                    value = int(content[2])
                except ValueError:
                    raise ValueError(f"All values must be integers: {line}")
                
               # Adjust column index to check if it is equals the number of columns to ensure 0-based indexing.
                adjusted_col = col - 1 if col == self.cols else col

                # Now validate the adjusted_col against standard 0-based bounds
                if not (0 <= row < self.rows and 0 <= adjusted_col < self.cols):
                    raise ValueError(f"Index out of bounds after adjustment: ({row}, {col} (adjusted to {adjusted_col})) "
                                     f"for matrix {self.rows}x{self.cols}. "
                                     "Please ensure row indices are 0-based (0 to rows-1) "
                                     "and column indices are consistent with the matrix dimensions, "
                                     "with 'cols' value referring to the last column provided.")
                
                self.elements.append((row, adjusted_col, value))
            
            # Sort elements by row then column for proper operations
            self.elements.sort(key=lambda x: (x[0], x[1]))
            
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise ValueError(f"Error loading matrix: {str(e)}")

    def get_element(self, row, col):
        # Getting element at (row, col). Returns 0 if not found.
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise ValueError("Indices out of range")
        
        # Binary search for proper lookup
        left, right = 0, len(self.elements)
        while left < right:
            mid = (left + right) // 2
            r, c, _ = self.elements[mid]
            if r == row and c == col:
                return self.elements[mid][2]
            elif r < row or (r == row and c < col):
                left = mid + 1
            else:
                right = mid
        return 0

    def set_element(self, row, col, value):
        """Set element at (row, col). If value=0, remove the element in file or directory."""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise ValueError("Indices out of range")
        
        # Find position to insert/update
        left, right = 0, len(self.elements)
        while left < right:
            mid = (left + right) // 2
            r, c, _ = self.elements[mid]
            if r == row and c == col:
                if value == 0:
                    del self.elements[mid]
                else:
                    self.elements[mid] = (row, col, value)
                return
            elif r < row or (r == row and c < col):
                left = mid + 1
            else:
                right = mid
        
        if value != 0:
            self.elements.insert(left, (row, col, value))

    def add(self, other):
        # Adding two matrices .
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition")
        
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        i = j = 0
        
        while i < len(self.elements) and j < len(other.elements):
            sr, sc, sv = self.elements[i]
            or_, oc, ov = other.elements[j]
            
            if (sr, sc) < (or_, oc):
                result.elements.append((sr, sc, sv))
                i += 1
            elif (sr, sc) > (or_, oc):
                result.elements.append((or_, oc, ov))
                j += 1
            else:
                sum_val = sv + ov
                if sum_val != 0:
                    result.elements.append((sr, sc, sum_val))
                i += 1
                j += 1
        
        # Add remaining elements
        while i < len(self.elements):
            result.elements.append(self.elements[i])
            i += 1
        while j < len(other.elements):
            result.elements.append(other.elements[j])
            j += 1
            
        return result

    def subtract(self, other):
        # Subtracting two matrices.
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for subtraction")
        
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        i = j = 0
        
        while i < len(self.elements) and j < len(other.elements):
            sr, sc, sv = self.elements[i]
            or_, oc, ov = other.elements[j]
            
            if (sr, sc) < (or_, oc):
                result.elements.append((sr, sc, sv))
                i += 1
            elif (sr, sc) > (or_, oc):
                result.elements.append((or_, oc, -ov))
                j += 1
            else:
                diff_val = sv - ov
                if diff_val != 0:
                    result.elements.append((sr, sc, diff_val))
                i += 1
                j += 1
        
        # Addition of remaining elements
        while i < len(self.elements):
            result.elements.append(self.elements[i])
            i += 1
        while j < len(other.elements):
            result.elements.append((other.elements[j][0], other.elements[j][1], -other.elements[j][2]))
            j += 1
            
        return result

    def multiply(self, other):
        # Multiplication of two matrices.
        if self.cols != other.rows:
            raise ValueError("Columns of first matrix must match rows of second matrix")
        
        result = SparseMatrix(num_rows=self.rows, num_cols=other.cols)
        
        # Create a dictionary for quick access to other matrix's elements by row
        other_dict = {}
        for r, c, v in other.elements:
            if r not in other_dict:
                other_dict[r] = []
            other_dict[r].append((c, v))
        
        # Multiplying non-zero elements
        temp = {}  # Temporary storage for result elements
        
        for sr, sc, sv in self.elements:
            if sc in other_dict:
                for oc, ov in other_dict[sc]:
                    key = (sr, oc)
                    temp[key] = temp.get(key, 0) + sv * ov
        
        # Convert temp dictionary to sorted elements list
        result.elements = [(r, c, v) for (r, c), v in temp.items() if v != 0]
        result.elements.sort(key=lambda x: (x[0], x[1]))
        
        return result

    def save_to_file(self, file_path):
        # Saving the matrices to file in specified format.
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(f"rows={self.rows}\n")
                f.write(f"cols={self.cols}\n")
                for row, col, value in self.elements:
                    f.write(f"({row}, {col}, {value})\n")
        except Exception as e:
            raise ValueError(f"Error saving to file: {str(e)}")

def get_user_input(prompt, validator=None):
    # Function to help in getting valid user inputs.
    while True:
        try:
            user_input = input(prompt).strip()
            # checking for empty inputs
            if not user_input and validator and validator.__name__ == 'validate_file_path':
                print("Input path cannot be empty.")
                continue
            if not user_input and validator and validator.__name__ == 'validate_output_filename':
                print("Output filename cannot be empty.")
                continue
            
            if validator:
                user_input = validator(user_input)
            return user_input
        except Exception as e:
            print(f"Invalid input: {str(e)}")

def validate_file_path(path):
    # Validating if file path exists.
    path = os.path.abspath(path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    return path

def validate_output_filename(name):
    # Validate output filename and check for .txt extension.
    if not name:
        raise ValueError("Output filename cannot be empty")
    if not name.endswith('.txt'):
        name += '.txt'
    return name

def main():
    # Main program interface.
    print("Sparse Matrix Operations")
    
    # check for output existance
    output_dir = os.path.join(os.getcwd(), "sample_outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    while True:
        print("\nMenu:")
        print("1. Add matrices")
        print("2. Subtract matrices")
        print("3. Multiply matrices")
        
        choice = get_user_input("Enter your choice (1-3): ", 
                                lambda x: x if x in ('1', '2', '3', ) else None)
    
        
        # Check for invalid choice if the validator in get_user_input returned None
        if choice is None:
            print("Invalid choice. Please enter 1, 2, or 3")
            continue

        try:
            # Get input files from user
            file1 = get_user_input("Enter path to first matrix file: ", validate_file_path)
            file2 = get_user_input("Enter path to second matrix file: ", validate_file_path)
            
            # Get output filename
            output_name = get_user_input("Enter output filename without extension: ", validate_output_filename)
            output_path = os.path.join(output_dir, output_name)
            
            # Loading matrices
            matrix1 = SparseMatrix(file1)
            matrix2 = SparseMatrix(file2)
            
            # Perform operation
            if choice == '1':
                result = matrix1.add(matrix2)
                op_name = "addition"
            elif choice == '2':
                result = matrix1.subtract(matrix2)
                op_name = "subtraction"
            else: # choice == '3'
                result = matrix1.multiply(matrix2)
                op_name = "multiplication"
            
            # Save the output result
            result.save_to_file(output_path)
            print(f"\nMatrix {op_name} completed successfully!")
            print(f"Result saved to: {os.path.abspath(output_path)}")
            
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again with valid inputs.")

if __name__ == "__main__":
    main()
