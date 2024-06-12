"""Implementation of Rule CC05."""

from typing import List, Optional

from sqlfluff.core.rules import BaseRule, LintResult, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_CC05(BaseRule):
    """Block a list of configurable strings from being used in identifiers.
    Think of this as the opposite of custom rule CC04 in this plugin: rather than
    whitelisting strings, it blacklists strings. Generally, you will only need
    one of the two; it is recommended to start with CC05 to quickly blacklist strings
    that one is certain they want to block early on, then switch to using CC04 to
    whitelist a set list of words after developing said list.

    This rule differs from the built-in rule CV09 in that it facilitates blocking of
    phrases or parts of words as well, collectively known as "strings". It also only
    applies to identifiers, as it makes little sense to block part of a keyword.

    This block list is case insensitive.

    **Example use cases**

    * We wish to enforce a naming convention where ```avg``` is used over ```average```
    in identifiers, e.g. ```avg_sales``` instead of ```average_sales```. We can
    add ```average``` to ```blocked_strings_all``` to cause a linting error to flag this.
    This use case would not be fulfilled with CV09.

    **Anti-pattern**

    If the ``blocked_strings_all`` config is set to ``deprecated`` then the
    following will flag:

    .. code-block:: sql

        SELECT * FROM deprecated_table WHERE 1 = 1;

    **Best practice**

    Do not used any blocked strings:

    .. code-block:: sql

        SELECT * FROM table WHERE 1 = 1;

    """

    groups = ("all", "convention")
    crawl_behaviour = SegmentSeekerCrawler({"identifier"})
    config_keywords = [
        "blocked_strings_all",
        "blocked_strings_columns",
        "blocked_strings_tables",
    ]

    def _eval(self, context: RuleContext) -> Optional[LintResult]:
        # Config type hints
        self.blocked_strings_all: Optional[str]
        self.blocked_strings_columns: Optional[str]
        self.blocked_strings_tables: Optional[str]

        # Exit early if no block list set
        if (
            not self.blocked_strings_all
            and not self.blocked_strings_columns
            and not self.blocked_strings_tables
        ):
            return None

        # Get the ignore list configuration and cache it
        try:
            blocked_strings_all_set = self.blocked_strings_all_set
            blocked_strings_columns_set = self.blocked_strings_columns_set
            blocked_strings_tables_set = self.blocked_strings_tables_set
        except AttributeError:
            # First-time only, read the settings from configuration.
            # So we can cache them for next time for speed.
            blocked_strings_all_set = set(self._init_blocked_strings_all())
            blocked_strings_columns_set = set(self._init_blocked_strings_columns())
            blocked_strings_tables_set = set(self._init_blocked_strings_tables())

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

        identifier = context.segment.raw.replace("`", "")

        for blocked_strings_set, condition in (
            (blocked_strings_all_set, identifier),
            (blocked_strings_columns_set, is_column),
            (blocked_strings_tables_set, is_table),
        ):
            if not condition:
                continue
            for blocked_string in blocked_strings_set:
                if blocked_string in identifier.upper():
                    # Return as long as at least one blocked string is used
                    return LintResult(
                        anchor=context.segment,
                        description=f"Use of blocked string(s) in '{context.segment.raw}'.",
                    )

    def _init_blocked_strings_all(self) -> List[str]:
        """Called first time rule is evaluated to fetch & cache the blocked_strings_all."""
        blocked_strings_all_config = getattr(self, "blocked_strings_all")
        if blocked_strings_all_config:
            self.blocked_strings_all_list = self.split_comma_separated_string(
                blocked_strings_all_config.upper()
            )
        else:  # pragma: no cover
            # Shouldn't get here as we exit early if no block list
            self.blocked_strings_all_list = []

        return self.blocked_strings_all_list

    def _init_blocked_strings_columns(self) -> List[str]:
        """Called first time rule is evaluated to fetch & cache the blocked_strings_columns."""
        blocked_strings_columns = getattr(self, "blocked_strings_columns")
        if blocked_strings_columns:
            self.blocked_strings_columns_list = self.split_comma_separated_string(
                blocked_strings_columns.upper()
            )
        else:  # pragma: no cover
            # Shouldn't get here as we exit early if no block list
            self.blocked_strings_columns_list = []

        return self.blocked_strings_columns_list

    def _init_blocked_strings_tables(self) -> List[str]:
        """Called first time rule is evaluated to fetch & cache the blocked_strings_tables."""
        blocked_strings_tables = getattr(self, "blocked_strings_tables")
        if blocked_strings_tables:
            self.blocked_strings_tables_list = self.split_comma_separated_string(
                blocked_strings_tables.upper()
            )
        else:  # pragma: no cover
            # Shouldn't get here as we exit early if no block list
            self.blocked_strings_tables_list = []

        return self.blocked_strings_tables_list
