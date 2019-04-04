Data un'istanza di 2-SAT si vuole trovare un'assegnamento delle variabili che soddisfa la formula.
Per fare questo si può utilizzare il problema di reachibility di un grafo, come oracolo.

Goal 1: Decidere se una formula è soddisfacibile o meno.

Goal 2: Esibire un'assegnamento delle variabili che soddisfa la formula (se esiste).

**Descrizione delle funzioni**

funzione prepare_G(n,m,a[],b[])

*Parametri*

n: numero di letterali

m: numero di clausole

I letterali sono numerati da 1 a n. Dato il letterale 1 <= *l* <= n, il numero *-l* rappresenta un'occorrenza del letterale negato, mentre il nuemro *l* rapprenseta un'occorrenza del letterale.

Per ogni 0 <= i < m,

  a[i] contiene il primo letterale della clausola i,

  b[i] contiene il secondo letterale della clausola i.

*Callbacks*

size_of_G(nG,mG): imposta la dimensione del grafo orientato che si vuole costruire. nG: numero di nodi mG: numero di archi

add_edge(u,v): inserisce un arco dal nodo u al nodo v con 0 <= u,v < nG.

is_satisfiable(n)

*Parametri*

n: numero di letterali

*Callbacks*

is_reachible(u,v): ritorna true se dati due nodi u,v nel grafo G preparato in precedenza, esiste un cammino tra u e v.

*Return Value*

La funzione ritorna true se la formula è soddisfacibile


find_assignment(n,m,a[],b[])

*Parametri*

n: numero di letterali

m: numero di clausole

I letterali sono numerati da 1 a n. Dato il letterale 1 <= *l* <= n, il numero *-l* rappresenta un'occorrenza del letterale negato, mentre il nuemro *l* rapprenseta un'occorrenza del letterale.

Per ogni 0 <= i < m,

  a[i] contiene il primo letterale della clausola i,

  b[i] contiene il secondo letterale della clausola i.

*Callbacks*

is_reachible(u,v): ritorna true se dati due nodi u,v nel grafo G preparato in precedenza, esiste un cammino tra u e v.

assign_variable(letteral,value): Inserisco la variabile 1<=*letteral*<=n nel modello, assegnandole il valore 0<=*value*<=1
