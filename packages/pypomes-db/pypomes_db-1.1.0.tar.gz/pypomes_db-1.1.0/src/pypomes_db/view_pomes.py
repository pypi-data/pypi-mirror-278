from logging import Logger
from typing import Any, Literal

from .db_pomes import db_select
from .db_common import _assert_engine


def db_get_views(errors: list[str],
                 view_type: Literal["S", "M"] = "S",
                 schema: str = None,
                 tables: list[str] = None,
                 engine: str = None,
                 connection: Any = None,
                 committable: bool = True,
                 logger: Logger = None) -> list[str]:
    """
    Retrieve and return the list of views in the database.

    The returned view names will be qualified with the schema they belong to.
    If a list of, possibly schema-qualified, table names is provided in *tables*, then only
    the views whose table dependencies are all included therein are returned.

    :param errors: incidental error messages
    :param view_type: the type of views to search for ("S": standard; "M": materialized, defaults to "S")
    :param schema: optional name of the schema to restrict the search to
    :param tables: optional list of, possibly schema-qualified, table names containing all views' dependencies
    :param engine: the database engine to use (uses the default engine, if not provided)
    :param connection: optional connection to use (obtains a new one, if not provided)
    :param committable: whether to commit upon errorless completion ('False' requires 'connection' to be provided)
    :param logger: optional logger
    :return: The schema-qualified views found, or 'None' if an error ocurred
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
            target: str = "all_mviews" if view_type == "M" else "all_views"
            sel_stmt: str = f"SELECT owner || '.' || view_name FROM {target}"
            if schema:
                sel_stmt += f" WHERE owner = '{schema.upper()}'"
        elif view_type == "M":  # materialized views
            if curr_engine == "postgres":
                sel_stmt = "SELECT schemaname || '.' || matviewname FROM pg_matview "
                if schema:
                    sel_stmt += f" WHERE LOWER(schemaname) = {schema}"
            else:  # sqlserver
                sel_stmt = ("SELECT SCHEMA_NAME(v.schema_id) || '.' || table_name FROM sys.views v "
                            "INNER JOIN sys.indexes i ON i.object_id - v.object_id "
                            f"WHERE i.index_id < 2")
                if schema:
                    sel_stmt +=  f" AND LOWER(SCHEMA_NAME(v.schema_id)) = {schema.lower()}"
        else:  # standard views
            sel_stmt: str = ("SELECT table_schema || '.' || table_name "
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
        for view_name in result:
            dependencies: list[str] = \
                db_get_view_dependencies(errors=errors,
                                         view_name=view_name,
                                         engine=engine,
                                         connection=connection,
                                         committable=committable,
                                         logger=logger)
            for dependency in dependencies:
                if dependency not in tables:
                    omitted_views.append(view_name)
                    break
        for omitted_view in omitted_views:
            result.remove(omitted_view)

    return result


def db_has_view(errors: list[str],
                view_name: str,
                view_type: Literal["S", "M"] = "S",
                engine: str = None,
                connection: Any = None,
                committable: bool = True,
                logger: Logger = None) -> bool:
    """
    Determine whether the view *view_name* exists in the database.

    If *view_name* is schema-qualified, then the search will be restricted to that schema.

    :param errors: incidental error messages
    :param view_name: the name of the view to look for
    :param view_type: the type of view to search for ("S": standard; "M": materialized, defaults to "S")
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
        # extract the schema, if possible
        schema_name: str | None = None
        splits: list[str] = view_name.split(".")
        if len(splits) > 1:
            schema_name = splits[0]
            view_name = splits[1]

        # build the query
        sel_stmt: str
        if curr_engine == "oracle":
            target: str = "all_mviews" if view_type == "M" else "all_views"
            sel_stmt = (f"SELECT COUNT(*) FROM {target} "
                        f"WHERE view_name = '{view_name.upper()}'")
            if schema_name:
                sel_stmt += f" AND owner = '{schema_name.upper()}'"
        elif view_type == "M":  # materialized views
            if curr_engine == "postgres":
                sel_stmt = ("SELECT COUNT(*) FROM pg_matview "
                            f"WHERE LOWER(matviewname) = '{view_name.lower()}'")
                if schema_name:
                    sel_stmt += f" AND LOWER(schemaname) = {schema_name.lower()}"
            else:  # sqlserver
                sel_stmt = ("SELECT COUNT(*) FROM sys.views v "
                            "INNER JOIN sys.indexes i ON i.object_id - v.object_id "
                            f"WHERE i.index_id < 2 AND LOWER(table_name) = {view_name.lower()}")
                if schema_name:
                    sel_stmt +=  f" AND LOWER(SCHEMA_NAME(v.schema_id)) = {schema_name.lower()}"
        else:  # standard views (postgres, sqlserver)
            sel_stmt = ("SELECT COUNT(*) "
                        "FROM information_schema.views "
                        f"WHERE LOWER(table_name) = '{view_name.lower()}'")
            if schema_name:
                sel_stmt += f" AND LOWER(table_schema) = '{schema_name.lower()}'"

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
                             view_type: Literal["S", "M"] = "S",
                             engine: str = None,
                             connection: Any = None,
                             committable: bool = True,
                             logger: Logger = None) -> list[str]:
    """
    Retrieve and return the names of the tables *view_name* depends on.

    If *view_name* is schema-qualified, then the search will be restricted to the view in that schema.
    The returned table names will be qualified with the schema they belong to.

    :param errors: incidental error messages
    :param view_name: the name of the view
    :param view_type: the type of the view ("S": standard; "M": materialized, defaults to "S")
    :param engine: the database engine to use (uses the default engine, if not provided)
    :param connection: optional connection to use (obtains a new one, if not provided)
    :param committable: whether to commit upon errorless completion ('False' requires 'connection' to be provided)
    :param logger: optional logger
    :return: The schema-qualified tables the view depends on, or 'None' if an error ocurred
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
        # extract the schema, if possible
        schema_name: str | None = None
        splits: list[str] = view_name.split(".")
        if len(splits) > 1:
            schema_name = splits[0]
            view_name = splits[1]

        # build the query
        sel_stmt: str | None = None
        match engine:
            case "mysql":
                pass
            case "oracle":
                vw_type: str = "MATERIALIZED VIEW" if view_type == "M" else "VIEW"
                sel_stmt = ("SELECT DISTINCT referenced_owner || '.' || referenced_name "
                            "FROM all_dependencies "
                            f"WHERE name = '{view_name.upper()}'"
                            f"AND type = '{vw_type}' AND referenced_type = 'TABLE'")
                if schema_name:
                    sel_stmt += f" AND owner = '{schema_name.upper()}'"
            case "postgres":
                sel_stmt = ("SELECT DISTINCT nsp.nspname || '.' || cl1.relname "
                            "FROM pg_class AS cl1 "
                            "INNER JOIN pg_namespace AS nsp ON nsp.oid = cl1.relnamespace "
                            "INNER JOIN pg_rewrite AS rw ON rw.ev_class = cl1.oid "
                            "INNER JOIN pg_depend AS d ON d.objid = rw.oid "
                            "INNER JOIN pg_class AS cl2 ON cl2.oid = d.refobjid "
                            f"WHERE LOWER(cl2.relname) = '{view_name.lower()}'")
                if view_type == "M":
                    sel_stmt += " AND cl2.relkind = 'm'"
                if schema_name:
                    sel_stmt += (" AND cl2.relnamespace = "
                                 f"(SELECT oid FROM pg_namespace "
                                 f"WHERE LOWER(nspname) = '{schema_name.lower()}')")
            case "sqlserver":
                entity: str = view_name.lower()
                if schema_name:
                    entity = schema_name.lower() + "." + entity
                sel_stmt = ("SELECT DISTINCT s.name || '.' || re.referencing_entity_name "
                            f"FROM sys.dm_sql_referencing_entities ('{entity}', 'OBJECT') as re "
                            "INNER JOIN sys.objects AS o ON o.object_id = re.referencing_id "
                            "INNER JOIN sys.schemas AS s ON s.schema_id = o.schema_id")
                if schema_name:
                    sel_stmt += f" WHERE LOWER(referencing_schema_name) = '{schema_name.lower()}'"

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
