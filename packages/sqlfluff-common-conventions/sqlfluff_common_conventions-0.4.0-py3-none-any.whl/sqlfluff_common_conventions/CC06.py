"""Implementation of Rule CC06."""

import re
from typing import Optional

from sqlfluff.core.rules import BaseRule, LintResult, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_CC06(BaseRule):
    """Ensure column and table names match a given regex.

    **Anti-pattern**

    If the ``column_name_regex`` config is set to ``^user_`` then the
    following will flag:

    .. code-block:: sql

        create table tbl (
            age string
        )

    **Best practice**

    Align column and table names with the given regex.

    .. code-block:: sql

        create table tbl (
            user_age string
        )
    """

    groups = ("all", "convention")

    crawl_behaviour = SegmentSeekerCrawler({"identifier"})
    config_keywords = [
        "column_name_regex",
        "table_name_regex",
    ]
    is_fix_compatible = False

    def _eval(self, context: RuleContext) -> Optional[LintResult]:
        """Find rule violations and provide fixes."""

        self.column_name_regex: Optional[str]
        self.table_name_regex: Optional[str]

        # Exit early if neither regex is set
        if not self.column_name_regex and not self.table_name_regex:
            return None

        # Account for presence of backticks in e.g. `proj-name.dataset.table`.
        identifier = context.segment.raw.replace("`", "")

        is_column = context.parent_stack[-1].is_type(
            "column_reference", "column_definition"
        ) or (
            context.parent_stack[-2].is_type("select_clause_element")
            and context.parent_stack[-1].is_type("alias_expression")
        )

        is_table = context.parent_stack[-1].is_type("table_reference") or (
            context.parent_stack[-2].is_type("from_expression_element")
            and context.parent_stack[-1].is_type("alias_expression")
        )

        if (
            self.column_name_regex
            and is_column
            and not re.search(rf"{self.column_name_regex}", identifier)
        ):
            return LintResult(
                anchor=context.segment,
                description=f"Column '{identifier}' does not match regex '{self.column_name_regex}'.",
            )

        if (
            self.table_name_regex
            and is_table
            and not re.search(rf"{self.table_name_regex}", identifier)
        ):
            return LintResult(
                anchor=context.segment,
                description=f"Table '{identifier}' does not match regex '{self.table_name_regex}'.",
            )
