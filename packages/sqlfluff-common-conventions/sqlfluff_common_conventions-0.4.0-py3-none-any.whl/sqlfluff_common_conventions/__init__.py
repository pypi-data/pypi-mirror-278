import os
from typing import List, Type

from sqlfluff.core.config import ConfigLoader
from sqlfluff.core.plugin import hookimpl
from sqlfluff.core.rules import BaseRule


@hookimpl
def get_rules() -> List[Type[BaseRule]]:
    """Get plugin rules."""
    from sqlfluff_common_conventions.CC01 import Rule_CC01
    from sqlfluff_common_conventions.CC02 import Rule_CC02
    from sqlfluff_common_conventions.CC03 import Rule_CC03
    from sqlfluff_common_conventions.CC04 import Rule_CC04
    from sqlfluff_common_conventions.CC05 import Rule_CC05
    from sqlfluff_common_conventions.CC06 import Rule_CC06

    return [Rule_CC01, Rule_CC02, Rule_CC03, Rule_CC04, Rule_CC05, Rule_CC06]


@hookimpl
def load_default_config() -> dict:
    """Loads the default configuration for the plugin."""
    return ConfigLoader.get_global().load_config_file(
        file_dir=os.path.dirname(__file__),
        file_name="plugin_default_config.cfg",
    )


@hookimpl
def get_configs_info() -> dict:
    """Get rule config validations and descriptions."""
    return {
        # CC01–CC03
        "naming_case": {
            "validation": ["snake", "dromedary", "pascal"],
            "definition": "What is the naming case?",
        },
        # CC04
        "allowed_strings_all": {
            "definition": "A list of strings to allow in all identifiers."
        },
        "allowed_strings_columns": {
            "definition": "A list of strings to allow in column identifiers."
        },
        "allowed_strings_tables": {
            "definition": "A list of strings to allow in table identifiers."
        },
        "allow_space_in_identifier": {  # whitespace is not detected as a string in .cfg
            "validation": [True, False],
            "definition": "Should whitespace be allowed?",
        },
        # CC05
        "blocked_strings_all": {
            "definition": "A list of strings to block in all identifiers."
        },
        "blocked_strings_columns": {
            "definition": "A list of strings to block in column identifiers."
        },
        "blocked_strings_tables": {
            "definition": "A list of strings to block in table identifiers."
        },
        "block_space_in_identifier": {  # whitespace is not detected as a string in .cfg
            "validation": [True, False],
            "definition": "Should whitespace be allowed?",
        },
        # CC06
        "column_name_regex": {
            "definition": "A regex that column names must match.",
        },
        "table_name_regex": {
            "definition": "A regex that table names must match.",
        },
    }
