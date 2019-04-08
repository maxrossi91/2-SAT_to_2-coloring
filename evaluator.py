import turingarena as ta
import networkx as nx
import random
import numpy as np

DEBUG = True

# Goals:
# - is satisfiable
# - give an assignment

def intersection(a, b):
    return list(set(a) & set(b))

def generate_random_formula(n,m,is_sat):
    # generate the list of letteral
    letteral = [i for i in range(n)]
    random.shuffle(letteral)
    clausole = [[],[]]
    if(is_sat):
        #I have to avoid cycles
        # G = nx.DiGraph()
        # G.add_nodes_from(range(2*n))
        assignment = np.random.choice([-1,1],n)
        while len(clausole[0]) < m:
            clausola = np.random.choice(letteral,2,replace=False)
            (correct,other) = np.random.choice([0,1],2,replace=False)
            other_dir = np.random.choice([-1,1])
            clausola[correct] = assignment[clausola[correct]] * (clausola[correct]+1)
            clausola[other] = other_dir * (clausola[other]+1)
            clausole[0].append(clausola[0])
            clausole[1].append(clausola[1])
            # a = random.choice(letteral)
            # b = random.choice(letteral)
            # while b == a:
            #     b = random.choice(letteral)
            #
            # a_dir = random.choice(range(2))
            # b_dir = random.choice(range(2))
            #
            # index_a = a + a_dir*n
            # index_b = b + b_dir*n
            #
            # index_not_a = (index_a + n)%(2*n)
            # index_not_b = (index_b + n)%(2*n)
            #
            # G.add_edge(index_not_a,index_b)
            # G.add_edge(index_not_b,index_a)
            #
            # reachable_from_a = list(nx.dfs_successors(G,index_a))
            # reaches_not_a = list(nx.dfs_predecessors(G,index_not_a))
            # reachable_from_b = list(nx.dfs_successors(G,index_b))
            # reaches_not_b = list(nx.dfs_predecessors(G,index_not_b))
            #
            # reachable_from_a_not = [(i+n)%(2*n) for i in reachable_from_a]
            # reachable_from_b_not = [(i+n)%(2*n) for i in reachable_from_b]
            #
            # connections_not_a_b = intersection(reaches_not_a,reachable_from_b_not)
            # connections_not_b_a = intersection(reaches_not_b,reachable_from_a_not)
            #
            # connections_not_b_a_not = [(i+n)%(2*n) for i in connections_not_b_a]
            #
            # unsat = intersection(connections_not_a_b,connections_not_b_a_not)
            #
            # if len(unsat):
            #     G.remove_edge(index_not_a,index_b)
            #     G.remove_edge(index_not_b,index_a)
            # else:
            #     clausole[0].append(((index_a%n) +1)*( -1 if index_a >= n else 1))
            #     clausole[1].append(((index_b%n) +1)*( -1 if index_b >= n else 1))
            #     # clausole.append([index_a,index_b])

    else:
        # I have to introduce a cycle
        cycle_length = np.random.choice(range(3,min(n,m)))
        path_length = int(cycle_length/2)
        cycle = np.random.choice(letteral,cycle_length,replace = False)
        directions = np.random.choice(range(2),cycle_length)
        unsat_variable = cycle[path_length]
        unsat_variable_not = ((unsat_variable + n)% (2*n))
        forward_path_length = len(range(path_length+1, cycle_length))
        forward_path = []
        forward_directions = []
        forward_index = []
        forward_index_not = []
        if forward_path_length:
          forward_path = [cycle[i] for i in range(path_length+1, cycle_length)]
          forward_directions = [directions[i] for i in range(path_length+1, cycle_length)]
          forward_index = [forward_path[i] + forward_directions[i]*n for i in range(forward_path_length)]
          forward_index_not = [(forward_index[i]+n)%(2*n) for i in range(forward_path_length)]

        backward_path_length = path_length
        backward_path = [cycle[i] for i in range(path_length)]
        backward_directions = [directions[i] for i in range(path_length)]
        backward_index = [backward_path[i] + backward_directions[i]*n for i in range(backward_path_length)]
        backward_index_not = [(backward_index[i]+n)%(2*n) for i in range(backward_path_length)]

        # Unsat cycle from unsat to unsat_not
        clausole[0].append(((unsat_variable%n) +1)*( -1 if unsat_variable >= n else 1))
        for i in range(backward_path_length):
            index_a = backward_index[i]
            index_a_not = backward_index_not[i]
            clausole[1].append(((index_a%n) +1)*( -1 if index_a >= n else 1))
            clausole[0].append(((index_a_not%n) +1)*( -1 if index_a_not >= n else 1))

        clausole[1].append(((unsat_variable_not%n) +1)*( -1 if unsat_variable_not >= n else 1))
        # Unsat cycle from unsat_not to unsat
        clausole[0].append(((unsat_variable_not%n) +1)*( -1 if unsat_variable_not >= n else 1))
        for i in range(forward_path_length):
            index_a = forward_index[i]
            index_a_not = forward_index_not[i]
            clausole[1].append(((index_a%n) +1)*( -1 if index_a >= n else 1))
            clausole[0].append(((index_a_not%n) +1)*( -1 if index_a_not >= n else 1))

        clausole[1].append(((unsat_variable%n) +1)*( -1 if unsat_variable >= n else 1))

        while len(clausole[0]) < m:
            letter = np.random.choice(letteral,2,replace = False)
            dir = np.random.choice(range(2),2)
            index_a = letter[0] + dir[0]*n
            index_b = letter[1] + dir[1]*n
            clausole[0].append(((index_a%n) +1)*( -1 if index_a >= n else 1))
            clausole[1].append(((index_b%n) +1)*( -1 if index_b >= n else 1))



    return clausole



