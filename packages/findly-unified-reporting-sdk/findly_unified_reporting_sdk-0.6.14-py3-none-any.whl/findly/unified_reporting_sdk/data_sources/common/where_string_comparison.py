# Contains classes which help in getting the where conditions when we are
# comparing string

import dataclasses
from dataclasses import dataclass
import logging
from typing import List, Optional
from sqlglot import parse_one
from sqlglot import expressions as sqlglot_expressions
from sqlglot import Expression

LOGGER = logging.getLogger(__name__)


@dataclass
class WhereClauseInformation:
    column_name: str
    column_operator: str
    column_value: str
    is_not_condition: bool = False


def parse_where_columns_from_sql_query(
    sql_query: str,
    dialect: str,
    where_clause_str: Optional[str] = None,
) -> List[WhereClauseInformation]:
    try:
        where_clause_maybe: Optional[Expression] = parse_one(
            sql=sql_query,
            read=dialect.lower(),
        ).args.get("where")

        if where_clause_maybe is None:
            LOGGER.info(
                {
                    "msg": "parse_where_column_condition_no_where_clause",
                    "where_clause": where_clause_str,
                    "sql_query": sql_query,
                }
            )
            return []

        where_clause: Expression = where_clause_maybe
        where_clause_list: list = list(
            # TODO: Too complicated to type this in right now, it uses a
            # base class to generate the information
            where_clause.find_all((sqlglot_expressions.Predicate,))  # type: ignore
        )
        where_clause_values: List[WhereClauseInformation] = []
        for condition in where_clause_list:
            not_condition = False
            try:
                if condition.parent.key.lower() == "not":
                    not_condition = True
            except Exception:
                pass

            column_operator_used_for_where_clause = condition.key
            if column_operator_used_for_where_clause == "in":
                # expression list cause this is an IN operator, so we get back
                # an array, lets handle that by iterating over the expressions
                for expression in condition.expressions:
                    where_clause_values.append(
                        WhereClauseInformation(
                            column_name=condition.this.sql(),
                            column_operator=condition.key,
                            column_value=expression.sql(),
                            is_not_condition=not_condition,
                        )
                    )
            elif column_operator_used_for_where_clause == "between":
                where_clause_values.append(
                    WhereClauseInformation(
                        column_name=condition.args["this"].sql(),
                        column_operator=condition.key,
                        column_value=f"{condition.args['low'].sql()} AND {condition.args['high'].sql()}",
                        is_not_condition=not_condition,
                    )
                )
            else:
                # We fail on parsing things like:
                # CAST(A as B)
                # for now this only happens with joining conditions and with
                # dates, since both are not necessary for edit distance fix
                # we can safeguard against the exception and keep going
                try:
                    where_clause_values.append(
                        WhereClauseInformation(
                            column_name=condition.this.sql(),
                            column_operator=condition.key,
                            column_value=condition.expression.sql(),
                            is_not_condition=not_condition,
                        )
                    )
                except Exception as e:
                    LOGGER.warning(
                        {
                            "msg": "error_parsing_where_condition",
                            "condition": condition.this.sql(),
                            "where_clause": where_clause_str,
                            "sql_query": sql_query,
                            "error": str(e),
                        }
                    )
        LOGGER.info(
            {
                "msg": "parse_where_column_condition_values",
                "where_clause": where_clause_str,
                "sql_query": sql_query,
                "where_clause_values": [
                    dataclasses.asdict(value) for value in where_clause_values
                ],
            }
        )
        return where_clause_values
    except Exception as e:
        LOGGER.error(
            {
                "msg": "error_parse_where_column_condition",
                "where_clause": where_clause_str,
                "sql_query": sql_query,
                "error": str(e),
            }
        )
        return []


# We are going to parse the where columns and just log them, to see if
# we can do it correctly
# if all things work, we can use edit distance here to fix things
def parse_where_column_condition(
    where_clause_str: str,
    dialect: str,
) -> List[WhereClauseInformation]:
    dummy_select_string = "select * from table"

    # if the where_clause_str doesn't start with a where, we need to add it.
    if not where_clause_str.lower().startswith("where"):
        where_clause_str = "where " + where_clause_str

    # The where clause already starts with a where on the completion, so
    # just appending it to the dummy string should work
    complete_sql = dummy_select_string + " " + where_clause_str
    return parse_where_columns_from_sql_query(
        sql_query=complete_sql,
        dialect=dialect,
        where_clause_str=where_clause_str,
    )
