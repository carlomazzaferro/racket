import os
import ast
import json
from typing import Union, List, Dict

from racket.managers.server import ServerManager
from racket.managers.version import VersionManager
from racket.managers.project import ProjectManager
from racket.models import db
from racket.models.base import MLModel, ModelScores, ActiveModel
from racket.models.exceptions import ModelNotFoundError
from racket.operations.utils import merge_and_unfold, unfold


def activate(model_id: int) -> None:
    app = ServerManager.create_app('prod', False)
    with app.app_context():
        active = db.session.query(ActiveModel).first()
        active.model_id = model_id
        db.session.commit()


def active_model_name_():
    app = ServerManager.create_app('prod', False)
    with app.app_context():
        active = __active()
        active = db.session.query(MLModel.model_name).filter(MLModel.model_id == active.model_id).one()
        return active[0]


def active_model_(scores: bool = False) -> Union[MLModel, List[MLModel]]:
    """
    Query the model id of the currently active model

    Returns
    -------
    active model
        Unique model identifier
    """

    app = ServerManager.create_app('prod', False)
    with app.app_context():
        active = __active()
        if scores:
            return db.session.query(MLModel, ModelScores).filter(MLModel.model_id == active.model_id) \
                .filter(ModelScores.model_id == MLModel.model_id) \
                .all()
        return active


def __active() -> ActiveModel:
    app = ServerManager.create_app('prod', False)
    with app.app_context():
        active_id = db.session.query(ActiveModel).first()
        active = db.session.query(MLModel).filter(MLModel.model_id == active_id.model_id).one()  # NOQA
        return active


def current_schema_() -> dict:
    # TODO: implement this
    """
    Get the input specification of the currently active model

    Returns
    -------
    schema: dict
        Dictionary of the specs

    app = ServerManager.create_app('prod', False)
    model = active_model_()
    with app.app_context():
        schema = db.session.query(MLModelInputs).filter(MLModelInputs.model_id == model).one()
    return schema
    """
    raise NotImplementedError


def query_by_id_(model_id: int, scores: bool = False) -> Union[List, MLModel]:
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


def model_filterer_(name: str = None, version: str = None, m_type: str = None, scores: bool = False) -> list:
    fs = []
    if name:
        fs.append(MLModel.model_name == name)
    if version:
        M, m, p = VersionManager.semantic_to_tuple(version)
        fs.append(MLModel.major == M)
        fs.append(MLModel.minor == m)
        fs.append(MLModel.patch == p)
    if m_type:
        fs.append(MLModel.model_type == m_type)
    app = ServerManager.create_app('prod', False)
    with app.app_context():
        if scores:
            return db.session.query(MLModel, ModelScores).filter(*fs) \
                .filter(ModelScores.model_id == MLModel.model_id) \
                .all()
        return db.session.query(MLModel).filter(*fs).all()


def query_all_(scores: bool = False) -> list:
    """
    Query all the models and their associated scores

    Parameters
    ----------
    scores: bool
        If true, return the models alongside with its associated scores

    Returns
    -------
    models: list
        List of models

    """
    app = ServerManager.create_app('prod', False)
    with app.app_context():
        if scores:
            query = db.session.query(MLModel, ModelScores) \
                .filter(MLModel.model_id == ModelScores.model_id)
        else:
            query = db.session.query(MLModel)
        return query.all()


def historic_scores_(model_id: int = None, name: str = None, version: str = None) -> Dict:
    """
    Get the historic scores for a model, in the form of::

        { val_loss: [...], val_acc: [..], acc: [...], loss: [...] }

    Where the arrays are the respective measures at the end of each epoch

    Parameters
    ----------
    version : str
        Model version in the format: "major.minor.patch". Ignored if model_id is passed
    name : str
        Name of the model. Must be provided if version is provided. Ignored if model_id is passed
    model_id : int
        Unique ID of the model

    Returns
    -------
    scores: dict
        Dictionary of key: score name, value: score array
    """

    model = _model_from_name_ver_id(model_id, name, version)
    base_path = ProjectManager.get_value('saved-models')
    hs_path = os.path.join(base_path, model.model_name + '_' + 'history' + '_' + model.version_dir + '.json')
    with open(hs_path, 'r') as scores:
        return json.load(scores)


def query_scores_(model_id: int = None, name: str = None, version: str = None) -> List:
    """
    Query model scores by model_id or model name, version

    Parameters
    ----------
    version : str
        Model version in the format: "major.minor.patch". Ignored if model_id is passed
    name : str
        Name of the model. Must be provided if version is provided. Ignored if model_id is passed
    model_id : int
        Unique ID of the model

    Returns
    -------
    models: List
        List of model scores
    """
    model = _model_from_name_ver_id(model_id, name, version)
    return db.session.query(ModelScores).filter(ModelScores.model_id == model.model_id).all()


def _model_from_name_ver_id(model_id: int = None, name: str = None, version: str = None) -> MLModel:
    if model_id:
        model = query_by_id_(model_id, scores=False)
    else:
        try:
            model = model_filterer_(name, version, scores=False)[0]
        except IndexError:
            model = []
    if not model:
        raise ValueError(f'No models with name: {name}, version: {version}, or id: {model_id} found')
    return model


def query_params_(model_id: int = None, name: str = None, version: str = None) -> Dict:
    """
    Query model parameters by model_id or model name, version

    Parameters
    ----------
    version : str
        Model version in the format: "major.minor.patch". Ignored if model_id is passed
    name : str
        Name of the model. Must be provided if version is provided. Ignored if model_id is passed
    model_id : int
        Unique ID of the model

    Returns
    -------
    models: dict
        Parameters of the model as dictionary
    """
    model = _model_from_name_ver_id(model_id, name, version)
    return ast.literal_eval(model.as_dict()['parameters'])


def list_models(name: str = None,
                version: str = None,
                m_type: str = None,
                active: bool = False,
                model_id: int = None,
                unique: bool = False) -> List[dict]:
    """
    List available models, filtering and sorting as desired

    Parameters
    ----------
    name : str
        Name of te model

    version : str
        Version of the mode, such as '1.1.0'

    m_type : str
        Model type, usually either `regression` or `classification`

    active : bool
        Flag to query the active model. All other flags will be ignored if this is passed

    model_id : int
        The id of the model to be queried. All other flags will be ignored if this is passed

    unique: bool
        Return only a single entry for each model, disregarding potential duplicate entries due to
        multiple scoring functions being used


    Returns
    -------
    List[dict]
        Results is printed to stdout
    """
    scores = not unique
    result_set = None

    if not all([model_id, name, version, m_type, active]):
        result_set = query_all_(scores=scores)

    if active:
        result_set = active_model_(scores=scores)

    if model_id:
        result_set = query_by_id_(model_id, scores=scores)

    if any([name, m_type, version]):
        result_set = model_filterer_(name, version, m_type)
    if scores:
        return merge_and_unfold(result_set, filter_keys=['id'])
    else:
        return unfold([result_set] if not isinstance(result_set, list) else result_set, filter_keys=['id'])
