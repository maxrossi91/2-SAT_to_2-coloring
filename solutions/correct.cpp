#include <vector>
#include <assert.h>

// the mapping of the nodes is
//  l1 -> 0
// !l1 -> 1
//  l2 -> 2
// !l2 -> 3
//    ...
//  ln -> 2(n-1)
// !ln -> 2(n-1) + 1
int lit_to_node(int l) {
    return ((l > 0) ? (2*(l-1)) : (2*((-l-1))+1));
}

void prepare_G(int n, int m, int *a, int *b,
        void size_of_G(int nG, int mG),
        void add_edge(int u, int v)) {
    size_of_G(2*n, 2*m);
    for (int i = 0; i < m; ++i) {
        // clause: a v b ~> edges: (!a,b), (!b, a)
        add_edge(lit_to_node(-a[i]), lit_to_node(b[i]));
        add_edge(lit_to_node(-b[i]), lit_to_node(a[i]));
    }
}

int is_satisfiable(int nG, int *components,
        void assign_variable(int letteral, int value)) {

    for (int l = 1; l <= nG/2; ++l) {
        if (components[lit_to_node(l)] == components[lit_to_node(-l)])
            return 0; // UNSAT
        else if (components[lit_to_node(-l)] < components[lit_to_node(l)])
            assign_variable(l,1); // l is TRUE
        else
            assign_variable(l,0); // l is FALSE
    }
    return 1; // SAT
}

