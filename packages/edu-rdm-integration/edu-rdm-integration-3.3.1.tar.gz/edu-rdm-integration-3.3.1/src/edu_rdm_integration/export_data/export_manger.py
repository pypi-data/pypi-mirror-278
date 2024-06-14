from datetime import (
    datetime,
)
from pathlib import (
    Path,
)
from typing import (
    List,
)

from django.conf import (
    settings,
)
from django.db.models import (
    F,
    Sum,
)
from django.db.transaction import (
    atomic,
)
from uploader_client.adapters import (
    adapter,
)

from educommon import (
    logger,
)

from edu_rdm_integration.consts import (
    LOGS_DELIMITER,
)
from edu_rdm_integration.enums import (
    FileUploadStatusEnum,
)
from edu_rdm_integration.export_data.base.consts import (
    OPERATIONS_METHODS_MAP,
    OPERATIONS_URLS_MAP,
)
from edu_rdm_integration.export_data.base.requests import (
    RegionalDataMartEntityRequest,
)
from edu_rdm_integration.export_data.consts import (
    TOTAL_ATTACHMENTS_SIZE_KEY,
)
from edu_rdm_integration.export_data.dataclasses import (
    UploadFile,
)
from edu_rdm_integration.export_data.queue import (
    Queue,
)
from edu_rdm_integration.models import (
    ExportingDataSubStage,
    ExportingDataSubStageAttachment,
    ExportingDataSubStageStatus,
    ExportingDataSubStageUploaderClientLog,
)
from edu_rdm_integration.redis_cache import (
    AbstractCache,
)


class ExportQueueSender:
    """Класс отправки данных в очередь РВД."""

    def __init__(self, data_cache: AbstractCache, queue: Queue):
        self.queue = queue
        self.cache = data_cache
        self.queue_total_file_size = self.cache.get(TOTAL_ATTACHMENTS_SIZE_KEY) or 0

    @staticmethod
    def get_exported_file_size() -> int:
        """Возвращает размер отправленных в РВД файлов.

        При расчете используются только файлы, отмеченные как отправленные, но не обработанные витриной.
        """
        sended_attachment_ids = ExportingDataSubStageUploaderClientLog.objects.filter(
            file_upload_status=FileUploadStatusEnum.IN_PROGRESS
        ).values_list('attachment_id', flat=True)
        file_size = ExportingDataSubStageAttachment.objects.filter(
            id__in=sended_attachment_ids
        ).aggregate(Sum('attachment_size'))['attachment_size__sum']

        return file_size or 0

    @staticmethod
    def get_sub_stages_attachments_to_export():
        """Выборка готовых к экспорту подэтапов."""
        return ExportingDataSubStage.objects.filter(
            status_id=ExportingDataSubStageStatus.READY_FOR_EXPORT.key
        ).annotate(
            attachment_id=F('exportingdatasubstageattachment__id'),
            attachment_name=F('exportingdatasubstageattachment__attachment'),
            attachment_size=F('exportingdatasubstageattachment__attachment_size'),
            operation=F('exportingdatasubstageattachment__operation'),
            entity=F('exportingdatasubstageentity__entity_id')
        ).order_by('started_at', 'operation').values(
            'id',
            'attachment_id',
            'attachment_name',
            'attachment_size',
            'operation',
            'entity',
        )

    def set_sub_stage_to_cache(self, sub_stage_id: int, entity_name: str, attachments: List[UploadFile]) -> bool:
        """Помещение подэтапа в очередь вместе с информацией по файлам и обновление счетчика объема файлов."""
        sub_stage_total_size = sum((attachment.attachment_size for attachment in attachments))
        if self.queue_total_file_size + sub_stage_total_size > settings.RDM_UPLOAD_QUEUE_MAX_SIZE:
            return False

        self.queue.enqueue(sub_stage_id, entity_name, attachments)
        self.queue_total_file_size += sub_stage_total_size
        # Обновим размер файлов в кеш
        self.cache.set(
            TOTAL_ATTACHMENTS_SIZE_KEY,
            self.queue_total_file_size,
            timeout=settings.RDM_REDIS_CACHE_TIMEOUT_SECONDS
        )

        return True

    def run(self):
        """Запуск работы менджера."""
        if not self.queue_total_file_size:
            self.queue_total_file_size = self.get_exported_file_size()

        if self.queue_total_file_size < settings.RDM_UPLOAD_QUEUE_MAX_SIZE:
            stage_files = []
            prev_sub_stage = None
            entity = ''
            # Если размер очереди позволяет - то отправляем все файлы подэтапа в очередь - иначе прерываем процесс
            for stage_attachment in self.get_sub_stages_attachments_to_export():
                if prev_sub_stage != stage_attachment['id']:
                    if stage_files:
                        to_cache = self.set_sub_stage_to_cache(prev_sub_stage, entity, stage_files)
                        logger.info(
                            f'ExportedDataSubStage {prev_sub_stage} {entity} added to the queue'
                        )
                        stage_files = []

                        if not to_cache:
                            break

                    prev_sub_stage = stage_attachment['id']

                if stage_attachment['attachment_size']:
                    stage_files.append(UploadFile(
                        stage_attachment['attachment_id'],
                        stage_attachment['attachment_name'],
                        stage_attachment['attachment_size'],
                        stage_attachment['operation']
                    ))
                    entity = stage_attachment['entity']

            # Обновляем общий объем очереди и закидываем последний элемент
            if stage_files:
                self.set_sub_stage_to_cache(prev_sub_stage, entity, stage_files)
        else:
            # Сохраняем объем отправленных файлов в кеш
            self.cache.set(
                TOTAL_ATTACHMENTS_SIZE_KEY,
                self.queue_total_file_size,
                timeout=settings.RDM_REDIS_CACHE_TIMEOUT_SECONDS
            )


