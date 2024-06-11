# noinspection DuplicatedCode
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
            sel_stmt: str = (f"SELECT table_name "
                             f"FROM all_tables")
            if schema:
                sel_stmt += f" WHERE owner = '{schema.upper()}'"
        else:
            sel_stmt: str = ("SELECT table_name "
                             "FROM information_schema.tables "
                             f"WHERE table_type = 'BASE TABLE'")
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
            sel_stmt: str = (f"SELECT COUNT(*) "
                             f"FROM all_tables "
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
                 engine: str = None,
                 connection: Any = None,
                 committable: bool = True,
                 logger: Logger = None) -> list[str]:
    """
    Retrieve and return the list of views in the database.

    :param errors: incidental error messages
    :param schema: optional name of the schema to restrict the search to
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
            sel_stmt: str = f"SELECT view_name FROM all_views"
            if schema:
                sel_stmt += f" WHERE owner = '{schema.upper()}'"
        else:
            sel_stmt: str = ("SELECT table_name "
                             "FROM information_schema.tables "
                             f"WHERE table_type = 'VIEW'")
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
            sel_stmt: str = (f"SELECT COUNT(*) "
                             f"FROM all_views "
                             f"WHERE view_name = '{view_name.upper()}'")
            if schema:
                sel_stmt += f" AND owner = '{schema.upper()}'"
        else:
            sel_stmt: str = ("SELECT COUNT(*) "
                             "FROM information_schema.tables "
                             f"WHERE table_type = 'VIEW' AND LOWER(table_name) = '{view_name.lower()}'")
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
    Retrieve and return the names of the tables *view_name* depends upon.

    :param errors: incidental error messages
    :param view_name: the name of the view
    :param schema: optional name of the schema to restrict the search to
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
            sel_stmt: str = (f"SELECT text "
                             f"FROM all_views "
                             f"WHERE view_name = '{view_name.upper()}'")
            if schema:
                sel_stmt += f" AND owner = '{schema.upper()}'"
        else:
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
            result = recs[0][0]

    # acknowledge eventual local errors, if appropriate
    if isinstance(errors, list):
        errors.extend(op_errors)

    return result
