import turingarena as ta
import networkx as nx
import random
import numpy.random as np

DEBUG = False

# Goals:
# - is satisfiable
# - give an assignment

def generate_random_formula(n,m,is_sat):
    # generate the list of letterals
    letteral = []
    for i in range(m):
        letteral.append(i)
        # letteral.append(n+i)

    random.shuffle(letteral)
    clausole = []
    if(is_sat):
        #I have to avoid cycles
        G = nx.DiGraph()
        G.add_nodes_from(range(2*n))
        while len(clausole) < m:
            a = random.choice(letteral)
            b = random.choice(letteral)
            while b == a:
                b = random.choice(letteral)

            a_dir = random.choice(2)
            b_dir = random.choice(2)

            index_a = a + a_dir*n
            index_b = b + b_dir*n

            index_not_a = (index_a + n)%n
            index_not_b = (index_b + n)%n

            G.add_edge(index_not_a,index_b)
            G.add_edge(index_not_b,index_a)

            reachable_from_a = list(nx.dfs_preorder_nodes(G,index_a))
            reachable_from_not_b = list(nx.dfs_preorder_nodes(G,index_not_b))

            if index_not_a in reachable_from_a or index_b in reachable_from_not_b:
                G.remove_edge(index_not_a,index_b)
                G.remove_edge(index_not_b,index_a)
            else:
                clausole.append([index_a,index_b])
    else:
        # I have to introduce a cycle
        cycle_length = random.choice(range(min(n,m)))
        cycle = np.random.choice(letterals,cycle_length,replace = False)
        directions = np.random.choice(range(2),cycle_length)
        index = [cycle[i] + directions[i]*n for i in range(cycle_length)]
        index_not = [(index[i]+n)%n for i in range(cycle_length)]

        

