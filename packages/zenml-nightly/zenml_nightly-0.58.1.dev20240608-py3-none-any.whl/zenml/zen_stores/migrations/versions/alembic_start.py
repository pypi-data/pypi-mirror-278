"""Initialize db with first revision.

Revision ID: alembic_start
Revises:
Create Date: 2022-10-19 11:17:54.753102

"""

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = "alembic_start"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema and/or data, creating a new revision."""
    # If the tables already exist, skip this migration.
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()
    if "projectschema" in tables:
        return

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "projectschema",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "description", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "roleschema",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "teamschema",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "userschema",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "full_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column(
            "password", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
        sa.Column(
            "activation_token",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=True,
        ),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("email_opted_in", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "flavorschema",
        sa.Column("project_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "source", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "integration", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
        sa.Column(
            "config_schema", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"], ["projectschema.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["userschema.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "pipelineschema",
        sa.Column("project_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "docstring",
            sqlmodel.sql.sqltypes.AutoString(length=4096),
            nullable=True,
        ),
        sa.Column(
            "spec",
            sqlmodel.sql.sqltypes.AutoString(length=4096),
            nullable=False,
        ),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"], ["projectschema.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["userschema.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "stackcomponentschema",
        sa.Column("project_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("is_shared", sa.Boolean(), nullable=False),
        sa.Column("type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "flavor", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column("configuration", sa.LargeBinary(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"], ["projectschema.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["userschema.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "stackschema",
        sa.Column("project_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("is_shared", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"], ["projectschema.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["userschema.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "teamassignmentschema",
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("team_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teamschema.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["userschema.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "team_id"),
    )
    op.create_table(
        "teamroleassignmentschema",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("role_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("team_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("project_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projectschema.id"],
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roleschema.id"],
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teamschema.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "userroleassignmentschema",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("role_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("project_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projectschema.id"],
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roleschema.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["userschema.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "pipelinerunschema",
        sa.Column("project_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("stack_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("pipeline_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "pipeline_configuration",
            sqlmodel.sql.sqltypes.AutoString(length=4096),
            nullable=False,
        ),
        sa.Column("num_steps", sa.Integer(), nullable=False),
        sa.Column(
            "zenml_version", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column(
            "git_sha", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("mlmd_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["pipeline_id"], ["pipelineschema.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["project_id"], ["projectschema.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["stack_id"], ["stackschema.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["userschema.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "stackcompositionschema",
        sa.Column("stack_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column(
            "component_id", sqlmodel.sql.sqltypes.GUID(), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["component_id"],
            ["stackcomponentschema.id"],
        ),
        sa.ForeignKeyConstraint(
            ["stack_id"],
            ["stackschema.id"],
        ),
        sa.PrimaryKeyConstraint("stack_id", "component_id"),
    )
    op.create_table(
        "steprunschema",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "pipeline_run_id", sqlmodel.sql.sqltypes.GUID(), nullable=False
        ),
        sa.Column(
            "entrypoint_name",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
        ),
        sa.Column(
            "parameters",
            sqlmodel.sql.sqltypes.AutoString(length=4096),
            nullable=False,
        ),
        sa.Column(
            "step_configuration",
            sqlmodel.sql.sqltypes.AutoString(length=4096),
            nullable=False,
        ),
        sa.Column(
            "docstring",
            sqlmodel.sql.sqltypes.AutoString(length=4096),
            nullable=True,
        ),
        sa.Column("mlmd_id", sa.Integer(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["pipeline_run_id"],
            ["pipelinerunschema.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "artifactschema",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "parent_step_id", sqlmodel.sql.sqltypes.GUID(), nullable=False
        ),
        sa.Column(
            "producer_step_id", sqlmodel.sql.sqltypes.GUID(), nullable=False
        ),
        sa.Column("type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("uri", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "materializer", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column(
            "data_type", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column("is_cached", sa.Boolean(), nullable=False),
        sa.Column("mlmd_id", sa.Integer(), nullable=True),
        sa.Column("mlmd_parent_step_id", sa.Integer(), nullable=True),
        sa.Column("mlmd_producer_step_id", sa.Integer(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["parent_step_id"],
            ["steprunschema.id"],
        ),
        sa.ForeignKeyConstraint(
            ["producer_step_id"],
            ["steprunschema.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "steprunorderschema",
        sa.Column("parent_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("child_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["child_id"],
            ["steprunschema.id"],
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["steprunschema.id"],
        ),
        sa.PrimaryKeyConstraint("parent_id", "child_id"),
    )
    op.create_table(
        "stepinputartifactschema",
        sa.Column("step_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("artifact_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["artifact_id"],
            ["artifactschema.id"],
        ),
        sa.ForeignKeyConstraint(
            ["step_id"],
            ["steprunschema.id"],
        ),
        sa.PrimaryKeyConstraint("step_id", "artifact_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade database schema and/or data back to the previous revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("stepinputartifactschema")
    op.drop_table("steprunorderschema")
    op.drop_table("artifactschema")
    op.drop_table("steprunschema")
    op.drop_table("stackcompositionschema")
    op.drop_table("pipelinerunschema")
    op.drop_table("userroleassignmentschema")
    op.drop_table("teamroleassignmentschema")
    op.drop_table("teamassignmentschema")
    op.drop_table("stackschema")
    op.drop_table("stackcomponentschema")
    op.drop_table("pipelineschema")
    op.drop_table("flavorschema")
    op.drop_table("userschema")
    op.drop_table("teamschema")
    op.drop_table("roleschema")
    op.drop_table("projectschema")
    # ### end Alembic commands ###
