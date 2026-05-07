import datetime
from typing import Dict, List, Optional, Tuple, Union
import uuid
import math
import json

class RenewableEnergyEngineer:
    def __init__(self):
        # Projects: {project_id: {"name": str, "type": str, "location": str, "capacity_mw": float, "status": str, "grid_code": str}}
        self.projects: Dict[str, Dict] = {}

        # Grid Integration Studies: {study_id: {"project_id": str, "type": str, "status": str, "compliance": Dict, "findings": List[Dict]}}
        self.grid_studies: Dict[str, Dict] = {}

        # Modeling Tools: {tool_id: {"name": str, "type": str, "last_used": str, "license": str}}
        self.modeling_tools: Dict[str, Dict] = {
            "PSCAD1": {"name": "PSCAD", "type": "Transient Stability", "last_used": "", "license": "Valid"},
            "PSSE1": {"name": "PSSE", "type": "Power Flow/Short Circuit", "last_used": "", "license": "Valid"}
        }

        # Power System Studies: {study_id: {"project_id": str, "type": str, "results": Dict, "mitigations": List[Dict]}}
        self.power_studies: Dict[str, Dict] = {}

        # Control Strategies: {strategy_id: {"project_id": str, "type": str, "parameters": Dict, "performance": Dict}}
        self.control_strategies: Dict[str, Dict] = {}

        # Performance Metrics: {metric_id: {"project_id": str, "metric": str, "value": float, "target": float}}
        self.performance_metrics: Dict[str, Dict] = {}

        # Audit Logs: List[Dict]
        self.audit_logs: List[Dict] = {}

        # Next IDs
        self.next_project_id = 1
        self.next_study_id = 1
        self.next_power_study_id = 1
        self.next_strategy_id = 1
        self.next_metric_id = 1

    # --- Project Management ---
    def create_project(self, name: str, project_type: str, location: str, capacity_mw: float, grid_code: str) -> str:
        """Create a new renewable energy project (solar/wind)."""
        project_id = f"PROJ{self.next_project_id}"
        self.next_project_id += 1
        self.projects[project_id] = {
            "name": name,
            "type": project_type,
            "location": location,
            "capacity_mw": capacity_mw,
            "status": "Design",
            "grid_code": grid_code,
            "interconnection_date": None,
            "stability_score": 0.0
        }
        self._log_activity("project_created", {
            "project_id": project_id,
            "name": name,
            "type": project_type,
            "capacity_mw": capacity_mw
        })
        return f"Project '{name}' created with ID: {project_id}"

    def update_project_status(self, project_id: str, status: str, interconnection_date: Optional[str] = None) -> str:
        """Update the status of a renewable energy project."""
        if project_id in self.projects:
            self.projects[project_id]["status"] = status
            if interconnection_date:
                self.projects[project_id]["interconnection_date"] = interconnection_date
            self._log_activity("project_updated", {
                "project_id": project_id,
                "status": status,
                "interconnection_date": interconnection_date
            })
            return f"Project {project_id} status updated to: {status}"
        return f"Project ID {project_id} not found."

    # --- Grid Integration Studies ---
    def create_grid_study(self, project_id: str, study_type: str) -> str:
        """Create a grid integration study for a project."""
        if project_id in self.projects:
            study_id = f"GS{self.next_study_id}"
            self.next_study_id += 1
            self.grid_studies[study_id] = {
                "project_id": project_id,
                "type": study_type,
                "status": "In Progress",
                "compliance": {
                    "grid_code": False,
                    "inverter_control": False,
                    "dynamic_performance": False
                },
                "findings": []
            }
            self._log_activity("grid_study_created", {
                "study_id": study_id,
                "project_id": project_id,
                "type": study_type
            })
            return f"Grid Integration Study created with ID: {study_id}"
        return f"Project ID {project_id} not found."

    def update_compliance(self, study_id: str, grid_code: bool, inverter_control: bool, dynamic_performance: bool) -> str:
        """Update compliance status for a grid integration study."""
        if study_id in self.grid_studies:
            self.grid_studies[study_id]["compliance"] = {
                "grid_code": grid_code,
                "inverter_control": inverter_control,
                "dynamic_performance": dynamic_performance
            }
            all_compliant = all(self.grid_studies[study_id]["compliance"].values())
            self.grid_studies[study_id]["status"] = "Compliant" if all_compliant else "Non-Compliant"
            self._log_activity("compliance_updated", {
                "study_id": study_id,
                "grid_code": grid_code,
                "inverter_control": inverter_control,
                "dynamic_performance": dynamic_performance
            })
            return f"Compliance updated for study {study_id}. Status: {'Compliant' if all_compliant else 'Non-Compliant'}"
        return f"Study ID {study_id} not found."

    def add_finding(self, study_id: str, finding: Dict) -> str:
        """Add a finding to a grid integration study."""
        if study_id in self.grid_studies:
            self.grid_studies[study_id]["findings"].append(finding)
            self._log_activity("finding_added", {
                "study_id": study_id,
                "finding": finding
            })
            return f"Finding added to study {study_id}"
        return f"Study ID {study_id} not found."

    # --- Modeling and Validation (PSCAD/PSSE) ---
    def use_modeling_tool(self, tool_id: str, project_id: str, study_type: str) -> str:
        """Use a modeling tool (PSCAD/PSSE) for a study."""
        if tool_id in self.modeling_tools and project_id in self.projects:
            self.modeling_tools[tool_id]["last_used"] = datetime.datetime.now().strftime("%Y-%m-%d")
            self._log_activity("tool_used", {
                "tool_id": tool_id,
                "project_id": project_id,
                "study_type": study_type
            })
            return f"Tool {self.modeling_tools[tool_id]['name']} used for {study_type} on project {project_id}"
        return f"Tool ID {tool_id} or Project ID {project_id} not found."

    def validate_system_model(self, project_id: str, tool_id: str, accuracy: float) -> str:
        """Validate system representation accuracy using modeling tools."""
        if project_id in self.projects and tool_id in self.modeling_tools:
            self.projects[project_id]["stability_score"] = accuracy
            self._log_activity("model_validated", {
                "project_id": project_id,
                "tool_id": tool_id,
                "accuracy": accuracy
            })
            return f"System model validated for project {project_id} with {accuracy}% accuracy using {self.modeling_tools[tool_id]['name']}"
        return f"Project ID {project_id} or Tool ID {tool_id} not found."

    # --- Power System Studies ---
    def create_power_study(self, project_id: str, study_type: str) -> str:
        """Create a power system study (power flow, short circuit, transient stability)."""
        if project_id in self.projects:
            study_id = f"PS{self.next_power_study_id}"
            self.next_power_study_id += 1
            self.power_studies[study_id] = {
                "project_id": project_id,
                "type": study_type,
                "results": {},
                "mitigations": []
            }
            self._log_activity("power_study_created", {
                "study_id": study_id,
                "project_id": project_id,
                "type": study_type
            })
            return f"Power System Study created with ID: {study_id}"
        return f"Project ID {project_id} not found."

    def add_study_results(self, study_id: str, results: Dict) -> str:
        """Add results to a power system study."""
        if study_id in self.power_studies:
            self.power_studies[study_id]["results"] = results
            self._log_activity("study_results_added", {
                "study_id": study_id,
                "results": results
            })
            return f"Results added to study {study_id}"
        return f"Study ID {study_id} not found."

    def add_mitigation(self, study_id: str, mitigation: Dict) -> str:
        """Add mitigation strategies to a power system study."""
        if study_id in self.power_studies:
            self.power_studies[study_id]["mitigations"].append(mitigation)
            self._log_activity("mitigation_added", {
                "study_id": study_id,
                "mitigation": mitigation
            })
            return f"Mitigation added to study {study_id}"
        return f"Study ID {study_id} not found."

    # --- Plant-Level Control Strategies ---
    def design_control_strategy(self, project_id: str, strategy_type: str, parameters: Dict) -> str:
        """Design a plant-level control strategy (e.g., voltage regulation, frequency control)."""
        if project_id in self.projects:
            strategy_id = f"CS{self.next_strategy_id}"
            self.next_strategy_id += 1
            self.control_strategies[strategy_id] = {
                "project_id": project_id,
                "type": strategy_type,
                "parameters": parameters,
                "performance": {
                    "resilience_improvement": 0.0,
                    "flexibility_improvement": 0.0
                }
            }
            self._log_activity("control_strategy_designed", {
                "strategy_id": strategy_id,
                "project_id": project_id,
                "type": strategy_type
            })
            return f"Control Strategy designed with ID: {strategy_id}"
        return f"Project ID {project_id} not found."

    def optimize_control_strategy(self, strategy_id: str, resilience: float, flexibility: float) -> str:
        """Optimize a control strategy and update performance metrics."""
        if strategy_id in self.control_strategies:
            self.control_strategies[strategy_id]["performance"] = {
                "resilience_improvement": resilience,
                "flexibility_improvement": flexibility
            }
            self._log_activity("strategy_optimized", {
                "strategy_id": strategy_id,
                "resilience": resilience,
                "flexibility": flexibility
            })
            return f"Control Strategy {strategy_id} optimized. Resilience: +{resilience}%, Flexibility: +{flexibility}%"
        return f"Strategy ID {strategy_id} not found."

    # --- Performance Metrics ---
    def add_performance_metric(self, project_id: str, metric: str, value: float, target: float) -> str:
        """Add a performance metric for a project."""
        if project_id in self.projects:
            metric_id = f"PM{self.next_metric_id}"
            self.next_metric_id += 1
            self.performance_metrics[metric_id] = {
                "project_id": project_id,
                "metric": metric,
                "value": value,
                "target": target,
                "achievement": (value / target) * 100 if target != 0 else 0
            }
            self._log_activity("metric_added", {
                "metric_id": metric_id,
                "project_id": project_id,
                "metric": metric,
                "value": value
            })
            return f"Performance Metric '{metric}' added with ID: {metric_id}. Achievement: {self.performance_metrics[metric_id]['achievement']:.1f}%"
        return f"Project ID {project_id} not found."

    # --- Audit Logging ---
    def _log_activity(self, action: str, details: Dict) -> None:
        """Log an activity to the audit trail."""
        log_entry = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "details": details
        }
        self.audit_logs.append(log_entry)

    def get_audit_logs(self) -> List[Dict]:
        """Retrieve all audit logs."""
        return self.audit_logs

    # --- Reporting ---
    def generate_project_report(self, project_id: str) -> Dict:
        """Generate a comprehensive report for a renewable energy project."""
        if project_id in self.projects:
            project = self.projects[project_id]
            report = {
                "project_id": project_id,
                "name": project["name"],
                "type": project["type"],
                "location": project["location"],
                "capacity_mw": project["capacity_mw"],
                "status": project["status"],
                "grid_code": project["grid_code"],
                "interconnection_date": project["interconnection_date"],
                "stability_score": project["stability_score"],
                "grid_studies": [gs for gs in self.grid_studies.values() if gs["project_id"] == project_id],
                "power_studies": [ps for ps in self.power_studies.values() if ps["project_id"] == project_id],
                "control_strategies": [cs for cs in self.control_strategies.values() if cs["project_id"] == project_id],
                "performance_metrics": [pm for pm in self.performance_metrics.values() if pm["project_id"] == project_id]
            }
            return report
        return {"error": "Project ID not found"}

    def generate_system_stability_report(self) -> Dict:
        """Generate a report on system stability across all projects."""
        report = {
            "total_projects": len(self.projects),
            "avg_stability_score": sum(proj["stability_score"] for proj in self.projects.values()) / len(self.projects) if self.projects else 0,
            "grid_studies": {
                "total": len(self.grid_studies),
                "compliant": sum(1 for gs in self.grid_studies.values() if gs["status"] == "Compliant"),
                "non_compliant": sum(1 for gs in self.grid_studies.values() if gs["status"] == "Non-Compliant")
            },
            "power_studies": {
                "total": len(self.power_studies),
                "types": {
                    "Power Flow": sum(1 for ps in self.power_studies.values() if ps["type"] == "Power Flow"),
                    "Short Circuit": sum(1 for ps in self.power_studies.values() if ps["type"] == "Short Circuit"),
                    "Transient Stability": sum(1 for ps in self.power_studies.values() if ps["type"] == "Transient Stability")
                }
            },
            "control_strategies": {
                "total": len(self.control_strategies),
                "avg_resilience_improvement": sum(cs["performance"]["resilience_improvement"] for cs in self.control_strategies.values()) / len(self.control_strategies) if self.control_strategies else 0,
                "avg_flexibility_improvement": sum(cs["performance"]["flexibility_improvement"] for cs in self.control_strategies.values()) / len(self.control_strategies) if self.control_strategies else 0
            }
        }
        return report

