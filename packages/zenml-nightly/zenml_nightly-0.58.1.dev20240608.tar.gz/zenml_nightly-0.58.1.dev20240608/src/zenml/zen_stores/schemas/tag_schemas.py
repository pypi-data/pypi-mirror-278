#  Copyright (c) ZenML GmbH 2023. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""SQLModel implementation of tag tables."""

from datetime import datetime
from typing import TYPE_CHECKING, Any, List
from uuid import UUID

from sqlalchemy import VARCHAR, Column
from sqlmodel import Field, Relationship

from zenml.enums import ColorVariants, TaggableResourceTypes
from zenml.models import (
    TagRequest,
    TagResourceRequest,
    TagResourceResponse,
    TagResourceResponseBody,
    TagResponse,
    TagResponseBody,
    TagUpdate,
)
from zenml.zen_stores.schemas.base_schemas import BaseSchema, NamedSchema
from zenml.zen_stores.schemas.schema_utils import build_foreign_key_field

if TYPE_CHECKING:
    from zenml.zen_stores.schemas.artifact_schemas import (
        ArtifactSchema,
        ArtifactVersionSchema,
    )
    from zenml.zen_stores.schemas.model_schemas import (
        ModelSchema,
        ModelVersionSchema,
    )


class TagSchema(NamedSchema, table=True):
    """SQL Model for tag."""

    __tablename__ = "tag"

    color: str = Field(sa_column=Column(VARCHAR(255), nullable=False))
    links: List["TagResourceSchema"] = Relationship(
        back_populates="tag",
        sa_relationship_kwargs={"cascade": "delete"},
    )

    @classmethod
    def from_request(cls, request: TagRequest) -> "TagSchema":
        """Convert an `TagRequest` to an `TagSchema`.

        Args:
            request: The request model to convert.

        Returns:
            The converted schema.
        """
        return cls(
            name=request.name,
            color=request.color.value,
        )

    def to_model(
        self,
        include_metadata: bool = False,
        include_resources: bool = False,
        **kwargs: Any,
    ) -> TagResponse:
        """Convert an `TagSchema` to an `TagResponse`.

        Args:
            include_metadata: Whether the metadata will be filled.
            include_resources: Whether the resources will be filled.
            **kwargs: Keyword arguments to allow schema specific logic


        Returns:
            The created `TagResponse`.
        """
        return TagResponse(
            id=self.id,
            name=self.name,
            body=TagResponseBody(
                created=self.created,
                updated=self.updated,
                color=ColorVariants(self.color),
                tagged_count=len(self.links),
            ),
        )

    def update(self, update: TagUpdate) -> "TagSchema":
        """Updates a `TagSchema` from a `TagUpdate`.

        Args:
            update: The `TagUpdate` to update from.

        Returns:
            The updated `TagSchema`.
        """
        for field, value in update.dict(exclude_unset=True).items():
            setattr(self, field, value)
        self.updated = datetime.utcnow()
        return self


class TagResourceSchema(BaseSchema, table=True):
    """SQL Model for tag resource relationship."""

    __tablename__ = "tag_resource"

    tag_id: UUID = build_foreign_key_field(
        source=__tablename__,
        target=TagSchema.__tablename__,
        source_column="tag_id",
        target_column="id",
        ondelete="CASCADE",
        nullable=False,
    )
    tag: "TagSchema" = Relationship(back_populates="links")
    resource_id: UUID
    resource_type: str = Field(sa_column=Column(VARCHAR(255), nullable=False))
    artifact: List["ArtifactSchema"] = Relationship(
        back_populates="tags",
        sa_relationship_kwargs=dict(
            primaryjoin=f"and_(TagResourceSchema.resource_type=='{TaggableResourceTypes.ARTIFACT.value}', foreign(TagResourceSchema.resource_id)==ArtifactSchema.id)",
            overlaps="tags,model,artifact_version,model_version",
        ),
    )
    artifact_version: List["ArtifactVersionSchema"] = Relationship(
        back_populates="tags",
        sa_relationship_kwargs=dict(
            primaryjoin=f"and_(TagResourceSchema.resource_type=='{TaggableResourceTypes.ARTIFACT_VERSION.value}', foreign(TagResourceSchema.resource_id)==ArtifactVersionSchema.id)",
            overlaps="tags,model,artifact,model_version",
        ),
    )
    model: List["ModelSchema"] = Relationship(
        back_populates="tags",
        sa_relationship_kwargs=dict(
            primaryjoin=f"and_(TagResourceSchema.resource_type=='{TaggableResourceTypes.MODEL.value}', foreign(TagResourceSchema.resource_id)==ModelSchema.id)",
            overlaps="tags,artifact,artifact_version,model_version",
        ),
    )
    model_version: List["ModelVersionSchema"] = Relationship(
        back_populates="tags",
        sa_relationship_kwargs=dict(
            primaryjoin=f"and_(TagResourceSchema.resource_type=='{TaggableResourceTypes.MODEL_VERSION.value}', foreign(TagResourceSchema.resource_id)==ModelVersionSchema.id)",
            overlaps="tags,model,artifact,artifact_version",
        ),
    )

    @classmethod
    def from_request(cls, request: TagResourceRequest) -> "TagResourceSchema":
        """Convert an `TagResourceRequest` to an `TagResourceSchema`.

        Args:
            request: The request model version to convert.

        Returns:
            The converted schema.
        """
        return cls(
            tag_id=request.tag_id,
            resource_id=request.resource_id,
            resource_type=request.resource_type.value,
        )

    def to_model(
        self,
        include_metadata: bool = False,
        include_resources: bool = False,
        **kwargs: Any,
    ) -> TagResourceResponse:
        """Convert an `TagResourceSchema` to an `TagResourceResponse`.

        Args:
            include_metadata: Whether the metadata will be filled.
            include_resources: Whether the resources will be filled.
            **kwargs: Keyword arguments to allow schema specific logic


        Returns:
            The created `TagResourceResponse`.
        """
        return TagResourceResponse(
            id=self.id,
            body=TagResourceResponseBody(
                tag_id=self.tag_id,
                resource_id=self.resource_id,
                created=self.created,
                updated=self.updated,
                resource_type=TaggableResourceTypes(self.resource_type),
            ),
        )