def test_case(n, m):
    print(f"\nEvaluating test case: N = {n}, M = {m}...  ")#)\t", end="")

    res = 1

    N = n_u
    M = n_v

    # edges density
    edges = m

    # create random graph
    G = nx.bipartite.gnmk_random_graph(N, M, edges, seed=0xC0FFEE)
    # U is 0..N-1, V is N..N+M-1
    U,V = range(0,N), range(N,N+M)

    try:
        with ta.run_algorithm(ta.submission.source, time_limit=0.15) as p:
            # build the graphs
            n1 = len(U)
            n2 = len(V)
            mG = edges

            u = [ x for x, _ in sorted(G.edges) ]
            v = [ y for _, y in sorted(G.edges) ]

            # initialize the H graph
            H = nx.DiGraph()
            H_edges = -1
            flow_start = None
            flow_end   = None

            def size_of_H(nH,mH):
                nonlocal H, H_edges
                if nH < 0:
                    raise Exception('negative number of nodes')
                if mH < 0:
                    raise Exception('negative number of edges')
                H.add_nodes_from(range(0,nH))
                H_edges = mH

            def add_edge(u,v,w):
                nonlocal H, H_edges
                if len(H.edges) == H_edges:
                    raise Exception('too many edges added with add_edge')
                if not H.has_node(u):
                    raise Exception('invalid node u={}'.format(u))
                if not H.has_node(v):
                    raise Exception('invalid node v={}'.format(v))
                H.add_edge(u,v, capacity=w)

            def set_s(s):
                nonlocal flow_start
                flow_start = s

            def set_t(t):
                nonlocal flow_end
                flow_end = t

            # the solution build H
            p.procedures.prepare_H_from_G(n1, n2, mG, u, v,
                    callbacks=[
                        size_of_H,
                        add_edge,
                        set_s,
                        set_t
                        ])

            # test that the information provided for H are consistent
            if flow_start is None:
                raise Exception('flow start not set (use set_s)')
            if flow_end is None:
                raise Exception('flow end not set (use set_t)')
            if len(H.edges) != H_edges:
                raise Exception('inconsistent number of edges')

            max_flow, flow = nx.algorithms.flow.maximum_flow(
                    H, flow_start, flow_end)

            matching = []
            cover_on_U = set()
            cover_on_V = set()

            def put_in_matching(u,v):
                nonlocal matching
                matching.append([u,v])

            def put_in_node_cover_on_side_U(u):
                nonlocal cover_on_U
                cover_on_U.add(u)

            def put_in_node_cover_on_side_V(v):
                nonlocal cover_on_V
                cover_on_V.add(v)

            def flow_val(u,v):
                nonlocal flow
                return flow[u][v]

            p.procedures.max_card_matching_and_min_node_cover_in_G(n1,n2,mG,u,v,
                    callbacks=[
                        put_in_matching,
                        put_in_node_cover_on_side_U,
                        put_in_node_cover_on_side_V,
                        flow_val
                        ])

            print("Evaluating the matching... \t", end="")

            try:
                # check the matching
                if max_flow != len(matching):
                    raise Exception('matching is not massimal')

                from_set = set()
                to_set = set()
                for u, v in matching:
                    # is a valid edge
                    if not G.has_edge(u,v):
                        raise Exception('({},{}) is not an edge'.format(v,u))

                    # single matching for every node
                    if u in from_set:
                        raise Exception('multiple matching for u={}'.format(u))
                    from_set.add(u)
                    if v in to_set:
                        raise Exception('multiple matching for v={}'.format(v))
                    to_set.add(v)

                # The matching is correct
                print("[CORRECT]")
                res = res * 2
            except Exception as e:
                print(f"[WRONG] \t error: {e}")




            print("Evaluating the node cover... \t", end="")

            try:
                # check the node cover
                if max_flow != (len(cover_on_U) + len(cover_on_V)):
                    raise Exception('wrong size of cover, {} vs {}'.format(
                        max_flow,(len(cover_on_U) + len(cover_on_V))))

                for (x,y) in G.edges:
                    if not x in cover_on_U and not y in cover_on_V:
                        raise Exception('edges ({},{}) is not covered'.format(x,y))

                # The node cover is correct

                print("[CORRECT]")
                res = res * 3

            except Exception as e:
                print(f"[WRONG] \t error: {e}")

            # compute the minimum cut

            min_cut, partition = nx.algorithms.flow.minimum_cut(
                    H, flow_start, flow_end)

            reachable, non_reachable = partition

            cutset = set()
            for u, nbrs in ((n, H[n]) for n in reachable):
                cutset.update((u, v) for v in nbrs if v in non_reachable)

            cutset = [ (x,y) for x,y in cutset ]

            iter_cut_left = 0
            iter_cut_right = 0
            cover_on_U = set()
            cover_on_V = set()

            def put_in_node_cover_on_side_U(u):
                nonlocal cover_on_U
                cover_on_U.add(u)

            def put_in_node_cover_on_side_V(v):
                nonlocal cover_on_V
                cover_on_V.add(v)

            def min_cut_value():
                nonlocal min_cut
                return min_cut

            def next_in_min_cut_left():
                nonlocal min_cut, iter_cut_left, cutset
                if iter_cut_left >= min_cut:
                    raise Exception('cut left has only {} nodes'.format(n1))
                iter_cut_left+=1
                return cutset[iter_cut_left-1][0]

            def next_in_min_cut_right():
                nonlocal min_cut, iter_cut_right, cutset
                if iter_cut_right >= min_cut:
                    raise Exception('cut right has only {} nodes'.format(n1))
                iter_cut_right+=1
                return cutset[iter_cut_right-1][1]

            p.procedures.min_node_cover_from_min_cut(n1,n2,
                    callbacks=[
                        put_in_node_cover_on_side_U,
                        put_in_node_cover_on_side_V,
                        min_cut_value,
                        next_in_min_cut_left,
                        next_in_min_cut_right
                        ])

            print("Evaluating the node cover... \t", end="")
            try:
                # check the node cover
                if max_flow != (len(cover_on_U) + len(cover_on_V)):
                    raise Exception('wrong size of cover, {} vs {}'.format(
                        max_flow,(len(cover_on_U) + len(cover_on_V))))

                for (x,y) in G.edges:
                    if not x in cover_on_U and not y in cover_on_V:
                        raise Exception('edges ({},{}) is not covered'.format(x,y))

                # The node cover is correct

                print("[CORRECT]")
                res = res * 5

            except Exception as e:
                print(f"[WRONG] \t error: {e}")

        if DEBUG:
            print(f"Time usage: {p.time_usage}")
    except Exception as e:
        print(f"[WRONG] \t error: {e}")

    if res == 2*3*5:
        print(f"test case: N_U = {n_u}, N_V = {n_u}, M = {m} [PASSED]")
    else:
        print(f"test case: N_U = {n_u}, N_V = {n_u}, M = {m} [FAILED]")

    return res


def main():
    for n_u,n_v in ((10,5), (15,20), (20,20)):
        for m in (10, 15, 20):
            ret = test_case(n_u,n_v,m)
            if ret%5:
                ta.goals["min_node_cover_from_min_cut"] = False
            if ret%3:
                ta.goals["min_node_cover"] = False
            if ret%2:
                ta.goals["max_card_matching"] = False
    ta.goals.setdefault("max_card_matching", True)
    ta.goals.setdefault("min_node_cover", True)
    ta.goals.setdefault("min_node_cover_from_min_cut", True)

    for n_u,n_v in ((100,50), (150,200), (200,200)):
        for m in (100, 150, 200):
            ret = test_case(n_u,n_v,m)
            if ret%5:
                ta.goals["min_node_cover_from_min_cut"] = False
            if ret%3:
                ta.goals["min_node_cover"] = False
            if ret%2:
                ta.goals["max_card_matching"] = False
    ta.goals.setdefault("max_card_matching", True)
    ta.goals.setdefault("min_node_cover", True)
    ta.goals.setdefault("min_node_cover_from_min_cut", True)

    for n_u,n_v in ((1000,500), (1500,2000), (2000,2000)):
        for m in (1000, 1500, 2000):
            ret = test_case(n_u,n_v,m)
            if ret%5:
                ta.goals["min_node_cover_from_min_cut"] = False
            if ret%3:
                ta.goals["min_node_cover"] = False
            if ret%2:
                ta.goals["max_card_matching"] = False

    ta.goals.setdefault("max_card_matching", True)
    ta.goals.setdefault("min_node_cover", True)
    ta.goals.setdefault("min_node_cover_from_min_cut", True)

    print(ta.goals)

if __name__ == "__main__":
    main()
