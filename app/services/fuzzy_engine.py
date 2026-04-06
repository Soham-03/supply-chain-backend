import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

supplier_risk = ctrl.Antecedent(np.arange(0, 101, 1), "supplier_risk")
transport_risk = ctrl.Antecedent(np.arange(0, 101, 1), "transport_risk")
demand_risk = ctrl.Antecedent(np.arange(0, 101, 1), "demand_risk")
overall_risk = ctrl.Consequent(np.arange(0, 101, 1), "overall_risk")

for var in [supplier_risk, transport_risk, demand_risk]:
    var["low"] = fuzz.trimf(var.universe, [0, 0, 40])
    var["medium"] = fuzz.trimf(var.universe, [25, 50, 75])
    var["high"] = fuzz.trimf(var.universe, [60, 100, 100])

overall_risk["low"] = fuzz.trimf(overall_risk.universe, [0, 0, 30])
overall_risk["medium"] = fuzz.trimf(overall_risk.universe, [20, 45, 65])
overall_risk["high"] = fuzz.trimf(overall_risk.universe, [55, 72, 88])
overall_risk["critical"] = fuzz.trimf(overall_risk.universe, [80, 100, 100])

rules = [
    ctrl.Rule(supplier_risk["low"] & transport_risk["low"] & demand_risk["low"], overall_risk["low"]),
    ctrl.Rule(supplier_risk["medium"] | transport_risk["medium"] | demand_risk["medium"], overall_risk["medium"]),
    ctrl.Rule((supplier_risk["high"] & transport_risk["medium"]) | (transport_risk["high"] & demand_risk["medium"]) | (supplier_risk["medium"] & demand_risk["high"]), overall_risk["high"]),
    ctrl.Rule(supplier_risk["high"] & transport_risk["high"], overall_risk["critical"]),
    ctrl.Rule(transport_risk["high"] & demand_risk["high"], overall_risk["critical"]),
    ctrl.Rule(supplier_risk["high"] & demand_risk["high"], overall_risk["critical"]),
    ctrl.Rule(supplier_risk["high"] & transport_risk["high"] & demand_risk["high"], overall_risk["critical"]),
]

risk_ctrl = ctrl.ControlSystem(rules)

def crisp_level(value: float) -> str:
    if value < 30:
        return "low"
    if value < 60:
        return "medium"
    if value < 80:
        return "high"
    return "critical"

def factor_level(value: float) -> str:
    if value < 35:
        return "low"
    if value < 70:
        return "medium"
    return "high"

def assess_risk(supplier_reliability: float, transportation_delay_risk: float, demand_uncertainty: float):
    sim = ctrl.ControlSystemSimulation(risk_ctrl)
    supplier_risk_score = 100 - supplier_reliability

    sim.input["supplier_risk"] = supplier_risk_score
    sim.input["transport_risk"] = transportation_delay_risk
    sim.input["demand_risk"] = demand_uncertainty
    sim.compute()

    overall_score = float(sim.output["overall_risk"])

    return {
        "supplier_risk_score": round(supplier_risk_score, 2),
        "supplier_risk_level": factor_level(supplier_risk_score),
        "transport_risk_level": factor_level(transportation_delay_risk),
        "demand_risk_level": factor_level(demand_uncertainty),
        "overall_risk_score": round(overall_score, 2),
        "overall_risk_level": crisp_level(overall_score),
    }