from datetime import datetime
from typing import Dict, Optional, List

import numpy as np
import pandas as pd
from pydantic import BaseModel, Extra, Field, root_validator

from chaiverse import config
from chaiverse.lib.now import utcnow
from chaiverse.schemas.leaderboard_row_schema import LeaderboardRow


DEFAULT_LEADERBOARD_HEADER_MAPPING = {
    'double_thumbs_up_ratio': '👍👍_ratio',
    'thumbs_up_ratio': '👍👍+👍_ratio',
    'single_thumbs_up_ratio': '👍_ratio',
    'thumbs_down_ratio': '👎_ratio',
}

DEFAULT_LEADERBOARD_INCLUDES = [
    'developer_uid',
    'submission_id',
    'celo_rating',
    'win_ratio',
    'num_battles',
    'double_thumbs_up_ratio',
    'thumbs_down_ratio',
    'feedback_count',
    'model_score',
    'safety_score',
    'best_of',
    'max_input_tokens',
    'max_output_tokens',
    'model_architecture',
    'model_repo',
    'reward_repo',
    'status',
    'model_name',
    'us_pacific_date',
    'ineligible_reason',
]

DEFAULT_LEADERBOARD_EXCLUDES = []

DEFAULT_LEADERBOARD_SORT_PARAMS = {
    'by': 'celo_rating',
    'ascending': False
}

DEFAULT_TABULATE_OPTIIONS = {
    'numalign': 'decimal',
}


class Leaderboard(BaseModel, extra=Extra.allow):
    '''
    We are migrating from storing in
        leaderboard_rows of List[LeaderboardRow] to
        leaderboard_dict of Dict[submission_id, LeaderboardRow]
    During the transition:
        Leaderboard loaded from firebase can either contain list or dict.
        The validator will auto populat the leaderboard_dict if only leaderboard_rows existed.
        All code should read from leaderboard_dict and write to leaderboard_dict.
    After transition:
        The leaderboard_rows will be deleted from the code together with the validator.
        The old leaderboards stored in firebase will be deleted in data migration.
    '''
    timestamp: datetime = Field(default_factory=lambda: utcnow())
    leaderboard_rows: Optional[List[LeaderboardRow]]
    leaderboard_dict: Dict[str, LeaderboardRow]

    @root_validator(pre=True)
    def validate_leaderboard(cls, values):
        if not isinstance(values.get('leaderboard_dict'), dict):
            rows = values.get('leaderboard_rows', [])
            leaderboard_dict = {getattr(row, 'submission_id', None) or row['submission_id']: row for row in rows}
            values['leaderboard_dict'] = leaderboard_dict
        return values

    @property
    def rows(self) -> List[LeaderboardRow]:
        return [*self.leaderboard_dict.values()]

    @property
    def df(self) -> pd.DataFrame:
        leaderboard_rows = [row.all_fields_dict() for row in self.rows]
        df = pd.DataFrame.from_records(leaderboard_rows)
        df = _sort_by_values(df, **DEFAULT_LEADERBOARD_SORT_PARAMS)
        return df

    def to_display_df(self, includes=None, excludes=None, sort_params=None, header_mapping=None) -> pd.DataFrame:
        includes = includes or DEFAULT_LEADERBOARD_INCLUDES
        excludes = excludes or DEFAULT_LEADERBOARD_EXCLUDES
        sort_params = sort_params or DEFAULT_LEADERBOARD_SORT_PARAMS
        header_mapping = header_mapping or DEFAULT_LEADERBOARD_HEADER_MAPPING
        df = self.df if len(self.df) > 0 else pd.DataFrame(columns=includes)
        df = _filter_by_leaderboard_eligibility(df)
        df = _add_repo_aggregate_columns(df)
        df = _include_listed_columns(df, includes)
        df = _exclude_listed_columns(df, excludes)
        df = _sort_by_values(df, **sort_params)
        df = df.round(2)
        df = df.rename(columns=header_mapping)
        return df

    def to_html(self, includes=None, header_mapping=None, sort_params=None):
        includes = includes or DEFAULT_LEADERBOARD_INCLUDES
        sort_params = sort_params or {"by": "celo_rating", "ascending": False}
        df = self.to_display_df(includes=includes, header_mapping=header_mapping, sort_params=sort_params)
        df.fillna("", inplace=True)
        html = df.to_html(classes="leaderboard-table table display nowrap", index=False, justify="center", escape=False)
        return html

    @property
    def auto_deactivation_candidates(self):
        rows = _get_can_auto_deactivate_rows(self.rows)
        rows = _sort_auto_deactivate_rows(rows)
        rows = _remove_top_models(rows)
        submission_ids = [row.submission_id for row in rows]
        return submission_ids

    def get_row_dict(self, submission_id):
        row = self.leaderboard_dict.get(submission_id, {})
        row_dict = row.all_fields_dict() if row else {}
        return row_dict

    def filter(self, **kwargs):
        leaderboard_rows = [
            row for row in self.leaderboard_dict.values() if
            filter_row(row, kwargs)
        ]
        return Leaderboard(timestamp=self.timestamp, leaderboard_rows=leaderboard_rows)


def filter_row(row, filters):
    row_matches_filters = [getattr(row, filter) == value for filter, value in filters.items()]
    return all(row_matches_filters)


def _add_repo_aggregate_columns(df):
    if len(df) > 0:
        df['model_group'] = df.get('model_group', '')
        df['best_of'] = df.get('best_of', 1)
        df = _aggregate_max_columns(df)
        df = _aggregate_sum_columns(df)
    return df


def _aggregate_max_columns(df):
    for column in ["celo_rating", "double_thumbs_up_ratio", "thumbs_down_ratio", "win_ratio", "safety_score", "model_score"]:
        grouped_by = df.groupby("model_group")[column]
        df[f"{column}_by_group"] = grouped_by.transform("max") if len(grouped_by) > 0 else None
    return df


def _aggregate_sum_columns(df):
    for column in ["feedback_count", "num_battles"]:
        grouped_by = df.groupby("model_group")[column]
        df[f"{column}_by_group"] = grouped_by.transform("sum") if len(grouped_by) > 0 else None
    return df


def _filter_by_leaderboard_eligibility(df):
    if "ineligible_reason" in df.columns:
        df = df[df.ineligible_reason.isnull()]
    return df


def _include_listed_columns(df, includes):
    df = df[[column for column in includes if column in df.columns]]
    return df


def _exclude_listed_columns(df, excludes):
    df = df[[column for column in df.columns if column not in excludes]]
    return df


def _sort_by_values(df, by: List[str], ascending: bool):
    if len(df) > 0:
        df = df.sort_values(by=by, ascending=ascending, na_position='last', ignore_index=True)
        df.index = np.arange(1, len(df) + 1)
    return df


def _get_can_auto_deactivate_rows(rows: List[LeaderboardRow]):
    rows = [row for row in rows if row.can_auto_deactivate()]
    return rows


def _sort_auto_deactivate_rows(rows: List[LeaderboardRow]):
    rows = sorted(rows, key=lambda row: row.celo_rating, reverse=True)
    return rows


def _remove_top_models(rows: List[LeaderboardRow]):
    rows = rows[config.AUTO_DEACTIVATION_MIN_RANK - 1:]
    return rows