# --- Example Usage ---
if __name__ == "__main__":
    engineer = RenewableEnergyEngineer()

    # Create renewable energy projects
    print("=== Project Management ===")
    print(engineer.create_project("Solar Farm Alpha", "Solar", "Lagos, Nigeria", 50.0, "NEC-2021"))
    print(engineer.create_project("Wind Farm Beta", "Wind", "Kano, Nigeria", 100.0, "IEEE-1547"))
    print(engineer.update_project_status("PROJ1", "Commissioned", "2022-06-15"))

    # Grid Integration Studies
    print("\n=== Grid Integration Studies ===")
    print(engineer.create_grid_study("PROJ1", "Interconnection Assessment"))
    print(engineer.update_compliance("GS1", True, True, True))  # Compliant with all codes
    print(engineer.add_finding("GS1", {
        "issue": "Voltage Fluctuations",
        "severity": "Medium",
        "recommendation": "Install dynamic voltage regulators"
    }))

    # Modeling and Validation
    print("\n=== Modeling and Validation ===")
    print(engineer.use_modeling_tool("PSCAD1", "PROJ1", "Transient Stability Analysis"))
    print(engineer.use_modeling_tool("PSSE1", "PROJ1", "Power Flow Analysis"))
    print(engineer.validate_system_model("PROJ1", "PSCAD1", 98.5))  # 98.5% accuracy

    # Power System Studies
    print("\n=== Power System Studies ===")
    print(engineer.create_power_study("PROJ1", "Power Flow"))
    print(engineer.add_study_results("PS1", {
        "voltage_levels": "Within Limits",
        "power_losses": "2.5%",
        "congestion": "None"
    }))
    print(engineer.add_mitigation("PS1", {
        "issue": "High Power Losses",
        "mitigation": "Upgrade transmission lines",
        "cost": "$500,000"
    }))

    # Plant-Level Control Strategies
    print("\n=== Plant-Level Control Strategies ===")
    print(engineer.design_control_strategy("PROJ1", "Voltage Regulation", {
        "voltage_setpoint": 1.0,
        "response_time": "0.5s",
        "control_mode": "Automatic"
    }))
    print(engineer.optimize_control_strategy("CS1", 15.0, 20.0))  # 15% resilience, 20% flexibility improvement

    # Performance Metrics
    print("\n=== Performance Metrics ===")
    print(engineer.add_performance_metric("PROJ1", "System Stability", 95.0, 100.0))
    print(engineer.add_performance_metric("PROJ1", "Grid Compliance", 98.0, 100.0))

    # Generate Reports
    print("\n=== Project Report for Solar Farm Alpha ===")
    project_report = engineer.generate_project_report("PROJ1")
    for key, value in project_report.items():
        print(f"{key}: {value}")

    print("\n=== System Stability Report ===")
    stability_report = engineer.generate_system_stability_report()
    for key, value in stability_report.items():
        print(f"{key}: {value}")
