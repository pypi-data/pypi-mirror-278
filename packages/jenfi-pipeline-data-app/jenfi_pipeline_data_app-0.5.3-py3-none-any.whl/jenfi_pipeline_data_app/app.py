import os
import platform
import sys
import tempfile
from pathlib import Path


class Application:
    """
    .. include:: API.md

    """

    from .app_funcs._constants import (
        PYTHON_ENV,
        RESULT_FILENAME,
        ROOT_DIR,
        STATUS_INSUFFICIENT_DATA,
        STATUS_NO_RESULT,
        STATUS_NOT_APPLICABLE,
        STATUS_NOTEBOOK_NOT_FOUND_S3,
        STATUS_SUCCESS,
    )
    from .app_funcs._db_handler import _close_db, _db_config, _init_db
    from .app_funcs._exit_program import (
        exit_insufficient_data,
        exit_not_applicable,
        notebook_not_found_s3,
    )
    from .app_funcs._models_s3 import (
        _init_config_s3,
        load_model_from_s3,
        push_model_to_s3,
    )
    from .app_funcs._parameters import _run_data, get_parameter, load_test_parameters
    from .app_funcs._query import _db_cache, df_query, query_all, query_one
    from .app_funcs._result import (
        _add_run_metadata,
        _remove_results_tmpfile,
        _results_to_tmpfile,
        load_result,
        write_result,
        write_result_to_db,
    )

    def boot(self):
        """Sets up configs, db connections. It is run as part of the module import."""
        self._init_db()
        self._init_config_s3()
        self._remove_results_tmpfile()  # Any lingering files

    def cleanup(self):
        """Closes connections and cleans up any lingering items."""
        self._close_db()
        self._remove_results_tmpfile()

    def tmp_dir(self) -> Path:
        if self.PYTHON_ENV == "production":
            tmp_path = "/tmp"
        elif self.PYTHON_ENV == "staging":
            tmp_path = "/tmp"
        else:
            tmp_path = (
                "/tmp" if platform.system() == "Darwin" else tempfile.gettempdir()
            )

        return Path(tmp_path)

    def tmp_filepath(self, rel_filepath) -> Path:
        tmp_path = self.tmp_dir()
        file_path = Path(os.path.join(tmp_path, rel_filepath))

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        return file_path

    def __repr__(self):
        return self.__dict__

    if "pytest" in sys.modules:
        from .app_funcs._test_funcs import (
            _test_access_global_var,
            _test_direct_module,
            _test_set_global_var,
        )
