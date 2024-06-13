# -*- coding: utf-8 -*-

def database_type_to_sqlalchemy_type(data_type, length=None):
    if data_type.startswith('int') or data_type == 'integer':
        return 'Integer', 'Integer'
    elif data_type.startswith('bigint'):
        return 'BigInteger', 'BigInteger'
    elif data_type == 'varchar' or data_type.startswith('varchar'):
        return 'String', 'String(%d)' % length
    elif data_type == 'datetime' or data_type.startswith('timestamp'):
        return 'DateTime', 'DateTime'
    elif data_type == 'date' or data_type.startswith('timestamp'):
        return 'Date', 'Date'
    elif data_type == 'time' or data_type.startswith('timestamp'):
        return 'Time', 'Time'
    elif data_type == 'blob' or data_type == 'longblob':
        return 'BLOB', 'BLOB'
    elif data_type.startswith('tinyint') or data_type.startswith(
            'smallint') or data_type == 'boolean':
        return 'Boolean', 'Boolean'
    elif data_type == 'text':
        return 'Text', 'Text'
    elif data_type.startswith('decimal'):
        return 'DECIMAL', 'DECIMAL'
    elif data_type.startswith('double'):
        return 'Float', 'Float'
    else:
        raise Exception('不支持的数据类型%s' % data_type)


def database_type_to_pydantic_type(data_type, length=None):
    if data_type.startswith('int') or data_type == 'integer':
        return 'int', 'int'
    elif data_type.startswith('bigint'):
        return 'int', 'int'
    elif data_type.startswith('varchar') or data_type == 'varchar':
        return 'constr', f'constr(max_length={length})' if length else 'constr'
    elif data_type == 'text':
        return 'str', 'str'
    elif data_type == 'datetime' or data_type.startswith('timestamp'):
        return 'str', 'str'
    elif data_type == 'date' or data_type.startswith('timestamp'):
        # Pydantic does not have a dedicated Date type, using string as an example.
        return 'str', 'str'
    elif data_type == 'time' or data_type.startswith('timestamp'):
        # Similarly, for time, we can use a string representation.
        return 'str', 'str'
    elif data_type == 'blob' or data_type == 'longblob':
        # Depending on use case, this could be a byte type or a string (hex encoded).
        return 'bytes', 'bytes'
    elif data_type.startswith('tinyint') or data_type.startswith('smallint') or data_type == 'boolean':
        return 'bool', 'bool'
    elif data_type.startswith('decimal'):
        # Assuming fixed precision and scale could be defined based on the actual column definition.
        return 'float', 'float'  # Simplified for illustration; Pydantic doesn't have a Decimal type out of the box.
    elif data_type.startswith('double'):
        return 'float', 'float'
    else:
        raise ValueError(f'unsupported data type {data_type}.')
