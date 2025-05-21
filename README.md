# DSA-HW01---Sparce-Matrix

This project is about creating programm in any language that perform basic operation on Matrix
like Add,Subtract and multiply matrice.

- it should load matrix from input file
- that input file should should contain list of tuples in format like

```
    rows = <number of rows>
    columns = <number of columns>
    (<row-index>, <col-index>, <value>)
    .
    .
    .
```
***

## Requirement

- you should have python3 installed on your system to run this file

***

## How to Run
1. Navigate to the project directory:
```
cd dsa/sparse_matrix/code/src
```
2. Run the Python script:
```
python sparse_matrix_operations.py
```

3. Follow on-screen prompts:

- Enter the paths of two matrix files.
- Choose an operation (Addition, Subtraction, Multiplication).
- View the result printed to the console.

## Usage

- clone this repository to you local pc
- check the format of input file  that located in  sample_inputs folder
- feel free to add any oyther input files in that folder as long as they follow the format
- save and run the file

## Outputs

- it will prompt you to enter file name for first matrix and file name for the second matrix
- it will load sparce matrix in background from choosen files, it will raise an error either if file doesn't exist in samaple_inputs folder or if it has wrong format

- if everyhting is good it ask you to choose operation
- after computing, it will create an output file in sample_output folder

---

## Error Handling
- Whitespace in files → Ignored automatically.
- Incorrect format (e.g., missing parentheses, wrong data types) → Raises std::invalid_argument("Input file has wrong format").
- Invalid operations (e.g., mismatched dimensions for multiplication) → Displays an error message and exits.


### **Credits**
```markdown
## Credits

- Python `os` module – for file path handling and existence checks
