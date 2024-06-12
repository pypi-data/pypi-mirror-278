# Copyright 2019-2023 Ingmar Dasseville, Pierre Carbonnelle
#
# This file is part of IDP-Z3.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

Methods to annotate the Abstract Syntax Tree (AST) of an IDP-Z3 program.

"""
from __future__ import annotations

from copy import copy, deepcopy
from itertools import chain
from typing import Union, List, NamedTuple, Optional
import string  # .digits

from .Parse import (IDP, Vocabulary, Import, TypeDeclaration, Declaration,
                    SymbolDeclaration, VarDeclaration, TheoryBlock, Definition,
                    Rule, Structure, SymbolInterpretation, Enumeration, Ranges,
                    FunctionEnum, TupleIDP, ConstructedFrom, Display)
from .Expression import (ASTNode, Expression, SETNAME, SetName,
                         BOOL_SETNAME, INT_SETNAME, REAL_SETNAME, DATE_SETNAME,
                         Constructor, CONSTRUCTOR, AIfExpr, IF,
                         AQuantification, Quantee, ARImplication, AImplication,
                         AEquivalence, AConjunction, ADisjunction,
                         Operator, AComparison, ASumMinus, AMultDiv, APower, AUnary,
                         AAggregate, AppliedSymbol, UnappliedSymbol, Variable,
                         VARIABLE, Brackets, SymbolExpr, Number, NOT,
                         EQUALS, AND, OR, TRUE, FALSE, ZERO, IMPLIES, FORALL, EXISTS)
from .utils import (BOOL, INT, REAL, DATE, CONCEPT, RESERVED_SYMBOLS,
                    OrderedSet, Semantics, IDPZ3Error, split_prefix)
from .WDF import is_subset_of

Exceptions = Union[Exception, List["Exceptions"]]  # nested list of Exceptions

Annotated = Expression
# class Annotated(NamedTuple):
#     node: Expression
#     wdf: Expression
#     warnings: Exceptions


# Class Vocabulary  #######################################################

def annotate_block(self: ASTNode,
                   idp: IDP,
                   ) -> Exceptions:
    assert isinstance(self, Vocabulary), "Internal error"
    self.idp = idp

    # process Import and determine the constructors of CONCEPT
    temp: dict[str, Declaration] = {}  # contains the new self.declarations
    for s in self.declarations:
        if isinstance(s, Import):
            other = self.idp.vocabularies[s.name]
            for s1 in other.declarations:
                if s1.name in temp:
                    s.check(str(temp[s1.name]) == str(s1),
                            f"Inconsistent declaration for {s1.name}")
                temp[s1.name] = s1

            # Also extend the current voc with the declared prefixes of the
            # imported block (but first check for clashes).
            for k, v in other.declared_prefixes.items():
                s.check(k not in self.declared_prefixes or
                        self.declared_prefixes[k] == v,
                        f'Conflicting prefix: {k}')
                self.declared_prefixes[k] = v
        else:
            s.block = self
            s.check(s.name not in temp or s.name in RESERVED_SYMBOLS,
                    f"Duplicate declaration of {s.name}")
            temp[s.name] = s

    self.declarations = list(temp.values())

    # annotate declarations
    for s in self.declarations:
        s.annotate_declaration(self)  # updates self.symbol_decls

    BOOL_SETNAME.annotate(self, {})
    INT_SETNAME.annotate(self, {})
    REAL_SETNAME.annotate(self, {})
    DATE_SETNAME.annotate(self, {})

    concepts = self.symbol_decls[CONCEPT]
    concepts.constructors=([CONSTRUCTOR(f"`{s}")
                            for s in [BOOL, INT, REAL, DATE, CONCEPT]]
                          +[CONSTRUCTOR(f"`{s.name}")
                            for s in temp.values()
                            if s.name not in RESERVED_SYMBOLS
                            and type(s) in Declaration.__args__])
    for c in concepts.constructors:
        c.concept_decl = self.symbol_decls[c.name[1:]]
        c.codomain = SetName(self, CONCEPT, c.concept_decl.domains,
                          c.concept_decl.codomain).annotate(self, {})

        self.symbol_decls[c.name] = c
        concepts.map[str(c)] = UnappliedSymbol.construct(c)
    return []
Vocabulary.annotate_block = annotate_block


# Class TypeDeclaration  #######################################################

def annotate_declaration(self: ASTNode,
                         voc: Vocabulary,
                         ) -> ASTNode:
    assert isinstance(self, TypeDeclaration), "Internal error"
    self.check(self.name not in voc.symbol_decls,
                f"duplicate declaration in vocabulary: {self.name}")
    voc.symbol_decls[self.name] = self
    for s in self.super_sets:
        s.annotate(voc, {})
    for s in self.domains:
        s.annotate(voc, {})
    self.codomain.annotate(voc, {})
    for c in self.constructors:
        c.codomain = self.domains[0]
        self.check(c.name not in voc.symbol_decls
                   or self.name == CONCEPT or self.super_set,
                    f"duplicate '{c.name}' constructor for '{self.name}' type")
        voc.symbol_decls[c.name] = c
    if self.interpretation:
        self.interpretation.annotate(voc, {})
        if isinstance(self.interpretation.enumeration, Ranges):
            self.super_set = self.interpretation.enumeration.type
            self.super_sets = [self.super_set]
    self.symbol_expr = SymbolExpr.make(self)

    # Verify prefix.
    self.prefix = split_prefix(self.name)
    self.check(self.prefix in voc.declared_prefixes or self.prefix is None,
               f"Unknown prefix for {self.name}")

    return self
TypeDeclaration.annotate_declaration = annotate_declaration


# Class SymbolDeclaration  #######################################################

def is_subsetname_of(d: SetName, s: SetName):
    if d == s: return TRUE
    if isinstance(d.decl, TypeDeclaration):  # can't go further up
        return FALSE
    if d.decl.super_sets[0] != d:
        return is_subsetname_of(d.decl.super_sets[0], s)
    return FALSE


def annotate_declaration(self: SymbolDeclaration,
                         voc: Vocabulary,
                         ) -> ASTNode:
    self.check(self.name is not None, "Internal error")
    self.check(self.name not in voc.symbol_decls,
                f"duplicate declaration in vocabulary: {self.name}")

    # annotate sorts -> sort_
    self.sort_.annotate(voc, {})
    self.sort_.check(isinstance(self.sort_.decl, TypeDeclaration),
               f"Type signature can only have types (found {self.sort_})")

    voc.symbol_decls[self.name] = self
    for s in self.sorts:
        s.annotate(voc, {})
        s.check(isinstance(s.decl, TypeDeclaration),
            f"Type signature can only have types (found {s})")

    # annotate domain and codomain
    self.codomain.annotate(voc, {})
    self.codomain.check(self.codomain.root_set is not None and len(self.codomain.root_set) == 1,
            f"Can't use n-ary {self.codomain.name} in a domain signature")

    # validations
    if self.repeat_name:
        self.check(False,
                   f"Subset relation is not supported for the moment (for {self.name})")
        self.check(self.codomain == BOOL_SETNAME or self.name in RESERVED_SYMBOLS,
                   f"Can't use subset relation in function declaration for {self.name}")
        self.check(self.repeat_name == self.name,
                    f"Expecting {self.name}, found {self.repeat_name}")
        self.check(self.sort_ == BOOL_SETNAME,
                    f"Subset relation can only be specified for predicates")
    elif self.domains != self.sorts:
        self.check(self.partiality != "total",
                   f"Can't declare a domain for total function {self.name}")
        self.check(self.codomain != BOOL_SETNAME or self.name in RESERVED_SYMBOLS,
                   f"Can't use domain in predicate declaration for {self.name}")
    if (len(self.sorts) == 0  # partial constant
        or (len(self.sorts) == 1 and not self.sorts[0].root_set)):  # TODO drop
        if self.domains:
            self.check(len(self.domains) == 1 and not self.domains[0].root_set,
                       f"Incorrect arity of domain: {self.domains[0]}")
            self.domains[0].annotate(voc, {})
            self.domains[0].check(not self.domains[0].root_set,
                    f"Expected arity 0 for {self.domains[0]} (found type {self.domains[0].root_set})")
        if self.super_sets:
            self.check(len(self.super_sets) == 1 and not self.super_sets[0].root_set,
                       f"Incorrect arity of superset: {self.super_sets[0]}")
            self.super_sets[0].annotate(voc, {})
            self.super_sets[0].check(not self.super_sets[0].root_set,
                    f"Expected arity 0 for {self.super_sets[0]} (found type {self.super_sets[0].root_set})")
    else:
        if len(self.sorts) == len(self.domains):  # domain: p1*pn
            for s, d in zip(self.sorts, self.domains):
                d.annotate(voc, {})
                d.check(d.root_set is not None and len(d.root_set) == 1,
                        f"Can't use n-ary {d.name} in a domain signature")
                try:
                    is_subsetname_of(d, s)  # raises an error if not
                except IDPZ3Error:
                    d.check(False, f"{d} is not a subset of {s}")
        else:  # domain: p
            self.domains[0].check(len(self.domains) == 1,
                   f"Incorrect arity of domain {self.domains}")
            self.domains[0].annotate(voc, {})
            self.domains[0].check(len(self.domains[0].root_set) == len(self.sorts),
                   f"Incorrect arity of domain {self.domains}")
            for s, d in zip(self.sorts, self.domains[0].decl.domains):
                d.annotate(voc, {})
                try:
                    is_subsetname_of(d, s)  # raises an error if not
                except IDPZ3Error:
                    d.check(False, f"{d} is not a subset of {s}")

        # the same, for super_sets
        if len(self.sorts) == len(self.super_sets):  # super_set: p1*pn
            for s, d in zip(self.sorts, self.super_sets):
                d.annotate(voc, {})
                d.check(d.root_set is not None and len(d.root_set) == 1,
                        f"Can't use n-ary {d.name} in a superset")
                try:
                    is_subsetname_of(d, s)  # raises an error if not
                except IDPZ3Error:
                    d.check(False, f"{d} is not a subset of {s}")
        else:  # super_set: p
            self.super_sets[0].check(len(self.super_sets) == 1,
                    f"Incorrect arity of superset {self.super_sets}")
            self.super_sets[0].annotate(voc, {})
            self.super_sets[0].check(len(self.super_sets[0].root_set) == len(self.sorts),
                   f"Incorrect arity of domain {self.super_sets}")
            for s, d in zip(self.sorts, self.super_sets[0].decl.super_sets):
                d.annotate(voc, {})
                try:
                    is_subsetname_of(d, s)  # raises an error if not
                except IDPZ3Error:
                    d.check(False, f"{d} is not a subset of {s}")

    self.arity = len(self.sorts)

    for s in chain(self.sorts, [self.sort_]):
        self.check(s.name != CONCEPT or s == s, # use equality to check nested concepts
                   f"`Concept` must be qualified with a type signature in {self}")

    # Verify prefix.
    self.prefix = split_prefix(self.name)
    self.check(self.prefix in voc.declared_prefixes or self.prefix is None,
               f"Unknown prefix for {self.name}")

    self.symbol_expr = SymbolExpr.make(self)
    return self
SymbolDeclaration.annotate_declaration = annotate_declaration


# Class VarDeclaration  #######################################################

def annotate_declaration(self: ASTNode,
                         voc: Vocabulary,
                         ) -> ASTNode:
    assert isinstance(self, VarDeclaration), "Internal error"
    self.check(self.name not in voc.symbol_decls,
                f"duplicate declaration in vocabulary: {self.name}")
    self.check(self.name == self.name.rstrip(string.digits),
                f"Variable {self.name} cannot be declared with a digital suffix.")
    voc.symbol_decls[self.name] = self
    self.subtype.annotate(voc, {})
    return self
VarDeclaration.annotate_declaration = annotate_declaration


# Class SetName  #######################################################

def root_set(s: SetName) -> List[SetName]:
    """ Recursively finds the root sets of a set in the hierarchy.

    For a set of tuples of domain elements, it returns
    the list of root sets of the elements of the tuple.
    For example, the root sets of `p: T1 * T2 -> Bool` are `[T1, T2]`

    It goes up the hierarchy until a declared type or a Concept[..] is found.
    """
    if type(s.decl) == TypeDeclaration:
        if s.decl.super_set and s.decl.super_set != s:  # a sub-type
            return root_set(s.decl.super_sets[0])
        elif s.decl.interpretation and hasattr(s.decl.interpretation.enumeration, "type"):
            return [s.decl.interpretation.enumeration.type]  # numeric type of the interpretation
        else:
            return [s]
    elif s.name == CONCEPT:
        return [s]
    elif s.decl.arity == 0:
        return []
    return [root_set(s1)[0] for s1 in s.decl.super_sets]

def annotate(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    assert isinstance(self, SetName), "Internal error"
    if self.name in q_vars:
        return q_vars[self.name]

    self.check(self.name in voc.symbol_decls,
               f'Undeclared symbol name: "{self.name}"')

    self.decl = voc.symbol_decls[self.name]
    self.variables = set()
    self.type = self.decl.codomain
    self.root_set = root_set(self)
    if self.codomain:  # a concept domain
        self.concept_domains = [s.annotate(voc, q_vars) for s in self.concept_domains]
        if len(self.concept_domains) != 1:  # concept_domains: p1*pn
            for s in self.concept_domains:
                s.check(s.root_set is not None and len(s.root_set) <= 1,
                        f"Can't use n-ary {s.name} in a type signature")
        else:  # concept_domains: p
            self.concept_domains[0].check(self.concept_domains[0].root_set is not None,
                                          f"Internal error")
        self.codomain = self.codomain.annotate(voc, q_vars)
    return self
SetName.annotate = annotate


# Class TheoryBlock  #######################################################

def collect_warnings(expr: Expression, out):
    """recursively finds the deepest Expression that is not well-defined in expr,
    and create a warning"""
    if not expr.WDF or expr.WDF.same_as(TRUE):  # well-defined
        return

    for e in expr.sub_exprs:  # recursive search
        collect_warnings(e, out)

    # Expression whose arguments are well-defined
    if all(not e.WDF or e.WDF.same_as(TRUE) for e in expr.sub_exprs):
        if expr.WDF and expr.WDF.same_as(FALSE):
            out.append(IDPZ3Error(
                f"Domain error: {expr.code[:20]} is undefined",
                node=expr, error=True))
        else:
            out.append(IDPZ3Error(
                f"Domain error: {expr.code[:20]} is defined only when {expr.WDF}",
                node=expr, error=True))

def annotate_block(self: ASTNode,
                   idp: IDP,
                   ) -> Exceptions:
    warnings = []
    assert isinstance(self, TheoryBlock), "Internal error"
    self.check(self.vocab_name in idp.vocabularies,
                f"Unknown vocabulary: {self.vocab_name}")
    self.voc = idp.vocabularies[self.vocab_name]

    for i in self.interpretations.values():
        i.block = self
        i.annotate(self.voc, {})
    self.voc.add_voc_to_block(self)

    self.definitions = [e.annotate(self.voc, {}) for e in self.definitions]
    for d in self.definitions:
        for r in d.rules:
            if r.WDF and not r.WDF.same_as(TRUE):
                collect_warnings(r.implication, warnings)

    constraints = OrderedSet()
    for c in self.constraints:
        c1 = c.annotate(self.voc, {})
        c1.check(c1.type == BOOL_SETNAME,
                    f"Formula {c.code} must be boolean, not {c1.type}")
        if c1.WDF and not c1.WDF.same_as(TRUE):
            collect_warnings(c1, warnings)
        constraints.append(c1)
    self.constraints = constraints
    return warnings
TheoryBlock.annotate_block = annotate_block


# Class Definition  #######################################################

def annotate(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    assert isinstance(self, Definition), "Internal error"
    self.rules = [r.annotate(voc, q_vars) for r in self.rules]

    # create level-mapping symbols, as needed
    # self.level_symbols: dict[SymbolDeclaration, SetName]
    dependencies = set()
    for r in self.rules:
        symbs: dict[str, SymbolDeclaration] = {}
        r.body.collect_symbols(symbs)
        for s in symbs.values():
            dependencies.add((r.definiendum.symbol.decl, s))

    while True:
        new_relations = set((x, w) for x, y in dependencies
                            for q, w in dependencies if q == y)
        closure_until_now = dependencies | new_relations
        if len(closure_until_now) == len(dependencies):
            break
        dependencies = closure_until_now

    # check for nested recursive symbols
    symbs = {s for (s, ss) in dependencies if s == ss}
    nested: set[SymbolDeclaration] = set()
    for r in self.rules:
        decl = r.definiendum.symbol.decl
        r.body.collect_nested_symbols(nested, False)
        if decl in symbs and decl not in self.inductive:
            self.inductive.add(decl)

    if self.mode == Semantics.RECDATA:
        # check that the variables in r.out are in the arguments of definiendum
        for r in self.rules:
            if r.out:
                args = set()
                for e in r.definiendum.sub_exprs:
                    for v in e.variables:
                        args.add(v)
                error = list(set(r.out.variables) - args)
                self.check(len(error) == 0,
                        f"Eliminate variable {error} in the head of : {r}")

    # check for nested recursive symbols
    nested = set()
    for r in self.rules:
        r.body.collect_nested_symbols(nested, False)
    for decl in self.inductive:
        self.check(decl not in nested,
                    f"Inductively defined nested symbols are not supported yet: "
                    f"{decl.name}.")
        if self.mode != Semantics.RECDATA:
            self.check(decl.codomain == BOOL_SETNAME,
                        f"Inductively defined functions are not supported yet: "
                        f"{decl.name}.")

    # create common variables, and rename vars in rule
    self.canonicals = {}
    for r in self.rules:
        # create common variables
        decl = voc.symbol_decls[r.definiendum.decl.name]
        if decl.name not in self.def_vars:
            name = f"{decl.name}_"
            q_v = {f"{decl.name}{str(i)}_":
                    VARIABLE(f"{decl.name}{str(i)}_", sort)
                    for i, sort in enumerate(decl.domains)}
            if decl.codomain != BOOL_SETNAME:
                q_v[name] = VARIABLE(name, decl.codomain)
            self.def_vars[decl.name] = q_v

        # rename the variables in the arguments of the definiendum
        new_vars_dict = self.def_vars[decl.name]
        new_vars = list(new_vars_dict.values())
        renamed = deepcopy(r)

        vars = {var.name : var for q in renamed.quantees for vars in q.vars for var in vars}
        args = renamed.definiendum.sub_exprs + ([renamed.out] if r.out else [])
        r.check(len(args) == len(new_vars), "Internal error")

        for i in range(len(args)- (1 if r.out else 0)):  # without rule.out
            arg, nv = renamed.definiendum.sub_exprs[i], new_vars[i]
            if type(arg) == Variable \
            and arg.name in vars and arg.name not in new_vars_dict:  # a variable, but not repeated (and not a new variable name, by chance)
                del vars[arg.name]
                rename_args(renamed, {arg.name: nv})
            else:
                eq = EQUALS([nv, arg])
                renamed.body = AND([eq, renamed.body])

        canonical = deepcopy(renamed)

        inferred = renamed.body.type_inference(voc)
        for v in vars.values():
            renamed.body = EXISTS([Quantee.make(v, sort=v.type)
                                   .annotate_quantee(voc, {}, inferred)],
                                  renamed.body)
        self.renamed.setdefault(decl, []).append(renamed)

        # rename the variable for the value of the definiendum
        if r.out:  # now process r.out
            arg, nv = canonical.out, new_vars[-1]
            if type(arg) == Variable \
            and arg.name in vars and arg.name not in new_vars:  # a variable, but not repeated (and not a new variable name, by chance)
                del vars[arg.name]
                rename_args(canonical, {arg.name: nv})
            else:
                eq = EQUALS([nv, arg])
                canonical.body = AND([eq, canonical.body])

        inferred = canonical.body.type_inference(voc)
        for v in vars.values():
            canonical.body = EXISTS([Quantee.make(v, sort=v.type)
                                     .annotate_quantee(voc, {}, inferred)],
                                    canonical.body)

        canonical.definiendum.sub_exprs = new_vars[:-1] if r.out else new_vars
        canonical.out = new_vars[-1] if r.out else None
        canonical.quantees = [Quantee.make(v, sort=v.type) for v in new_vars]

        self.canonicals.setdefault(decl, []).append(canonical)

    # join the bodies of rules
    for decl, rules in self.canonicals.items():
        new_rule = copy(rules[0])
        exprs = [deepcopy(rule.body) for rule in rules]
        new_rule.body = OR(exprs)
        self.clarks[decl] = new_rule
    return self
Definition.annotate = annotate


# Class Rule  #######################################################

def annotate(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    assert isinstance(self, Rule), "Internal error"
    self.original = copy(self)
    self.check(self.definiendum.symbol.name,
                f"No support for intentional objects in the head of a rule: "
                f"{self}")
    # create head variables
    q_v = copy(q_vars)
    inferred = self.definiendum.type_inference(voc)
    inferred.update(self.body.type_inference(voc))
    for q in self.quantees:
        q.annotate_quantee(voc, q_vars, inferred)
        for vars in q.vars:
            for var in vars:
                var.type = q.sub_exprs[0] if q.sub_exprs else None
                q_v[var.name] = var

    self.definiendum = self.definiendum.annotate(voc, q_v)
    self.body = self.body.annotate(voc, q_v)
    if self.out:
        self.out = self.out.annotate(voc, q_v)

    # compute WDF
    head = self.definiendum if not self.out else EQUALS([self.definiendum, self.out])
    expr = FORALL(self.quantees, IMPLIES([self.body, head]))
    expr.fill_WDF()
    expr._tx_position, expr._tx_position_end = self._tx_position, self._tx_position_end
    expr.parent = self.parent
    self.implication = expr
    self.WDF = expr.WDF

    return self
Rule.annotate = annotate

def rename_args(self: Rule, subs: dict[str, Expression]):
    """replace old variables by new variables
        (ignoring arguments in the head before the it
    """
    self.body = self.body.interpret(None, subs)
    self.out = (self.out.interpret(None, subs) if self.out else
                self.out)
    args = self.definiendum.sub_exprs
    for j in range(0, len(args)):
        args[j] = args[j].interpret(None, subs)


# Class Structure  #######################################################

def annotate_block(self: ASTNode,
                   idp: IDP,
                   ) -> Exceptions:
    """
    Annotates the structure with the enumerations found in it.
    Every enumeration is converted into an assignment, which is added to
    `self.assignments`.

    :arg idp: a `Parse.IDP` object.
    :returns None:
    """
    assert isinstance(self, Structure), "Internal error"
    self.check(self.vocab_name in idp.vocabularies,
               f"Unknown vocabulary: {self.vocab_name}")
    self.voc = idp.vocabularies[self.vocab_name]
    for i in self.interpretations.values():
        i.block = self
        i.annotate(self.voc, {})
    self.voc.add_voc_to_block(self)
    return []
Structure.annotate_block = annotate_block


# Class SymbolInterpretation  #######################################################

def annotate(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    """
    Annotate the symbol.

    :arg block: a Structure object
    :returns None:
    """
    assert isinstance(self, SymbolInterpretation), "Internal error"
    self.symbol_decl = voc.symbol_decls[self.name]
    enumeration = self.enumeration  # shorthand

    # create constructors if it is a type enumeration
    self.is_type_enumeration = (type(self.symbol_decl) != SymbolDeclaration)
    if self.is_type_enumeration and enumeration.constructors:
        # create Constructors before annotating the tuples
        for c in enumeration.constructors:
            if type(self.symbol_decl) == TypeDeclaration:
                c.codomain = self.symbol_decl.domains[0]
            self.check(c.name not in voc.symbol_decls or
                       (type(self.symbol_decl) == TypeDeclaration and self.symbol_decl.super_set),
                    f"duplicate '{c.name}' constructor for '{self.name}' symbol")
            voc.symbol_decls[c.name] = c  #TODO risk of side-effects => use local decls ? issue #81

            # Also verify that the constructor's prefix exists.
            self.check(c.prefix in voc.declared_prefixes or c.prefix is None,
                       f"Unknown prefix for {c.name}")

    enumeration.annotate(voc, q_vars)

    self.check(self.is_type_enumeration
                or all(s not in [INT_SETNAME, REAL_SETNAME, DATE_SETNAME]  # finite domain #TODO
                        for s in self.symbol_decl.domains)
                or self.default is None,
        f"Can't use default value for '{self.name}' on infinite domain nor for type enumeration.")

    self.check(not(self.symbol_decl.codomain.root_set
                   and len(self.symbol_decl.codomain.root_set) == 1
                   and self.symbol_decl.codomain.root_set[0] == BOOL_SETNAME
                   and type(enumeration) == FunctionEnum),
        f"Can't use function enumeration for predicates '{self.name}' (yet)")

    # predicate enumeration have FALSE default
    if type(enumeration) != FunctionEnum and self.default is None:
        self.default = FALSE

    if self.default is not None:
        self.default = self.default.annotate(voc, {})
        self.check(self.default.is_value(),
                   f"Value for '{self.name}' may only use numerals,"
                   f" identifiers or constructors: '{self.default}'")

    return self
SymbolInterpretation.annotate = annotate


# Class Enumeration  #######################################################

def annotate(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    assert isinstance(self, Enumeration), "Internal error"
    if self.tuples:
        for t in self.tuples:
            t.annotate(voc, q_vars)
    return self
Enumeration.annotate = annotate


# Class TupleIDP  #######################################################

def annotate(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    assert isinstance(self, TupleIDP), "Internal error"
    self.args = [arg.annotate(voc, q_vars) for arg in self.args]
    self.check(all(a.is_value() for a in self.args),
               f"Interpretation may only contain numerals,"
               f" identifiers or constructors: '{self}'")
    return self
TupleIDP.annotate = annotate


# Class ConstructedFrom  #######################################################

def annotate(self: ASTNode,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    assert isinstance(self, ConstructedFrom), "Internal error"
    for c in self.constructors:
        for i, ts in enumerate(c.args):
            if not ts.accessor:
                ts.accessor = f"{c.name}_{i}"
            if ts.accessor in self.accessors:
                self.check(self.accessors[ts.accessor] == i,
                           "Accessors used at incompatible indices")
            else:
                self.accessors[ts.accessor] = i
        c.annotate(voc, q_vars)
    return self
ConstructedFrom.annotate = annotate


# Class Constructor  #######################################################

def annotate(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    assert isinstance(self, Constructor), "Internal error"
    for a in self.args:
        self.check(a.codomain.name in voc.symbol_decls,
                   f"Unknown type: {a.codomain}" )
        a.decl = SymbolDeclaration.make(self,
            name=a.accessor, sorts=[self.codomain], sort_=a.codomain)
        a.decl.by_z3 = True
        a.decl.annotate_declaration(voc)
    for s in self.domains:
        s.annotate(voc, {})
    self.tester = SymbolDeclaration.make(self,
            name=f"is_{self.name}", sorts=[self.codomain], sort_=BOOL_SETNAME)
    self.tester.by_z3 = True
    self.tester.annotate_declaration(voc)
    return self
Constructor.annotate = annotate


# Class Display  #######################################################

def annotate_block(self: ASTNode,
                   idp: IDP,
                   ) -> Exceptions:
    assert isinstance(self, Display), "Internal error"
    self.voc = idp.vocabulary

    # add display predicates

    viewType = TypeDeclaration(self, name='_ViewType',
        constructors=[CONSTRUCTOR('normal'),
                        CONSTRUCTOR('expanded')])
    viewType.annotate_declaration(self.voc)

    # Check the AST for any constructors that belong to open types.
    # For now, the only open types are `unit`, `heading` and `introduction`.
    open_constructors = {'unit': [], 'heading': [], 'introduction': []}
    for constraint in self.constraints:
        constraint.generate_constructors(open_constructors)

    # Next, we convert the list of constructors to actual types.
    open_types: dict[str, Optional[SetName]] = {}
    for name, constructors in open_constructors.items():
        # If no constructors were found, then the type is not used.
        if not constructors:
            open_types[name] = None
            continue

        type_name = name.capitalize()  # e.g. type Unit (not unit)
        open_type = TypeDeclaration(self, name=type_name,
                                    constructors=constructors)
        open_type.annotate_declaration(self.voc)
        open_types[name] = SETNAME(type_name)

    for name, sort_ in [
        ('expand', BOOL_SETNAME),
        ('hide', BOOL_SETNAME),
        ('view', SETNAME('_ViewType')),
        ('moveSymbols', BOOL_SETNAME),
        ('optionalPropagation', BOOL_SETNAME),
        ('manualPropagation', BOOL_SETNAME),
        ('optionalRelevance', BOOL_SETNAME),
        ('manualRelevance', BOOL_SETNAME),
        ('unit', open_types['unit']),
        ('heading', open_types['heading']),
        ('introduction', open_types['introduction']),
        ('counter', BOOL_SETNAME),
        ('noOptimization', BOOL_SETNAME)
    ]:
        symbol_decl = SymbolDeclaration.make(self, name=name, sorts=[],
                sort_=sort_ or BOOL_SETNAME)
        symbol_decl.annotate_declaration(self.voc)

    # annotate constraints and interpretations
    for constraint in self.constraints:
        constraint.annotate(self.voc, {})
    for i in self.interpretations.values():
        i.block = self
        i.annotate(self.voc, {})
    return []
Display.annotate_block = annotate_block


# Class Expression  #######################################################

def annotate(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    """annotate tree after parsing

    Resolve names and determine type as well as variables in the expression

    Args:
        voc (Vocabulary): the vocabulary
        q_vars (dict[str, Variable]): the quantifier variables that may appear in the expression

    Returns:
        Expression: an equivalent AST node, with updated type, .variables
    """
    self.sub_exprs = [e.annotate(voc, q_vars) for e in self.sub_exprs]
    self = self.fill_attributes_and_check().merge_WDFs()
    return self
Expression.annotate = annotate


def fill_attributes_and_check(self: Expression) -> Expression:
    " annotations that are common to __init__ and make() "
    self.variables = set()
    for e in self.sub_exprs:
        self.variables.update(e.variables)
    return self
Expression.fill_attributes_and_check = fill_attributes_and_check


# Class AIfExpr  #######################################################

def fill_attributes_and_check(self: AIfExpr) -> Expression:
    self.sub_exprs[0].check(self.sub_exprs[0].type == BOOL_SETNAME,
        f"Boolean expected ({self.sub_exprs[0].type} found)")
    self.type = base_type(self.sub_exprs[1:])
    return Expression.fill_attributes_and_check(self)
AIfExpr.fill_attributes_and_check = fill_attributes_and_check


# Class Quantee  #######################################################

def annotate_quantee(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable],
             inferred: dict[str, SetName]
             ) -> Annotated:
    assert isinstance(self, Quantee), "Internal error"
    Expression.annotate(self, voc, q_vars)
    if self.sub_exprs and self.sub_exprs[0].decl:
        self.check(type(self.sub_exprs[0].decl) == TypeDeclaration
                or self.sub_exprs[0].decl.sort_ == BOOL_SETNAME,
                f"Can't use function {self.sub_exprs[0]} in quantification")
    for vars in self.vars:
        for i, var in enumerate(vars):
            self.check(var.name not in voc.symbol_decls
                        or type(voc.symbol_decls[var.name]) == VarDeclaration,
                f"the quantified variable '{var.name}' cannot have"
                f" the same name as another symbol")
            # 1. get variable sort from the quantee, if possible
            if len(vars) == 1 and self.sub_exprs and type(self.sub_exprs[0]) == SetName:
                var.type = self.sub_exprs[0]   # `x in p` or `x in Concept[...]`
            elif self.sub_exprs:
                if self.sub_exprs[0].decl:  # `(x,y) in p`
                    var.type = self.sub_exprs[0].decl.domains[i]
                elif self.sub_exprs[0].sub_exprs[0].type:  #  `(x,y) in $(p)`
                    var.type = self.sub_exprs[0].sub_exprs[0].type.root_set[i].concept_domains[0]
            else:
                var.type = None
            # 2. compare with variable declaration, if any
            var_decl = voc.symbol_decls.get(var.name.rstrip(string.digits), None)
            if var_decl and type(var_decl) == VarDeclaration:
                subtype = var_decl.subtype
                if var.type:
                    self.check(var.type.name == subtype.name,
                        f"Can't use declared {var.name} as a "
                        f"{var.type.name if var.type else ''}")
                else:
                    self.sub_exprs = [subtype.annotate(voc, {})]
                    var.type = self.sub_exprs[0]
            # 3. use type inference if still not found
            if var.type is None:
                var.type = inferred.get(var.name) if inferred else None
            var.type = var.type
            q_vars[var.name] = var
    if not self.sub_exprs and var.type:
        self.sub_exprs = [var.type]
    return self.fill_attributes_and_check()
Quantee.annotate_quantee = annotate_quantee

def fill_attributes_and_check(self: AQuantification) -> Expression:
    assert isinstance(self, Quantee), "Internal error"
    Expression.fill_attributes_and_check(self)
    for vars in self.vars:
        self.check(not self.sub_exprs
                   or not self.sub_exprs[0].decl
                   or len(vars)==self.sub_exprs[0].decl.arity,
                    f"Incorrect arity for {self}")
    return self
Quantee.fill_attributes_and_check = fill_attributes_and_check


# Class AQuantification  #######################################################

def annotate(self: Expression,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    # also called by AAgregate.annotate
    assert isinstance(self, AQuantification) or isinstance(self, AAggregate), "Internal error"
    q_v = copy(q_vars)
    inferred = self.sub_exprs[0].type_inference(voc)
    for q in self.quantees:
        q.annotate_quantee(voc, q_v, inferred)  # adds inner variables to q_v
    self.sub_exprs = [e.annotate(voc, q_v) for e in self.sub_exprs]
    return self.fill_attributes_and_check().merge_WDFs()
AQuantification.annotate = annotate

def fill_attributes_and_check(self: AQuantification) -> Expression:
    Expression.fill_attributes_and_check(self)
    for q in self.quantees:  # remove declared variables
        for vs in q.vars:
            for v in vs:
                self.variables.discard(v.name)
    for q in self.quantees:  # add variables in sort expression
        for sort in q.sub_exprs:
            self.variables.update(sort.variables)
    if type(self) == AQuantification:
        for e in self.sub_exprs:
            e.check(e.type == BOOL_SETNAME,
                f"Quantified formula must be boolean (instead of {e.type})")
    return self
AQuantification.fill_attributes_and_check = fill_attributes_and_check


# Class Operator  #######################################################

def base_type(exprs: List[Expression], bases: List[SetName] = None) -> Optional[SetName]:
    """ Checks or determines the (sub)types of the expressions in exprs.

    Raises an error if the (sub)type of an expression is not in `bases`.
    Raises an error if the expressions have incompatible (sub)types.
    Returns None if exprs is empty.

    A mix of Int and Real (or Int and Date) is allowed.
    """
    if not exprs:
        return None if not bases else bases[0]
    if exprs[0].type:
        base = exprs[0].type.root_set[0] if not bases else bases[0]
        bases = set([base.name]) if not bases else set([b.name for b in bases])
        if base in [REAL_SETNAME, DATE_SETNAME]:
            bases.add(INT)  # also accept INT for REAL and DATE
        if (hasattr(exprs[0], 'decl') and
                hasattr(exprs[0].decl, 'range') and
                exprs[0].decl.range and
                exprs[0].decl.range[0].type in [INT_SETNAME, REAL_SETNAME, DATE_SETNAME]):
            # Ensures that types can be interpreted with ints, reals and dates
            # in the structure. See https://gitlab.com/krr/IDP-Z3/-/issues/342
            bases.add(INT)
        for e in exprs:
            if e.type:
                b = e.type.root_set[0]
                if b.name not in bases:
                    if base == INT_SETNAME and b in [REAL_SETNAME, DATE_SETNAME]:
                        base = b
                        bases.add(b.name)
                    else:
                        e.check(False, f"{base.name} value expected ({b.name} found: {e} )")
                elif b in [REAL_SETNAME, DATE_SETNAME]:
                    base = b
                # else continue
            else:
                e.check(False, f"Can't determine the type of {e}")
        return base
    else:
        exprs[0].check(False, f"Can't determine the type of {exprs[0]}")
    return None

def fill_attributes_and_check(self: Operator) -> Expression:
    assert all(e.type for e in self.sub_exprs), "Can't handle nested concepts yet."

    for e in self.sub_exprs:
        if self.operator[0] in '&|∧∨⇒⇐⇔':
            self.check(e.type is None or e.type == BOOL_SETNAME or e.str in ['true', 'false'],
                       f"Expected boolean formula, got {e.type}: {e}")

    self.type = base_type(self.sub_exprs)
    self.check(self.type is not None, "Type error")
    return Expression.fill_attributes_and_check(self)
Operator.fill_attributes_and_check = fill_attributes_and_check


# Class AImplication  #######################################################

def fill_attributes_and_check(self: AImplication) -> Expression:
    self.check(len(self.sub_exprs) == 2,
               "Implication is not associative.  Please use parenthesis.")
    _ = base_type(self.sub_exprs, [BOOL_SETNAME])  # type check the sub-exprs
    self.type = BOOL_SETNAME
    return Expression.fill_attributes_and_check(self)
AImplication.fill_attributes_and_check = fill_attributes_and_check


# Class AEquivalence  #######################################################

def fill_attributes_and_check(self: AEquivalence) -> Expression:
    self.check(len(self.sub_exprs) == 2,
               "Equivalence is not associative.  Please use parenthesis.")
    _ = base_type(self.sub_exprs, [BOOL_SETNAME])  # type check the sub_exprs
    self.type = BOOL_SETNAME
    return Expression.fill_attributes_and_check(self)
AEquivalence.fill_attributes_and_check = fill_attributes_and_check

# Class ARImplication  #######################################################

def annotate(self: ARImplication,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    # reverse the implication
    self.sub_exprs = [e.annotate(voc, q_vars) for e in self.sub_exprs]
    out = AImplication.make(ops=['⇒'], operands=list(reversed(list(self.sub_exprs))),
                        annotations=None, parent=self)
    out.original = self
    return out.annotate(voc, q_vars)
ARImplication.annotate = annotate

# Class AConjunction, ADisjunction  #######################################################

def fill_attributes_and_check(self: Expression) -> Expression:
    self.type = base_type(self.sub_exprs, [BOOL_SETNAME])
    return Expression.fill_attributes_and_check(self)
AConjunction.fill_attributes_and_check = fill_attributes_and_check
ADisjunction.fill_attributes_and_check = fill_attributes_and_check


# Class AComparison  #######################################################

def annotate(self: AComparison,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:

    out = Operator.annotate(self, voc, q_vars)

    # a≠b --> Not(a=b)
    if len(self.sub_exprs) == 2 and self.operator == ['≠']:
        out = NOT(EQUALS(self.sub_exprs)).annotate(voc, q_vars)
        return out
    return out
AComparison.annotate = annotate

def fill_attributes_and_check(self: AppliedSymbol) -> Expression:
    bases = ([INT_SETNAME, REAL_SETNAME, DATE_SETNAME] if any(e in "<>≤≥" for e in self.operator) else
             None)
    _ = base_type(self.sub_exprs, bases) # type check the sub-expressions
    self.type = BOOL_SETNAME
    return Expression.fill_attributes_and_check(self)
AComparison.fill_attributes_and_check = fill_attributes_and_check


# Class ASumMinus  #######################################################

def fill_attributes_and_check(self: ASumMinus) -> Expression:
    self.type = base_type(self.sub_exprs, [INT_SETNAME, REAL_SETNAME, DATE_SETNAME])
    return Expression.fill_attributes_and_check(self)
ASumMinus.fill_attributes_and_check = fill_attributes_and_check


# Class AMultDiv  #######################################################

def fill_attributes_and_check(self: AMultDiv) -> Expression:
    self.type = base_type(self.sub_exprs, [INT_SETNAME, REAL_SETNAME])
    return Expression.fill_attributes_and_check(self)
AMultDiv.fill_attributes_and_check = fill_attributes_and_check


# Class APower  #######################################################

def fill_attributes_and_check(self: APower) -> Expression:
    self.sub_exprs[1].check(self.sub_exprs[0].type in [INT_SETNAME, REAL_SETNAME],
               f"Number expected ({self.sub_exprs[1].type} found: {self.sub_exprs[1].type})")
    self.sub_exprs[1].check(self.sub_exprs[1].type == INT_SETNAME,
               f"Integer expected ({self.sub_exprs[1].type} found: {self.sub_exprs[1].type})")
    return Expression.fill_attributes_and_check(self)
APower.fill_attributes_and_check = fill_attributes_and_check


# Class AUnary  #######################################################

def fill_attributes_and_check(self: AUnary) -> Expression:
    if len(self.operators) % 2 == 0: # negation of negation
        return self.sub_exprs[0]
    self.type = self.sub_exprs[0].type
    return Expression.fill_attributes_and_check(self)
AUnary.fill_attributes_and_check = fill_attributes_and_check


# Class AAggregate  #######################################################

def annotate(self: AAggregate,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    if not self.annotated:

        self = AQuantification.annotate(self, voc, q_vars)

        if self.aggtype == "sum" and len(self.sub_exprs) == 2:
            self.original = copy(self)
            self.sub_exprs[0].check(
                self.sub_exprs[0].type.root_set[0] in [INT_SETNAME, REAL_SETNAME],
                f"Must be numeric: {self.sub_exprs[0]}")
            self.sub_exprs[1].check(
                self.sub_exprs[1].type.root_set[0] == BOOL_SETNAME,
                f"Must be boolean: {self.sub_exprs[1]}")
            self.sub_exprs = [AIfExpr(self.parent, self.sub_exprs[1],
                                    self.sub_exprs[0], ZERO).fill_attributes_and_check()]

        if self.aggtype == "#":
            self.sub_exprs[0].check(
                self.sub_exprs[0].type.root_set[0] == BOOL_SETNAME,
                f"Must be boolean: {self.sub_exprs[0]}")
            self.sub_exprs = [IF(self.sub_exprs[0], Number(number='1'),
                                 Number(number='0'))]
            self.type = INT_SETNAME
        else:
            self.type = self.sub_exprs[0].type
            if self.aggtype in ["min", "max"]:
                # the `min` aggregate in `!y in T: min(lamda x in type: term(x,y) if cond(x,y))=0`
                # is replaced by `_*(y)` with the following co-constraint:
                #     !y in T: ( ?x in type: cond(x,y) & term(x) = _*(y)
                #                !x in type: cond(x,y) => term(x) =< _*(y).
                self.check(self.type, f"Can't infer type of {self}")
                name = "__" + self.str
                if name in voc.symbol_decls:
                    symbol_decl = voc.symbol_decls[name]
                    to_create = False
                else:
                    symbol_decl = SymbolDeclaration.make(self,
                        "__"+self.str, # name `__ *`
                        [SETNAME(v.type.name) for v in q_vars.values()],
                        self.type).annotate_declaration(voc)    # output_domain
                    to_create = True
                symbol = symbol_decl.symbol_expr
                applied = AppliedSymbol.make(symbol, q_vars.values())
                applied = applied.annotate(voc, q_vars)
                applied.WDF = self.WDF
                # set location of applied
                applied._tx_position = self._tx_position
                applied._tx_position_end = self._tx_position_end
                applied.parent = self.parent

                if to_create:
                    eq = EQUALS([deepcopy(applied), self.sub_exprs[0]])
                    if len(self.sub_exprs) == 2:
                        eq = AND([self.sub_exprs[1], eq])
                    coc1 = EXISTS(self.quantees, eq)

                    op = '≤' if self.aggtype == "min" else '≥'
                    comp = AComparison.make(op,
                                    deepcopy([applied, self.sub_exprs[0]]))
                    if len(self.sub_exprs) == 2:
                        comp = IMPLIES([self.sub_exprs[1], comp])
                    coc2 = FORALL(deepcopy(self.quantees), comp)

                    coc = AND([coc1, coc2])
                    inferred = coc.type_inference(voc)
                    quantees = [Quantee.make(v, sort=v.type)
                                .annotate_quantee(voc, {}, inferred)
                                for v in q_vars.values()]
                    applied.co_constraint = (
                        coc if not quantees else
                        FORALL(quantees, coc).annotate(voc, q_vars))
                    applied.co_constraint.annotations['reading'] = f"Calculation of {self.code}"
                return applied
        self.annotated = True
        self.type = base_type(self.sub_exprs)
        self.sub_exprs[0].check(self.type in [INT_SETNAME, REAL_SETNAME, DATE_SETNAME],
            f"Aggregate formula must be numeric (instead of {self.type})")
    return self
AAggregate.annotate = annotate
AAggregate.fill_attributes_and_check = AQuantification.fill_attributes_and_check


# Class AppliedSymbol  #######################################################

def annotate(self: AppliedSymbol,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    self.symbol = self.symbol.annotate(voc, q_vars)
    self.sub_exprs = [e.annotate(voc, q_vars) for e in self.sub_exprs]
    if self.in_enumeration:
        self.in_enumeration.annotate(voc, q_vars)
    out = self.fill_attributes_and_check().merge_WDFs()

    # move the negation out
    if 'not' in self.is_enumerated:
        out = AppliedSymbol.make(out.symbol, out.sub_exprs,
                                 is_enumerated='is enumerated')
        out = NOT(out)
    elif 'not' in self.is_enumeration:
        out = AppliedSymbol.make(out.symbol, out.sub_exprs,
                                 is_enumeration='in',
                                 in_enumeration=out.in_enumeration)
        out = NOT(out)
    return out
AppliedSymbol.annotate = annotate

def fill_attributes_and_check(self: AppliedSymbol, type_check=True) -> Expression:
    out = Expression.fill_attributes_and_check(self)
    assert type(out) == AppliedSymbol, "Internal error"
    out.symbol = out.symbol.fill_attributes_and_check()
    out.variables.update(out.symbol.variables)
    if not out.decl and out.symbol.name:
        out.decl = out.symbol.decl

    if out.symbol.decl:
        self.check(out.symbol.decl.arity == len(out.sub_exprs)
                   or out.symbol.decl.name in ['hide', 'unit', 'heading',
                                               'noOptimization',
                                               'introduction',
                                               'counter'],
            f"Incorrect number of arguments in {out}: "
            f"should be {out.symbol.decl.arity}")
    out.check((not out.symbol.decl or type(out.symbol.decl) != Constructor
                or 0 < out.symbol.decl.arity),
               f"Constructor `{out.symbol}` cannot be applied to argument(s)")

    # check type of arguments
    if out.decl and type_check:
        for e, s in zip(out.sub_exprs, out.decl.domains):
            if not type(out.decl) == TypeDeclaration:  # Type predicates accept anything
                e.check(e.type is not None,
                        f"Unknown type of {e}")
                e.check(len(e.type.root_set) == 1 and e.type.root_set[0] == s.root_set[0],
                        f"{s.root_set[0]} expected ({e.type.root_set[0]} found: {e})")
                type_ = e.type
                # while type_ != s:  # handle case where e_type is a subset of s
                #     e.check(type_ != type_.decl.domains[0],
                #             f"{s} expected ({e.type} found: {e})")
                #     type_ = type_.decl.domains[0]

    if self.is_enumeration == 'in':
        # check the type of elements in the enumeration
        codomain = self.decl.codomain
        if len(codomain.root_set) == 1:
            codomain = codomain.root_set[0]
        _ = base_type([t.args[0] for t in self.in_enumeration.tuples], [codomain])

    # determine type
    if out.is_enumerated or out.in_enumeration:
        out.type = BOOL_SETNAME
    elif out.decl and out.decl.codomain:
        out.type = out.decl.codomain
    elif type(out.symbol)==SymbolExpr and out.symbol.eval:
        type_ = out.symbol.sub_exprs[0].type
        out.symbol.check(type_.root_set[0].name == CONCEPT,
            f"Concept expected ({type_} found: {out.symbol})")
        if type_.name == CONCEPT:
            out.type = type_.codomain
        else:
            while not type_.codomain:  # type is a subset of a concept
                type_ = type_.decl.super_sets[0]
            out.type = type_.codomain

    return out.simplify1()
AppliedSymbol.fill_attributes_and_check = fill_attributes_and_check

# Class SymbolExpr  #######################################################

def annotate(self: SymbolExpr,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    self.decl = voc.symbol_decls.get(self.name, None)
    out = Expression.annotate(self, voc, q_vars)
    return out.simplify1()
SymbolExpr.annotate = annotate


# Class Variable  #######################################################

def annotate(self: Variable,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    self.WDF = TRUE
    return self
Variable.annotate = annotate


# Class Number  #######################################################

def annotate(self: Number,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    self.WDF = TRUE
    self.decl = voc.symbol_decls[self.type.name]
    return self
Number.annotate = annotate


# Class UnappliedSymbol  #######################################################

def annotate(self: UnappliedSymbol,
             voc: Vocabulary,
             q_vars: dict[str, Variable]
             ) -> Annotated:
    self.WDF = TRUE
    if self.name in q_vars:  # ignore VarDeclaration
        return q_vars[self.name]
    if self.name in voc.symbol_decls:
        self.decl = voc.symbol_decls[self.name]
        self.type = self.decl.codomain
        self.variables = set()
        self.check(type(self.decl) == Constructor,
                   f"{self} should be applied to arguments (or prefixed with a back-tick)")
        return self
    # elif self.name in voc.symbol_decls:  # in symbol_decls
    #     out = AppliedSymbol.make(self.s, self.sub_exprs)
    #     return out.annotate(voc, q_vars)
    # If this code is reached, an undefined symbol was present.
      # after considering it as a declared symbol
    self.check(self.name.rstrip(string.digits) in q_vars,
               f"Symbol not in vocabulary: {self}")
    return self
UnappliedSymbol.annotate = annotate


# Class Brackets  #######################################################

def fill_attributes_and_check(self: Brackets) -> Expression:
    if not self.annotations:
        return self.sub_exprs[0]  # remove the bracket
    self.type = self.sub_exprs[0].type
    if self.annotations['reading']:
        self.sub_exprs[0].annotations = self.annotations
    self.variables = self.sub_exprs[0].variables
    return self
Brackets.fill_attributes_and_check = fill_attributes_and_check


Done = True
