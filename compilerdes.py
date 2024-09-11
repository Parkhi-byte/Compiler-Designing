import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Compiler:
    def __init__(self, source):
        self.source = source
        self.tokens = self.tokenize()
        self.pos = 0

    def tokenize(self):
        tokens = []
        i = 0
        while i < len(self.source):
            if self.source[i] == ' ':
                i += 1
                continue
            if self.source[i] == '+':
                tokens.append(Token('PLUS', '+'))
                i += 1
            elif self.source[i] == '*':
                tokens.append(Token('TIMES', '*'))
                i += 1
            elif self.source[i] == '/':
                tokens.append(Token('DIVIDE', '/'))
                i += 1
            elif self.source[i] == '-':
                tokens.append(Token('MINUS', '-'))
                i += 1
            elif self.source[i] == '(':
                tokens.append(Token('LPAREN', '('))
                i += 1
            elif self.source[i] == ')':
                tokens.append(Token('RPAREN', ')'))
                i += 1
            elif self.source[i] >= '0' and self.source[i] <= '9':
                j = i
                while j < len(self.source) and self.source[j] >= '0' and self.source[j] <= '9':
                    j += 1
                tokens.append(Token('NUMBER', int(self.source[i:j])))
                i = j
            else:
                raise Exception(f"Invalid character '{self.source[i]}' at position {i}")
        return tokens

    def eat(self, token_type):
        if self.tokens[self.pos].type == token_type:
            self.pos += 1
        else:
            raise Exception(f"Expected {token_type} but got {self.tokens[self.pos].type} instead")

    def factor(self):
        token = self.tokens[self.pos]
        if token.type == 'NUMBER':
            self.pos += 1
            return token.value
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            value = self.expr()
            self.eat('RPAREN')
            return value
        else:
            raise Exception(f"Invalid syntax at position {self.pos}")

    def term(self):
        value = self.factor()
        while self.pos < len(self.tokens) and (self.tokens[self.pos].type == 'TIMES' or self.tokens[self.pos].type == 'DIVIDE'):
            token = self.tokens[self.pos]
            if token.type == 'TIMES':
                self.eat('TIMES')
                value *= self.factor()
            elif token.type == 'DIVIDE':
                self.eat('DIVIDE')
                value /= self.factor()
        return value

    def expr(self):
        value = self.term()
        while self.pos < len(self.tokens) and (self.tokens[self.pos].type == 'PLUS' or self.tokens[self.pos].type == 'MINUS'):
            token = self.tokens[self.pos]
            if token.type == 'PLUS':
                self.eat('PLUS')
                value += self.term()
            elif token.type == 'MINUS':
                self.eat('MINUS')
                value -= self.term()
        return value

    def postfix(self):
        output = []
        operator_stack = []

        for token in self.tokens:
            if token.type == 'NUMBER':
                output.append(token.value)
            elif token.type in ['PLUS', 'MINUS', 'TIMES', 'DIVIDE']:
                while operator_stack and self.precedence(operator_stack[-1]) >= self.precedence(token.value):
                    output.append(operator_stack.pop())
                operator_stack.append(token.value)
            elif token.type == 'LPAREN':
                operator_stack.append(token.value)
            elif token.type == 'RPAREN':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                operator_stack.pop()  # Discard the '('

        while operator_stack:
            output.append(operator_stack.pop())

        return ' '.join(map(str, output))

    def precedence(self, operator):
        if operator in ['+', '-']:
            return 1
        elif operator in ['*', '/']:
            return 2
        return 0

    def compile(self):
        return self.expr()

class CompilerWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Compiler")
        self.geometry("500x600")

        self.source_var = tk.StringVar()
        self.result_text = tk.Text(self, height=10, width=50, state='disabled')
        self.postfix_text = tk.Text(self, height=10, width=50, state='disabled')
        self.previous_result = ''

        self.result_label = tk.Label(self, text="Result")
        self.result_label.pack()

        self.result_text.pack(pady=10)

        self.postfix_label = tk.Label(self, text="Postfix Expression")
        self.postfix_label.pack()

        self.postfix_text.pack(pady=10)

        self.source_entry = ttk.Entry(self, textvariable=self.source_var)
        self.source_entry.pack(pady=20)

        self.compile_button = ttk.Button(self, text="Compile", command=self.compile)
        self.compile_button.pack(pady=10)

        self.clear_button = ttk.Button(self, text="Clear", command=self.clear_output)
        self.clear_button.pack(pady=10)

    def compile(self):
        source = self.source_var.get()
        compiler = Compiler(source)
        try:
            result = compiler.compile()
            postfix = compiler.postfix()

            print("Input Source Code:", source)
            print("Result:", result)
            print("Postfix Expression:", postfix)

            self.result_text.config(state='normal')
            self.result_text.insert('end', '\n' + str(result))
            self.result_text.config(state='disabled')

            self.postfix_text.config(state='normal')
            self.postfix_text.insert('end', '\n' + postfix)
            self.postfix_text.config(state='disabled')

            self.previous_result = str(result)

        except Exception as e:
            self.show_error(str(e))

    def clear_output(self):
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', 'end')
        self.result_text.config(state='disabled')

        self.postfix_text.config(state='normal')
        self.postfix_text.delete('1.0', 'end')
        self.postfix_text.config(state='disabled')

    def show_error(self, message):
        messagebox.showerror("Error", message)

if __name__ == "__main__":
    app = CompilerWindow()
    app.mainloop()
