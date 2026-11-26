from sqlalchemy.orm import Session


class BaseRepository:
    """Repositories receive the active session from the service layer."""

    def __init__(self, session: Session) -> None:
        self._session = session
