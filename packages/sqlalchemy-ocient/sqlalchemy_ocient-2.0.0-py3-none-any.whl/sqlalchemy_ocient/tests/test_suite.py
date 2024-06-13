from sqlalchemy.testing.suite.test_select import ExpandingBoundInTest as _ExpandingBoundInTest
from sqlalchemy.testing.suite.test_select import FetchLimitOffsetTest as _FetchLimitOffsetTest
from sqlalchemy.testing.suite.test_select import LikeFunctionsTest as _LikeFunctionsTest
from sqlalchemy.testing.suite.test_select import PostCompileParamsTest as _PostCompileParamsTest
from sqlalchemy.testing.suite.test_select import SameNamedSchemaTableTest as _SameNamedSchemaTableTest
from sqlalchemy.testing.suite.test_select import ValuesExpressionTest as _ValuesExpressionTest
from sqlalchemy.testing.suite.test_select import *

"""
Import and override (where necessary) the sqlalchemy test suite
"""


class LikeFunctionsTest(_LikeFunctionsTest):
    # Ocient DB doesn;t support ESCAPE
    @testing.skip("ocient")
    def test_startswith_autoescape(self):
        return

    @testing.skip("ocient")
    def test_startswith_autoescape_escape(self):
        return

    @testing.skip("ocient")
    def test_startswith_escape(self):
        return

    @testing.skip("ocient")
    def test_endswith_autoescape(self):
        return

    @testing.skip("ocient")
    def test_endswith_autoescape_escape(self):
        return

    @testing.skip("ocient")
    def test_endswith_escape(self):
        return

    @testing.skip("ocient")
    def test_contains_autoescape(self):
        return

    @testing.skip("ocient")
    def test_contains_autoescape_escape(self):
        return

    @testing.skip("ocient")
    def test_contains_escape(self):
        return


class ExpandingBoundInTest(_ExpandingBoundInTest):

    # Ocient database doesn't support raw tuples (e.g. (a, b)). It
    # requirs tuple(a, b).  These tests hardcode the raw tuples
    @testing.skip("ocient")
    def test_bound_in_heterogeneous_two_tuple_text_bindparam(self):
        return

    @testing.skip("ocient")
    def test_bound_in_heterogeneous_two_tuple_text_bindparam_non_tuple(self):
        return

    @testing.skip("ocient")
    def test_bound_in_heterogeneous_two_tuple_typed_bindparam_non_tuple(self):
        return


class PostCompileParamsTest(_PostCompileParamsTest):
    # This is another raw tuple  issue
    @testing.skip("ocient")
    def test_execute_tuple_expanding_plus_literal_execute(self, connection):
        return

    @testing.skip("ocient")
    def test_execute_tuple_expanding_plus_literal_heterogeneous_execute(self, connection):
        return


class SameNamedSchemaTableTest(_SameNamedSchemaTableTest):
    """
    These are currently broken in the database, pending a fix for DB-28794
    """

    @testing.skip("ocient")
    def test_subquery(self, connection):
        return

    @testing.skip("ocient")
    def test_simple_join_both_tables(self, connection):
        return

    @testing.skip("ocient")
    def test_simple_join_whereclause_only(self, connection):
        return


class ValuesExpressionTest(_ValuesExpressionTest):
    # Ocient DB doesn't support FROM(VALUES ...)
    @testing.skip("ocient")
    def test_tuples(self, connection):
        return


class FetchLimitOffsetTest(_FetchLimitOffsetTest):
    # IMHO, the test in the test suite is not correct because
    # it uses LIMIT without ORDER BY, and thus the results
    # are nondeterministic.  This test just adds ORDER_BY
    def test_limit_render_multiple_times(self, connection):
        table = self.tables.some_table
        stmt = select(table.c.id).order_by(table.c.id).limit(1).scalar_subquery()

        u = union(select(stmt), select(stmt)).subquery().select()

        self._assert_result(
            connection,
            u,
            [
                (1,),
            ],
        )