def test_case(n, m, is_sat):
    print(f"\nEvaluating test case: N = {n}, M = {m}...  ")#)\t", end="")

    res = 1

    # edges density
    (a,b) = generate_random_formula(n,m,is_sat)

    if DEBUG:
        for elem in a:
            assert elem <= n and elem >= -n and elem != 0
        for elem in b:
            assert elem <= n and elem >= -n and elem != 0
    # for elem in a:
    #     assert elem <= n and elem >= -n and elem != 0
    # for elem in b:
    #     assert elem <= n and elem >= -n and elem != 0

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
                    raise Exception('in function add_edge. Invalid node u={}'.format(u))
                if not G.has_node(v):
                    raise Exception('in function add_edge. Invalid node v={}'.format(v))
                G.add_edge(u,v)


            # the solution build G
            p.procedures.prepare_G(n,m,a,b,
                    callbacks=[
                        size_of_G,
                        add_edge
                        ])

            def is_reachible(u,v):
                if not G.has_node(u):
                    raise Exception('in function is_reachible. Invalid node u={}'.format(u))
                if not G.has_node(v):
                    raise Exception('in function is_reachible. Invalid node v={}'.format(v))
                succ_u = list(nx.dfs_successors(G,u))
                return (v in succ_u)

            # the solution build H
            ris = p.functions.is_satisfiable(n,
                    callbacks=[
                        is_reachible
                        ])

            if ris != is_sat:
                if ris:
                    raise Exception('The formula is satisfiable, but you claim that is not satisfiable')
                else:
                    raise Exception('The formula is not satisfiable, but you claim that is satisfiable')

            res *= 2
            def is_reachible(u,v):
                if not G.has_node(u):
                    raise Exception('in function is_reachible. Invalid node u={}'.format(u))
                if not G.has_node(v):
                    raise Exception('in function is_reachible. Invalid node v={}'.format(v))
                succ_u = list(nx.dfs_successors(G,u))
                return (v in succ_u)

            assignments = [-1]*(n+1)
            n_of_assignments = 0
            def assign_variable(letteral,value):
                nonlocal n_of_assignments
                if letteral > n:
                    raise Exception('in function assign_variable. Invalid letteral {}'.format(letteral))
                if assignments[letteral] != -1:
                    raise Exception('multiple assignments for letteral {}'.format(letteral))
                assignments[letteral] = False if value <= 0 else True
                n_of_assignments = n_of_assignments + 1

            p.procedures.find_assignment(n, m, a, b,
                    callbacks=[
                        is_reachible,
                        assign_variable
                        ])

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

        if DEBUG:
            print(f"Time usage: {p.time_usage}")
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
            if ret%3:
                ta.goals["model"] = False
            if ret%2:
                ta.goals["decision"] = False
    ta.goals.setdefault("decision", True)
    ta.goals.setdefault("model", True)

    for n in (100, 150, 200):
        for m in (100, 150, 200):
            is_sat = random.choice([True,False])
            ret = test_case(n,m,is_sat)
            if ret%3:
                ta.goals["model"] = False
            if ret%2:
                ta.goals["decision"] = False
    ta.goals.setdefault("decision", True)
    ta.goals.setdefault("model", True)

    for n in (1000, 1500, 2000):
        for m in (1000, 1500, 2000):
            is_sat = random.choice([True,False])
            ret = test_case(n,m,is_sat)
            if ret%3:
                ta.goals["model"] = False
            if ret%2:
                ta.goals["decision"] = False
    ta.goals.setdefault("decision", True)
    ta.goals.setdefault("model", True)

    print(ta.goals)

if __name__ == "__main__":
    main()
