import os


class InterpreterError(Exception):
  pass

# main class
class Interpreter:
  def __init__(self):

      self.sym_tab = {}

  


  def read_file(self, file_path):
        # Made a precaution in case a file has permission issues
        if not os.path.exists(file_path):
            
            raise InterpreterError(f"File not found: {file_path}")


        if not os.access(file_path, os.R_OK):
            raise InterpreterError(f"No read permission for file: {file_path}")
        if not os.access(file_path, os.W_OK):
            raise InterpreterError(f"No write permission for file: {file_path}")

        # opening file with a handler 
        with open(file_path, 'r') as file:
            return file.read()
        
  # tokenizing
  def tokenize(self, input_string):
        tokens = []
        i = 0
        while i < len(input_string):
            
            if input_string[i].isspace():
                i += 1
            
            elif input_string[i] in "+-*/=;()":
                tokens.append(input_string[i])
                i += 1
            # tokenizing numbers
            elif input_string[i].isdigit():
                num = input_string[i]
                i += 1
                while i < len(input_string) and input_string[i].isdigit():
                    num += input_string[i]
                    i += 1

                # checking for leading 0s
                if num.startswith('0') and len(num) > 1:
                    raise InterpreterError("Invalid literal: " + num)

                tokens.append(int(num))
            # tokenizing identifiers
            elif input_string[i].isalpha() or input_string[i] == '_':
                id_str = input_string[i]
                i += 1
                while i < len(input_string) and (input_string[i].isalnum() or input_string[i] == '_'):
                    id_str += input_string[i]
                    i += 1
                tokens.append(id_str)
            else:

                raise InterpreterError(f"Unrecognized character: {input_string[i]}")
        return tokens
  

  def parse(self, tokens):
      def parse_factor(tokens):
            if not tokens:
                raise InterpreterError("Unexpected end of input in factor")


            if tokens[0] == '(':
                result, rest = parse_expression(tokens[1:])
                if rest[0] != ')':
                    raise InterpreterError("Expected ')' at the end of expression")
                return result, rest[1:]
            
            
            if tokens[0] in ['+', '-']:
                op = tokens[0]
                value, rest = parse_factor(tokens[1:])
                while rest and rest[0] in ['+', '-']:
                    next_op = rest[0]
                    next_value, next_rest = parse_factor(rest[1:])
                    value = value + next_value if next_op == '+' else value - next_value
                    rest = next_rest
                return value, rest


            if isinstance(tokens[0], str) and tokens[0] in self.sym_tab:
                return self.sym_tab[tokens[0]], tokens[1:]


            if isinstance(tokens[0], int):
                return tokens[0], tokens[1:]

            raise InterpreterError(f"Invalid factor: {tokens[0]}")
      
      # Nested function to parse terms (it handles multiplication).
      def parse_term(tokens):
          result, rest = parse_factor(tokens)
          while rest and rest[0] == '*':
              next_result, next_rest = parse_factor(rest[1:])
              result *= next_result
              rest = next_rest
          return result, rest
      
        #parsing expression
      def parse_expression(tokens):
          result, rest = parse_term(tokens)
          while rest and rest[0] in "+-":
              op = rest[0]
              next_result, next_rest = parse_term(rest[1:])
              result = result + next_result if op == '+' else result - next_result
              rest = next_rest
          return result, rest
      

      i = 0
      while i < len(tokens):
            identifier = tokens[i]
            if tokens[i + 1] != '=':
                raise InterpreterError("Expected '=' after identifier")
            value, rest = parse_expression(tokens[i + 2:])
            if rest and rest[0] != ';':
                raise InterpreterError("Expected ';' at the end of assignment")
            

            if isinstance(identifier, int) or identifier in self.sym_tab:
                self.sym_tab[identifier] = value
            else:

                self.sym_tab[identifier] = value


            i = i + 3 + len(tokens[i + 2:]) - len(rest) 
  
  # main function to interpret string
  def interpret(self, input_string):
      tokens = self.tokenize(input_string)
      self.parse(tokens)

      output = ""
      for key, val in self.sym_tab.items():
          output += f"{key} = {val}\n"
      return output.strip()


interpreter = Interpreter()

# CHANGE FILE HERE 
file_path = 'input1.txt'

try:
    file_content = interpreter.read_file(file_path)
    result = interpreter.interpret(file_content)
    print(result)
except InterpreterError as e:
    print("error:", e)
