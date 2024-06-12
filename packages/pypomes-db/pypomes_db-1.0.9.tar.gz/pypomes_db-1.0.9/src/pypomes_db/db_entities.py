from logging import Logger
from typing import Any

from .db_pomes import db_select
from .db_common import _assert_engine


def db_get_tables(errors: list[str],
                  schema: str = None,
                  engine: str = None,
                  connection: Any = None,
                  committable: bool = True,
                  logger: Logger = None) -> list[str]:
    """
    Retrieve and return the list of tables in the database.

    :param errors: incidental error messages
    :param schema: optional name of the schema to restrict the search to
    :param engine: the database engine to use (uses the default engine, if not provided)
    :param connection: optional connection to use (obtains a new one, if not provided)
    :param committable: whether to commit upon errorless completion ('False' requires 'connection' to be provided)
    :param logger: optional logger
    :return: the tables was found, or 'None' if an error ocurred
    """
    #initialize the return variable
    result: list[str] | None = None

    # initialize the local errors list
    op_errors: list[str] = []

    # determine the database engine
    curr_engine: str = _assert_engine(errors=op_errors,
                                      engine=engine)

    # proceed, if no errors
    if not op_errors:
        # build the query
        if curr_engine == "oracle":
            sel_stmt: str = "SELECT table_name FROM all_tables"
            if schema:
                sel_stmt += f" WHERE owner = '{schema.upper()}'"
        else:
            sel_stmt: str = ("SELECT table_name "
                             "FROM information_schema.tables "
                             "WHERE table_type = 'BASE TABLE'")
            if schema:
                sel_stmt += f" AND LOWER(table_schema) = '{schema.lower()}'"

        # execute the query
        recs: list[tuple[str]] = db_select(errors=op_errors,
                                           sel_stmt=sel_stmt,
                                           engine=curr_engine,
                                           connection=connection,
                                           committable=committable,
                                           logger=logger)
        # process the query result
        if not op_errors:
            result = [rec[0] for rec in recs]

    # acknowledge eventual local errors, if appropriate
    if isinstance(errors, list):
        errors.extend(op_errors)

    return result


def db_has_table(errors: list[str],
                 table_name: str,
                 schema: str = None,
                 engine: str = None,
                 connection: Any = None,
                 committable: bool = True,
                 logger: Logger = None) -> bool:
    """
    Determine whether the table *table_name* exists in the database.

    :param errors: incidental error messages
    :param table_name: the name of the table to look for
    :param schema: optional name of the schema to restrict the search to
    :param engine: the database engine to use (uses the default engine, if not provided)
    :param connection: optional connection to use (obtains a new one, if not provided)
    :param committable: whether to commit upon errorless completion ('False' requires 'connection' to be provided)
    :param logger: optional logger
    :return: the views found, or 'None' if an error ocurred
    """
    #initialize the return variable
    result: bool | None = None

    # initialize the local errors list
    op_errors: list[str] = []

    # determine the database engine
    curr_engine: str = _assert_engine(errors=op_errors,
                                      engine=engine)

    # proceed, if no errors
    if not op_errors:
        # build the query
        if curr_engine == "oracle":
            sel_stmt: str = ("SELECT COUNT(*) FROM all_tables "
                             f"WHERE table_name = '{table_name.upper()}'")
            if schema:
                sel_stmt += f" AND owner = '{schema.upper()}'"
        else:
            sel_stmt: str = ("SELECT COUNT(*) "
                             "FROM information_schema.tables "
                             f"WHERE table_type = 'BASE TABLE' AND LOWER(table_name) = '{table_name.lower()}'")
            if schema:
                sel_stmt += f" AND LOWER(table_schema) = '{schema.lower()}'"

        # execute the query
        reply: list[tuple[int]] = db_select(errors=op_errors,
                                            sel_stmt=sel_stmt,
                                            engine=curr_engine,
                                            connection=connection,
                                            committable=committable,
                                             logger=logger)
        # process the query result
        if not op_errors:
            result = reply[0][0] > 0

    # acknowledge eventual local errors, if appropriate
    if isinstance(errors, list):
        errors.extend(op_errors)

    return result


