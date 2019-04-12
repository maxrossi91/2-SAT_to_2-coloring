Data un'istanza di 2-SAT si vuole trovare un'assegnamento delle variabili che soddisfa la formula, se possibile.
Nel caso di 2-SAT è possibile usare il calcolo delle componenti fortemente connesse di un grafo come oracolo per risolvere il problema.

In questo esericizio dovrai prima costruire un grafo a partire da una formula 2-SAT.
Una volta costruito il grafo ti verrà chiesto di dimostrare che la formula è soddisfacibilie oppure no utilizzando solo le componenti fortemente connesse del grafo precedentemente costruito.
Nel caso il problema sia soddisfacibile, è anche possibile fornire un modello che soddisfa le formule per ricevere punti addizionali.


Goal 1: Decidere se una formula è soddisfacibile o meno.

Goal 2: Esibire un'assegnamento delle variabili che soddisfa la formula (se esiste).

***Descrizione delle funzioni***

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


is_satisfiable(nG,components)

*Parametri*

nG: numero di nodi del grafo

per ogni 0 <= i < nG
  components[i]: ritorna l'identificatore della componente fortemente connessa a cui il nodo appartiene.
  Le componenti sono ordinate secondo un ordinamento topologico: dati due nodi u,v in G, components[u] <= components[v] se esiste un cammino da u a v.

*Callbacks*

assign_variable(letteral,value): Inserisco la variabile 1<=*letteral*<=n nel modello, assegnandole il valore 0<=*value*<=1

*Return Value*

La funzione ritorna true se e solo se la formula è soddisfacibile.
Nel caso la formula sia soddisfaci

