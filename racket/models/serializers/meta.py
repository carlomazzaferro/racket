from racket.models import db
from racket.models.base import MLModel, ModelScores
from racket.operations.schema import activate
from racket.managers.server import ServerManager
from racket.models.serializers.base import ModelSerializer
from racket.utils import Printer as p


class MetadataSerializer(ModelSerializer):

    def __init__(self, path: str, model_name: str):
        super().__init__(path, model_name)

    def store(self, historic_scores: dict, sql: MLModel) -> None:
        app = ServerManager.create_app('prod', False)
        with app.app_context():
            db.session.add(sql)
            db.session.commit()
            activate(sql.model_id)
            for scoring_function, score in historic_scores.items():
                obj = db.session.query(MLModel).order_by(MLModel.model_id.desc()).first()
                # noinspection PyArgumentList
                scoring_entry = ModelScores(model_id=obj.model_id, scoring_fn=scoring_function, score=score)
                db.session.add(scoring_entry)
            db.session.commit()
            p.print_success(f'Successfully stored metadata for model: {self.model_name}')

