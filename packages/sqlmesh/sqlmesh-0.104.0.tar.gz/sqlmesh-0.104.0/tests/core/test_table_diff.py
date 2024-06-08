import pytest
import pandas as pd
from sqlglot import exp

from sqlmesh.core.config import AutoCategorizationMode, CategorizerConfig
from sqlmesh.core.model import SqlModel


@pytest.mark.slow
def test_data_diff(sushi_context_fixed_date):
    model = sushi_context_fixed_date.models['"memory"."sushi"."customer_revenue_by_day"']

    model.query.select(exp.cast("'1'", "VARCHAR").as_("modified_col"), "1 AS y", copy=False)
    sushi_context_fixed_date.upsert_model(model)

    sushi_context_fixed_date.plan(
        "source_dev",
        no_prompts=True,
        auto_apply=True,
        skip_tests=True,
        start="2023-01-31",
        end="2023-01-31",
    )
    model = sushi_context_fixed_date.models['"memory"."sushi"."customer_revenue_by_day"']

    for column in model.query.find_all(exp.Column):
        if column.name == "total":
            column.replace(
                exp.func(
                    "IF",
                    exp.column("total", "ot") < 4,
                    exp.column("total", "ot") * 0.1,
                    exp.column("total", "ot"),
                )
            )

    for alias in model.query.find_all(exp.Alias):
        if alias.alias == "modified_col":
            alias.this.set("to", exp.DataType.build("INT"))
        if alias.alias == "y":
            alias.pop()

    model.query.select("1 AS z", copy=False).limit(10000, copy=False)
    # add row to table with UNION
    modified_model = model.dict()
    modified_model["query"] = (
        exp.select("*")
        .from_(model.query.subquery())
        .union("select -1, 9999.00, 0, CAST('2023-01-31' AS DATE), 1, 1")
    )
    modified_sqlmodel = SqlModel(**modified_model)
    sushi_context_fixed_date.upsert_model(modified_sqlmodel)

    sushi_context_fixed_date.auto_categorize_changes = CategorizerConfig(
        sql=AutoCategorizationMode.FULL
    )
    sushi_context_fixed_date.plan(
        "target_dev",
        create_from="source_dev",
        no_prompts=True,
        auto_apply=True,
        skip_tests=True,
        start="2023-01-31",
        end="2023-01-31",
    )

    diff = sushi_context_fixed_date.table_diff(
        source="source_dev",
        target="target_dev",
        on=exp.condition("s.customer_id = t.customer_id AND s.event_date = t.event_date"),
        model_or_snapshot="sushi.customer_revenue_by_day",
    )

    schema_diff = diff.schema_diff()
    assert schema_diff.added == [("z", exp.DataType.build("int"))]
    assert schema_diff.modified == {
        "modified_col": (exp.DataType.build("varchar"), exp.DataType.build("int"))
    }
    assert schema_diff.removed == [("y", exp.DataType.build("int"))]

    row_diff = diff.row_diff()
    assert row_diff.source_count == 17
    assert row_diff.target_count == 18
    assert row_diff.join_count == 17
    assert row_diff.full_match_count == 17
    assert row_diff.full_match_pct == 97.14
    assert row_diff.partial_match_count == 0.0
    assert row_diff.partial_match_pct == 0.0
    assert row_diff.s_only_count == 0
    assert row_diff.t_only_count == 1
    assert row_diff.sample.shape == (1, 12)
    assert row_diff.joined_sample.shape == (0, 2)
    assert row_diff.s_sample.shape == (0, 6)
    assert row_diff.t_sample.shape == (1, 6)


@pytest.mark.slow
def test_data_diff_decimals(sushi_context_fixed_date):
    engine_adapter = sushi_context_fixed_date.engine_adapter

    engine_adapter.ctas(
        "table_diff_source",
        pd.DataFrame(
            {
                "key": [1, 2, 3],
                "value": [1.0, 2.0, 3.1233],
            }
        ),
    )

    engine_adapter.ctas(
        "table_diff_target",
        pd.DataFrame(
            {
                "key": [1, 2, 3],
                "value": [1.0, 2.0, 3.1234],
            }
        ),
    )

    diff = sushi_context_fixed_date.table_diff(
        source="table_diff_source",
        target="table_diff_target",
        on=["key"],
    )
    assert diff.row_diff().full_match_count == 3
    assert diff.row_diff().partial_match_count == 0

    diff = sushi_context_fixed_date.table_diff(
        source="table_diff_source",
        target="table_diff_target",
        on=["key"],
        decimals=4,
    )
    assert diff.row_diff().full_match_count == 2
    assert diff.row_diff().partial_match_count == 1
