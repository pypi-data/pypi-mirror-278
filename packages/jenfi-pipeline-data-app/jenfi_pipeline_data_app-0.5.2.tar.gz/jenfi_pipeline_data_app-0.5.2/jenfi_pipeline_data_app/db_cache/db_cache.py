from pathlib import Path

import pandas as pd
from sqlalchemy.engine import Engine

from .cacher import Cacher


class DbCache:
    def __init__(
        self,
        db,
        db_engine: Engine,
        logical_step_name: str,
        state_machine_run_id: str,
        local_cache_dir: Path,
        s3_bucket_name: str,
        disable_cache: bool,
    ) -> None:
        self.db = db
        self.db_engine = db_engine
        self.disable_cache = disable_cache
        self.cacher = Cacher(
            logical_step_name, state_machine_run_id, local_cache_dir, s3_bucket_name
        )

        pass

    def df_query(self, query_str: str, rebuild_cache: bool) -> pd.DataFrame:
        return self._with_cacher(self._df_query, query_str, rebuild_cache)

    def _df_query(self, query_str: str) -> pd.DataFrame:
        # For pandas 2.2.0
        # https://stackoverflow.com/a/77949093

        # Debugging
        print(query_str)
        print(self.db_engine)
        with self.db_engine.connect() as conn:
            return pd.read_sql(query_str, conn.connection)

    def query_one(self, query_str: str, rebuild_cache: bool):
        return self._with_cacher(self._query_one, query_str, rebuild_cache)

    def _query_one(self, query_str: str):
        return self.db.execute(query_str).fetchone()

    def query_all(self, query_str: str, rebuild_cache: bool):
        return self._with_cacher(self._query_all, query_str, rebuild_cache)

    def _query_all(self, query_str: str):
        return self.db.execute(query_str).fetchall()

    def _with_cacher(self, query_func, query_str: str, rebuild_cache: bool):
        if self.disable_cache and not rebuild_cache:
            return query_func(query_str)
        elif self.cacher.exists(query_str) and not rebuild_cache:
            return self.cacher.from_cache(query_str)
        else:
            result = query_func(query_str)

            self.cacher.to_cache(query_str, result)

            return result
