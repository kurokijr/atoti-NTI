from __future__ import annotations

import atoti as tt

from .constants import (
    Cube,
    ProjectContractTableColumn,
    ProjectCubeHierarchy,
    ProjectCubeMaturityLevel,
    ProjectCubeMeasure,
    ProjectCubeModalityLevel,
    ProjectCubeProjectTypeLevel,
    ProjectCubeTimelineLevel,
    ProjectCubeUnitLevel,
    ProjectFinancingModalityColumn,
    ProjectProjectTableColumn,
    Table,
    UEUnitTableColumn,
)


def create_project_cube(session: tt.Session, /) -> None:
    ue_unit_table = session.tables[Table.UE_UNIT.value]
    project_contract_table = session.tables[Table.PROJECT_CONTRACT.value]
    session.tables[Table.PROJECT_PROJECT_UE.value]
    project_project_table = session.tables[Table.PROJECT_PROJECT.value]
    session.tables[Table.PROJECT_CONTRACT.value]
    project_financing_modality = session.tables[Table.PROJECT_FINANCING_MODALITY.value]

    cube = session.create_cube(project_project_table, Cube.PROJECT.value, mode="manual")
    h, l, m = cube.hierarchies, cube.levels, cube.measures

    h.update(
        {
            ProjectCubeHierarchy.UNIT.value: {
                ProjectCubeUnitLevel.UNIT.value: ue_unit_table[
                    UEUnitTableColumn.NAME.value
                ]
            },
            ProjectCubeHierarchy.MODALITY.value: {
                ProjectCubeModalityLevel.MODALITY.value: project_financing_modality[
                    ProjectFinancingModalityColumn.MODEL.value
                ]
            },
            ProjectCubeHierarchy.PROJECT_TYPE.value: {
                ProjectCubeProjectTypeLevel.PROJECT_TYPE.value: project_project_table[
                    ProjectProjectTableColumn.PROJECT_TYPE.value
                ]
            },
            ProjectCubeHierarchy.MATURITY.value: {
                ProjectCubeMaturityLevel.CONTRACT_DEFINED_MATURITY_LEVEL.value: project_contract_table[
                    ProjectContractTableColumn.DEFINED_MATURITY_LEVEL.value
                ],
                ProjectCubeMaturityLevel.PROJECT_FINAL_MATURITY_LEVEL.value: project_project_table[
                    ProjectProjectTableColumn.FINAL_MATURITY_LEVEL.value
                ],
                ProjectCubeMaturityLevel.CONTRACT_FINAL_MATURITY_LEVEL.value: project_contract_table[
                    ProjectContractTableColumn.FINAL_MATURITY_LEVEL.value
                ]
            },
            ProjectCubeHierarchy.TIMELINE.value: {
                ProjectCubeTimelineLevel.CONTRACT_DATE.value: project_contract_table[
                    ProjectContractTableColumn.CONTRACT_DATE.value
                ],
                ProjectCubeTimelineLevel.START_DATE.value: project_contract_table[
                    ProjectContractTableColumn.START_DATE.value
                ],
                ProjectCubeTimelineLevel.FINISH_DATE.value: project_contract_table[
                    ProjectContractTableColumn.FINISH_DATE.value
                ]
            }
        }
    )

    m.update(
        {
            ProjectCubeMeasure.EMBRAPII_AMOUNT.value: tt.agg.sum(
                project_contract_table[ProjectContractTableColumn.EMBRAPII_AMOUNT.value]
            ),
            ProjectCubeMeasure.COMPANY_AMOUNT.value: tt.agg.sum(
                project_contract_table[ProjectContractTableColumn.COMPANY_AMOUNT.value]
            ),
            ProjectCubeMeasure.UE_AMOUNT.value: tt.agg.sum(
                project_contract_table[ProjectContractTableColumn.UE_AMOUNT.value]
            )
        }
    )

def create_cubes(session: tt.Session, /) -> None:
    create_project_cube(session)
