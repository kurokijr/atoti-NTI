from __future__ import annotations

from enum import Enum


class Table(Enum):
    UE_UNIT = "Unidade Embrapii"
    PROJECT_PROJECT_UE = "Projeto VS UE"
    PROJECT_PROJECT = "Descrição do projeto"
    PROJECT_CONTRACT = "Contrato do projeto"
    PROJECT_FINANCING_MODALITY = "Modalidade de financiamento do projeto"


class UEUnitTableColumn(Enum):
    ID = "ID"
    NAME = "Nome"

class ProjectProjectUETableColumn(Enum):
    ID = "ID"
    PROJECT_ID = "ID Projeto"
    UNIT_ID = "ID Unidade"

class ProjectProjectTableColumn(Enum):
    ID = "ID"
    CODE = "Codigo"
    PROJECT_TYPE = "Tipo Projeto"
    FINAL_MATURITY_LEVEL = "Nivel final de maturidade"
    STATUS = "Status"

class ProjectFinancingModalityColumn(Enum):
    ID = "ID"
    MODEL = "Modelo de financiamento"
    ALIAS = "Alias do modelo de financiamento"
    DESCRIPTION = "Descrição da modalidade"

class ProjectContractTableColumn(Enum):
    ID = "ID"
    CONTRACT_DATE = "Data da contratação do projeto"
    START_DATE = "Data de início do projeto"
    FINISH_DATE = "Data de finalização do projeto"
    DEFINED_MATURITY_LEVEL = "Nível de maturidade"
    EMBRAPII_AMOUNT = "Investimento Embrapii"
    COMPANY_AMOUNT = "Investimento Empresa"
    UE_AMOUNT = "Investimento UE"
    TOTAL_AMOUNT = "Investimento total"
    PROJECT_RELATED_ID = "Projeto relacionado"
    FINANCING_MODALITY = "Modalidade de financiamento"
    FINAL_MATURITY_LEVEL = "Maturidade final"

class Cube(Enum):
    PROJECT = "Projeto"


class ProjectCubeHierarchy(Enum):
    UNIT = UEUnitTableColumn.NAME.value
    MODALITY = ProjectFinancingModalityColumn.MODEL.value
    PROJECT_TYPE = ProjectProjectTableColumn.PROJECT_TYPE.value
    MATURITY = "Maturity"
    TIMELINE = "Timeline"

class ProjectCubeUnitLevel(Enum):
    UNIT = UEUnitTableColumn.NAME.value

class ProjectCubeModalityLevel(Enum):
    MODALITY = ProjectFinancingModalityColumn.MODEL.value

class ProjectCubeProjectTypeLevel(Enum):
    PROJECT_TYPE = ProjectProjectTableColumn.PROJECT_TYPE.value

class ProjectCubeMaturityLevel(Enum):
    PROJECT_FINAL_MATURITY_LEVEL = ProjectProjectTableColumn.FINAL_MATURITY_LEVEL.value
    CONTRACT_FINAL_MATURITY_LEVEL = ProjectContractTableColumn.FINAL_MATURITY_LEVEL.value
    CONTRACT_DEFINED_MATURITY_LEVEL = ProjectContractTableColumn.DEFINED_MATURITY_LEVEL.value

class ProjectCubeTimelineLevel(Enum):
    CONTRACT_DATE = ProjectContractTableColumn.CONTRACT_DATE.value
    START_DATE = ProjectContractTableColumn.START_DATE.value
    FINISH_DATE = ProjectContractTableColumn.FINISH_DATE.value

class ProjectCubeMeasure(Enum):
    EMBRAPII_AMOUNT = ProjectContractTableColumn.EMBRAPII_AMOUNT.value
    COMPANY_AMOUNT = ProjectContractTableColumn.COMPANY_AMOUNT.value
    UE_AMOUNT = ProjectContractTableColumn.UE_AMOUNT.value
