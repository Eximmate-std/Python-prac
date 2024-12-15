from math import *


def interpreter():
    functions = {}
    processed_lines = 0

    while True:
        line = input().strip()
        processed_lines += 1

        if line.startswith(':'):
            parts = line[1:].split(' ')
            func_name = parts[0]
            params = parts[1:-1]
            expression = parts[-1]

            functions[func_name] = (params, expression)

        elif line.startswith('quit'):
            format_string = line.split(' ', 1)[1].strip('"')
            print(format_string.format(len(functions) + 1, processed_lines))
            break
        else:
            parts = line.split(' ')
            func_name = parts[0]
            arguments = parts[1:]

            if func_name in functions:
                params, expression = functions[func_name]

                if len(params) == 1:
                    arg_values = [arguments[0]]
                else:
                    arg_values = arguments

                local_scope = {params[i]: eval(arg_values[i]) for i in range(len(params))}

                try:
                    result = eval(expression, globals(), local_scope)
                    print(result)
                except:
                    raise Exception

interpreter()

"""
:sin x sin(x)
sin 1
:decorate s "--<<{}>>--".format(s)
decorate "ЖЖЖ"
sin 2
quit "{}, {}"

"""
