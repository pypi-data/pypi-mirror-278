"""
Ocient SQLAlchemy Dialect
"""

import collections.abc as collections_abc
import logging
import urllib

from sqlalchemy import pool
from sqlalchemy import types
from sqlalchemy import types as sqltypes
from sqlalchemy import util
from sqlalchemy.engine import default, interfaces, reflection
from sqlalchemy.sql import compiler, elements
from sqlalchemy.types import BIGINT, BINARY, BOOLEAN, CHAR, DATE, FLOAT, INTEGER, SMALLINT, TIME, TIMESTAMP, VARCHAR

import pyocient

try:
    from version import __version__  # gazelle:ignore version.__version__

    version = __version__
except ImportError:
    version = "1.0.0"

logger = logging.getLogger("sqlalchemy_ocient")


class OcientType(types.TypeEngine):
    pass


class IP(OcientType):
    __visit_name__ = "IP"


class IPV4(OcientType):
    __visit_name__ = "IPV4"


class HASH(OcientType):
    __visit_name__ = "HASH"


class DECIMAL(OcientType):
    __visit_name__ = "DECIMAL"


class DOUBLE(OcientType):
    __visit_name__ = "DOUBLE"


class POINT(OcientType):
    __visit_name__ = "POINT"


class LINESTRING(OcientType):
    __visit_name__ = "LINESTRING"


class POLYGON(OcientType):
    __visit_name__ = "POLYGON"


class BYTE(OcientType):
    __visit_name__ = "BYTE"


class UUID(OcientType):
    __visit_name__ = "UUID"


class ARRAY(OcientType):
    __visit_name__ = "ARRAY"


class TUPLE(OcientType):
    __visit_name__ = "TUPLE"


class OcientExecutionContext(default.DefaultExecutionContext):
    pass


class OcientCompiler(compiler.SQLCompiler):
    extract_map = compiler.SQLCompiler.extract_map.copy()
    extract_map.update(
        {
            "month": "m",
            "day": "d",
            "year": "yyyy",
            "second": "s",
            "hour": "h",
            "doy": "y",
            "minute": "n",
            "quarter": "q",
            "dow": "w",
            "week": "ww",
        }
    )

    def _literal_execute_expanding_parameter(self, name, parameter, values):
        """
        This is a hack, and we need to have a stern word with the sqlalchemy people
        about it.  We can't override the processing of tuples easily. Alternatively,
        we really should treat (a, b, c) as a tuple by default in the Ocient DB in the
        right contexts

        This is heavily motivated by the function of the same name in sqlalchemy's
        compiler.py
        """
        if parameter.type._is_tuple_type or (
            parameter.type._isnull
            and len(values) > 0
            and isinstance(values[0], collections_abc.Sequence)
            and not isinstance(values[0], (str, bytes))
        ):
            assert not parameter.type._is_array
            to_update = [
                ("%s_%s_%s" % (name, i, j), value)
                for i, tuple_element in enumerate(values, 1)
                for j, value in enumerate(tuple_element, 1)
            ]

            replacement_expression = ", ".join(
                "tuple(%s)"
                % (
                    ", ".join(
                        self.compilation_bindtemplate % {"name": to_update[i * len(tuple_element) + j][0]}
                        for j, value in enumerate(tuple_element)
                    )
                )
                for i, tuple_element in enumerate(values)
            )

            return to_update, replacement_expression
        else:
            return super()._literal_execute_expanding_parameter(name, parameter, values)

    def limit_clause(self, select, **kw):
        text = ""
        if select._limit_clause is not None:
            text += "\n LIMIT " + self.process(select._limit_clause, **kw)
        if select._offset_clause is not None:
            text += " OFFSET " + self.process(select._offset_clause, **kw)
        return text

    def visit_binary(self, binary, override_operator=None, eager_grouping=False, **kw):
        return super(OcientCompiler, self).visit_binary(
            binary,
            override_operator=override_operator,
            eager_grouping=eager_grouping,
            **kw,
        )

    def for_update_clause(self, select):
        """FOR UPDATE is not supported by Ocient; silently ignore"""
        return ""

    def visit_column(self, column, add_to_result_map=None, include_table=True, **kwargs):
        name = orig_name = column.name
        if name is None:
            name = self._fallback_column_name(column)

        is_literal = column.is_literal
        if not is_literal and isinstance(name, elements._truncated_label):
            name = self._truncated_identifier("colident", name)

        if add_to_result_map is not None:
            add_to_result_map(name, orig_name, (column, name, column.key), column.type)

        if is_literal:
            name = self.escape_literal_column(name)
        else:
            name = self.preparer.quote(name)
        table = column.table
        if table is None or not include_table or not table.named_with_column:
            return name
        else:
            effective_schema = self.preparer.schema_for_object(table)
            schema_prefix = ""
            tablename = table.name
            if isinstance(tablename, elements._truncated_label):
                tablename = self._truncated_identifier("alias", tablename)

            return schema_prefix + self.preparer.quote(tablename) + "." + name

    def visit_tuple(self, clauselist, **kw):
        return "tuple(%s)" % self.visit_clauselist(clauselist, **kw)

    def visit_join(self, join, asfrom=False, **kwargs):
        return (
            "("
            + self.process(join.left, asfrom=True)
            + (join.isouter and " LEFT OUTER JOIN " or " INNER JOIN ")
            + self.process(join.right, asfrom=True)
            + " ON "
            + self.process(join.onclause)
            + ")"
        )

    def visit_extract(self, extract, **kw):
        field = self.extract_map.get(extract.field, extract.field)
        return 'DATEPART("%s", %s)' % (field, self.process(extract.expr, **kw))