def db_get_views(errors: list[str],
                 schema: str = None,
                 tables: list[str] = None,
                 engine: str = None,
                 connection: Any = None,
                 committable: bool = True,
                 logger: Logger = None) -> list[str]:
    """
    Retrieve and return the list of views in the database.
    If a list of table names in provided in *tables*, then only the views whose table
    dependencies are all included therein ae returned

    :param errors: incidental error messages
    :param schema: optional name of the schema to restrict the search to
    :param tables: optional list of tables containing all views' dependencies
    :param engine: the database engine to use (uses the default engine, if not provided)
    :param connection: optional connection to use (obtains a new one, if not provided)
    :param committable: whether to commit upon errorless completion ('False' requires 'connection' to be provided)
    :param logger: optional logger
    :return: 'True' if the table was found, 'False' otherwise, 'None' if an error ocurred
    """
    #initialize the return variable
    result: list[str] | None = None

    # initialize the local errors list
    op_errors: list[str] = []

    # determine the database engine
    curr_engine: str = _assert_engine(errors=op_errors,
                                      engine=engine)

    # proceed, if no errors
    if not op_errors:
        # build the query
        if curr_engine == "oracle":
            sel_stmt: str = "SELECT view_name FROM all_views"
            if schema:
                sel_stmt += f" WHERE owner = '{schema.upper()}'"
        else:
            sel_stmt: str = ("SELECT table_name "
                             "FROM information_schema.views")
            if schema:
                sel_stmt += f" WHERE LOWER(table_schema) = '{schema.lower()}'"

        # execute the query
        recs: list[tuple[str]] = db_select(errors=op_errors,
                                           sel_stmt=sel_stmt,
                                           engine=curr_engine,
                                           connection=connection,
                                           committable=committable,
                                           logger=logger)
        # process the query result
        if not op_errors:
            result = [rec[0] for rec in recs]

    # acknowledge eventual local errors, if appropriate
    if isinstance(errors, list):
        errors.extend(op_errors)

    # omit views with dependencies not in 'tables', if applicable
    if result and tables:
        omitted_views: list[str] = []
        for view in result:
            dependencies: list[str] = \
                db_get_view_dependencies(errors=errors,
                                         view_name=view,
                                         schema=schema,
                                         engine=engine,
                                         connection=connection,
                                         committable=committable,
                                         logger=logger)
            for dependency in dependencies:
                if dependency not in tables:
                    omitted_views.append(view)
                    break
        for omitted_view in omitted_views:
            result.remove(omitted_view)

    return result


def db_has_view(errors: list[str],
                view_name: str,
                schema: str = None,
                engine: str = None,
                connection: Any = None,
                committable: bool = True,
                logger: Logger = None) -> bool:
    """
    Determine whether the view *view_name* exists in the database.

    :param errors: incidental error messages
    :param view_name: the name of the view to look for
    :param schema: optional name of the schema to restrict the search to
    :param engine: the database engine to use (uses the default engine, if not provided)
    :param connection: optional connection to use (obtains a new one, if not provided)
    :param committable: whether to commit upon errorless completion ('False' requires 'connection' to be provided)
    :param logger: optional logger
    :return: 'True' if the view was found, 'False' otherwise, 'None' if an error ocurred
    """
    #initialize the return variable
    result: bool | None = None

    # initialize the local errors list
    op_errors: list[str] = []

    # determine the database engine
    curr_engine: str = _assert_engine(errors=op_errors,
                                      engine=engine)

    # proceed, if no errors
    if not op_errors:
        # build the query
        if curr_engine == "oracle":
            sel_stmt: str = ("SELECT COUNT(*) FROM all_views "
                             f"WHERE view_name = '{view_name.upper()}'")
            if schema:
                sel_stmt += f" AND owner = '{schema.upper()}'"
        else:
            sel_stmt: str = ("SELECT COUNT(*) "
                             "FROM information_schema.views "
                             f"WHERE LOWER(table_name) = '{view_name.lower()}'")
            if schema:
                sel_stmt += f" AND LOWER(table_schema) = '{schema.lower()}'"

        # execute the query
        recs: list[tuple[int]] = db_select(errors=op_errors,
                                           sel_stmt=sel_stmt,
                                           engine=curr_engine,
                                           connection=connection,
                                           committable=committable,
                                           logger=logger)
        # process the query result
        if not op_errors:
            result = recs[0][0] > 0

    # acknowledge eventual local errors, if appropriate
    if isinstance(errors, list):
        errors.extend(op_errors)

    return result


