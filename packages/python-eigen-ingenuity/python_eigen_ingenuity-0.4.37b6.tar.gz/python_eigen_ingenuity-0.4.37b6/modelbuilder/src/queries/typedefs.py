"""Cymple's API type definitions."""
from collections import namedtuple
import ast
import datetime
import messages

Mapping = namedtuple('Mapping', ['ref_name', 'returned_name'], defaults=(None, None))

class Properties(dict):
    """A dict class storing a set of properties."""

    @staticmethod
    def _escape(string: str) -> str:
        res = string.replace('\\', '\\\\').replace('\r', '\\r').replace('\n', '\\n').replace('"', '\\"')
        return res

    @staticmethod
    def _format_value(key, value):

        def try_date_format(date_format):
            try:
                tested_date = datetime.datetime.strptime(value.replace('/', '-'), date_format).date()
            except:
                tested_date = None
            return tested_date

        def try_dates():
            date1 = try_date_format('%Y-%m-%d')
            date2 = try_date_format('%d-%m-%Y')
            date_found = date1 or date2
            return date_found

        quote = '"'
        escaped_value = Properties._escape(value)
        if len(key.split(':')) == 2:
            # data type defined on header
            given_data_type = key.split(':')[-1]
            try:
                match given_data_type:
                    case 'str':
                        result = quote + escaped_value + quote
                    case 'int':
                        # Remove any leading zeroes because the literal_eval function does not support them
                        while escaped_value.startswith('0'):
                            escaped_value = escaped_value[1:]
                        result = int(ast.literal_eval(escaped_value))
                        if result != ast.literal_eval(escaped_value):
                            messages.warning_message('Invalid data: ', f'{ast.literal_eval(escaped_value)} is not a valid Integer, {result} used instead')
                    case 'float':
                        result = float(ast.literal_eval(escaped_value))
                    case 'bool':
                        result = ast.literal_eval(escaped_value.capitalize())
                        if str(result) not in ['True', 'False']:
                            messages.error_message('Invalid data: ', f'{ast.literal_eval(escaped_value)} is not a valid boolean so not set')
                            result = ''
                    case 'date':
                        formatted_date = try_dates()
                        if formatted_date:
                            result = 'date("' + str(formatted_date) + '")'
                        else:
                            messages.error_message(f'Invalid data: {value} is not a valid date so value not set')
                            result = ''
                    case _:
                        # Treat unsupported formats as strings
                        result = quote + escaped_value + quote
            except:
                messages.error_message('Invalid data: ', f'{value} is not valid for type {given_data_type} so value not set!')
                result = ''
        else:
            try:
                # Use .capitalize() here to catch incorrectly formatted Booleans (e.g. 'true')
                boolean_check = value.capitalize()
                if boolean_check == 'True' or boolean_check == 'False':
                    data_type = bool
                else:
                    data_type = type(ast.literal_eval(value))
            except:
                # Now see if it's a date
                date1 = try_date_format('%Y-%m-%d')
                date2 = try_date_format('%d-%m-%Y')
                formatted_date = date1 or date2
                data_type = 'date' if formatted_date else 'str'

            if value is None:
                result = 'null'
            else:
                match str(data_type):
                    case 'str':
                        result = quote + escaped_value + quote
                    case "<class 'int'>":
                        if escaped_value != '0' and escaped_value.startswith('0'):
                            # Has a leading 0, so treat as a string
                            result = quote + escaped_value + quote
                        else:
                            result = int(ast.literal_eval(escaped_value))
                            if result != ast.literal_eval(escaped_value):
                                messages.warning_message('Invalid data: ', f'{ast.literal_eval(escaped_value)} is not a valid Integer, {result} used instead')
                    case "<class 'float'>":
                        result = ast.literal_eval(escaped_value)
                    case "<class 'bool'>":
                        result = ast.literal_eval(escaped_value.capitalize())
                    case "<class 'list'>":
                        result = escaped_value
                    case 'date':
                        formatted_date = try_dates()
                        if formatted_date:
                            result = 'date("' + str(formatted_date) + '")'
                        else:
                            messages.error_message('Invalid data: ', f'{value} is not valid for type {data_type} so value not set')
                            result = ''
                    case _:
                        # Shouldn't get here, but just in case use a string
                        result = quote + escaped_value + quote

        return result

    def to_str(self, comparison_operator: str = ':', boolean_operator: str = ',') -> str:
        """Convert this Properties dictionary to a serialised string suitable for a cypher query"""
        pairs = [f'{key.split(":")[0]}{comparison_operator}{Properties._format_value(key, str(value))}' for key, value in self.items()]
        res = boolean_operator.join(pairs)
        return res

    def format(self):
        # Reformat using identified data types
        pairs = []
        for key, value in self.items():
            pairs.append(f'{key.split(":")[0]}:{Properties._format_value(key, str(value))}')
        return '{' + ','.join(pairs) + '}'

    def __str__(self) -> str:
        return self.to_str()
