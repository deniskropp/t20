from typing import List, Optional, Union, Dict, Any
from .ast import Program, Statement, Command, IfStatement, Expression, Identifier, LiteralValue, Directive
from .tokens import TokenType
from t20.core.custom_types import Plan, Task, Role, Team, Prompt, AgentOutput

def generate_plan(program: Program) -> Plan:
    high_level_goal = "Executed KickLang Program"
    reasoning = "Generated from KickLang source."
    roles: List[Role] = []
    tasks: List[Task] = []
    
    role_map: Dict[str, Role] = {}

    def get_or_create_role(name: str) -> str:
        if name not in role_map:
            role_map[name] = Role(title=name, purpose=f"Role responsible for {name}")
            roles.append(role_map[name])
        return name

    def process_statements(statements: List[Statement]) -> List[Task]:
        generated_tasks: List[Task] = []
        for stmt in statements:
            if isinstance(stmt, Command):
                # PLAN Command
                if stmt.verb == TokenType.PLAN:
                    nonlocal high_level_goal
                    if stmt.args:
                        parts = []
                        for arg in stmt.args:
                             if isinstance(arg, Identifier): parts.append(arg.value)
                             elif isinstance(arg, LiteralValue): parts.append(str(arg.value))
                        high_level_goal = " ".join(parts)
                    
                    if stmt.subject and isinstance(stmt.subject, Identifier):
                        get_or_create_role(stmt.subject.value)
                
                # KNOWN Verbs
                elif stmt.verb != TokenType.IDENTIFIER and stmt.verb != TokenType.PLAN:
                     task_id = f"T-{len(tasks) + len(generated_tasks) + 1:02d}"
                     role_name = "GeneralAgent"
                     
                     if stmt.subject and isinstance(stmt.subject, Identifier):
                         task_id = stmt.subject.value
                     
                     description = f"Execute {stmt.verb.name}"
                     
                     arg_strs = []
                     for arg in stmt.args:
                         if isinstance(arg, Identifier): arg_strs.append(arg.value)
                         elif isinstance(arg, LiteralValue): arg_strs.append(str(arg.value))
                     
                     if arg_strs:
                         description += ": " + " ".join(arg_strs)
                         
                     generated_tasks.append(Task(
                         id=task_id,
                         description=description,
                         role=get_or_create_role(role_name),
                         agent="Agent1",
                         deps=[]
                     ))

                # UNKNOWN Verbs
                elif stmt.verb == TokenType.IDENTIFIER:
                    real_args = stmt.args
                    if len(real_args) >= 3:
                         t_id_node = real_args[0]
                         role_node = real_args[1]
                         verb_node = real_args[2]
                         
                         if isinstance(t_id_node, Identifier) and isinstance(role_node, Identifier) and isinstance(verb_node, Identifier):
                             task_id = t_id_node.value
                             role_name = role_node.value
                             action_verb = verb_node.value
                             
                             params = []
                             for a in real_args[3:]:
                                 if isinstance(a, Identifier): params.append(a.value)
                                 elif isinstance(a, LiteralValue): params.append(str(a.value))
                             
                             description = f"{action_verb} " + " ".join(params)
                             
                             generated_tasks.append(Task(
                                 id=task_id,
                                 description=description,
                                 role=get_or_create_role(role_name),
                                 agent="Agent1",
                                 deps=[],
                                 subtasks=process_statements(stmt.block) if stmt.block else None
                             ))
                    elif len(real_args) > 0:
                         if isinstance(real_args[0], Identifier) and real_args[0].value == "END":
                             continue 

            elif isinstance(stmt, IfStatement):
                 condition_str = "Condition"
                 if stmt.condition:
                     parts = []
                     for c in stmt.condition:
                         if isinstance(c, Identifier): parts.append(c.value)
                     condition_str = " ".join(parts)

                 subtasks = []
                 if stmt.then_block:
                     subtasks.extend(process_statements(stmt.then_block))
                 if stmt.else_block:
                     subtasks.extend(process_statements(stmt.else_block))

                 task_id = f"IF-{len(tasks) + len(generated_tasks)}"
                 generated_tasks.append(Task(
                     id=task_id,
                     description=f"Check if {condition_str}",
                     role=get_or_create_role("LogicController"),
                     agent="System",
                     deps=[],
                     subtasks=subtasks if subtasks else None
                 ))
        return generated_tasks

    tasks = process_statements(program.statements)

    return Plan(
        high_level_goal=high_level_goal,
        reasoning=reasoning,
        roles=roles,
        tasks=tasks
    )