def db_get_view_dependencies(errors: list[str],
                             view_name: str,
                             schema: str = None,
                             engine: str = None,
                             connection: Any = None,
                             committable: bool = True,
                             logger: Logger = None) -> list[str]:
    """
    Retrieve and return the names of the tables *view_name* depends on.

    :param errors: incidental error messages
    :param view_name: the name of the view
    :param schema: optional name of the schema to restrict the search to
    :param engine: the database engine to use (uses the default engine, if not provided)
    :param connection: optional connection to use (obtains a new one, if not provided)
    :param committable: whether to commit upon errorless completion ('False' requires 'connection' to be provided)
    :param logger: optional logger
    :return: The tables the view depends on, or 'None' if an error ocurred
    """
    #initialize the return variable
    result: list[str] | None = None

    # initialize the local errors list
    op_errors: list[str] = []

    # determine the database engine
    curr_engine: str = _assert_engine(errors=op_errors,
                                      engine=engine)

    # proceed, if no errors
    if not op_errors:
        # build the query
        sel_stmt: str | None = None
        match engine:
            case "mysql":
                pass
            case "oracle":
                sel_stmt = ("SELECT DISTINCT referenced_name "
                            "FROM all_dependencies "
                            f"WHERE name = '{view_name.upper()}'"
                            "AND type = 'VIEW' AND referenced_type = 'TABLE'")
                if schema:
                    sel_stmt += f" AND owner = '{schema.upper()}'"
            case "postgres":
                sel_stmt = ("SELECT DISTINCT cl1.relname "
                            "FROM pg_class AS cl1 "
                            "JOIN pg_rewrite AS rw ON rw.ev_class = cl1.oid "
                            "JOIN pg_depend AS d ON d.objid = rw.oid "
                            "JOIN pg_class AS cl2 ON cl2.oid = d.refobjid "
                            f"WHERE LOWER(cl2.relname) = '{view_name.lower()}'")
                if schema:
                    sel_stmt += (" AND cl2.relnamespace = "
                                 f"(SELECT oid FROM pg_namespace "
                                 f"WHERE LOWER(nspname) = '{schema.lower()}')")
            case "sqlserver":
                sel_stmt = ("SELECT DISTINCT referencing_entity_name "
                            f"FROM sys.dm_sql_referencing_entities ('{view_name.lower()}', 'OBJECT') ")
                if schema:
                    sel_stmt += f" WHERE LOWER(referencing_schema_name) = '{schema.lower()}'"

        # execute the query
        recs: list[tuple[str]] = db_select(errors=op_errors,
                                           sel_stmt=sel_stmt,
                                           engine=curr_engine,
                                           connection=connection,
                                           committable=committable,
                                           logger=logger)
        # process the query result
        if not op_errors:
            result = [rec[0] for rec in recs]

    # acknowledge eventual local errors, if appropriate
    if isinstance(errors, list):
        errors.extend(op_errors)

    return result


def db_get_view_script(errors: list[str],
                       view_name: str,
                       schema: str = None,
                       engine: str = None,
                       connection: Any = None,
                       committable: bool = True,
                       logger: Logger = None) -> str:
    """
    Retrieve and return the SQL script used to create the view *view_name*.

    :param errors: incidental error messages
    :param view_name: the name of the view
    :param schema: optional name of the schema to restrict the search to
    :param engine: the database engine to use (uses the default engine, if not provided)
    :param connection: optional connection to use (obtains a new one, if not provided)
    :param committable: whether to commit upon errorless completion ('False' requires 'connection' to be provided)
    :param logger: optional logger
    :return: The SQL script used to create the view, or 'None' if the view does not exist, or an error ocurred
    """
    #initialize the return variable
    result: str | None = None

    # initialize the local errors list
    op_errors: list[str] = []

    # determine the database engine
    curr_engine: str = _assert_engine(errors=op_errors,
                                      engine=engine)

    # proceed, if no errors
    if not op_errors:
        # build the query
        if curr_engine == "oracle":
            prefix: str = f"CREATE VIEW {view_name.upper()} AS "
            sel_stmt: str = ("SELECT text FROM all_views "
                             f"WHERE view_name = '{view_name.upper()}'")
            if schema:
                sel_stmt += f" AND owner = '{schema.upper()}'"
        else:
            prefix: str = ""
            sel_stmt: str = ("SELECT view_definition "
                             "FROM information_schema.views "
                             f"WHERE LOWER(table_name) = '{view_name.lower()}'")
            if schema:
                sel_stmt += f" AND LOWER(table_schema) = '{schema.lower()}'"

        # execute the query
        recs: list[tuple[str]] = db_select(errors=op_errors,
                                           sel_stmt=sel_stmt,
                                           engine=curr_engine,
                                           connection=connection,
                                           committable=committable,
                                           logger=logger)
        # process the query result
        if not op_errors and recs:
            result = prefix + recs[0][0]

    # acknowledge eventual local errors, if applicable
    if isinstance(errors, list):
        errors.extend(op_errors)

    return result