class OcientDDLCompiler(compiler.DDLCompiler):
    def visit_primary_key_constraint(self, constraint, **kw):
        """Ocient DB doesn't support primary key.  Turn them into
        clustering keys for now (the semantics
        are totally different of course)
        """
        if len(constraint) == 0:
            return ""
        text = "KEY "
        if constraint.name is not None:
            formatted_name = self.preparer.format_constraint(constraint)
        else:
            formatted_name = "pk_idx"

        text = "CLUSTERING KEY %s" % formatted_name
        text += "(%s) -- pk" % ", ".join(
            self.preparer.quote(c.name)
            for c in (constraint.columns_autoinc_first if constraint._implicit_generated else constraint.columns)
        )

        return text

    def visit_foreign_key_constraint(self, constraint, **kw):
        return "-- fk"


class OcientTypeCompiler(compiler.GenericTypeCompiler):
    def visit_BOOLEAN(self, type_, **kw):
        return "BOOLEAN"

    def visit_INT(self, type_, **kw):
        return "INT"

    def visit_INT8(self, type_, **kw):
        return "INT8"

    def visit_INT16(self, type_, **kw):
        return "INT16"

    def visit_INT32(self, type_, **kw):
        return "INT32"

    def visit_INT64(self, type_, **kw):
        return "INT64"

    def visit_SHORT(self, type_, **kw):
        return "SHORT"

    def visit_LONG(self, type_, **kw):
        return "LONG"

    def visit_FLOAT(self, type_, **kw):
        return "FLOAT"

    def visit_DOUBLE(self, type_, **kw):
        return "DOUBLE"

    def visit_FLOAT32(self, type_, **kw):
        return "FLOAT32"

    def visit_FLOAT64(self, type_, **kw):
        return "FLOAT64"

    def visit_BLOB(self, type_, **kw):
        return "BLOB"

    def visit_IPV4(self, type_, **kw):
        return "IPV4"

    def visit_UUID(self, type_, **kw):
        return "UUID"

    def visit_HASH(self, type_, **kw):
        return "HASH"


ischema_names = {
    "BIGINT": BIGINT,
    "LONG": BIGINT,
    "BINARY": BINARY,
    "HASH": HASH,
    "BOOLEAN": BOOLEAN,
    "CHARACTER": CHAR,
    "CHAR": CHAR,
    "DATE": DATE,
    "DECIMAL": DECIMAL,
    "DOUBLE PRECISION": DOUBLE,
    "DOUBLE": DOUBLE,
    "INT": INTEGER,
    "IPV4": IPV4,
    "IP": IP,
    "POINT": POINT,
    "ST_POINT": POINT,
    "LINESTRING": LINESTRING,
    "ST_LINESTRING": LINESTRING,
    "POLYGON": POLYGON,
    "ST_POLYGON": POLYGON,
    "REAL": FLOAT,
    "FLOAT": FLOAT,
    "SINGLE PRECISION": FLOAT,
    "SMALLINT": SMALLINT,
    "SHORT": SMALLINT,
    "TIME": TIME,
    "TIMESTAMP": TIMESTAMP,
    "TINYINT": BYTE,
    "BYTE": BYTE,
    "UUID": UUID,
}

