import sys

input_file = open('myData.cvs','r')
input_text = input_file.read()

program_lines = input_text.split('\n')

combines = {}

ast = []

for line in program_lines:
    if('|' in line):
        tokens = tokenize(line)
        ast_line = parse(tokens, line)
        ast.append(ast_line)

execute(ast)

#Clean
def remove_space(s):
    return s.replace(' ','')

#Tokenization
def tokenize(line):
    tokens = line.split('|')
    tokens = [ t.strip() for t in tokens ]
    tokens = [ None if t == '' else t for t in tokens ]
    if(len(tokens) == 2):
        tokens.append(None)
    if(len(tokens) != 3):
        raise Exception('Too many columns - {}', line)
    return tokens

#Parsing
def parse(tokens, line):
    if(is_input(tokens)):
        return ('INPUT', tokens[0], tokens[1])
    elif(is_assign(tokens)):
        return ('ASSIGN', tokens[0], tokens[1])
    elif(is_output(tokens)):
        return ('OUTPUT', tokens[1], tokens[2])
    elif(is_calculation(tokens)):
        return ('CALCULATION', tokens[0], tokens[1], token[2])
    else:
        return Exception('Line type not supported - {}', line)

#Check token
def is_input(tokens):
    return no_third_col(tokens) and has_question_mark(tokens)

def is_assign(tokens):
    return no_third_col(tokens) and not has_question_mark(tokens)

def is_output(tokens):
    return no_first_col(tokens)

def is_calculation(tokens):
    return has_three_col(tokens)

#Functions of check
def no_third_col(tokens):
    return tokens[0] != None and tokens[1] != None and tokens[2] == None

def no_first_col(tokens):
    return tokens[0] == None and tokens[1] != None and tokens[2] != None

def has_three_col(tokens):
    return tokens[0] != None and tokens[1] != None and tokens[2] != None

def has_question_mark(tokens):
    return tokens[1][-1] == '?'

#Execution
def exe(ast):
    for line in ast:
        line_type = line[0]
        params = line[1]
        if(line_type == 'INPUT'): exe_input(*params)
        if(line_type == 'ASSIGN'): exe_assign(*params)
        if(line_type == 'OUTPUT'): exe_output(*params)
        if(line_type == 'CALCULATION'): exe_calculation(*params)


def exe_input(var_name, question):
    var_name = remove_space(var_name)
    combines[var_name] = int(input(question + ' '))

def exe_assign(var_name, expression):
    var_name = remove_space(var_name)
    expression = remove_space(expression)
    statement = var_name + '=' + expression
    exec(statement, combines)

def exe_output(expression, output_format):
    exe_assign('temp_var', expression)
    print(output_format.replace('__', str(combines['temp_var'])))

def exe_calculation(var_name, expression, output_format):
    exe_assign(var_name, expression)
    var_name = remove_space(var_name)
    print(output_format.replace('__',str(combines[var_name])))

