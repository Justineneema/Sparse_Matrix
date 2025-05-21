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

### **Credits**
```markdown
## Credits

- Python `os` module – for file path handling and existence checks
