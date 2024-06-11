from typing import List

import httpx

from pinexq_client.core.hco.hco_base import Hco, Property
from pinexq_client.core.hco.link_hco import LinkHco
from pinexq_client.job_management.hcos.job_hco import JobHco
from pinexq_client.job_management.known_relations import Relations
from pinexq_client.job_management.model.sirenentities import JobQueryResultEntity, JobEntity


class JobQueryResultPaginationLink(LinkHco):
    def navigate(self) -> 'JobQueryResultHco':
        return JobQueryResultHco.from_entity(self._client, self._navigate_internal(JobQueryResultEntity))


class JobQueryResultLink(LinkHco):
    def navigate(self) -> 'JobQueryResultHco':
        return JobQueryResultHco.from_entity(self._client, self._navigate_internal(JobQueryResultEntity))


class JobQueryResultHco(Hco[JobQueryResultEntity]):
    self_link: JobQueryResultLink
    all_link: JobQueryResultPaginationLink | None
    first_link: JobQueryResultPaginationLink | None
    last_link: JobQueryResultPaginationLink | None
    next_link: JobQueryResultPaginationLink | None
    previous_link: JobQueryResultPaginationLink | None

    total_entities: int = Property()
    current_entities_count: int = Property()
    jobs: List[JobHco]

    @classmethod
    def from_entity(cls, client: httpx.Client, entity: JobQueryResultEntity) -> 'JobQueryResultHco':
        instance = cls(client, entity)

        Hco.check_classes(instance._entity.class_, ["JobQueryResult"])

        # pagination links
        instance.self_link = JobQueryResultLink.from_entity(instance._client, instance._entity, Relations.SELF)
        instance.all_link = JobQueryResultPaginationLink.from_entity_optional(instance._client, instance._entity,
                                                                              Relations.ALL)
        instance.first_link = JobQueryResultPaginationLink.from_entity_optional(instance._client, instance._entity,
                                                                                Relations.FIRST)
        instance.last_link = JobQueryResultPaginationLink.from_entity_optional(instance._client, instance._entity,
                                                                               Relations.LAST)
        instance.next_link = JobQueryResultPaginationLink.from_entity_optional(instance._client, instance._entity,
                                                                               Relations.NEXT)
        instance.previous_link = JobQueryResultPaginationLink.from_entity_optional(instance._client, instance._entity,
                                                                                   Relations.PREVIOUS)

        # entities
        instance._extract_jobs()

        return instance

    def _extract_jobs(self):
        self.jobs = []
        jobs = self._entity.find_all_entities_with_relation(Relations.ITEM, JobEntity)
        for job in jobs:
            job_hco: JobHco = JobHco.from_entity(job, self._client)
            self.jobs.append(job_hco)