mutable_types = {
    "ARRAY": ARRAY,
    "TUPLE": TUPLE,
    "HASH": HASH,
    "ST_POINT": POINT,
}


class OcientIdentifierPreparer(compiler.IdentifierPreparer):
    # It would be nice to get this at runtime from sys.reserved_words
    # This was retrieved from v24
    reserved_words = {
        "add",
        "all",
        "alter",
        "and",
        "anti",
        "any",
        "array",
        "as",
        "bad_data_target",
        "balance",
        "between",
        "cache",
        "call",
        "cancel",
        "case",
        "cast",
        "check",
        "class",
        "clustering",
        "column",
        "colvector",
        "comment",
        "compression",
        "connectivity_pool",
        "count",
        "create",
        "cross",
        "current",
        "current_database",
        "current_date",
        "current_schema",
        "current_time",
        "current_timestamp",
        "current_user",
        "data",
        "database",
        "default",
        "delete",
        "disable",
        "disable_stats_file_updates",
        "distinct",
        "drop",
        "else",
        "enable",
        "enable_stats_file_updates",
        "end",
        "equals",
        "error",
        "except",
        "execute",
        "existing",
        "explain",
        "export",
        "extract",
        "false",
        "first",
        "fix",
        "following",
        "for",
        "from",
        "full",
        "function",
        "gdc",
        "grant",
        "having",
        "if",
        "ignore",
        "ilike",
        "in",
        "index",
        "inner",
        "insert",
        "intersect",
        "interval",
        "into",
        "invalidate",
        "is",
        "join",
        "last",
        "lateral",
        "left",
        "like",
        "load",
        "loaders",
        "matrix",
        "mlmodel",
        "move",
        "node",
        "not",
        "null",
        "nulls",
        "offset",
        "on",
        "option",
        "options",
        "order",
        "outer",
        "over",
        "partition",
        "pragma",
        "preceding",
        "procedure",
        "quarantine",
        "range",
        "redundancy",
        "refresh",
        "regex",
        "remove",
        "rename",
        "reset",
        "revoke",
        "right",
        "role",
        "row",
        "rows",
        "rowvector",
        "sample",
        "segment",
        "segmentsize",
        "select",
        "semi",
        "service",
        "set",
        "show",
        "similar",
        "skip_cache",
        "skip_cache_read",
        "skip_cache_write",
        "sleep_in_optimizer",
        "some",
        "source",
        "sso integration",
        "start",
        "stats",
        "stop",
        "storagespace",
        "streamloader_properties",
        "streamloaders",
        "summary_stats",
        "sysauth",
        "table",
        "table_with_rowids",
        "tag",
        "task",
        "then",
        "to",
        "trace",
        "true",
        "truncate",
        "tuple",
        "type",
        "unbounded",
        "union",
        "use",
        "using",
        "view",
        "when",
        "where",
        "with",
        "zstd",
    }

    def __init__(self, dialect):
        super(OcientIdentifierPreparer, self).__init__(dialect, initial_quote='"', final_quote='"')


