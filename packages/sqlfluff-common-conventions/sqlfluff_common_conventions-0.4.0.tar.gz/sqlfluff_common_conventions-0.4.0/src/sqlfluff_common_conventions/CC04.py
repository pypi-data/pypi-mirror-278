"""Implementation of Rule CC04."""

import re
from typing import List, Optional

from sqlfluff.core.rules import BaseRule, LintResult, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler

# TODO: Ignore project and dataset names, i.e. given abc.def.ghi, only look at ghi.
# This is harder to implement, though, so this rule currently checks all identifiers.


class Rule_CC04(BaseRule):
    """Only allow a list of configurable strings to be used in identifiers.
    Think of this as the opposite of custom rule CC05 in this plugin: rather than
    blacklisting strings (words, phrases, and parts of words), it whitelists strings.
    Generally, you will only need one of the two; it is recommended to start with CC05
    to quickly blacklist strings that one is certain they want to block early on, then
    switch to using CC04 to whitelist a set list of words after developing said list.

    This whitelist is case insensitive.

    **Anti-pattern**

    If the ``allowed_strings_all`` config is set to ``user,profile,id,_``, then
    the following will flag:

    .. code-block:: sql

        select * from profile_of_user;

    **Best practice**

    Only use allowed strings:

    .. code-block:: sql

        select * from user_profile;

    """

    groups = ("all", "convention")

    crawl_behaviour = SegmentSeekerCrawler({"identifier"})
    config_keywords = [
        "allowed_strings_all",
        "allowed_strings_columns",
        "allowed_strings_tables",
    ]
    is_fix_compatible = False

    def _eval(self, context: RuleContext) -> Optional[LintResult]:
        """Find rule violations and provide fixes."""

        self.allowed_strings_all: Optional[str]
        self.allowed_strings_columns: Optional[str]
        self.allowed_strings_tables: Optional[str]

        # Exit early if allowed_strings_all is not set
        if (
            not self.allowed_strings_all
            and not self.allowed_strings_columns
            and not self.allowed_strings_tables
        ):
            return None

        # Get the allowed list configuration and cache it
        try:
            allowed_strings_all_set = self.allowed_strings_all_set
            allowed_strings_columns_set = self.allowed_strings_columns_set
            allowed_strings_tables_set = self.allowed_strings_tables_set
        except AttributeError:
            # First-time only, read the settings from configuration.
            # So we can cache them for next time for speed.
            allowed_strings_all_set = set(self._init_allowed_strings_all())
            allowed_strings_columns_set = set(self._init_allowed_strings_columns())
            allowed_strings_tables_set = set(self._init_allowed_strings_tables())

        # Account for presence of backticks or quotation marks to wrap identifiers.
        identifier = context.segment.raw.replace("`", "").replace('"', "")

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

        allowed_strings_columns_set.update(allowed_strings_all_set)
        allowed_strings_tables_set.update(allowed_strings_all_set)

        for allowed_strings_set, condition, set_type in (
            (allowed_strings_columns_set, is_column, "col"),
            (allowed_strings_tables_set, is_table, "table"),
        ):
            if allowed_strings_set and condition:
                allowed_strings_set_regex = "|".join(allowed_strings_set) + "|\\s"

                match = re.findall(
                    # . allowed because of e.g. `proj-name.dataset.table`
                    rf"^(?:{allowed_strings_set_regex}|\.)+$",
                    identifier,
                    re.IGNORECASE,
                )

                if not match:
                    return LintResult(
                        anchor=context.segment,
                        description=f"Use of unallowed string(s) in '{identifier}'.",
                    )

    def _init_allowed_strings_all(self) -> List[str]:
        """Called first time rule is evaluated to fetch & cache the allowed_strings_all."""
        allowed_strings_all = getattr(self, "allowed_strings_all")
        if allowed_strings_all:
            self.allowed_strings_all_list = self.split_comma_separated_string(
                allowed_strings_all.upper()
            )
        else:  # pragma: no cover
            # Shouldn't get here as we exit early if no allow list
            self.allowed_strings_all_list = []

        return self.allowed_strings_all_list

    def _init_allowed_strings_columns(self) -> List[str]:
        """Called first time rule is evaluated to fetch & cache the allowed_strings_columns."""
        allowed_strings_columns = getattr(self, "allowed_strings_columns")
        if allowed_strings_columns:
            self.allowed_strings_columns_list = self.split_comma_separated_string(
                allowed_strings_columns.upper()
            )
        else:  # pragma: no cover
            # Shouldn't get here as we exit early if no allow list
            self.allowed_strings_columns_list = []

        return self.allowed_strings_columns_list

    def _init_allowed_strings_tables(self) -> List[str]:
        """Called first time rule is evaluated to fetch & cache the allowed_strings_tables."""
        allowed_strings_tables = getattr(self, "allowed_strings_tables")
        if allowed_strings_tables:
            self.allowed_strings_tables_list = self.split_comma_separated_string(
                allowed_strings_tables.upper()
            )
        else:  # pragma: no cover
            # Shouldn't get here as we exit early if no allow list
            self.allowed_strings_tables_list = []

        return self.allowed_strings_tables_list
