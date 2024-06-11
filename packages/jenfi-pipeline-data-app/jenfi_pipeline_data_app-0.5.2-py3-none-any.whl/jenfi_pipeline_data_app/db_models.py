import datetime
import os

from sqlalchemy import JSON, Column, DateTime, Integer, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict


# This shouldn't be a function, but I can't figure out how to pass a db_engine before the class creation on import.
# ATM, all classes will have to be loaded via function =\
#
# https://stackoverflow.com/questions/4215920/how-to-bind-engine-when-i-want-when-using-declarative-base-in-sqlalchemy
# The above is the same problem. It recommends using a DeferredRefelection, but that didn't work for me.
def state_machine_run_model(app):
    if _is_nellie():
        return _load_nellie_state_machine_run_model(app)
    else:
        return _load_core_state_machine_run_model(app)

def _load_nellie_state_machine_run_model(app):
    Base = declarative_base()
    metadata = MetaData(bind=app.db_engine)

    class NellieStateMachineRun(Base):
        __table__ = Table(
            "pipeline_statemachinerun",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("result", MutableDict.as_mutable(JSON)),
            Column("created", DateTime, default=datetime.datetime.now),
            Column("modified", DateTime, default=datetime.datetime.now),
            autoload=True,
        )

        def result_to_db(self, logical_step_name, state_machine_run_id, results):
            sm_run = (
                app.db.query(NellieStateMachineRun)
                .populate_existing()
                .with_for_update(of=NellieStateMachineRun, nowait=False)
                .get(state_machine_run_id)
            )
            sm_run.result[logical_step_name] = results

            return app.db.commit()

    return NellieStateMachineRun

def _load_core_state_machine_run_model(app):
    Base = declarative_base()
    metadata = MetaData(bind=app.db_engine)

    class StateMachineRun(Base):
        __table__ = Table(
            "pipeline_state_machine_runs",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("result", MutableDict.as_mutable(JSON)),
            Column("created_at", DateTime, default=datetime.datetime.now),
            Column("updated_at", DateTime, default=datetime.datetime.now),
            autoload=True,
        )

        def result_to_db(self, logical_step_name, state_machine_run_id, results):
            sm_run = (
                app.db.query(StateMachineRun)
                .populate_existing()
                .with_for_update(of=StateMachineRun, nowait=False)
                .get(state_machine_run_id)
            )
            sm_run.result[logical_step_name] = results

            return app.db.commit()

    return StateMachineRun

def _is_nellie():
    app_name = os.getenv("CORE_APP_NAME", None)
    if app_name is None:
        return False

    return app_name.startswith("Nellie")
