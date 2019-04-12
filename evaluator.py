import turingarena as ta
import networkx as nx
import networkx.algorithms.components as nx_comp
import random
import numpy as np
from random import choice

DEBUG = True

def generate_random_formula(n,m,is_sat):
    # generate the list of letteral
    clausole = [[],[]]
    if(is_sat):
        litterals = [i for i in range(n)]
        assignment = np.random.choice([-1,1],n)
        while len(clausole[0]) < m:
            clausola = np.random.choice(litterals,2,replace=False)
            (correct,other) = np.random.choice([0,1],2,replace=False)
            other_dir = np.random.choice([-1,1])
            clausola[correct] = assignment[clausola[correct]] * (clausola[correct]+1)
            clausola[other] = other_dir * (clausola[other]+1)
            clausole[0].append(clausola[0])
            clausole[1].append(clausola[1])

    else:
        litterals = []
        for i in range(1, n+1):
            litterals.append(i)
            litterals.append(-i)

        # litteral that can not be True nor False
        unsat_lit = np.random.choice(range(1,n+1))

        # build a cycle
        cycle_length = np.random.choice(range(1,m-1))
        first_half   = np.random.choice(range(cycle_length))

        # assuming unsat_lit = True deduce unsat_lit = False
        lit = -unsat_lit # False in the assumption
        for i in range(first_half):
            # propagate
            clausole[0].append(lit)
            other = np.random.choice(litterals)
            clausole[1].append(other)
            lit = -other
        # deduce contradiction
        clausole[0].append(lit)
        clausole[1].append(-unsat_lit)

        # assuming unsat_lit = False deduce unsat_lit = True
        lit = unsat_lit # False in the assumption
        for i in range(first_half,cycle_length):
            # propagate
            clausole[0].append(lit)
            other = np.random.choice(litterals)
            clausole[1].append(other)
            lit = -other
        # deduce contradiction
        clausole[0].append(lit)
        clausole[1].append(unsat_lit)

        # randomly fill the rest (already set cycle_length + 2)
        for i in range(cycle_length+2,m):
            clausole[0].append(np.random.choice(litterals))
            clausole[1].append(np.random.choice(litterals))

        assert(len(clausole[0]) == m)
        assert(len(clausole[1]) == m)

    return clausole

def test_case(n, m, is_sat):
    print(f"\nEvaluating test case: N = {n}, M = {m} SAT={is_sat}...  ")

    res = 1

    # edges density
    (a,b) = generate_random_formula(n,m,is_sat)

    try:
        with ta.run_algorithm(ta.submission.source, time_limit=0.15) as p:
            # initialize the H graph
            G = nx.DiGraph()
            G_edges = 0

            def size_of_G(nG,mG):
                nonlocal G, G_edges
                if nG < 0:
                    raise Exception('negative number of nodes')
                if mG < 0:
                    raise Exception('negative number of edges')
                G.add_nodes_from(range(0,nG))
                G_edges = mG

            def add_edge(u,v):
                nonlocal G, G_edges
                if len(G.edges) == G_edges:
                    raise Exception('too many edges added with add_edge')

                if not G.has_node(u):
                    raise Exception(
                            'in function add_edge. Invalid node u={}'.format(u))
                if not G.has_node(v):
                    raise Exception(
                            'in function add_edge. Invalid node v={}'.format(v))
                G.add_edge(u,v)


            print("Evaluating the satisfiability... ", end="")

            # the solution build G
            p.procedures.prepare_G(n,m,a,b,
                    callbacks=[
                        size_of_G,
                        add_edge
                        ])

            assignments = [-1]*(n+1)
            n_of_assignments = 0

            def assign_variable(letteral,value):
                nonlocal n, n_of_assignments, assignments
                if letteral > n:
                    raise Exception('in function assign_variable. Invalid letteral {}'.format(letteral))
                if assignments[letteral] != -1:
                    raise Exception('multiple assignments for letteral {}'.format(letteral))
                assignments[letteral] = False if value <= 0 else True
                n_of_assignments = n_of_assignments + 1


            nG = len(G)
            components = [-1] * nG
            comp = 0

            # generate strongly connected components in reverse topological order
            scc = nx_comp.strongly_connected_components_recursive(G)
            # assigns components in topologigical order
            for C in reversed(list(scc)):
                for node in C:
                    components[node] = comp
                comp += 1

            ris = p.functions.is_satisfiable(nG,components,
                    callbacks=[
                        assign_variable
                        ])

            if ris <= 0:
                ris = False
            else:
                ris = True

            if ris != is_sat:
                print("[WRONG]")
                if ris:
                    raise Exception('The formula is unsatisfiable, but you claim that is satisfiable')
                else:
                    raise Exception('The formula is satisfiable, but you claim that is not satisfiable')

            print("[CORRECT]")

            res *= 2

            # nothing to do for unsat instances
            if not is_sat:
                return res

            print("Evaluating the assignments... \t", end="")
            try:
                # check the assignment
                if n_of_assignments != n:
                    raise Exception('you assigned less letterals than those in the formula')

                result = True;
                for i in range(m):
                    letteral_a = abs(a[i])
                    letteral_b = abs(b[i])
                    dir_a = False if a[i] < 0 else True
                    dir_b = False if b[i] < 0 else True
                    if (assignments[letteral_a] != dir_a and assignments[letteral_b] != dir_b):
                        raise Exception('the assignment is not a model. The assignments {}={} and {}={}, falsifies the clausole ({} v {})'.format(
                                letteral_a,assignments[letteral_a],letteral_b,assignments[letteral_b],a[i],b[i]))

                # The assignement is correct
                print("[CORRECT]")
                res = res * 3
            except Exception as e:
                print(f"[WRONG] \t error: {e}")

    except Exception as e:
        print(f"[WRONG] \t error: {e}")

    if res == 2*3:
        print(f"test case: N = {n}, M = {m} [PASSED]")
    else:
        print(f"test case: N = {n}, M = {m} [FAILED]")

    return res


def main():
    for n in (10, 15, 20):
        for m in (10, 15, 20):
            is_sat = random.choice([True,False])
            ret = test_case(n,m,is_sat)
            if is_sat and ret%3:
                ta.goals["model"] = False
            if ret%2:
                ta.goals["decision"] = False

    ta.goals.setdefault("decision", True)
    ta.goals.setdefault("model", True)

    for n in (100, 150, 200):
        for m in (100, 150, 200):
            is_sat = random.choice([True,False])
            ret = test_case(n,m,is_sat)
            if is_sat and ret%3:
                ta.goals["model"] = False
            if ret%2:
                ta.goals["decision"] = False
    ta.goals.setdefault("decision", True)
    ta.goals.setdefault("model", True)

    for n in (1000, 1500, 2000):
        for m in (1000, 1500, 2000):
            is_sat = random.choice([True,False])
            ret = test_case(n,m,is_sat)
            if is_sat and ret%3:
                ta.goals["model"] = False
            if ret%2:
                ta.goals["decision"] = False
    ta.goals.setdefault("decision", True)
    ta.goals.setdefault("model", True)

    print(ta.goals)

if __name__ == "__main__":
    main()
