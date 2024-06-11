import math

from .exceptions import ExpressionError, ExpressionVariableError
from .globals import SIXTH_PI, QUARTER_PI, THIRD_PI, PI, TWO_PI, ONE_AND_HALF_PI, HALF_PI


class ExpressionLog:
    
    def __init__(self):
        self.variables = {}
        self.statements = []

    def add_variable(self, variable, value):
        if variable not in self.variables:
            self.variables[variable] = value

    def __str__(self):
        return f"Expression Log Statements: {self.statements}, Variables: {self.variables}"


class ExpressionBuilder:
    op_none = 0
    op_plus = 1
    op_minus = 2
    op_multiply = 3
    op_divide = 4
    logic_variable = 5
    logic_eq = 6
    logic_ne = 7
    logic_gt = 8
    logic_gte = 9
    logic_lt = 10
    logic_lte = 11
    logic_and = 12
    logic_or = 13
    logic_xor = 14
    question_mark = 15
    question_mark_separator = 16
    result_eq_variable = 17

    def __init__(self):

        self.operators_map = {self.op_none: '',
                              self.op_plus: '+',
                              self.op_minus: '-',
                              self.op_multiply: '*',
                              self.op_divide: '/',
                              self.logic_variable: '',
                              self.logic_eq: '==',
                              self.logic_ne: '!=',
                              self.logic_gt: '>',
                              self.logic_gte: '>=',
                              self.logic_lt: '<',
                              self.logic_lte: '<=',
                              self.logic_and: '&&',
                              self.logic_or: '||',
                              self.logic_xor: 'XOR',
                              self.question_mark: '?',
                              self.question_mark_separator: ':',
                              self.result_eq_variable: '='
                              }

        self.operators = {'+': self.op_plus,
                          '-': self.op_minus,
                          '*': self.op_multiply,
                          '/': self.op_divide}

        self.logic_first_operators = {'>': self.logic_gt,
                                      '<': self.logic_lt}
        self.logic_second_operators = {'=': self.logic_eq,
                                       '!': self.logic_ne,
                                       '>': self.logic_gte,
                                       '<': self.logic_lte}

        self.global_data = {}
        self.options = {}
        self.global_set_data = {}
        self.global_usage_dict_data = {}
        self.global_statement_data = {}
        self.global_set_statement_data = {}
        self.global_string_statement_data = {}
        self.global_symbolic_link_data = {}
        self.used_statements = {}
        self.highest_inheritance_level = -1  # used for inheritance for indirect values

    def run_statement(self, statement, variables=None, statement_variables=None,
                      replace_values=None, statement_inheritance_level=-1,
                      _process_multi_part=True, expression_log=None, default_value=None):
        """

        This is the main guts of the class. This function is recursive when brackets are used
        The data get pre passed and then processed by three functions
        @param statement:
        @param variables:
        @param statement_variables:
        @param replace_values:
        @param statement_inheritance_level:
        @param _process_multi_part: boolean
        @param expression_log: dict

        """
        log_statement_index = None
        if expression_log is not None:
            if not isinstance(expression_log, ExpressionLog):
                assert False, 'Variable expression_log must be the "ExpressionLog" class'
            else:
                expression_log.statements.append('')
                log_statement_index = len(expression_log.statements) - 1

        if statement == "" or statement is None:
            return ""
        elif isinstance(statement, (int, float, bool)):
            return statement
        use_default = default_value is not None
        self.highest_inheritance_level = statement_inheritance_level
        bracket_count = 0
        current_statement = ""

        current_operator = self.op_none
        parts = []
        statement_length = len(str(statement))

        skip_characters = 0
        current_string_char = None
        function_name = None
        dictionary_value_mode = False
        new_statement = None
        replace_string_mode = False

        for (current_character_index, current_character) in enumerate(str(statement)):
            next_character2 = ''
            if skip_characters > 0:
                skip_characters -= 1
                continue
            elif current_character_index < statement_length - 1:
                next_character = statement[current_character_index + 1]
                if current_character_index < statement_length - 2:
                    next_character2 = statement[current_character_index + 2]
            else:
                next_character = ''
            if ((current_character == "'" or current_character == '"') and  # string handling  (' or ")
                    (current_character == current_string_char or current_string_char is None)):
                if current_string_char is None:
                    current_string_char = current_character
                elif bracket_count == 0:
                    if replace_string_mode:
                        current_statement = self.string_replace(current_statement,
                                                                variables,
                                                                statement_variables,
                                                                replace_values)
                        replace_string_mode = False
                    if not dictionary_value_mode:

                        self.log_operator_symbol(expression_log=expression_log,
                                                 log_statement_index=log_statement_index,
                                                 operator=current_operator,
                                                 statement=f'{current_character}{current_statement}{current_character}')
                        parts.append((current_operator, self.convert_variables(current_statement=current_statement,
                                                                               is_string=True,
                                                                               variables=variables,
                                                                               statement_variables=statement_variables,
                                                                               replace_values=replace_values,
                                                                               process_multi_part=_process_multi_part,
                                                                               expression_log=expression_log)))
                        current_statement = ""
                    current_string_char = None
                else:
                    current_string_char = None
                if bracket_count > 0 or dictionary_value_mode:
                    current_statement += current_character
            elif current_string_char is not None:  # string handling ' or "
                if current_character == "\\" and (next_character == "'" or next_character == '"'):
                    current_statement += next_character
                    skip_characters = 1
                else:
                    current_statement += current_character
            elif ((current_character == '{' or current_character == '{') and
                  bracket_count == 0 and current_string_char is None):
                current_statement += current_character
                dictionary_value_mode = True if current_character == '{' else '}'
            elif current_character == '(':
                if bracket_count == 0 and current_statement != "":
                    if expression_log is not None:
                        expression_log.statements[log_statement_index] += f'{current_statement}'
                    function_name = current_statement
                    current_statement = ""
                if bracket_count > 0:
                    current_statement += current_character
                bracket_count += 1
                continue
            elif current_character == ')':
                bracket_count -= 1
                if bracket_count > 0:
                    current_statement += current_character
                elif bracket_count == 0:
                    if expression_log is not None:
                        self.log_operator_symbol(expression_log=expression_log,
                                                 log_statement_index=log_statement_index,
                                                 operator=current_operator,
                                                 statement=f'({current_statement})')

                    if function_name is not None:

                        arguments = []
                        for argument in self.get_function_arguments(current_statement):
                            arg_statement = self.run_statement(argument,
                                                               variables=variables,
                                                               statement_variables=statement_variables,
                                                               replace_values=replace_values,
                                                               statement_inheritance_level=self.get_inheritance_level(),
                                                               expression_log=expression_log,
                                                               default_value=default_value)
                            arguments.append(arg_statement)

                        try:
                            function_data = self.convert_functions(function_name, arguments)
                        except ValueError:
                            raise ExpressionError(f'Value error ({statement})')
                        if function_data['routine']:
                            if function_name == "switch":
                                function_value, skip_characters = self.process_switch_statement(
                                    switch_value=function_data['value'],
                                    statement=statement,
                                    current_character_index=current_character_index,
                                    variables=variables,
                                    statement_variables=statement_variables,
                                    replace_values=replace_values,
                                    expression_log=expression_log)
                                self.append_part(parts=parts,
                                                 expression_log=expression_log,
                                                 log_statement_index=log_statement_index,
                                                 operator=current_operator,
                                                 statement=function_value,
                                                 statement_value=True)
                        else:
                            self.append_part(parts=parts,
                                             expression_log=expression_log,
                                             log_statement_index=log_statement_index,
                                             operator=current_operator,
                                             statement=function_data['value'],
                                             statement_value=True)
                        function_name = None
                        current_statement = ""
                        continue

                    current_statement = self.run_statement(current_statement,
                                                           variables=variables,
                                                           statement_variables=statement_variables,
                                                           replace_values=replace_values,
                                                           statement_inheritance_level=self.get_inheritance_level(),
                                                           expression_log=expression_log,
                                                           default_value=default_value)

                    if isinstance(current_statement, dict):
                        parts.append((current_operator, current_statement))
                    else:
                        try:
                            value = float(current_statement)
                        except ValueError:
                            value = current_statement
                        parts.append((current_operator, value))

                        if expression_log is not None:
                            expression_log.statements[log_statement_index] += f'[{value}]'

                    current_statement = ""
                continue

            elif bracket_count > 0:
                current_statement += current_character
                continue
            elif current_character == ' ':
                continue

            elif self.is_math_operator(current_character):
                if len(current_statement) > 0:
                    self.add_to_part(current_operator=current_operator,
                                     current_statement=current_statement,
                                     variables=variables,
                                     statement_variables=statement_variables,
                                     replace_values=replace_values,
                                     parts=parts,
                                     process_multi_part=_process_multi_part,
                                     expression_log=expression_log,
                                     log_statement_index=log_statement_index)
                    current_statement = ""
                current_operator = self.operators[current_character]

            elif (current_character == "X" and next_character == "O"
                  and next_character2 == "R" and statement[current_character_index - 1] == ' '):
                self.add_to_part(current_operator=current_operator,
                                 current_statement=current_statement,
                                 variables=variables,
                                 statement_variables=statement_variables,
                                 replace_values=replace_values,
                                 parts=parts,
                                 process_multi_part=_process_multi_part,
                                 expression_log=expression_log,
                                 log_statement_index=log_statement_index)
                self.append_part(parts=parts,
                                 expression_log=expression_log,
                                 log_statement_index=log_statement_index,
                                 operator=self.logic_xor)

                skip_characters = 2
                current_statement = ""
                current_operator = self.op_none

            elif self.is_logical_operator(current_character):

                if next_character == "=" and current_character in self.logic_second_operators:
                    self.add_to_part(current_operator=current_operator,
                                     current_statement=current_statement,
                                     variables=variables,
                                     statement_variables=statement_variables,
                                     replace_values=replace_values,
                                     parts=parts,
                                     process_multi_part=_process_multi_part,
                                     expression_log=expression_log,
                                     log_statement_index=log_statement_index)

                    self.append_part(parts=parts,
                                     expression_log=expression_log,
                                     log_statement_index=log_statement_index,
                                     operator=self.logic_second_operators[current_character])
                    skip_characters = 1

                elif current_character == "&" and next_character == "&":
                    self.add_to_part(current_operator=current_operator,
                                     current_statement=current_statement,
                                     variables=variables,
                                     statement_variables=statement_variables,
                                     replace_values=replace_values,
                                     parts=parts,
                                     process_multi_part=_process_multi_part,
                                     expression_log=expression_log,
                                     log_statement_index=log_statement_index)

                    self.append_part(parts=parts,
                                     expression_log=expression_log,
                                     log_statement_index=log_statement_index,
                                     operator=self.logic_and)
                    skip_characters = 1
                elif current_character == "|" and next_character == "|":
                    self.add_to_part(current_operator=current_operator,
                                     current_statement=current_statement,
                                     variables=variables,
                                     statement_variables=statement_variables,
                                     replace_values=replace_values,
                                     parts=parts,
                                     process_multi_part=_process_multi_part,
                                     expression_log=expression_log,
                                     log_statement_index=log_statement_index)
                    self.append_part(parts=parts,
                                     expression_log=expression_log,
                                     log_statement_index=log_statement_index,
                                     operator=self.logic_or)
                    skip_characters = 1

                elif current_character in self.logic_first_operators:
                    self.add_to_part(current_operator=current_operator,
                                     current_statement=current_statement,
                                     variables=variables,
                                     statement_variables=statement_variables,
                                     replace_values=replace_values,
                                     parts=parts,
                                     process_multi_part=_process_multi_part,
                                     expression_log=expression_log,
                                     log_statement_index=log_statement_index)

                    self.append_part(parts=parts,
                                     expression_log=expression_log,
                                     log_statement_index=log_statement_index,
                                     operator=self.logic_first_operators[current_character])
                elif current_character == "?":
                    self.add_to_part(current_operator=current_operator,
                                     current_statement=current_statement,
                                     variables=variables,
                                     statement_variables=statement_variables,
                                     replace_values=replace_values,
                                     parts=parts,
                                     process_multi_part=_process_multi_part,
                                     expression_log=expression_log,
                                     log_statement_index=log_statement_index)

                    self.append_part(parts=parts,
                                     expression_log=expression_log,
                                     log_statement_index=log_statement_index,
                                     operator=self.question_mark)
                elif current_character == ":":
                    self.add_to_part(current_operator=current_operator,
                                     current_statement=current_statement,
                                     variables=variables,
                                     statement_variables=statement_variables,
                                     replace_values=replace_values,
                                     parts=parts,
                                     process_multi_part=_process_multi_part,
                                     expression_log=expression_log,
                                     log_statement_index=log_statement_index)

                    self.append_part(parts=parts,
                                     expression_log=expression_log,
                                     log_statement_index=log_statement_index,
                                     operator=self.question_mark_separator)
                elif current_character == "=":
                    if current_statement != '':
                        use_default = False
                        self.append_part(parts=parts,
                                         expression_log=expression_log,
                                         log_statement_index=log_statement_index,
                                         operator=self.result_eq_variable,
                                         statement=current_statement)
                current_statement = ""
                current_operator = self.op_none
            elif current_character == ';':
                new_statement = statement[current_character_index + 1:]
                break
            elif current_character == '^':
                replace_string_mode = True
            else:
                current_statement += current_character

        if len(current_statement) > 0:

            if use_default:
                self.append_part(parts=parts,
                                 expression_log=expression_log,
                                 log_statement_index=log_statement_index,
                                 operator=self.result_eq_variable,
                                 statement=current_statement)
                self.add_to_part(current_operator=current_operator,
                                 current_statement=str(default_value),
                                 variables=variables,
                                 statement_variables=statement_variables,
                                 replace_values=replace_values,
                                 parts=parts,
                                 process_multi_part=_process_multi_part,
                                 expression_log=expression_log,
                                 log_statement_index=log_statement_index)
            else:
                self.add_to_part(current_operator=current_operator,
                                 current_statement=current_statement,
                                 variables=variables,
                                 statement_variables=statement_variables,
                                 replace_values=replace_values,
                                 parts=parts,
                                 process_multi_part=_process_multi_part,
                                 expression_log=expression_log,
                                 log_statement_index=log_statement_index)
        results = self.process_parts(statement, parts)

        if new_statement is not None and len(new_statement) > 0:
            if not isinstance(results, dict):
                raise ExpressionError('Bad statement (%s)' % statement)
            new_variables = variables
            if new_variables is None:
                new_variables = results

            extra_statements_results = self.run_statement(new_statement,
                                                          variables=new_variables,
                                                          statement_variables=statement_variables,
                                                          replace_values=replace_values,
                                                          statement_inheritance_level=self.get_inheritance_level(),
                                                          expression_log=expression_log,
                                                          default_value=default_value)

            results = dict(list(results.items()) + list(extra_statements_results.items()))

        return results

    def append_part(self, parts, expression_log, log_statement_index, operator,
                    statement=None, statement_value=False):
        self.log_operator_symbol(expression_log=expression_log,
                                 log_statement_index=log_statement_index,
                                 operator=operator,
                                 statement=statement,
                                 statement_value=statement_value
                                 )

        parts.append((operator, statement))

    def add_to_part(self, current_operator, current_statement, variables,
                    statement_variables, replace_values, parts,
                    process_multi_part, expression_log, log_statement_index):
        if current_statement != "":
            self.log_operator_symbol(expression_log=expression_log,
                                     log_statement_index=log_statement_index,
                                     operator=current_operator,
                                     statement=current_statement)

            parts.append((current_operator, self.convert_variables(current_statement=current_statement,
                                                                   is_string=False,
                                                                   variables=variables,
                                                                   statement_variables=statement_variables,
                                                                   replace_values=replace_values,
                                                                   process_multi_part=process_multi_part,
                                                                   expression_log=expression_log)))

    def log_operator_symbol(self, expression_log, log_statement_index, operator,
                            statement=None, statement_value=False):
        if expression_log is not None:
            operator_symbol = self.operators_map.get(operator)
            if operator not in [self.op_none, self.result_eq_variable] and operator_symbol is not None:
                expression_log.statements[log_statement_index] += f' {operator_symbol} '
            if statement is not None:
                if statement_value:
                    expression_log.statements[log_statement_index] += f'[{statement}]'
                else:
                    expression_log.statements[log_statement_index] += statement

            if operator == self.result_eq_variable and operator_symbol is not None:
                expression_log.statements[log_statement_index] += f' {operator_symbol} '

    def string_replace(self, statement, variables=None, statement_variables=None, replace_values=None,
                       expression_log=None):

        return_string = ""
        bracket_count = 0
        current_statement = ""
        if statement is None:
            return ''
        for current_character in statement:
            if isinstance(current_character, int):
                current_character = chr(current_character)

            if current_character == '[':
                if bracket_count == 0:
                    current_statement = ""
                if bracket_count > 0:
                    current_statement += current_character
                bracket_count += 1
                continue
            elif current_character == ']':
                bracket_count -= 1
                if bracket_count > 0:
                    current_statement += current_character
                elif bracket_count == 0:
                    value = self.run_statement(current_statement,
                                               variables=variables,
                                               statement_variables=statement_variables,
                                               replace_values=replace_values,
                                               statement_inheritance_level=self.get_inheritance_level(),
                                               expression_log=expression_log)
                    if isinstance(value, (float, int)):
                        return_string += "%g" % value
                    else:
                        return_string += value

            elif bracket_count > 0:
                current_statement += current_character
            else:
                return_string += current_character
        return return_string

    @staticmethod
    def convert_functions(function_name, arguments):
        """
        deals with a function with one argument
        @param function_name:
        @param arguments:
        """

        if function_name == "tan":
            return {'value': math.tan(float(arguments[0])), 'routine': False}
        elif function_name == "atan":
            return {'value': math.atan(float(arguments[0])), 'routine': False}
        elif function_name == "atan2":
            return {'value': math.atan2(float(arguments[0]), float(arguments[1])), 'routine': False}
        elif function_name == "tand":
            return {'value': math.tan(float(arguments[0]) * PI / 180.0), 'routine': False}
        elif function_name == "atand":
            value = math.atan(float(arguments[0]))
            value *= 180.0 / PI
            return {'value': value, 'routine': False}
        elif function_name == "cos":
            return {'value': math.cos(float(arguments[0])), 'routine': False}
        elif function_name == "acos":
            return {'value': math.acos(float(arguments[0])), 'routine': False}
        elif function_name == "cosd":
            return {'value': math.cos(float(arguments[0]) * PI / 180.0), 'routine': False}
        elif function_name == "acosd":
            value = math.acos(float(arguments[0]))
            value *= 180.0 / PI
            return {'value': value, 'routine': False}
        elif function_name == "sin":
            return {'value': math.sin(float(arguments[0])), 'routine': False}
        elif function_name == "asin":
            return {'value': math.asin(float(arguments[0])), 'routine': False}
        elif function_name == "sind":
            return {'value': math.sin(float(arguments[0]) * PI / 180.0), 'routine': False}
        elif function_name == "asind":
            value = math.asin(float(arguments[0]))
            value *= 180.0 / PI
            return {'value': value, 'routine': False}
        elif function_name == "switch":
            return {'value': arguments[0], 'routine': True}
        elif function_name == "sqrt":
            return {'value': math.sqrt(float(arguments[0])), 'routine': False}
        elif function_name == "hypot":
            return {'value': math.hypot(float(arguments[0]), float(arguments[1])), 'routine': False}
        elif function_name == "int":
            return {'value': int(arguments[0]), 'routine': False}
        elif function_name == "get":
            return {'value': arguments[0].get(arguments[1]), 'routine': False}
        else:
            raise ExpressionError('No function named %s' % function_name)

    @staticmethod
    def get_function_arguments(all_arguments):

        arguments = []

        if ',' in all_arguments:

            bracket_count = 0
            current_statement = ''
            statement_length = len(all_arguments)
            current_string_char = None

            skip_characters = 0

            for (current_character_index, current_character) in enumerate(all_arguments):
                if skip_characters > 0:
                    skip_characters -= 1
                    continue
                if current_character_index < statement_length - 1:
                    next_character = all_arguments[current_character_index + 1]
                else:
                    next_character = ''

                if (current_character == "'" or current_character == '"') and current_character == current_string_char:
                    current_string_char = None
                    current_statement += current_character
                elif (current_character == "'" or current_character == '"') and current_string_char is None:
                    current_string_char = current_character
                    current_statement += current_character
                elif current_string_char is not None:  # string handling ' or "
                    current_statement += current_character
                    if current_character == "\\" and (next_character == "'" or next_character == '"'):
                        current_statement += next_character
                        skip_characters = 1
                elif current_character == '(':
                    bracket_count += 1
                    current_statement += current_character
                elif current_character == ')':
                    bracket_count -= 1
                    current_statement += current_character
                elif bracket_count == 0 and current_character == ',':
                    arguments.append(current_statement)
                    current_statement = ''
                else:
                    current_statement += current_character
            if current_statement != '':
                arguments.append(current_statement)
        else:
            arguments.append(all_arguments)
        return arguments

    def split_statement(self, current_statement, variables, statement_variables, replace_values, expression_log):
        """head
        This split a statement so it can be used for dictionaries
        dict_name[key] is normal use if dict_name{key} will mean that if it key doesn't
         exist it will try a key of blank
         @param current_statement:
         @param variables:
         @param statement_variables:
         @param replace_values:
         @param expression_log: boolean

        """
        if not ('{' in current_statement or '[' in current_statement):
            return [current_statement]

        current_part = ''
        return_data = []
        special_mode = False
        in_quotes_char = None
        last_character = None
        for current_character in current_statement:
            if in_quotes_char is None and (current_character == '"' or current_character == "'"):
                in_quotes_char = current_character
                current_part += current_character
            elif last_character != '\'' and current_character == in_quotes_char:
                current_part += current_character
                last_character = None
                in_quotes_char = None
            elif in_quotes_char is not None:
                last_character = current_character
                current_part += current_character
            elif current_character == '{' or current_character == '[':
                special_mode = True
                if current_part != '':
                    return_data.append((current_part, False))
                    current_part = ''
            elif current_character == '}' or current_character == ']':
                current_part = self.run_statement(current_part,
                                                  variables=variables,
                                                  statement_variables=statement_variables,
                                                  replace_values=replace_values,
                                                  statement_inheritance_level=self.get_inheritance_level(),
                                                  expression_log=expression_log)
                return_data.append((current_part, True if current_character == '}' else False))
                current_part = ''
                special_mode = False
            elif current_character == '.' and not special_mode:
                if current_part != '':
                    return_data.append((current_part, False))
                    current_part = ''
            else:
                current_part += current_character
        if current_part != '':
            return_data.append((current_part, False))
        return return_data

    def convert_variables(self, current_statement, is_string, variables,
                          statement_variables, replace_values, process_multi_part, expression_log):
        if not is_string:

            if replace_values is not None:
                for find_char, replace_with in replace_values.items():
                    current_statement = current_statement.replace(find_char, str(replace_with))
            current_statement_split = self.split_statement(current_statement=current_statement,
                                                           variables=variables,
                                                           statement_variables=statement_variables,
                                                           replace_values=replace_values,
                                                           expression_log=expression_log)

            if current_statement in self.global_symbolic_link_data:
                current_statement = self.global_symbolic_link_data[current_statement]['link_to']

            if variables is not None and current_statement in variables:
                is_string = True
                self.add_to_used_variables(variable_name=current_statement,
                                           expression_log=expression_log,
                                           value=variables[current_statement])
                current_statement = variables[current_statement]
            elif current_statement in self.global_data:
                is_string = True
                self.add_to_used_variables(variable_name=current_statement,
                                           expression_log=expression_log,
                                           value=self.global_data[current_statement][0])
                highest_inheritance_level = self.global_data[current_statement][1]
                current_statement = self.global_data[current_statement][0]
                if self.highest_inheritance_level < highest_inheritance_level:
                    self.highest_inheritance_level = highest_inheritance_level

            elif current_statement in self.options:
                is_string = True
                current_statement = self.process_options(option_code=current_statement,
                                                         variables=variables,
                                                         statement_variables=statement_variables,
                                                         expression_log=expression_log)

            elif statement_variables is not None and current_statement in statement_variables:
                is_string = True
                current_statement = self.run_statement(statement_variables[current_statement],
                                                       variables=variables,
                                                       statement_variables=statement_variables,
                                                       replace_values=replace_values,
                                                       statement_inheritance_level=self.get_inheritance_level(),
                                                       expression_log=expression_log)
            elif current_statement in self.global_statement_data:
                is_string = True
                current_statement = self.run_statement(self.global_statement_data[current_statement],
                                                       variables=variables,
                                                       statement_variables=statement_variables,
                                                       replace_values=replace_values,
                                                       statement_inheritance_level=self.get_inheritance_level(),
                                                       expression_log=expression_log)
            elif current_statement in self.global_string_statement_data:
                return self.string_replace(statement=self.global_string_statement_data[current_statement],
                                           variables=variables,
                                           statement_variables=statement_variables,
                                           replace_values=replace_values,
                                           expression_log=expression_log)
            elif len(current_statement_split) > 1 and current_statement_split[0][0] in self.global_usage_dict_data:

                current_dict_or_value = self.global_usage_dict_data[current_statement_split[0][0]]
                for cs in current_statement_split[1:]:
                    if cs[0] in current_dict_or_value:
                        current_dict_or_value = current_dict_or_value[cs[0]]
                    elif cs[1] and '' in current_dict_or_value:
                        current_dict_or_value = current_dict_or_value['']
                    else:
                        return current_dict_or_value
                return current_dict_or_value
            else:
                value = self.fix_variables(current_statement)
                if value is not None:
                    return value
                found = False
                if len(self.global_set_data) > 0:
                    for set_code, set_data in self.global_set_data.items():
                        if current_statement in set_data:
                            is_string = True
                            self.add_to_used_variables(variable_name=current_statement,
                                                       expression_log=expression_log,
                                                       value=set_data[current_statement][0])
                            highest_inheritance_level = set_data[current_statement][1]
                            current_statement = set_data[current_statement][0]
                            if self.highest_inheritance_level < highest_inheritance_level:
                                self.highest_inheritance_level = highest_inheritance_level
                                found = True
                                break
                if not found and len(self.global_set_statement_data) > 0:
                    for set_code, set_data in self.global_set_statement_data.items():
                        if current_statement in set_data:
                            is_string = True
                            current_statement = self.run_statement(
                                set_data[current_statement],
                                variables=variables,
                                statement_variables=statement_variables,
                                replace_values=replace_values,
                                statement_inheritance_level=self.get_inheritance_level(),
                                expression_log=expression_log)
                            break

        if current_statement is None:
            return None
        if isinstance(current_statement, dict):
            return current_statement
        elif isinstance(current_statement, list):
            return current_statement
        elif isinstance(current_statement, bool):
            return current_statement
        try:
            return float(current_statement)
        except ValueError:
            if is_string:
                return current_statement
            elif process_multi_part and '.' in current_statement:
                # lets see if the first part is part of an equation
                # noinspection PyTypeChecker
                return self.process_multi_part_statement(current_statement=current_statement,
                                                         variables=variables,
                                                         statement_variables=statement_variables,
                                                         replace_values=replace_values,
                                                         expression_log=expression_log)

            else:
                raise ExpressionVariableError(f'No variable named {current_statement}')

    @staticmethod
    def fix_variables(current_statement):
        variables = {'TRUE': True,
                     'YES': True,
                     'FALSE': False,
                     'NO': False,
                     'PI': PI,
                     'HALF_PI': HALF_PI,
                     'TWO_PI': TWO_PI,
                     'ONE_AND_HALF_PI': ONE_AND_HALF_PI,
                     'SIXTH_PI': SIXTH_PI,
                     'QUARTER_PI': QUARTER_PI,
                     'THIRD_PI': THIRD_PI}

        return variables.get(current_statement.upper())

    def process_multi_part_statement(self, current_statement, variables,
                                     statement_variables, replace_values, expression_log):
        parts = current_statement.split('.')

        part_statement = self.run_statement(
            parts[0],
            variables=variables,
            statement_variables=statement_variables,
            replace_values=replace_values,
            statement_inheritance_level=self.get_inheritance_level(),
            _process_multi_part=False,
            expression_log=expression_log)

        parts[0] = part_statement
        current_statement = '.'.join(parts)

        current_statement = self.run_statement(
            current_statement,
            variables=variables,
            statement_variables=statement_variables,
            replace_values=replace_values,
            statement_inheritance_level=self.get_inheritance_level(),
            _process_multi_part=False,
            expression_log=expression_log)
        return current_statement

    def add_to_used_variables(self, variable_name, expression_log, value):
        if variable_name in self.used_statements:
            self.used_statements[variable_name] += 1
        else:
            self.used_statements[variable_name] = 1
        
        if expression_log is not None:
            expression_log.add_variable(variable_name, value)
            expression_log.statements[-1] += f'[{value}]'

    def clear_used_variables(self):
        self.used_statements = {}

    def get_used_variables(self):
        return self.used_statements

    def reset_highest_inheritance_level(self):
        self.highest_inheritance_level = -1

    def get_inheritance_level(self):
        """
        Gets the highest inheritance level
        @return:
        """
        return self.highest_inheritance_level

    def process_parts(self, original_statement, parts):
        self.process_maths(original_statement, parts)
        self.process_logical_operator(original_statement, parts)
        self.process_questions_marks(parts)
        results = self.process_return_variables(original_statement, parts)
        return results

    def process_return_variables(self, original_statement, parts):
        parts_length = len(parts)
        if parts_length == 1:
            return self.calculator(original_statement, 0, parts[0][0], parts[0][1])
        elif parts_length == 0:
            raise ExpressionError('Bad statement (%s)' % original_statement)
        results = {}
        current_variable = ''
        value_valid = False
        for part in parts:
            if part[0] == self.result_eq_variable and not value_valid:
                current_variable = part[1]
                value_valid = True
            elif part[0] == self.result_eq_variable and value_valid:
                raise ExpressionError('Bad statement (%s)' % original_statement)
            elif part[0] == self.op_none and value_valid:
                results[current_variable] = self.calculator(original_statement, 0, part[0], part[1])
                value_valid = False
            elif part[0] == self.op_none and not value_valid:
                raise ExpressionError('Bad statement (%s)' % original_statement)
        return results

    def process_maths(self, original_statement, parts):
        """
            PEMDAS/BODMAS ordering
            @param original_statement:
            @param parts:
        """

        if parts[0][0] == self.op_minus:
            parts[0] = self.op_none, -parts[0][1]

        for current_operators in [(self.op_multiply, self.op_divide),
                                  (self.op_plus, self.op_minus)]:
            if len(parts) == 1:
                return
            found = True
            while found:
                if len(parts) == 1:
                    return
                found = False
                for (counter, part) in enumerate(parts):
                    if (part[0] == current_operators[0] or part[0] == current_operators[1]) and counter > 0:
                        if self.is_coded_math_operator(parts[counter - 1][0]):
                            value = self.calculator(original_statement, parts[counter - 1][1], part[0], part[1])
                            parts[counter - 1] = (parts[counter - 1][0], value)
                            del (parts[counter])
                            found = True
                            break

    def process_logical_operator(self, original_statement, parts):
        """
            deals with >, <, = etc
            @param original_statement:
            @param parts:
        """
        if len(parts) <= 1:
            return

        found = True
        include_and_or = False
        while found:
            parts_length = len(parts)
            if parts_length == 1:
                break
            found = False
            for (counter, part) in enumerate(parts):
                if 0 < counter < parts_length and self.is_coded_logical_operator(part[0], include_and_or):
                    value = self.calculator(original_statement, parts[counter - 1][1], part[0], parts[counter + 1][1])
                    parts[counter] = (self.op_none, value)
                    del (parts[counter + 1])
                    del (parts[counter - 1])

                    found = True
                    break
            if not found and not include_and_or and len(parts) > 1:
                include_and_or = True
                found = True

    def process_questions_marks(self, parts):
        """
            deals with question marks ie a=100?90:100;
            @param parts:
        """
        if len(parts) <= 1:
            return
        found = True
        while found:
            parts_length = len(parts)
            if parts_length == 1:
                break
            found = False
            for (counter, part) in enumerate(parts):
                if part[0] == self.question_mark:

                    found = True

                    start_false = None
                    inner_question_marks = 0

                    for x in range(counter + 1, parts_length):
                        if parts[x][0] == self.question_mark:
                            inner_question_marks += 1
                        elif parts[x][0] == self.question_mark_separator and inner_question_marks > 0:
                            inner_question_marks -= 1
                        elif parts[x][0] == self.question_mark_separator:
                            start_false = x
                            break
                    if start_false is not None:
                        if parts[counter - 1][1]:
                            for x in reversed(range(start_false, parts_length)):
                                del parts[x]
                            del parts[counter]
                            del parts[counter - 1]
                        else:
                            for x in reversed(range(counter - 1, start_false + 1)):
                                del parts[x]
                        break
                    else:
                        raise ExpressionError('Question mark not valid')

    def is_coded_math_operator(self, c):
        return (c == self.op_none or
                c == self.op_plus or
                c == self.op_minus or
                c == self.op_divide or
                c == self.op_multiply)

    @staticmethod
    def is_math_operator(c, ignore_brackets=False):
        if ignore_brackets:
            return c in ['+', '-', '/', '*']
        else:
            return c in ['+', '-', '/', '*', '(', ')']

    def is_coded_logical_operator(self, character, include_and_or):
        if include_and_or:
            if character in [self.logic_and, self.logic_or, self.logic_xor]:
                return True
        return character in [self.logic_eq,
                             self.logic_ne,
                             self.logic_gt,
                             self.logic_gte,
                             self.logic_lt,
                             self.logic_lte]

    @staticmethod
    def is_logical_operator(c):
        return c in ['=', '<', '>', '&', '|', '!', '?', ':']

    def calculator(self, original_statement, left_hand_statement, operator, right_hand_statement):

        if operator != self.op_none:
            left_hand_statement, right_hand_statement = self.get_compare_values(
                left_hand_statement=left_hand_statement,
                right_hand_statement=right_hand_statement,
                statement=original_statement)
        if isinstance(left_hand_statement, list):
            if operator == self.logic_eq:
                return right_hand_statement in left_hand_statement
            elif operator == self.logic_ne:
                return right_hand_statement not in left_hand_statement
            raise ExpressionError('Unable to do check list with operator')
        elif (operator not in [self.op_none, self.logic_and, self.logic_or,
                               self.logic_xor, self.logic_eq, self.logic_ne]
                and isinstance(left_hand_statement, str)
                and isinstance(right_hand_statement, str)
                and left_hand_statement == ''
                and right_hand_statement == ''):
            return left_hand_statement

        if operator == self.op_none:
            return right_hand_statement
        elif operator == self.op_plus:

            return left_hand_statement + right_hand_statement
        elif operator == self.op_minus:
            return left_hand_statement - right_hand_statement
        elif operator == self.op_multiply:
            return left_hand_statement * right_hand_statement
        elif operator == self.op_divide:
            return left_hand_statement / right_hand_statement
        elif operator == self.logic_eq:
            return left_hand_statement == right_hand_statement
        elif operator == self.logic_ne:
            return left_hand_statement != right_hand_statement
        elif operator == self.logic_gt:
            return left_hand_statement > right_hand_statement
        elif operator == self.logic_gte:
            return left_hand_statement >= right_hand_statement
        elif operator == self.logic_lt:
            return left_hand_statement < right_hand_statement
        elif operator == self.logic_lte:
            return left_hand_statement <= right_hand_statement
        elif operator == self.logic_and:
            return left_hand_statement and right_hand_statement
        elif operator == self.logic_or:
            return left_hand_statement or right_hand_statement
        elif operator == self.logic_xor:
            return bool(left_hand_statement) != bool(right_hand_statement)

        return 0.0

    @staticmethod
    def get_compare_values(left_hand_statement, right_hand_statement, statement):
        if left_hand_statement is None and right_hand_statement is None:
            return None, None
        elif isinstance(left_hand_statement, type(right_hand_statement)):
            return left_hand_statement, right_hand_statement
        elif ((isinstance(left_hand_statement, (int, float, bool)) and
               isinstance(right_hand_statement, str)) or
              (isinstance(left_hand_statement, str) and
               isinstance(right_hand_statement, (int, float, bool)))):
            if isinstance(left_hand_statement, str) and left_hand_statement == '':
                left_hand_statement = 0
            elif isinstance(right_hand_statement, str) and right_hand_statement == '':
                right_hand_statement = 0
            else:
                raise ExpressionError('Different type compare (%s)' % statement)
        elif left_hand_statement is None or right_hand_statement is None:
            if left_hand_statement is None:
                if isinstance(right_hand_statement, str):
                    left_hand_statement = ''
                else:
                    left_hand_statement = 0
            else:
                if isinstance(left_hand_statement, str):
                    right_hand_statement = ''
                else:
                    right_hand_statement = 0

        return left_hand_statement, right_hand_statement

    def add_to_global(self, name, value, inheritance_level=-1, set_name=None):
        """
            This will add a normal global data. The data that is the value will not get evaluated.
            @param name:
            @param value:
            @param inheritance_level:
            @param set_name:
        """
        if value is None:
            value_data = ("", inheritance_level)
        else:
            value_data = (value, inheritance_level)

        if set_name is None:
            self.global_data[name] = value_data
        else:
            if set_name not in self.global_set_data:
                self.global_set_data[set_name] = {}
            self.global_set_data[set_name][name] = value_data

    def add_to_global_dict(self, values, inheritance_level=-1, set_name=None):
        """
            This will add a normal global data from a dictionary. The data that is the value will not get evaluated.
            @param values: dict
            @param inheritance_level:
            @param set_name:
        """

        for name, value in values.items():
            self.add_to_global(name, value, inheritance_level, set_name)

    def add_to_global_statement(self, name, value, set_name=None):
        """
            This will add a global data it works like function.
            The data that is the value will get evaluated at run time.
            @param name:
            @param value:
            @param set_name:
        """
        if set_name is None:
            self.global_statement_data[name] = value
        else:
            if set_name not in self.global_set_statement_data:
                self.global_set_statement_data[set_name] = {}

            self.global_set_statement_data[set_name][name] = value

    def add_to_global_statement_dict(self, values, set_name=None):
        """
            This will add a global statements data from a dictionary. It works like function.
            The data in the dictionary that is the value will get evaluated at run time.
            @param values: dict
            @param set_name: str
        """

        if set_name is None:
            for name, value in values.items():
                self.global_statement_data[name] = value
        else:
            if set_name not in self.global_set_statement_data:
                self.global_set_statement_data[set_name] = {}
            for name, value in values.items():
                self.global_set_statement_data[set_name][name] = value

    def add_to_global_string_statement(self, name, value):
        """
            This will add a global string data it will work like function.
            All data inside square brackets will get evaluated.
            @param name:
            @param value:
        """
        self.global_string_statement_data[name] = value

    def add_to_global_usage_dict(self, name, value):
        """
            This will add a dict usage global data. The data that is the value will not get evaluated.
            example usage see class UsageGlobalTests
            @param name:
            @param value:
        """
        current_key = ''
        key_parts = []
        for c in name:
            if c == '.':
                key_parts.append(current_key)
                current_key = ''
            else:
                current_key += c
        if current_key != '':
            key_parts.append(current_key)

        if len(key_parts) == 1:
            self.global_usage_dict_data[key_parts[0]] = value
        elif len(key_parts) > 1:
            if key_parts[0] not in self.global_usage_dict_data:
                self.global_usage_dict_data[key_parts[0]] = {}
            global_dict = self.global_usage_dict_data[key_parts[0]]
            for key_part in key_parts[1:-1]:
                if key_part not in global_dict:
                    global_dict[key_part] = {}
                global_dict = global_dict[key_part]
            global_dict[key_parts[-1]] = value

    def add_symbolic_link_global(self, line_name, link_to, category=''):
        """
            This will add a symbolic link to global data.
            @param line_name:
            @param link_to:
            @param category:
        """
        self.global_symbolic_link_data[line_name] = {'category': category,
                                                     'link_to': link_to}

    def clear_all_symbolic_link_global(self, category_to_remove=None):
        """
            This will clear all symbolic link from global data.
            @param category_to_remove:
        """
        if category_to_remove is None:
            self.global_symbolic_link_data = {}
        else:
            global_symbolic_link_data = {}
            for key, value in self.global_symbolic_link_data.items():
                if value['category'] == category_to_remove:
                    continue
                global_symbolic_link_data[key] = value
            self.global_symbolic_link_data = global_symbolic_link_data

    def process_switch_statement(self, switch_value, statement, current_character_index,
                                 variables, statement_variables, replace_values, expression_log):

        matched_statement = ''
        case_statement = ''
        in_case_statement = False
        in_matched_statement = False
        finished_matching = False
        bracket_count = 0
        skip_characters = 0
        current_word = ''
        in_quotes_char = None
        last_character = None

        for (current_character_index, current_character) in enumerate(statement[current_character_index:]):
            skip_characters += 1

            if in_quotes_char is None and (current_character == '"' or current_character == "'"):
                in_quotes_char = current_character

            if ((last_character is not None and last_character != '\'' and current_character == in_quotes_char) or
                    in_quotes_char is not None):

                if in_case_statement:
                    case_statement += current_character
                elif in_matched_statement:
                    matched_statement += current_character

                if last_character is not None and last_character != '\'' and current_character == in_quotes_char:
                    last_character = None
                    in_quotes_char = None
                else:
                    last_character = current_character
                continue

            if current_character == '{':
                bracket_count += 1
                if bracket_count == 1:
                    continue
            elif current_character == '}':
                if bracket_count == 1:
                    break
                bracket_count -= 1
            if finished_matching:
                continue

            if in_case_statement and current_character == ':':

                if not in_matched_statement:
                    if isinstance(switch_value, (float, int)) and switch_value == float(case_statement):
                        in_matched_statement = True
                    elif switch_value == case_statement[1:-1]:
                        in_matched_statement = True

                in_case_statement = False
            elif in_case_statement:
                case_statement += current_character
            elif in_matched_statement:
                matched_statement += current_character

            if bracket_count == 1:

                if current_character in (' ', ';', ':', '\r', '\n'):
                    if current_word == 'case':
                        if in_matched_statement:
                            matched_statement = matched_statement[:-5]
                        in_case_statement = True
                        case_statement = ''
                    elif current_word == 'break' and in_matched_statement:
                        in_matched_statement = False
                        finished_matching = True
                        matched_statement = matched_statement[:-7]
                    elif current_word == 'default':
                        in_matched_statement = True
                    current_word = ''
                else:
                    current_word += current_character

        current_statement = self.run_statement(matched_statement,
                                               variables=variables,
                                               statement_variables=statement_variables,
                                               replace_values=replace_values,
                                               statement_inheritance_level=self.get_inheritance_level(),
                                               expression_log=expression_log)

        return current_statement, skip_characters

    def process_options(self, option_code, variables, statement_variables, expression_log):
        option_data = self.options[option_code]
        if 'value' in option_data:
            return option_data['value']

        result, local_statement_variables = self.process_option_part(option=option_data['multiple_statements'],
                                                                     variables=variables,
                                                                     statement_variables=statement_variables,
                                                                     expression_log=expression_log)
        if result is None:
            result = option_data['default_value']
        if isinstance(result, dict):
            new_dict = {}

            option_statement_variables = statement_variables
            if option_statement_variables is None:
                option_statement_variables = local_statement_variables
            elif local_statement_variables is not None:
                option_statement_variables = {**variables, **local_statement_variables}

            self.process_dict_option(result=result,
                                     new_dict=new_dict,
                                     variables=variables,
                                     statement_variables=option_statement_variables,
                                     expression_log=expression_log)
            result = new_dict
        option_data['value'] = result
        return result

    def process_dict_option(self, result, new_dict, variables, statement_variables, expression_log):
        for code, value in result.items():
            if isinstance(value, dict):
                new_dict[code] = {}
                self.process_dict_option(result=value,
                                         new_dict=new_dict[code],
                                         variables=variables,
                                         statement_variables=statement_variables,
                                         expression_log=expression_log)

            elif not isinstance(value, (int, float)):
                value = self.run_statement(statement=value,
                                           variables=variables,
                                           statement_variables=statement_variables,
                                           expression_log=expression_log)
                new_dict[code] = value
            else:
                new_dict[code] = value

    def process_option_part(self, option, variables, statement_variables, expression_log):
        for row in option:
            statement = row[0]
            value_data = row[1]
            result = self.run_statement(statement=statement,
                                        variables=variables,
                                        statement_variables=statement_variables,
                                        expression_log=expression_log)

            if result:
                local_variables = {}
                if len(row) > 2:
                    local_variables = row[2]

                if isinstance(value_data, list):
                    option_statement_variables = statement_variables
                    if option_statement_variables is None:
                        option_statement_variables = local_variables
                    elif statement_variables is not None:
                        option_statement_variables = {**statement_variables, **local_variables}

                    return self.process_option_part(option=value_data,
                                                    variables=variables,
                                                    statement_variables=option_statement_variables,
                                                    expression_log=expression_log)

                return value_data, local_variables
        return None, None

    def clear_global_set(self, set_name):
        self.global_set_data[set_name] = {}
        self.global_set_statement_data[set_name] = {}

    def get_variables_for_debug(self, set_name=None):
        variables = []
        if set_name is not None:
            if set_name in self.global_set_data:
                for code, value in self.global_set_data[set_name].items():
                    variables.append({'code': code,
                                      'value': value[0]})

            if set_name in self.global_set_statement_data:
                for code, statement in self.global_set_statement_data[set_name].items():
                    try:
                        value = self.run_statement(code)
                        variables.append({'code': code,
                                          'statement': statement,
                                          'value': value})
                    except ExpressionError as e:
                        variables.append({'code': code,
                                          'statement': statement,
                                          'error': e.value})
        for code, value in self.global_data.items():
            variables.append({'code': code,
                              'value': value[0]})

        for code, statement in self.global_statement_data.items():
            try:
                value = self.run_statement(code)
                variables.append({'code': code,
                                  'statement': statement,
                                  'value': value})
            except ExpressionError as e:
                variables.append({'code': code,
                                  'statement': statement,
                                  'error': e.value})
        return variables

    def add_option(self, code, multiple_statements, default_value=None):
        self.options[code] = {'multiple_statements': multiple_statements,
                              'default_value': default_value}
