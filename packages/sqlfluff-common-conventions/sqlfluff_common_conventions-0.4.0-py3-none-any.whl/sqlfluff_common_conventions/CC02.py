"""Implementation of Rule CC02."""

from typing import List, Optional

from sqlfluff.core.rules import LintResult, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler

from sqlfluff_common_conventions.CC01 import Rule_CC01


class Rule_CC02(Rule_CC01):
    """Do not have a datetime, time, or timestamp column that does not end with `at`.

    **Anti-pattern**

    .. code-block:: sql

        create table tbl (
            created datetime,
            updated time,
            deleted timestamp
        )

    **Best practice**

    End datetime, time, and timestamp columns with `at`.

    .. code-block:: sql

        create table tbl (
            created_at datetime,
            updated_at time,
            deleted_at timestamp
        )
    """

    groups = ("all", "convention")

    crawl_behaviour = SegmentSeekerCrawler(
        {
            "data_type_identifier",
            "primitive_type",
            "data_type",
            "select_clause_element",
        }
    )
    config_keywords = ["naming_case"]
    is_fix_compatible = False
    _acceptable_data_types = ["DATETIME", "TIME", "TIMESTAMP"]
    _description_elem = "Datetime, time, or timestamp"
    _starts_with = []
    _ends_with = ["at"]

    def _eval(self, context: RuleContext) -> Optional[List[LintResult]]:
        """Find rule violations and provide fixes."""

        return super()._eval(context=context)
