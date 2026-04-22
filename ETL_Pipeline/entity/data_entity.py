from dataclasses import dataclass

@dataclass
class Trading_data:
    stock_data_path: str
    nse_index_data_path : str

@dataclass
class Risk_data:
    risk_data_path: str

@dataclass
class Audit_data:
    audit_file_path: str

@dataclass
class Final_data:
    Final_df: str