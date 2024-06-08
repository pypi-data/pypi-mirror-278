from datetime import datetime, timedelta
from typing import Literal, Optional

import click
from gable.helpers.data_asset_s3.path_pattern_manager import PathPatternManager
from gable.helpers.emoji import EMOJI


def validate_input(
    action: Literal["register", "check"],
    bucket: Optional[str],
    lookback_days: int,
    include: Optional[tuple[str, ...]],
    history: Optional[bool],
) -> None:
    if not bucket:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} Missing required option --bucket for S3 file registration and checking. You can use the --debug or --trace flags for more details."
        )

    if history:
        if action == "check":
            raise click.ClickException(
                f"{EMOJI.RED_X.value} --history is only valid for the register command."
            )
        if include is None or len(include) != 2:
            raise click.ClickException(
                "Two include patterns are required for historical data asset detection when using --history."
            )

    if lookback_days <= 0:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} --lookback-days must be at least 1."
        )

    if not history and include is not None:
        for pattern in include:
            _, dt = PathPatternManager().substitute_date_placeholders(pattern)
            if dt and dt < datetime.now() - timedelta(days=lookback_days):
                raise click.ClickException(
                    f"{EMOJI.RED_X.value} Include pattern '{pattern}' must be within lookback window (between --lookback-days ago and now())."
                )
