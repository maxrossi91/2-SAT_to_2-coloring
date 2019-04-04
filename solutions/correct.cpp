#include <vector>

// the mapping of the nodes is
//  l1 -> 0
// !l1 -> 1
//  l2 -> 2
// !l2 -> 3
//    ...
//  ln -> 2(n-1)
// !ln -> 2(n-1) + 1
int lit_to_node(int l) {
    return l > 0 ? (2*(l-1)) : (2*(-(l-1))+1);
}

void prepare_G(int n, int m, int *a, int *b, void size_of_G(int nG, int mG), void add_edge(int u, int v)) {
    size_of_G(2*n, m);
    for (int i = 0; i < m; ++i) {
        // clause: a v b ~> edges: (!a,b), (!b, a)
        add_edge(lit_to_node(-a[i]), lit_to_node(b[i]));
        add_edge(lit_to_node(-b[i]), lit_to_node(a[i]));
    }
}

int is_satisfiable(int n, int is_reachible(int u, int v)) {
    for (int i = 1; i <= n; ++i) {
        if ( is_reachible(lit_to_node( i), lit_to_node(-i)) &&
             is_reachible(lit_to_node(-i), lit_to_node( i)) )
            return 0;
    }
    return 1;
}

void find_assignment(int n, int m, int *a, int *b, int is_reachible(int u, int v), void assign_variable(int letteral, int value)) {
    std::vector<bool> assigned(n+1,false);

    for(int i = 1; i <= n; ++i) {
        if (assigned[i]) continue;

        if (!is_reachible(lit_to_node(i), lit_to_node(-i))) {
            // true don't generate a conflict
            assign_variable(i, 1);
            assingned[i] = true;

            for(int j = i+1; j <= n; ++j) {
                if (assigned[j]) continue;

                if (is_reachible(lit_to_node(i), lit_to_node(j))) {
                    assign_variable(j, 1);
                    assigned[j] = true;
                }

                if (is_reachible(lit_to_node(i), lit_to_node(-j))) {
                    assign_variable(j, 0);
                    assigned[j] = true;
                }
            }

        }
        else {
            // false don't generate a conflict
            assign_variable(i, 0);
            assigned[i] = true;

            for(int j = i+1; j <= n; ++j) {
                if (assigned[j]) continue;

                if (is_reachible(lit_to_node(-i), lit_to_node(j))) {
                    assign_variable(j, 1);
                    assigned[j] = true;
                }

                if (is_reachible(lit_to_node(-i), lit_to_node(-j))) {
                    assign_variable(j, 0);
                    assigned[j] = true;
                }
            }
        }
    }
}
