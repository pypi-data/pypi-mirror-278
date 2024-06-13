import contextlib

from amsdal.configs.main import settings
from amsdal_models.classes.constants import USER_MODELS_MODULE
from amsdal_models.classes.data_models.dependencies import DependencyModelNames
from amsdal_models.classes.errors import AmsdalClassNotFoundError
from amsdal_models.classes.helpers.reference_loader import ReferenceLoader
from amsdal_models.classes.manager import ClassManager
from amsdal_models.classes.utils import resolve_base_class_for_schema
from amsdal_models.classes.writer import ClassWriter
from amsdal_models.querysets.executor import LAKEHOUSE_DB_ALIAS
from amsdal_models.schemas.data_models.schema import ObjectSchema
from amsdal_utils.models.enums import SchemaTypes


def build_missing_models() -> list[str]:
    class_manager = ClassManager()
    class_writer = ClassWriter(settings.models_root_path)
    ClassObjectMeta = class_manager.import_class('ClassObjectMeta', SchemaTypes.CORE)  # noqa: N806
    model_names = DependencyModelNames.build_from_database()

    missed_models = []

    for object_meta in (
        ClassObjectMeta.objects.latest()  # type: ignore[attr-defined]
        .filter(
            _metadata__is_deleted=False,
        )
        .execute()
    ):
        class_object_object = ReferenceLoader(object_meta.get_metadata().class_meta_schema_reference).load_reference(
            using=LAKEHOUSE_DB_ALIAS
        )

        model = None
        for _schema_type in [SchemaTypes.USER, SchemaTypes.CONTRIB, SchemaTypes.CORE]:
            with contextlib.suppress(AmsdalClassNotFoundError):
                model = ClassManager().import_model_class(object_meta.title, _schema_type)

            if model:
                break

        if not model:
            missed_models.append(object_meta.title)

            dump = object_meta.model_dump()
            dump.update(class_object_object.model_dump())
            object_schema = ObjectSchema(**dump)

            class_writer.generate_model(
                schema=object_schema,
                schema_type=SchemaTypes.USER,
                base_class=resolve_base_class_for_schema(object_schema),
                model_names=model_names,
                sub_models_directory=USER_MODELS_MODULE,
            )

    return missed_models