def db_get_indexes(errors: list[str],
                   schema: str = None,
                   omit_pks: bool = True,
                   tables: list[str] = None,
                   engine: str = None,
                   connection: Any = None,
                   committable: bool = True,
                   logger: Logger = None) -> list[str]:
    """
    Retrieve and return the list of indexes in the database.

    If the list of table names *tables* is provided,
    only the indexes created on any of these tables' columns are returned.
    If *omit_pks* is set to 'True' (its default value),
    indexes created on primary key columns will not be included.

    :param errors: incidental error messages
    :param schema: optional name of the schema to restrict the search to
    :param omit_pks: omit indexes on primary key columns (defaults to 'True')
    :param tables: optional list of tables whose columns the indexes were created on
    :param engine: the database engine to use (uses the default engine, if not provided)
    :param connection: optional connection to use (obtains a new one, if not provided)
    :param committable: whether to commit upon errorless completion ('False' requires 'connection' to be provided)
    :param logger: optional logger
    :return: 'True' if the table was found, 'False' otherwise, 'None' if an error ocurred
    """
    #initialize the return variable
    result: list[str] | None = None

    # initialize the local errors list
    op_errors: list[str] = []

    # determine the database engine
    curr_engine: str = _assert_engine(errors=op_errors,
                                      engine=engine)

    # proceed, if no errors
    if not op_errors:
        # build the query
        sel_stmt: str | None = None
        match curr_engine:
            case "mysql":
                pass
            case "oracle":
                sel_stmt: str = "SELECT ai.index_name FROM all_indexes ai "
                if omit_pks:
                    sel_stmt += ("INNER JOIN all_ind_columns aic ON ai.index_name = aic.index_name "
                                 "INNER JOIN all_cons_columns acc "
                                 "ON aic.table_name = acc.table_name AND aic.column_name = acc.column_name "
                                 "INNER JOIN all_constraints ac "
                                 "ON acc.constraint_name = ac.constraint_name AND ac.constraint_type != 'P' ")
                sel_stmt += "WHERE ai.dropped = 'NO' AND "
                if schema:
                    sel_stmt += f"owner = '{schema.upper()}' AND "
                if tables:
                    in_tables: str = "','".join(tables)
                    sel_stmt += f"table_name IN ('{in_tables.upper()}') AND "
                sel_stmt = sel_stmt[:-5]
            case "postgres":
                sel_stmt: str = ("SELECT i.relname FROM pg_class t "
                                 "INNER JOIN pg_namespace ns ON ns.oid = t.relnamespace "
                                 "INNER JOIN pg_index ix ON ix.indrelid = t.oid "
                                 "INNER JOIN pg_class i ON i.oid = ix.indexrelid ")
                if omit_pks or schema or tables:
                    sel_stmt += " WHERE "
                    if omit_pks:
                        sel_stmt += "ix.indisprimary = false AND "
                    if schema:
                        sel_stmt += f"LOWER(ns.nspname) = '{schema.lower()}' AND "
                    if tables:
                        in_tables: str = "','".join(tables)
                        sel_stmt += f"LOWER(t.relname) IN ('{in_tables.lower()}') AND "
                    sel_stmt = sel_stmt[:-5]
            case "sqlserver":
                sel_stmt = ("SELECT i.name FROM sys.tables t "
                            "INNER JOIN sys.indexes i ON i.object_id = t.object_id")
                if omit_pks or schema or tables:
                    sel_stmt += " WHERE "
                    if omit_pks:
                        sel_stmt += "i.is_primary_key = 0 AND "
                    if schema:
                        sel_stmt += f"SCHEMA_NAME(t.schema_id) = '{schema.lower()}' AND "
                    if tables:
                        in_tables: str = "','".join(tables)
                        sel_stmt += f"LOWER(t.name) IN ('{in_tables.lower()}') AND "
                    sel_stmt = sel_stmt[:-5]

        # execute the query
        recs: list[tuple[str]] = db_select(errors=op_errors,
                                           sel_stmt=sel_stmt,
                                           engine=curr_engine,
                                           connection=connection,
                                           committable=committable,
                                           logger=logger)
        # process the query result
        if not op_errors:
            result = [rec[0] for rec in recs]

    # acknowledge eventual local errors, if appropriate
    if isinstance(errors, list):
        errors.extend(op_errors)

    return result
