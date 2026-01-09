"""
Graph Backend Module for KickLang SDK.
Defines the interface for Graph Backends and provides a Python-based implementation
with JIT optimizations.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union, Callable
from dataclasses import dataclass, field
from functools import lru_cache
import re
import logging

logger = logging.getLogger(__name__)

@dataclass
class ConditionNode:
    type: str  # "AND", "OR", "EXPRESSION"
    left: Optional[List['ConditionNode']] = None
    right: Optional[List['ConditionNode']] = None
    property: Optional[str] = None
    operator: Optional[str] = None
    value: Any = None

@dataclass
class ParsedQuery:
    entity_type: str
    conditions: Optional[ConditionNode]
    limit: Optional[int]
    is_count: bool = False
    target_id: Optional[str] = None  # For traversal
    relationship_type: Optional[str] = None  # For traversal

class QueryParser:
    """Parses query strings into structured ParsedQuery objects."""
    
    def __init__(self):
        self._tokens = []
        self._pos = 0

    def parse_query(self, query_string: str) -> ParsedQuery:
        """Parses a full query string."""
        # Unified regex: (find|count) <entity> [related to <id> [via <type>]] [where <cond>] [limit <num>]
        base_regex = r"(?:find|count) (\w+)(?: related to \"?([\w\-]+)\"?)?(?: via \"?([\w\-]+)\"?)?(?: where (.+?))?(?: limit (\d+))?$"
        query_pattern = re.compile(base_regex, re.IGNORECASE)
        match = query_pattern.match(query_string.strip())
        
        is_count = False
        if query_string.strip().lower().startswith("count"):
            is_count = True

        if not match:
             raise ValueError("Invalid query format.")

        entity_type = match.group(1)
        target_id = match.group(2)
        rel_type = match.group(3)
        condition_str = match.group(4)
        limit_str = match.group(5)
        
        conditions = self.parse_conditions(condition_str) if condition_str else None
        limit = int(limit_str) if limit_str else None

        return ParsedQuery(
            entity_type=entity_type, 
            conditions=conditions, 
            limit=limit,
            is_count=is_count,
            target_id=target_id,
            relationship_type=rel_type
        )

    def parse_conditions(self, condition_str: str) -> ConditionNode:
        """Parses the 'where' clause conditions."""
        self._tokens = self.tokenize(condition_str)
        self._pos = 0
        return self._parse_condition_recursive()

    def tokenize(self, condition_str: str) -> List[str]:
        """Tokenizes the condition string."""
        token_regex = re.compile(
            r"(\b(?:and|or|related|to|via|count)\b)|"    # 1. Keywords
            r"([=!<>]=?|contains|in)|"           # 2. Operators
            r"\"([^\"]*)\"|'([^']*)'|"           # 3. Strings
            r"(\(|\))|"                          # 4. Parentheses
            r"([\w.]+)"                          # 5. Identifiers
            , re.IGNORECASE
        )
        
        tokens = []
        for match in token_regex.finditer(condition_str):
            if match.group(1): tokens.append(match.group(1).lower())
            elif match.group(2): tokens.append(match.group(2))
            elif match.group(3) is not None: tokens.append(match.group(3))
            elif match.group(4) is not None: tokens.append(match.group(4))
            elif match.group(5): tokens.append(match.group(5))
            elif match.group(6): tokens.append(match.group(6))
        
        return tokens

    def _parse_condition_recursive(self) -> ConditionNode:
        """Recursive descent parser implementation."""
        node = self._parse_expression()
        
        while self._pos < len(self._tokens):
            token = self._tokens[self._pos]
            if token == ')': break
            if token.lower() in ['and', 'or']:
                self._pos += 1
                right = self._parse_condition_recursive()
                node = ConditionNode(type=token.upper(), left=[node], right=[right])
            else:
                break
        return node

    def _parse_expression(self) -> ConditionNode:
        """Parses a single expression or parenthesized condition."""
        if self._pos >= len(self._tokens): raise ValueError("Unexpected end of query")
        token = self._tokens[self._pos]
        
        if token == '(':
            self._pos += 1
            node = self._parse_condition_recursive()
            if self._pos < len(self._tokens) and self._tokens[self._pos] == ')': self._pos += 1
            else: raise ValueError("Missing closing parenthesis")
            return node
            
        prop = token
        self._pos += 1
        if self._pos >= len(self._tokens): raise ValueError(f"Unexpected end of query after property '{prop}'")
        op = self._tokens[self._pos]
        self._pos += 1
        if self._pos >= len(self._tokens): raise ValueError(f"Unexpected end of query after operator '{op}'")
        val = self._tokens[self._pos]
        self._pos += 1
        
        return ConditionNode(type="EXPRESSION", property=prop, operator=op, value=self._convert_value(val))

    def _convert_value(self, val: str) -> Any:
        try:
             f_val = float(val)
             if f_val.is_integer(): return int(f_val)
             return f_val
        except ValueError:
             if val.lower() == 'true': return True
             if val.lower() == 'false': return False
             return val

class GraphBackend(ABC):
    """Abstract Base Class for Graph Storage Backends."""
    
    @abstractmethod
    def add_concept(self, concept: Dict[str, Any]) -> bool:
        pass
        
    @abstractmethod
    def add_relationship(self, relationship: Dict[str, Any]) -> bool:
        pass
        
    @abstractmethod
    def query(self, query_string: str) -> Union[List[Any], int, Exception]:
        pass

class PythonGraphBackend(GraphBackend):
    """In-memory Python implementation with JIT compilation."""
    
    def __init__(self):
        self._concepts: Dict[str, Dict[str, Any]] = {}
        self._relationships: List[Dict[str, Any]] = []
        self._roles: Dict[str, Dict[str, Any]] = {}
        self._agents: Dict[str, Dict[str, Any]] = {}
        
        self._idx_source: Dict[str, List[Dict[str, Any]]] = {}
        self._idx_target: Dict[str, List[Dict[str, Any]]] = {}
        
        # Inverted Index: { "properties.domain": { "CS": {"C1", "C3"} } }
        self._idx_properties: Dict[str, Dict[Any, set]] = {}
        
        self._parser = QueryParser()
        self._compiled_cache: Dict[str, Callable[[Any], bool]] = {}

    def add_concept(self, concept: Dict[str, Any]) -> bool:
        c_id = concept.get('id')
        if not c_id: return False
        if c_id in self._concepts: return False
        self._concepts[c_id] = concept
        
        # Index properties
        if 'properties' in concept:
            self._index_entity(c_id, concept['properties'], prefix="properties")
            
        return True

    def _index_entity(self, entity_id: str, data: Dict[str, Any], prefix: str):
        """Recursively indexes scalar values in the data dict."""
        for key, value in data.items():
            path = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                self._index_entity(entity_id, value, path)
            elif isinstance(value, (str, int, float, bool)):
                if path not in self._idx_properties:
                    self._idx_properties[path] = {}
                if value not in self._idx_properties[path]:
                    self._idx_properties[path][value] = set()
                self._idx_properties[path][value].add(entity_id)

    def add_relationship(self, relationship: Dict[str, Any]) -> bool:
        if 'source' not in relationship or 'target' not in relationship or 'type' not in relationship:
            return False
            
        self._relationships.append(relationship)
        
        src = relationship['source']
        tgt = relationship['target']
        
        if src not in self._idx_source: self._idx_source[src] = []
        self._idx_source[src].append(relationship)
        
        if tgt not in self._idx_target: self._idx_target[tgt] = []
        self._idx_target[tgt].append(relationship)
        
        return True

    def query(self, query_string: str) -> Union[List[Any], int, Exception]:
        try:
            parsed = self._parser.parse_query(query_string)
            entities = self._get_entities(parsed.entity_type)
            
            # Traversal
            if parsed.target_id:
                related_ids = set()
                outgoing = self._idx_source.get(parsed.target_id, [])
                for rel in outgoing:
                    if not parsed.relationship_type or rel.get('type') == parsed.relationship_type:
                        related_ids.add(rel.get('target'))
                incoming = self._idx_target.get(parsed.target_id, [])
                for rel in incoming:
                    if not parsed.relationship_type or rel.get('type') == parsed.relationship_type:
                        related_ids.add(rel.get('source'))
                if parsed.entity_type.lower().startswith('concept'):
                    entities = [self._concepts[rid] for rid in related_ids if rid in self._concepts]
                else:
                    entities = [e for e in entities if e.get('id') in related_ids]

            # Index Optimization: Pre-filter potential candidates
            if parsed.conditions and parsed.entity_type.lower().startswith('concept'):
                # Try to use property index
                candidates = self._get_candidates(parsed.conditions)
                if candidates is not None:
                    # Intersect traversal results with index results if both exist
                    # 'entities' currently holds the traversal result (or full list)
                    # We can optimized by filtering 'entities' against 'candidates'
                    
                    # If we haven't filtered by traversal (entities is full list), just map candidates
                    # Else filter existing.
                    candidate_set = candidates
                    entities = [e for e in entities if e.get('id') in candidate_set]

            # JIT Filter
            if query_string in self._compiled_cache:
                matcher = self._compiled_cache[query_string]
            else:
                matcher = self._compile_condition(parsed.conditions)
                self._compiled_cache[query_string] = matcher

            filtered = [e for e in entities if matcher(e)]
            
            if parsed.is_count: return len(filtered)
            if parsed.limit: return filtered[:parsed.limit]
            return filtered
            
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return e

    def _get_entities(self, entity_type: str) -> List[Any]:
        if entity_type.lower().startswith('concept'): return list(self._concepts.values())
        if entity_type.lower().startswith('relationship'): return self._relationships
        if entity_type.lower().startswith('role'): return list(self._roles.values())
        if entity_type.lower().startswith('agent'): return list(self._agents.values())
        raise ValueError(f"Unknown entity type: {entity_type}")

    def _get_candidates(self, node: Optional[ConditionNode]) -> Optional[set]:
        """
        Returns a set of entity IDs that POTENTIALLY match the condition.
        Returns None if index cannot be used (implies 'Scan All').
        """
        if not node: return None
        
        if node.type == 'AND':
            left = self._get_candidates(node.left[0]) if node.left else None
            right = self._get_candidates(node.right[0]) if node.right else None
            
            if left is not None and right is not None:
                return left.intersection(right)
            # If one is indexed and other is not, we can restrict search to the indexed one!
            if left is not None: return left
            if right is not None: return right
            return None
            
        if node.type == 'OR':
            left = self._get_candidates(node.left[0]) if node.left else None
            right = self._get_candidates(node.right[0]) if node.right else None
            
            # For OR, we need BOTH sides to be indexable to narrow the search. 
            # If one side is unknown, we must scan all.
            if left is not None and right is not None:
                return left.union(right)
            return None
            
        if node.type == 'EXPRESSION':
            # We only index equality for now
            if node.operator in ('=', None) and node.property in self._idx_properties:
                idx = self._idx_properties[node.property]
                val = node.value
                if val in idx:
                    return idx[val]
                return set() # Empty set, value not found in index
        
        return None

    def _compile_condition(self, node: Optional[ConditionNode]) -> Callable[[Any], bool]:
        if not node: return lambda e: True
        
        if node.type == 'AND':
            left = self._compile_condition(node.left[0]) if node.left else (lambda e: True)
            right = self._compile_condition(node.right[0]) if node.right else (lambda e: True)
            return lambda e: left(e) and right(e)
            
        if node.type == 'OR':
            left = self._compile_condition(node.left[0]) if node.left else (lambda e: False)
            right = self._compile_condition(node.right[0]) if node.right else (lambda e: False)
            return lambda e: left(e) or right(e)
            
        if node.type == 'EXPRESSION':
            path = node.property.split('.') if node.property else []
            t_val = node.value
            op = node.operator.lower() if node.operator else '='
            
            def getter(obj):
                curr = obj
                for p in path:
                    if isinstance(curr, dict): curr = curr.get(p)
                    else: return None
                    if curr is None: return None
                return curr

            if op == '=': return lambda e: getter(e) == t_val
            if op == '!=': return lambda e: getter(e) != t_val
            if op == '>': return lambda e: (v:=getter(e)) is not None and v > t_val
            if op == '<': return lambda e: (v:=getter(e)) is not None and v < t_val
            if op == '>=': return lambda e: (v:=getter(e)) is not None and v >= t_val
            if op == '<=': return lambda e: (v:=getter(e)) is not None and v <= t_val
            if op == 'contains': return lambda e: (v:=getter(e)) is not None and (t_val in v if isinstance(v, (list, str)) else False)
            if op == 'in': 
                l_val = t_val if isinstance(t_val, list) else [t_val]
                return lambda e: (v:=getter(e)) is not None and v in l_val

            return lambda e: False
        return lambda e: False

class WasmGraphBackend(GraphBackend):
    """Stub for future WebAssembly backend."""
    def __init__(self, wasm_module_path: str):
        self.wasm_path = wasm_module_path
        logger.warning("WasmGraphBackend is not yet implemented.")
        
    def add_concept(self, concept: Dict[str, Any]) -> bool:
        raise NotImplementedError("WASM Backend not active")

    def add_relationship(self, relationship: Dict[str, Any]) -> bool:
        raise NotImplementedError("WASM Backend not active")

    def query(self, query_string: str) -> Union[List[Any], int, Exception]:
        raise NotImplementedError("WASM Backend not active")
