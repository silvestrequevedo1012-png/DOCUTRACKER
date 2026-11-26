from __future__ import annotations

from sqlalchemy import select

from models.document_type import DocumentType
from repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository):
    def get_by_code(self, code: str) -> DocumentType | None:
        return self._session.scalar(select(DocumentType).where(DocumentType.code == code))

    def list_active(self) -> list[DocumentType]:
        return list(
            self._session.scalars(
                select(DocumentType).where(DocumentType.is_active.is_(True)).order_by(DocumentType.name)
            )
        )

    def add(self, doc_type: DocumentType) -> DocumentType:
        self._session.add(doc_type)
        self._session.flush()
        return doc_type
