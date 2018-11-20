from typing import Union

from sqlalchemy.orm.exc import NoResultFound

from racket.managers.server import ServerManager
from racket.managers.version import VersionManager
from racket.models import db
from racket.models.base import MLModelInputs, MLModel, ModelScores
from racket.models.exceptions import ModelNotFoundError
from racket.operations.utils import merge_and_unfold
from racket.utils import dict_tabulate


def deactivate() -> None:
    app = ServerManager.create_app('prod', False)
    with app.app_context():
        try:
            active = db.session.query(MLModel).filter(MLModel.active == True).one()  # NOQA
        except NoResultFound:
            return
        active.active = False
        db.session.commit()


def activate(model_id: int) -> None:
    app = ServerManager.create_app('prod', False)
    with app.app_context():
        active = db.session.query(MLModel).filter(MLModel.model_id == model_id).one()
        active.active = True
        db.session.commit()


def active_model_(name: bool = None, scores: bool = False) -> Union[str, dict]:
    """
    Query the model id of the currently active model
    Returns
    -------
    str
        Unique model identifier
    """

    app = ServerManager.create_app('prod', False)
    with app.app_context():
        active = db.session.query(MLModel).filter(MLModel.active == True).one()  # NOQA
        if scores:
            return db.session.query(MLModel, ModelScores).filter(MLModel.model_id == active.model_id) \
                .filter(ModelScores.model_id == MLModel.model_id) \
                .all()
        if name:
            active = db.session.query(MLModel.model_name).filter(MLModel.model_id == active.model_id).one()
            return active[0]
        return active.as_dict()


def determine_current_schema() -> dict:
    """
    Get the input specification of the currently active model
    Returns
    -------
    dict: dictionary of the specs
    """
    app = ServerManager.create_app('prod', False)
    model = active_model_()
    with app.app_context():
        schema = db.session.query(MLModelInputs).filter(MLModelInputs.model_id == model).one()
    return schema


def query_by_id_(model_id: int, scores: bool = False) -> MLModel:
    app = ServerManager.create_app('prod', False)
    with app.app_context():
        if scores:
            return db.session.query(MLModel, ModelScores).filter(MLModel.model_id == model_id) \
                .filter(ModelScores.model_id == MLModel.model_id) \
                .all()
        servable = db.session.query(MLModel).filter(MLModel.model_id == model_id).one_or_none()
        if not servable:
            raise ModelNotFoundError(f'The model requested with id {model_id} was not found in the database')
        return servable


def model_filterer_(name, version, m_type):
    fs = []
    if name:
        fs.append(MLModel.model_name == name)
    if version:
        c, v = VersionManager.parse_cli_v(version)
        fs.append(getattr(MLModel, c) == v)
    if m_type:
        fs.append(MLModel.model_type == m_type)
    app = ServerManager.create_app('prod', False)
    with app.app_context():
        query = db.session.query(MLModel, ModelScores) \
            .filter(*fs)
        return query.all()


def query_all_():
    app = ServerManager.create_app('prod', False)
    with app.app_context():
        query = db.session.query(MLModel, ModelScores) \
            .filter(MLModel.model_id == ModelScores.model_id)
        return query.all()


def list_models(name: str = None, version: str = None, m_type: str = None, active: bool = None, model_id: int = None):
    """List available models, filtering and sorting as desired

    Examples
    --------

    Running::

        $ racket ls -a  # returns the active model's metadata

    Will return::

          model_id  model_name      major    minor    patch    version_dir  active    created_at                  model_type    scoring_fn            score
        ----------  ------------  -------  -------  -------  -------------  --------  --------------------------  ------------  ------------------  -------
                 1  base                0        1        0              1  True      2018-11-14 22:53:52.455635  regression    loss                9378.25
                 1  base                0        1        0              1  True      2018-11-14 22:53:52.455635  regression    mean_squared_error  9378.25


    """
    if active:
        dict_tabulate(merge_and_unfold(active_model_(scores=True), filter_keys=['id']))
        return

    if model_id:
        dict_tabulate(merge_and_unfold(query_by_id_(model_id, scores=True), filter_keys=['id']))
        return

    if any([name, m_type, version]):
        result_set = model_filterer_(name, version, m_type)
        dict_tabulate(merge_and_unfold(result_set, filter_keys=['id']))
        return

    return dict_tabulate(merge_and_unfold(query_all_()))
