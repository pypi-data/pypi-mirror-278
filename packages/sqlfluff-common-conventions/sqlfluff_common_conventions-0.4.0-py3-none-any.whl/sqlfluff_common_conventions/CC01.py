"""Implementation of Rule CC01."""

from typing import List, Optional, Tuple

from sqlfluff.core.parser import BaseSegment
from sqlfluff.core.rules import BaseRule, LintResult, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


def format_description_list(lst: List[str]) -> str:
    with_backticks = list(map(lambda x: "`" + x + "`", lst))
    if len(lst) == 1:
        return with_backticks[0]
    elif len(lst) == 2:
        return " or ".join(with_backticks)
    else:
        return ", ".join(with_backticks[:-1]) + ", or " + with_backticks[-1]


class Rule_CC01(BaseRule):
    """Do not have a boolean column that does not start with `is` or `has`.

    **Anti-pattern**

    .. code-block:: sql

        create table tbl (
            happy bool,
            money bool,
            created_at datetime,
            updated_at datetime
        )

    **Best practice**

    Start boolean columns with `is` or `has`.

    .. code-block:: sql

        create table tbl (
            is_happy bool,
            has_money bool,
            created_at datetime,
            updated_at datetime
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
    _acceptable_data_types = ["BOOL", "BOOLEAN"]
    _description_elem = "Boolean"
    _starts_with = ["is", "has"]
    _ends_with = []

    def _eval(self, context: RuleContext) -> Optional[List[LintResult]]:
        """Find rule violations and provide fixes."""

        self.naming_case: str

        identifier_seg, data_type_seg = self._extract_identifier_and_data_type_segments(
            context
        )
        if (
            not identifier_seg
            or not data_type_seg
            or data_type_seg.raw_upper not in self._acceptable_data_types
        ):
            return None

        results = []
        if self._starts_with:
            results.append(self._process_starts_with(identifier_seg))
        if self._ends_with:
            results.append(self._process_ends_with(identifier_seg))

        return list(filter(lambda r: r is not None, results))

    def _extract_identifier_and_data_type_segments(
        self, context: RuleContext
    ) -> Tuple[Optional[BaseSegment], Optional[BaseSegment]]:

        segment = context.segment
        identifier, data_type = None, None

        if segment.is_type("data_type_identifier", "primitive_type", "data_type"):
            data_type = segment

            has_create_table_statement = False
            for seg in context.parent_stack:
                if seg.is_type("create_table_statement"):
                    has_create_table_statement = True
                    break

            if has_create_table_statement:
                for sib_seg in context.siblings_pre[::-1]:
                    if sib_seg.is_type(
                        "column_reference", "column_definition", "identifier"
                    ):
                        identifier = sib_seg
                        break
        else:

            # We only look for select clause elements with casting,
            # as that is the only way we know a selected element's data type.
            # We do not look directly for cast expressions or functions as
            # we need to be able to get the alias behind them.

            function = segment.get_child("function")
            expression = segment.get_child("expression")
            if not function and not (
                expression and expression.get_child("cast_expression")
            ):
                return identifier, data_type

            if function:
                function_name = function.get_child("function_name")
                alias_expression = segment.get_child("alias_expression")

                if (
                    function_name.raw_upper not in ["CAST", "CONVERT"]
                    or not alias_expression
                ):
                    return identifier, data_type

                identifier = alias_expression.get_child("identifier")
                data_type = function.get_child("bracketed").get_child("data_type")
            else:
                alias_expression = segment.get_child("alias_expression")
                identifier = (
                    expression.get_child("cast_expression").get_child(
                        "column_reference"
                    )
                    if not alias_expression
                    else alias_expression.get_child("identifier")
                )
                data_type = expression.get_child("cast_expression").get_child(
                    "data_type"
                )

        return identifier, data_type

    def _process_starts_with(self, identifier_seg) -> Optional[LintResult]:

        snake = tuple(map(lambda x: x + "_", self._starts_with))
        dromedary = tuple(self._starts_with)
        pascal = tuple(map(lambda x: x.capitalize(), self._starts_with))

        identifier = identifier_seg.raw

        if self.naming_case == "snake" and not identifier.startswith(snake):
            return LintResult(
                anchor=identifier_seg,
                description=f"{self._description_elem} column does not start with "
                f"{format_description_list(snake)}.",
            )
        elif self.naming_case == "dromedary" and (
            not identifier.startswith(dromedary)
            or any(
                [
                    identifier.startswith(s)
                    and len(identifier) > len(s)
                    and not identifier[len(s)].isupper()
                    and not identifier[len(s)].isdigit()
                    for s in dromedary
                ]
            )
        ):
            return LintResult(
                anchor=identifier_seg,
                description=f"{self._description_elem} column does not start with "
                f"{format_description_list(dromedary)}.",
            )
        elif self.naming_case == "pascal" and (
            not identifier.startswith(pascal)
            or any(
                [
                    identifier.startswith(s)
                    and len(identifier) > len(s)
                    and not identifier[len(s)].isupper()
                    and not identifier[len(s)].isdigit()
                    for s in pascal
                ]
            )
        ):
            return LintResult(
                anchor=identifier_seg,
                description=f"{self._description_elem} column does not start with "
                f"{format_description_list(pascal)}.",
            )

    def _process_ends_with(self, identifier_seg) -> Optional[LintResult]:

        snake = tuple(map(lambda x: "_" + x, self._ends_with))
        dromedary_and_pascal = tuple(map(lambda x: x.capitalize(), self._ends_with))

        identifier = identifier_seg.raw

        if self.naming_case == "snake" and not identifier.endswith(snake):
            return LintResult(
                anchor=identifier_seg,
                description=f"{self._description_elem} column does not end with "
                f"{format_description_list(snake)}.",
            )
        elif self.naming_case in ["dromedary", "pascal"] and not identifier.endswith(
            dromedary_and_pascal
        ):
            return LintResult(
                anchor=identifier_seg,
                description=f"{self._description_elem} column does not end with "
                f"{format_description_list(dromedary_and_pascal)}.",
            )
