from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Session

from fastdup.vldbaccess.connection_manager import get_session
from fastdup.vldbaccess.dataset import DatasetDB


def create_and_fill_partition(dataset_id: UUID):
    with get_session(autocommit=True) as session:
        dialect = session.bind.dialect.name
        if dialect == "postgresql":
            create_and_fill_partition_pg(dataset_id, session)
        elif dialect == "duckdb":
            create_and_fill_partition_duckdb(dataset_id, session)
        else:
            raise NotImplementedError(f"Unsupported dialect {dialect}")


def create_and_fill_partition_duckdb(dataset_id: UUID, session: Session):
    # TODO: remove duplication
    partition_name = "flat_similarity_clusters"
    session.execute(sa.text(
        """
    WITH -- fill partition {dataset_id} images
    clusers_and_images AS (
        SELECT
            images.image_uri,
            images.id as image_id,
            images.metadata,
            images.original_uri,
            NULL::int[] as bounding_box,
            images_to_similarity_clusters.image_id image_or_object_id,
            images_to_similarity_clusters.cluster_id,
            images_to_similarity_clusters.dataset_id,
            images_to_similarity_clusters.preview_order,
            similarity_clusters.display_name,
            similarity_clusters.cluster_type,
            similarity_clusters.n_images,
            similarity_clusters.n_objects,
            similarity_clusters.size_bytes,
            similarity_clusters.similarity_threshold,
            similarity_clusters.formed_by,
            images.dir_path
        FROM
            similarity_clusters,
            images_to_similarity_clusters,
            images
        WHERE
            similarity_clusters.dataset_id = :dataset_id
            AND images_to_similarity_clusters.dataset_id = :dataset_id
            AND images.dataset_id = :dataset_id
            AND similarity_clusters.id = images_to_similarity_clusters.cluster_id
            AND images.id = images_to_similarity_clusters.image_id
    ),
    images_and_issues AS (
        SELECT
            image_issues.image_id as image_or_object_id,
            list(distinct image_issues.type_id) issue_type_ids
        FROM
        image_issues
        WHERE image_issues.type_id is not null
        AND image_issues.cause is null
        AND image_issues.dataset_id = :dataset_id
        GROUP BY image_issues.image_id
    ),
    images_and_labels AS (
        SELECT
            labels.image_id image_or_object_id,
            list_distinct(list(CASE WHEN labels.source = 'USER' THEN labels.category_display_name END)) AS labels,
            list_distinct(list(CASE WHEN labels.source = 'VL' THEN labels.category_display_name END)) AS vl_labels
        FROM
            labels
        WHERE
            labels.category_display_name is not null
            AND labels.bounding_box is null
            AND labels.dataset_id = :dataset_id
        GROUP BY
            labels.image_id
    ),
    clusters_union AS (
        SELECT
            clusers_and_images.*,
            images_and_labels.labels,
            images_and_labels.vl_labels,
            images_and_issues.issue_type_ids
        FROM
            clusers_and_images
            LEFT JOIN images_and_issues ON clusers_and_images.image_id = images_and_issues.image_or_object_id
            LEFT JOIN images_and_labels ON clusers_and_images.image_id = images_and_labels.image_or_object_id
    ),
    clusters_union_with_captions AS (
        SELECT
            clusters_union.*,
            media_to_captions.caption
        FROM
            clusters_union
            LEFT JOIN media_to_captions ON clusters_union.image_or_object_id = media_to_captions.media_id
    ),
    clusters_ranked_by_preview_order AS (
        SELECT *, rank() OVER (PARTITION BY cluster_id ORDER BY preview_order) rank
        FROM clusters_union_with_captions
    )
    INSERT INTO flat_similarity_clusters (
        SELECT
            image_uri,
            image_id,
            metadata,
            original_uri,
            bounding_box,
            image_or_object_id,
            cluster_id,
            dataset_id,
            preview_order,
            display_name,
            cluster_type,
            n_images,
            n_objects,
            size_bytes,
            similarity_threshold,
            labels,
            issue_type_ids,
            caption,
            rank,
            formed_by,
            dir_path,
            vl_labels
        FROM
            clusters_ranked_by_preview_order
    );  

        """.format(partition_name=partition_name, dataset_id=dataset_id)),
        {'dataset_id': dataset_id}
    )
    session.execute(sa.text(
        """
            WITH -- fill partition {dataset_id} objects
    clusters_and_objects AS (
        SELECT DISTINCT on (objects_to_similarity_clusters.cluster_id, objects_to_similarity_clusters.object_id)
            images.image_uri,
            images.id AS image_id,
            images.metadata,
            images.original_uri,
            objects_to_images.bounding_box,
            objects_to_similarity_clusters.object_id image_or_object_id,
            objects_to_similarity_clusters.cluster_id,
            objects_to_similarity_clusters.dataset_id,
            objects_to_similarity_clusters.preview_order,
            similarity_clusters.display_name,
            similarity_clusters.cluster_type,
            similarity_clusters.n_images,
            similarity_clusters.n_objects,
            similarity_clusters.size_bytes,
            similarity_clusters.similarity_threshold,
            similarity_clusters.formed_by,
            objects_to_images.dir_path
        FROM
            similarity_clusters,
            objects_to_similarity_clusters,
            objects_to_images,
            images
        WHERE
            similarity_clusters.id = objects_to_similarity_clusters.cluster_id
            AND objects_to_similarity_clusters.object_id = objects_to_images.object_id
            AND objects_to_images.image_id = images.id
            AND similarity_clusters.dataset_id = :dataset_id
            AND objects_to_similarity_clusters.dataset_id = :dataset_id
            AND objects_to_images.dataset_id = :dataset_id
            AND images.dataset_id = :dataset_id
    ),
    objects_and_issues AS (
        SELECT
            image_issues.cause as object_id,
            list(distinct image_issues.type_id) issue_type_ids
        FROM
            image_issues
        WHERE
        	image_issues.type_id is not null
            AND image_issues.dataset_id = :dataset_id
            AND image_issues.cause IS NOT NULL
        GROUP BY
            image_issues.cause
    ),
    objects_and_labels AS (
        SELECT
            objects_to_images.object_id,
            list_distinct(list(CASE WHEN labels.source = 'USER' THEN labels.category_display_name END)) AS labels,
            list_distinct(list(CASE WHEN labels.source = 'VL' THEN labels.category_display_name END)) AS vl_labels
        FROM labels
        JOIN objects_to_images ON objects_to_images.object_id = labels.id
        WHERE labels.category_display_name is not NULL
        AND labels.dataset_id = :dataset_id
        AND objects_to_images.dataset_id = :dataset_id
        GROUP BY objects_to_images.object_id
    ),
    clusters_union AS (
        SELECT
            clusters_and_objects.*,
            objects_and_labels.labels,
            objects_and_labels.vl_labels,
            objects_and_issues.issue_type_ids
        FROM
            clusters_and_objects
            LEFT JOIN objects_and_issues ON clusters_and_objects.image_or_object_id = objects_and_issues.object_id
            LEFT JOIN objects_and_labels ON clusters_and_objects.image_or_object_id = objects_and_labels.object_id
    ),
    clusters_union_with_captions AS (
        SELECT
            clusters_union.*,
            media_to_captions.caption
        FROM
            clusters_union
            LEFT JOIN media_to_captions ON clusters_union.image_or_object_id = media_to_captions.media_id
    ),
    clusters_ranked_by_preview_order AS (
        SELECT *, rank() OVER (PARTITION BY cluster_id ORDER BY preview_order) rank
        FROM clusters_union_with_captions
    )
    INSERT INTO flat_similarity_clusters (
        SELECT
            image_uri,
            image_id,
            metadata,
            original_uri,
            bounding_box,
            image_or_object_id,
            cluster_id,
            dataset_id,
            preview_order,
            display_name,
            cluster_type,
            n_images,
            n_objects,
            size_bytes,
            similarity_threshold,
            labels,
            issue_type_ids,
            caption,
            rank,
            formed_by,
            dir_path,
            vl_labels
        FROM
            clusters_ranked_by_preview_order
    );
        """.format(partition_name=partition_name, dataset_id=dataset_id)),
        {'dataset_id': dataset_id}
    )
    # recreate FTS index
    session.execute(
        sa.text("""
        PRAGMA create_fts_index(
            flat_similarity_clusters, image_or_object_id, caption, labels, vl_labels, stemmer='porter',
            stopwords='english', ignore='(\\.|[^a-z])+',
            strip_accents=1, lower=1, overwrite=1
        );
        """)
    )