class OcientDialect(default.DefaultDialect):
    name = "ocient"
    driver = "pyocient"
    supports_comments = True
    inline_comments = True
    supports_sane_rowcount = False
    supports_sane_multi_rowcount = False
    supports_unicode_statements = False
    supports_unicode_binds = False
    supports_simple_order_by_label = True
    supports_statement_cache = True
    supports_empty_insert = True
    supports_default_values = True
    supports_native_decimal = True
    supports_multivalues_insert = True
    delete_returning = False
    insert_returning = False
    update_returning = False
    requires_name_normalize = False
    use_insertmanyvalues = True
    use_insertmanyvalues_wo_returning = True
    bind_typing = interfaces.BindTyping.RENDER_CASTS

    poolclass = pool.SingletonThreadPool
    type_compiler = OcientTypeCompiler
    statement_compiler = OcientCompiler
    ddl_compiler = OcientDDLCompiler
    preparer = OcientIdentifierPreparer
    execution_ctx_cls = OcientExecutionContext

    ischema_names = ischema_names

    @classmethod
    def import_dbapi(cls):
        return pyocient

    def do_execute(self, cursor, statement, parameters, context=None):
        if (stripped := statement.strip())[-1] == ";":
            statement = stripped[:-1]
        cursor.execute(statement, parameters)

    def create_connect_args(self, url):
        urlstr = urllib.parse.unquote(url.render_as_string(hide_password=False)).replace("ocientdb", "ocient")
        urlstr = urlstr.replace("ocient+pyocient", "ocient")
        return [[urlstr], {}]

    @reflection.cache
    def get_schema_names(self, connection, schema=None, **kw):
        conn = connection.engine.raw_connection()
        try:
            cursor = conn.cursor()
            schema_names = []
            for rows in cursor.tables(schema="%", table="%"):
                rows = [str(r) for r in rows]
                if rows[1] not in schema_names:
                    schema_names.append(rows[1])
            schema_names.append("public")
            cursor.close()
        finally:
            conn.close()
        return schema_names

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        conn = connection.engine.raw_connection()
        try:
            cursor = conn.cursor()
            table_names = []
            if schema == None:
                sc = "%"
            else:
                sc = schema
            for rows in cursor.tables(schema=sc, table="%"):
                rows = [str(r) for r in rows]
                table_names.append(rows[2])
            cursor.close()
        finally:
            conn.close()
        return table_names

    @reflection.cache
    def get_view_names(self, connection, schema=None, **kw):
        conn = connection.engine.raw_connection()
        try:
            cursor = conn.cursor()
            view_names = []
            if schema == None:
                sc = "%"
            else:
                sc = schema
            for rows in cursor.views():
                rows = [str(r) for r in rows]
                view_names.append(rows[2])
            cursor.close()
        finally:
            conn.close()
        return view_names

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        conn = connection.engine.raw_connection()
        try:
            cursor = conn.cursor()
            query = f"select 1 FROM {schema}.{table_name} limit 1"
            cursor.execute(query)
            columns = []
            for rows in cursor.columns(schema=schema, table=table_name, column="%"):
                col_info = self._get_column_info(rows[3], rows[5], rows[10], rows[11], rows[15])
                columns.append(col_info)
            cursor.close()
        finally:
            conn.close()
        return columns

    def has_table(self, connection, table_name, schema=None):
        conn = connection.engine.raw_connection()
        cursor = conn.cursor()
        if schema is not None:
            prefix = f"{schema}."
        else:
            prefix = ""
        query = f"SELECT 1 AS has_table FROM {prefix}{table_name}"
        if schema is None:
            schema = "%"
        try:
            c = cursor.execute(query)
            columns = [col[3] for col in c.columns(table=table_name, schema=schema)]
        except pyocient.Error:
            return False
        else:
            return True

    def _get_column_info(self, name, type_, nullable, remarks, length):
        for mutable_type in mutable_types:
            if type_.startswith(mutable_type):
                coltype = mutable_types[mutable_type]
                break
        else:
            coltype = self.ischema_names.get(type_, None)

        kwargs = {}

        if coltype in (CHAR, VARCHAR):
            args = (length,)
        else:
            args = ()

        if coltype:
            coltype = coltype(*args, **kwargs)
        else:
            util.warn("Did not recognize type '%s' of column '%s'" % (type_, name))
            coltype = sqltypes.NULLTYPE

        column_info = dict(name=name, type=coltype, nullable=nullable, remarks=remarks)
        return column_info

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        constrained_columns = []
        cdict = {"constrained_columns": constrained_columns, "name": None}
        return cdict

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        foreign_keys = []
        return foreign_keys

    @reflection.cache
    def get_unique_constraints(self, connection, table_name, schema=None, **kw):
        constraints = []
        return constraints

    @reflection.cache
    def get_check_constraints(self, connection, table_name, schema=None, **kw):
        constraints = []
        return constraints

    @reflection.cache
    def get_table_comment(self, connection, table_name, schema=None, **kw):
        comment = {"text": None}
        return comment

    @reflection.cache
    def get_indexes(self, connection, table_name, schema=None, **kw):
        # TODO Leverage info schema to redurn indexes. See https://ocient.atlassian.net/browse/DB-23236
        indexes = []
        return indexes

    def _check_unicode_returns(self, connection, additional_tests=None):
        return False

    def _check_unicode_description(self, connection):
        return False

    def do_rollback(self, dbapi_connection):
        # No support for transactions.
        pass


dialect = OcientDialect
