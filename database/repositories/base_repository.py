"""
====================================================================
File: base_repository.py

Project : ConfigVista AI

Purpose
-------
Generic Repository implementing reusable CRUD operations.

Every repository in the application inherits from this class.

Responsibilities
----------------
- Generic CRUD operations
- Transaction support
- Common query helpers
- Logging
- Exception handling

====================================================================
"""

import logging

from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm import Query
from sqlalchemy.orm import Session


# ------------------------------------------------------------------
# Logger
# ------------------------------------------------------------------

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Generic SQLAlchemy Model Type
# ------------------------------------------------------------------

T = TypeVar("T", bound=DeclarativeMeta)


# ------------------------------------------------------------------
# Base Repository
# ------------------------------------------------------------------

class BaseRepository(Generic[T]):
    """
    Generic repository implementing reusable CRUD operations.
    """

    def __init__(self, session: Session, model: Type[T]):

        self.session = session
        self.model = model

    # ==============================================================
    # CREATE
    # ==============================================================

    def add(self, entity: T) -> T:
        """
        Add an entity to the current transaction.
        """

        try:

            self.session.add(entity)

            self.session.flush()

            self.session.refresh(entity)

            logger.info(
                "%s added successfully.",
                self.model.__name__
            )

            return entity

        except Exception:

            logger.exception(
                "Failed to add %s.",
                self.model.__name__
            )

            self.session.rollback()

            raise

    # ==============================================================
    # READ
    # ==============================================================

    def get_by_id(self, entity_id: int) -> Optional[T]:
        """
        Retrieve entity using primary key.
        """

        return self.session.get(self.model, entity_id)

    def get_all(self) -> List[T]:
        """
        Retrieve all entities.
        """

        return self.session.query(self.model).all()

    def get_first(self) -> Optional[T]:
        """
        Retrieve first entity.
        """

        return self.session.query(self.model).first()

    def get_or_none(self, entity_id: int) -> Optional[T]:
        """
        Retrieve entity or None.
        """

        return self.session.get(self.model, entity_id)

    def exists(self, entity_id: int) -> bool:
        """
        Check whether entity exists.
        """

        return self.get_by_id(entity_id) is not None

    def count(self) -> int:
        """
        Count number of entities.
        """

        return self.session.query(self.model).count()

    def query(self) -> Query:
        """
        Return SQLAlchemy query object.
        """

        return self.session.query(self.model)

    # ==============================================================
    # UPDATE
    # ==============================================================

    def update(self, entity: T) -> T:
        """
        Update an existing entity.
        """

        try:

            merged_entity = self.session.merge(entity)

            self.session.flush()

            logger.info(
                "%s updated successfully.",
                self.model.__name__
            )

            return merged_entity

        except Exception:

            logger.exception(
                "Failed to update %s.",
                self.model.__name__
            )

            self.session.rollback()

            raise

    # ==============================================================
    # DELETE
    # ==============================================================

    def delete(self, entity: T) -> None:
        """
        Delete an entity.
        """

        try:

            self.session.delete(entity)

            self.session.flush()

            logger.info(
                "%s deleted successfully.",
                self.model.__name__
            )

        except Exception:

            logger.exception(
                "Failed to delete %s.",
                self.model.__name__
            )

            self.session.rollback()

            raise

    # ==============================================================
    # TRANSACTION MANAGEMENT
    # ==============================================================

    def flush(self) -> None:
        """
        Flush pending changes to the database.
        """

        self.session.flush()

    def refresh(self, entity: T) -> None:
        """
        Refresh entity from the database.
        """

        self.session.refresh(entity)

    def commit(self) -> None:
        """
        Commit current transaction.
        """

        try:

            self.session.commit()

            logger.info("Transaction committed successfully.")

        except Exception:

            logger.exception("Transaction commit failed.")

            self.session.rollback()

            raise

    def rollback(self) -> None:
        """
        Rollback current transaction.
        """

        logger.warning("Transaction rolled back.")

        self.session.rollback()

    def close(self) -> None:
        """
        Close database session.
        """

        self.session.close()

        logger.info("Database session closed.")