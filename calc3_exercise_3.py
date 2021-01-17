INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Interpreter:
    # lexer = takes input and converts it into a stream of tokens
    # parser = feeds off the stream of tokens provided by the lexer and tries to recognize the structure
    # interpreter = generates results from parsed expression
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    # lexer segment
    def error(self):
        raise Exception("Invalid Syntax")

    def advance(self):
        """ Advances the `pos` counter and sets the current character to either None or the current value. """
        self.pos += 1
        if (self.pos > len(self.text) - 1):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char.isspace() and self.current_char not None:
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isdigit():
                return Token(INTEGER, int(self.current_char))
            elif self.current_char.isspace():
                self.skip_whitespace()
                continue
            elif self.current_char == '+':
                return Token(PLUS, str(self.current_char))
            elif self.current_char == '-':
                return Token(MINUS, str(self.current_char))

            self.error()

        return Token(EOF, None)

    # parser and interpreter segment
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        """Return an INTEGER token value."""
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        """Arithmetic expression parser / interpreter."""
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result

def main():
    while True:
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            # text = raw_input('calc> ')
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()