def create_and_fill_partition_pg(dataset_id: UUID, session: Session):
    partition_name = DatasetDB.flat_partition_name(dataset_id)
    check_name = f'{partition_name}_chk'

    # drop partition if exists
    with session.begin(nested=True):
        DatasetDB.remove_partition(dataset_id, session)
    # create partition
    with session.begin(nested=True):
        session.execute(
            sa.text(f"""
            CREATE TABLE {partition_name}
            (LIKE flat_similarity_clusters INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
            """)
        )
        session.execute(sa.text(f"""
            ALTER TABLE {partition_name} ADD CONSTRAINT {check_name} CHECK (dataset_id='{dataset_id}')
            """), {'dataset_id': dataset_id})
    # insert into partition
    with session.begin(nested=True):
        session.execute(sa.text("SET enable_nestloop TO off;"))
        session.execute(sa.text(
            """
    WITH -- fill partition {dataset_id}
    clusers_and_images AS (
        SELECT
            images.image_uri,
            images.id as image_id,
            images.metadata,
            images.original_uri,
            NULL::int[] as bounding_box,
            images_to_similarity_clusters.image_id image_or_object_id,
            images_to_similarity_clusters.cluster_id,
            images_to_similarity_clusters.dataset_id,
            images_to_similarity_clusters.preview_order,
            similarity_clusters.display_name,
            similarity_clusters.cluster_type,
            similarity_clusters.n_images,
            similarity_clusters.n_objects,
            similarity_clusters.size_bytes,
            similarity_clusters.similarity_threshold,
            similarity_clusters.formed_by,
            images.dir_path
        FROM
            similarity_clusters,
            images_to_similarity_clusters,
            images
        WHERE
            similarity_clusters.dataset_id = :dataset_id
            AND images_to_similarity_clusters.dataset_id = :dataset_id
            AND images.dataset_id = :dataset_id
            AND similarity_clusters.id = images_to_similarity_clusters.cluster_id
            AND images.id = images_to_similarity_clusters.image_id
    ),
    image_labels AS (
        SELECT
            image_id,
            source,
            category_display_name
        FROM
            labels
        WHERE
            labels.dataset_id = :dataset_id
            AND bounding_box IS null
    ),
    images_and_issues AS (
        SELECT
            images.id image_or_object_id,
            array_remove(array_agg(DISTINCT image_issues.type_id), NULL) issue_type_ids
        FROM
            images,
            image_issues
        WHERE
            image_issues.cause IS NULL
            AND images.id = image_issues.image_id
            AND images.dataset_id = :dataset_id
            AND image_issues.dataset_id = :dataset_id
        GROUP BY
            images.id
    ),
    images_and_labels AS (
        SELECT
            images.id image_or_object_id,
            array_remove(array_agg(CASE WHEN image_labels.source = 'USER' THEN image_labels.category_display_name ELSE NULL END), NULL) AS labels,
            array_remove(array_agg(CASE WHEN image_labels.source = 'VL' THEN image_labels.category_display_name ELSE NULL END), NULL) AS vl_labels
        FROM
            images,
            image_labels
        WHERE
            images.id = image_labels.image_id
            AND images.dataset_id = :dataset_id
        GROUP BY
            images.id
    ),
    clusters_and_objects AS (
        SELECT DISTINCT on (objects_to_similarity_clusters.cluster_id, objects_to_similarity_clusters.object_id)
            images.image_uri,
            images.id AS image_id,
            images.metadata,
            images.original_uri,
            objects_to_images.bounding_box,
            objects_to_similarity_clusters.object_id image_or_object_id,
            objects_to_similarity_clusters.cluster_id,
            objects_to_similarity_clusters.dataset_id,
            objects_to_similarity_clusters.preview_order,
            similarity_clusters.display_name,
            similarity_clusters.cluster_type,
            similarity_clusters.n_images,
            similarity_clusters.n_objects,
            similarity_clusters.size_bytes,
            similarity_clusters.similarity_threshold,
            similarity_clusters.formed_by,
            objects_to_images.dir_path
        FROM
            similarity_clusters,
            objects_to_similarity_clusters,
            objects_to_images,
            images
        WHERE
            similarity_clusters.id = objects_to_similarity_clusters.cluster_id
            AND objects_to_similarity_clusters.object_id = objects_to_images.object_id
            AND objects_to_images.image_id = images.id
            AND similarity_clusters.dataset_id = :dataset_id
            AND objects_to_similarity_clusters.dataset_id = :dataset_id
            AND objects_to_images.dataset_id = :dataset_id
            AND images.dataset_id = :dataset_id
    ),
    objects_and_issues AS (
        SELECT
            objects_to_images.object_id,
            array_remove(array_agg(DISTINCT image_issues.type_id), NULL) issue_type_ids
        FROM
            objects_to_images,
            image_issues
        WHERE
            objects_to_images.object_id = image_issues.cause
            AND objects_to_images.dataset_id = :dataset_id
            AND image_issues.dataset_id = :dataset_id
            AND image_issues.cause IS NOT NULL
        GROUP BY
            objects_to_images.object_id
    ),
    objects_and_labels AS (
        SELECT
            objects_to_images.object_id,
            array_remove(array_agg(CASE WHEN labels.source = 'USER' THEN labels.category_display_name ELSE NULL END), NULL) AS labels,
            array_remove(array_agg(CASE WHEN labels.source = 'VL' THEN labels.category_display_name ELSE NULL END), NULL) AS vl_labels
        FROM
            objects_to_images,
            labels
        WHERE
            objects_to_images.object_id = labels.id
            AND objects_to_images.dataset_id = :dataset_id
            AND labels.dataset_id = :dataset_id
        GROUP BY
            objects_to_images.object_id
    ),
    clusters_union AS (
        SELECT
            clusers_and_images.*,
            images_and_labels.labels,
            images_and_labels.vl_labels,
            images_and_issues.issue_type_ids
        FROM
            clusers_and_images
            LEFT JOIN images_and_issues ON clusers_and_images.image_id = images_and_issues.image_or_object_id
            LEFT JOIN images_and_labels ON clusers_and_images.image_id = images_and_labels.image_or_object_id
        UNION ALL
        SELECT
            clusters_and_objects.*,
            objects_and_labels.labels,
            objects_and_labels.vl_labels,
            objects_and_issues.issue_type_ids
        FROM
            clusters_and_objects
            LEFT JOIN objects_and_issues ON clusters_and_objects.image_or_object_id = objects_and_issues.object_id
            LEFT JOIN objects_and_labels ON clusters_and_objects.image_or_object_id = objects_and_labels.object_id
    ),
    clusters_union_with_captions AS (
        SELECT
            clusters_union.*,
            media_to_captions.caption
        FROM
            clusters_union
            LEFT JOIN media_to_captions ON clusters_union.image_or_object_id = media_to_captions.media_id
    ),
    clusters_ranked_by_preview_order AS (
        SELECT *, rank() OVER (PARTITION BY cluster_id ORDER BY preview_order) rank
        FROM clusters_union_with_captions
    )
    INSERT INTO {partition_name} (
        SELECT
            image_uri,
            image_id,
            metadata,
            original_uri,
            bounding_box,
            image_or_object_id,
            cluster_id,
            dataset_id,
            preview_order,
            display_name,
            cluster_type,
            n_images,
            n_objects,
            size_bytes,
            similarity_threshold,
            labels,
            issue_type_ids,
            caption,
            rank,
            formed_by,
            dir_path,
            vl_labels
        FROM
            clusters_ranked_by_preview_order
    );
            """.format(partition_name=partition_name, dataset_id=dataset_id)),
            {'dataset_id': dataset_id}
        )
        session.execute(sa.text("SET enable_nestloop TO on;"))

    with session.begin(nested=True) as _tx:
        session.execute(
            sa.text("""
            ALTER TABLE flat_similarity_clusters ATTACH PARTITION {partition_name} FOR VALUES IN ('{dataset_id}');
            """.format(partition_name=partition_name, dataset_id=dataset_id))
        )
