from __future__ import annotations

import jijmodeling as jm
from google.protobuf.text_encoding import CEscape, CUnescape

from jijzept_dashboard_client import schema


# Remove "\displaystyle" & "$$ " from the latex string
def sanitize_latex(latex: str) -> str:
    text = latex.replace("$$", "").replace("\\displaystyle ", "")
    return text


class Problem:
    def __init__(self, name: str):
        """
        Create a Problem instance with descriptions.

        Args:
            name (str): The name of the problem.
        """
        self.name = name
        self.constraints: dict[str, jm.Constraint] = {}
        self.constraint_description: dict[str, str] = {}
        self.obj_description = ""
        self.objective = 0

    # Support += operator
    def __iadd__(
        self,
        expr_description: tuple[jm.Constraint, str] | jm.Constraint,
    ) -> Problem:
        if isinstance(expr_description, tuple):
            INTENDED_TUPLE_LENGTH = 2
            if len(expr_description) != INTENDED_TUPLE_LENGTH:
                raise ValueError("The tuple must have 2 elements")
            expr, description = expr_description
        else:
            expr = expr_description
            description = ""

        if isinstance(expr, jm.Constraint):
            self.constraints[expr.name] = expr
            self.constraint_description[expr.name] = description
        else:
            self.objective = expr
            self.obj_description = description
        return self

    def get_jm_problem(self) -> jm.Problem:
        problem = jm.Problem(self.name)
        for c in self.constraints.values():
            problem += c
        problem += self.objective
        return problem

    # このメソッドがこのセクションにおける具体的な処理
    def to_serializable(self) -> dict:
        problem = self.get_jm_problem()

        def _extract_vars(expr) -> list:
            vars = [
                {
                    "name": var.name,
                    "latex": sanitize_latex(var._repr_latex_()),
                    "description": (
                        "" if var.description is None else var.description
                    ),
                }
                for var in jm.extract_variables(expr)
                if isinstance(
                    var,
                    (
                        jm.Placeholder,
                        jm.BinaryVar,
                        jm.IntegerVar,
                        jm.ContinuousVar,
                        jm.SemiIntegerVar,
                        jm.SemiContinuousVar,
                    ),
                )
            ]
            return vars

        # Objective ------------------------------------------
        objective = schema.Objective(
            latex=sanitize_latex(problem.objective._repr_latex_()),
            description=self.obj_description,
            related_variables=_extract_vars(problem.objective),
        )

        constraints = [
            schema.Constraint(
                name=constraint.name,
                latex=sanitize_latex(constraint._repr_latex_()),
                description=self.constraint_description[constraint.name],
                related_variables=_extract_vars(constraint),
            )
            for constraint in problem.constraints.values()
        ]

        DecisionVarType = (
            jm.BinaryVar,
            jm.IntegerVar,
            jm.ContinuousVar,
            jm.SemiIntegerVar,
            jm.SemiContinuousVar,
        )
        vars = [
            var
            for var in jm.extract_variables(problem)
            if isinstance(var, DecisionVarType)
        ]
        decision_vars = []
        for var in vars:
            if isinstance(var, jm.BinaryVar):
                lower_bound = "0"
                upper_bound = "1"
                kind = schema.DecisionVarKind.binary
            else:
                lower_bound = sanitize_latex(var.lower_bound._repr_latex_())
                upper_bound = sanitize_latex(var.upper_bound._repr_latex_())
                if isinstance(var, jm.IntegerVar):
                    kind = schema.DecisionVarKind.integer
                elif isinstance(var, jm.ContinuousVar):
                    kind = schema.DecisionVarKind.continuous
                elif isinstance(var, jm.SemiIntegerVar):
                    kind = schema.DecisionVarKind.semi_integer
                elif isinstance(var, jm.SemiContinuousVar):
                    kind = schema.DecisionVarKind.semi_continuous

            lower_bound = (
                "0"
                if isinstance(var, jm.BinaryVar)
                else sanitize_latex(var.lower_bound._repr_latex_())
            )
            upper_bound = (
                "1"
                if isinstance(var, jm.BinaryVar)
                else sanitize_latex(var.upper_bound._repr_latex_())
            )
            decision_vars.append(
                schema.DecisionVar(
                    name=var.name,
                    kind=kind,
                    lower_bound=lower_bound,
                    upper_bound=upper_bound,
                    shape=[
                        sanitize_latex(s._repr_latex_()) for s in var.shape
                    ],
                    latex=sanitize_latex(var._repr_latex_()),
                    description=var.description,
                ),
            )

        vars = [
            var
            for var in jm.extract_variables(problem)
            if isinstance(var, (jm.Placeholder, jm.ArrayLength))
        ]
        constants = []
        for var in vars:
            if isinstance(var, jm.Placeholder):
                constants.append(
                    schema.Constant(
                        name=var.name,
                        ndim=var.ndim,
                        latex=sanitize_latex(var._repr_latex_()),
                        description=(
                            "" if var.description is None else var.description
                        ),
                    ),
                )
            else:
                constants.append(
                    schema.Constant(
                        name=(f"length of {var.array.name} " f"at {var.axis}"),
                        ndim=0,
                        latex=sanitize_latex(var._repr_latex_()),
                        description=(
                            "" if var.description is None else var.description
                        ),
                    ),
                )

        return schema.Source(
            serializable=CEscape(jm.to_protobuf(problem), as_utf8=False),
            objective=objective,
            constraints=constraints,
            decision_vars=decision_vars,
            constants=constants,
            name=problem.name,
        ).model_dump()

    @classmethod
    def from_serializable(cls, serializable: dict) -> Problem:
        prob_proto = serializable["serializable"]
        prob: jm.Problem = jm.from_protobuf(CUnescape(prob_proto))
        p = cls(prob.name)
        p.objective = prob.objective
        for const in prob.constraints.values():
            p.constraints[const.name] = const
        p.obj_description = serializable["objective"]["description"]
        for const in serializable["constraints"]:
            p.constraint_description[const["name"]] = const["description"]
        return p

    @classmethod
    def from_jm_problem(
        cls,
        jm_problem: jm.Problem,
        objective_description: str = "",
        constraint_descriptions: dict[str, str] = {},
    ) -> Problem:
        """
        Create a Problem instance from a Problem instance of jijmodeling.

        Args:
            jm_problem (jm.Problem): A Problem instance of jijmodeling.
            objective_description (str):
                A description of the objective function.
            constraint_descriptions (dict[str, str]):
                A dictionary of constraint names and their descriptions.

        Returns:
            Problem: A Problem with descriptions.
        """
        for constr_name in constraint_descriptions.keys():
            if constr_name not in jm_problem.constraints:
                raise ValueError(
                    f"Constraint {constr_name} is not found "
                    f"in the `jm_problem`."
                )

        jdc_problem = cls(jm_problem.name)
        jdc_problem += (jm_problem.objective, objective_description)

        for k, v in jm_problem.constraints.items():
            if k in constraint_descriptions:
                jdc_problem += (v, constraint_descriptions[k])
            else:
                jdc_problem += v

        return jdc_problem
