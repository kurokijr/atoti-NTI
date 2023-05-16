from __future__ import annotations

import atoti as tt

from .constants import (
    ProjectContractTableColumn,
    ProjectFinancingModality,
    ProjectProjectTableColumn,
    ProjectProjectUETableColumn,
    Table,
    UEUnitTableColumn,
)


def create_ue_unit_table(session: tt.Session, /) -> None:
    session.create_table(
        Table.UE_UNIT.value,
        keys=[
            UEUnitTableColumn.ID.value,
            UEUnitTableColumn.NAME.value,
        ],
        types={
            UEUnitTableColumn.ID.value: tt.type.INT,
            UEUnitTableColumn.NAME.value: tt.type.STRING,
        },
    )


def create_ue_project_project_table(session: tt.Session, /) -> None:
    session.create_table(
        Table.PROJECT_PROJECT_UE.value,
        keys=[
            ProjectProjectUETableColumn.ID.value,
            ProjectProjectUETableColumn.PROJECT_ID.value,
            ProjectProjectUETableColumn.UNIT_ID.value,
        ],
        types={
            ProjectProjectUETableColumn.ID.value: tt.type.INT,
            ProjectProjectUETableColumn.PROJECT_ID.value: tt.type.INT,
            ProjectProjectUETableColumn.UNIT_ID.value: tt.type.INT,
        },
    )

def create_project_project_table(session: tt.Session, /) -> None:
    session.create_table(
        Table.PROJECT_PROJECT.value,
        keys=[
            ProjectProjectTableColumn.ID.value,
            ProjectProjectTableColumn.CODE.value,
            ProjectProjectTableColumn.PROJECT_TYPE.value,
            ProjectProjectTableColumn.FINAL_MATURITY_LEVEL.value,
            ProjectProjectTableColumn.STATUS.value,
        ],
        types={
            ProjectProjectTableColumn.ID.value: tt.type.INT,
            ProjectProjectTableColumn.CODE.value: tt.type.STRING,
            ProjectProjectTableColumn.PROJECT_TYPE.value: tt.type.STRING,
            ProjectProjectTableColumn.FINAL_MATURITY_LEVEL.value: tt.type.STRING,
            ProjectProjectTableColumn.STATUS.value: tt.type.STRING,
        },
    )

def create_project_contract_table(session: tt.Session, /) -> None:
    session.create_table(
        Table.PROJECT_CONTRACT.value,
        keys=[
            ProjectContractTableColumn.ID.value,
            ProjectContractTableColumn.CONTRACT_DATE.value,
            ProjectContractTableColumn.START_DATE.value,
            ProjectContractTableColumn.FINISH_DATE.value,
            ProjectContractTableColumn.DEFINED_MATURITY_LEVEL.value,
            ProjectContractTableColumn.EMBRAPII_AMOUNT.value,
            ProjectContractTableColumn.COMPANY_AMOUNT.value,
            ProjectContractTableColumn.UE_AMOUNT.value,
            ProjectContractTableColumn.TOTAL_AMOUNT.value,
            ProjectContractTableColumn.PROJECT_RELATED_ID.value,
            ProjectContractTableColumn.FINANCING_MODALITY.value,
            ProjectContractTableColumn.FINAL_MATURITY_LEVEL.value,
        ],
        types={
            ProjectContractTableColumn.ID.value: tt.type.INT,
            ProjectContractTableColumn.CONTRACT_DATE.value: tt.type.LOCAL_DATE,
            ProjectContractTableColumn.START_DATE.value: tt.type.LOCAL_DATE,
            ProjectContractTableColumn.FINISH_DATE.value: tt.type.LOCAL_DATE,
            ProjectContractTableColumn.DEFINED_MATURITY_LEVEL.value: tt.type.STRING,
            ProjectContractTableColumn.EMBRAPII_AMOUNT.value: tt.type.FLOAT,
            ProjectContractTableColumn.COMPANY_AMOUNT.value:tt.type.FLOAT,
            ProjectContractTableColumn.UE_AMOUNT.value:tt.type.FLOAT,
            ProjectContractTableColumn.TOTAL_AMOUNT.value:tt.type.FLOAT,
            ProjectContractTableColumn.PROJECT_RELATED_ID.value:tt.type.INT,
            ProjectContractTableColumn.FINANCING_MODALITY.value:tt.type.INT,
            ProjectContractTableColumn.FINAL_MATURITY_LEVEL.value: tt.type.STRING,
        },
    )

def create_project_financing_modality_table(session: tt.Session, /) -> None:
    session.create_table(
        Table.PROJECT_FINANCING_MODALITY.value,
        keys=[
            ProjectFinancingModality.ID.value,
            ProjectFinancingModality.MODEL.value,
            ProjectFinancingModality.ALIAS.value,
            ProjectFinancingModality.DESCRIPTION.value,
        ],
        types={
            ProjectFinancingModality.ID.value: tt.type.INT,
            ProjectFinancingModality.MODEL.value: tt.type.INT,
            ProjectFinancingModality.ALIAS.value: tt.type.STRING,
            ProjectFinancingModality.DESCRIPTION.value: tt.type.STRING,
        },
    )

def join_tables(session: tt.Session, /) -> None:

    # JOIN PROJECT_PROJECT com PROJECT_UE
    session.tables[Table.PROJECT_PROJECT.value].join(
        session.tables[Table.PROJECT_PROJECT_UE.value],
        session.tables[Table.PROJECT_PROJECT.value][
            ProjectProjectTableColumn.ID.value
        ]
        == session.tables[Table.PROJECT_PROJECT_UE.value][
            ProjectProjectUETableColumn.PROJECT_ID.value
        ],
    )

    session.tables[Table.PROJECT_PROJECT.value].join(
        session.tables[Table.PROJECT_CONTRACT.value],
        session.tables[Table.PROJECT_PROJECT.value][
            ProjectProjectTableColumn.ID.value
        ]
        == session.tables[Table.PROJECT_CONTRACT.value][
            ProjectContractTableColumn.PROJECT_RELATED_ID.value
        ],
    )

    session.tables[Table.PROJECT_CONTRACT.value].join(
        session.tables[Table.PROJECT_FINANCING_MODALITY.value],
        session.tables[Table.PROJECT_CONTRACT.value][
            ProjectContractTableColumn.FINANCING_MODALITY.value
        ]
        == session.tables[Table.PROJECT_FINANCING_MODALITY.value][
            ProjectFinancingModality.ID.value
        ],
    )

def create_and_join_tables(session: tt.Session, /) -> None:
    create_ue_unit_table(session)
    create_ue_project_project_table(session)
    create_project_contract_table(session)
    create_project_financing_modality_table(session)
    create_project_project_table(session)
    join_tables(session)
