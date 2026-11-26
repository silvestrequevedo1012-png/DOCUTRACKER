from __future__ import annotations

from models.audit_log import AuditLog
from repositories.base_repository import BaseRepository


class AuditRepository(BaseRepository):
    def log(
        self,
        action: str,
        user_id: int | None = None,
        entity_type: str | None = None,
        entity_id: int | str | None = None,
        details: dict | None = None,
        ip_address: str | None = None,
    ) -> AuditLog:
        entry = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=str(entity_id) if entity_id is not None else None,
            details=details,
            ip_address=ip_address,
        )
        self._session.add(entry)
        return entry