class WorkerSender:
    """Непосредственная отправка файлов."""

    def __init__(self, queue: Queue):
        self.queue = queue

    def send_files(self):
        """Отправка файлов."""
        sub_stages = self.queue.dequeue()
        for (sub_stage_id, entity_key), upload_files in sub_stages.items():
            sub_stage = ExportingDataSubStage.objects.filter(id=sub_stage_id).first()
            if not sub_stage:
                return

            result_to_save = []
            errors = []
            status = ExportingDataSubStageStatus.FINISHED.key
            for file in upload_files:
                if settings.RDM_UPLOADER_CLIENT_ENABLE_REQUEST_EMULATION:
                    logger.warning(
                        f'{LOGS_DELIMITER * 3}ATTENTION!!! REGIONAL DATA MART INTEGRATION REQUEST EMULATION ENABLED!'
                    )

                method = OPERATIONS_METHODS_MAP.get(file.operation)
                file_path = Path.joinpath(Path(settings.MEDIA_ROOT), file.attachment_name)

                request = RegionalDataMartEntityRequest(
                    datamart_name=settings.RDM_UPLOADER_CLIENT_DATAMART_NAME,
                    table_name=entity_key.lower(),
                    method=method,
                    operation=OPERATIONS_URLS_MAP.get(file.operation),
                    parameters={},
                    headers={
                        'Content-Type': 'text/csv',
                    },
                    files=[],
                    data=file_path.open('rb').read(),
                )

                result = adapter.send(request)

                request_id = ''
                if not result.error:
                    request_id = result.response.text

                file_upload_status = FileUploadStatusEnum.IN_PROGRESS if request_id else FileUploadStatusEnum.ERROR

                sub_stage_uploader_client_log = ExportingDataSubStageUploaderClientLog(
                    entry=result.log,
                    sub_stage_id=sub_stage_id,
                    attachment_id=file.attachment_id,
                    request_id=request_id,
                    file_upload_status=file_upload_status,
                    is_emulation=settings.RDM_UPLOADER_CLIENT_ENABLE_REQUEST_EMULATION,
                )
                result_to_save.append(sub_stage_uploader_client_log)
                if result.error:
                    logger.warning(
                        f'{result.error}\nrequest - "{result.log.request}"\nresponse - "{result.log.response}"'
                    )

                    errors.append(result.error)
                    status = ExportingDataSubStageStatus.FAILED.key
                else:
                    logger.info(
                        f'Response with {result.response.status_code} code and content {result.response.text}'
                    )

            # Сохраняем информацию об отправке файлов и убираем подэтап с файлами из очереди
            if result_to_save:
                with atomic():
                    ExportingDataSubStageUploaderClientLog.objects.bulk_create(result_to_save)
                    sub_stage.status_id = status
                    sub_stage.save()

            self.queue.delete_from_queue(sub_stage_id=sub_stage_id, entity_name=entity_key)

    def run(self):
        """Запуск воркера отправки."""
        self.send_files()
