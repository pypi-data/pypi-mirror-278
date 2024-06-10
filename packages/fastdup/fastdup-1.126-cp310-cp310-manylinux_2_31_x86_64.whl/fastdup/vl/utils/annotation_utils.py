import json
import typing
from typing import Optional, List

import pandas as pd
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate
from pydantic import BaseModel

from fastdup.vl.common import logging_init

logger = logging_init.get_vl_logger(__name__)


def normalize_bbox(scale_factor, col_x, row_y, width, height):
    return tuple(dim * scale_factor for dim in (int(col_x), int(row_y), int(width), int(height)))


class AnnotatedBoundingBox(BaseModel):
    col_x: int
    row_y: int
    width: int
    height: int
    annotations: List[str]


class AnnotationsMap:
    images_table_data: Optional[pd.DataFrame] = None
    objects_table_data: Optional[pd.DataFrame] = None

    def load_single_table_data(self, data: pd.DataFrame):
        if is_objects_annotations(data):
            self.objects_table_data = data
        else:
            self.images_table_data = data

    def load_from_json_data(self, data):
        image_id_to_filename = {img['id']: img['file_name'] for img in data['images']}
        category_id_to_label = {category['id']: category['name'] for category in data['categories']}

        image_annotations = []
        object_annotations = []

        for annotation in data['annotations']:
            image_id = annotation['image_id']
            category_id = annotation['category_id']
            filename = image_id_to_filename[image_id]
            label = category_id_to_label[category_id]

            if 'bbox' in annotation:
                col_x, row_y, width, height = annotation['bbox']
                object_annotations.append({
                    'filename': filename,
                    'col_x': col_x,
                    'row_y': row_y,
                    'width': width,
                    'height': height,
                    'label': label
                })
            else:
                image_annotations.append({
                    'filename': filename,
                    'label': label
                })

        self.images_table_data = pd.DataFrame(image_annotations)
        self.objects_table_data = pd.DataFrame(object_annotations)

    def check_duplicates(self) -> bool:
        return (self.images_table_data is not None and self.images_table_data.duplicated().any()) \
            or (self.objects_table_data is not None and self.objects_table_data.duplicated().any())

    def get_image_labels_from_filename(self, filename: str):
        if self.images_table_data is None:
            return []
        labels = self.images_table_data.loc[self.images_table_data['filename'] == filename, 'label'].tolist()
        return labels

    def get_object_labels_from_filename(self, filename: str, scale_factor: float):
        if self.objects_table_data is None:
            return []

        filtered_by_filename = self.objects_table_data[self.objects_table_data['filename'] == filename]

        grouped_by_bbx = filtered_by_filename.groupby(['col_x', 'row_y', 'width', 'height'])['label'].apply(list)

        object_annotations = []

        for (col_x, row_y, width, height), labels in grouped_by_bbx.items():
            col_x, row_y, width, height = normalize_bbox(scale_factor, col_x, row_y, width, height)

            annotated_bbox = AnnotatedBoundingBox(
                col_x=col_x,
                row_y=row_y,
                width=width,
                height=height,
                annotations=labels
            )
            object_annotations.append(annotated_bbox)

        return object_annotations


COCO_SCHEMA = {
    "type": "object",
    "properties": {
        "images": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "file_name": {"type": "string"}
                },
                "required": ["id", "file_name"]
            }
        },
        "categories": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"}
                },
                "required": ["id", "name"]
            }
        },
        "annotations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "image_id": {"type": "integer"},
                    "category_id": {"type": "integer"},
                    "bbox": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 4,
                        "maxItems": 4
                    }
                },
                "required": ["id", "image_id", "category_id"]
            }
        }
    },
    "required": ["images", "categories", "annotations"]
}


def validate_json_file(file: typing.BinaryIO) -> tuple[bool, Optional[AnnotationsMap], Optional[str]]:
    """
    returns a tuple of [is_valid, data, message]
    """
    try:
        content = file.read()
        data = json.loads(content)

        validate(instance=data, schema=COCO_SCHEMA)

        annotations = AnnotationsMap()
        annotations.load_from_json_data(data)

        if annotations.check_duplicates():
            return True, annotations, 'Annotations contain duplicate rows'

        return True, annotations, None

    except json.decoder.JSONDecodeError as e:
        logger.error(e, exc_info=True)
        return False, None, 'Invalid JSON file'
    except ValidationError as e:
        logger.error(e, exc_info=True)
        return False, None, 'Invalid COCO JSON format'


def check_required_columns(df, required_columns):
    return all(column in df.columns for column in required_columns)


def validate_table_file(
        file: typing.BinaryIO, file_format: str
) -> tuple[bool, Optional[typing.Any], Optional[str]]:
    def validate_df_format(df):
        return (
                check_required_columns(df, {"filename", "label"})
                or
                check_required_columns(df, {"filename", "col_x", "row_y", "width", "height", "label"})
        )

    try:
        file.seek(0)
        read_function = pd.read_csv if file_format == 'csv' else pd.read_parquet
        data = read_function(file)
    except Exception as e:
        logger.exception(e, exc_info=True)
        return False, None, 'Unreadable file'

    if validate_df_format(data):
        return True, data, None
    else:
        return False, data, f'Invalid {file_format} file format'


def is_objects_annotations(df) -> bool:
    return check_required_columns(df, {"filename", "col_x", "row_y", "width", "height", "label"})

