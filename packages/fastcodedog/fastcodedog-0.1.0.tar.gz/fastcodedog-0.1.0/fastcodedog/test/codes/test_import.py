# -*- coding: utf-8 -*-

from fastcodedog.generation.import_stmt import ImportStmt


def test_import():
    import_stmt = ImportStmt()
    import_stmt.add_import('fastcodedog.stmt.import_stmt', '_ImportExpression', '_I')
    import_stmt.add_import('fastcodedog.stmt.import_stmt', '_FromExpression', '_F')
    import_stmt.add_import('fastcodedog.stmt.import_stmt', 'ImportStmt')
    import_stmt.add_import(None, 'pandas', 'pd')
    print('\n')
    print(import_stmt.serialize('    '))
