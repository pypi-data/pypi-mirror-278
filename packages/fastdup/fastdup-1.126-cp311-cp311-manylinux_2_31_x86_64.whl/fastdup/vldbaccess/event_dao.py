from uuid import UUID

import sqlalchemy as sa

from fastdup.vldbaccess.models import events
from fastdup.vldbaccess.connection_manager import get_session, get_engine_dialect


class EventDAO:

    @staticmethod
    def store(event: events.Event) -> None:
        if get_engine_dialect() == 'duckdb':
            return
        with get_session(autocommit=True) as session:
            sequence_name = f'event_seq_{event.dataset_id}'.replace('-', '_')
            session.execute(
                sa.text(f'CREATE SEQUENCE IF NOT EXISTS {sequence_name} MINVALUE 0 START WITH 0;')
            )
            session.execute(
                sa.text(
                    '''
                    INSERT INTO events (serial_n, dataset_id, event_type, event)
                    VALUES (nextval(:sequence_name), :dataset_id, :event_type, (:event)::jsonb);
                    '''
                ),
                {
                    'sequence_name': sequence_name,
                    'dataset_id': event.dataset_id,
                    'event_type': event.event_type,
                    'event': event.json()
                }
            )

    @staticmethod
    def load(dataset_id: UUID, offset: int = 0) -> list[events.Event]:
        if get_engine_dialect() == 'duckdb':
            return []
        with get_session() as session:
            res_events: list[events.Event] = []
            query_result = session.execute(
                sa.text(
                    '''
                    SELECT
                        *
                    FROM
                        events 
                    WHERE
                        dataset_id = :dataset_id 
                        AND serial_n >= :offset 
                    ORDER BY
                        serial_n;
                    '''
                ),
                {'dataset_id': dataset_id, 'offset': offset}
            )
            for row in query_result.mappings().all():
                event_type = row['event_type']
                event_class = getattr(events, event_type)
                event_instance: events.Event = event_class(**row['event'])
                event_instance.serial = row['serial_n']
                res_events.append(event_instance)

        return res_events

    @staticmethod
    def load_by_event_type(
            dataset_id: UUID,
            event_type: str,
    ) -> list:
        if get_engine_dialect() == 'duckdb':
            return []
        with get_session() as session:
            query = sa.text(
                '''
                SELECT
                    *
                FROM
                    events 
                WHERE
                    dataset_id = :dataset_id 
                    AND event_type = :event_type
                ORDER BY
                    serial_n
                '''
            )
            query_result = session.execute(
                query,
                {'dataset_id': dataset_id, 'event_type': event_type}
            )
            res_events: list[events.S3MediaPreview] = []
            event_class = getattr(events, event_type)
            for row in query_result.mappings().all():
                event_instance = event_class(**row['event'])
                event_instance.serial = row['serial_n']
                res_events.append(event_instance)

        return res_events
