from pydantic import BaseModel

class SupplierRecord(BaseModel):
    supplier_id: str
    supplier_name: str
    supplier_reliability: float
    transportation_delay_risk: float
    demand_uncertainty: float

class AssessedSupplier(SupplierRecord):
    supplier_risk_score: float
    supplier_risk_level: str
    transport_risk_level: str
    demand_risk_level: str
    overall_risk_score: float
    overall_risk_level: str