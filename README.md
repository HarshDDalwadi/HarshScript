# HarshScript - A Custom Programming Language

**HarshScript** is a simple and lightweight programming language developed to demonstrate the basics of language design. It supports essential arithmetic, logical, and relational operations, along with variable creation and manipulation. This project features a fully implemented lexer, parser, and interpreter in Python.

## Features

- **Arithmetic Operations**:
  - Addition (`+`), Subtraction (`-`), Multiplication (`*`), Division (`/`).
  
- **Logical Operations**:
  - Logical `AND`, `OR`, and `NOT`.

- **Relational Operators**:
  - Comparisons like `>=`, `<=`, `>`, `<`.

- **Variables**:
  - Declare and use variables in operations.

## Project Structure

The language implementation consists of:
1. **Lexer**: Breaks down the input text into tokens for processing.
2. **Parser**: Analyzes the token sequence and builds an abstract syntax tree (AST).
3. **Interpreter**: Executes the AST and evaluates the expressions.

## Example Usage

### Arithmetic Operations
x = 10;
y = 20;
z = x + y;
print(z);  // Outputs: 30

### Logical Operations 
a = true;
b = false;
result = a AND b;
print(result);  // Outputs: false

### Relational Operations
x = 15;
y = 10;
result = x > y;
print(result);  // Outputs: true

