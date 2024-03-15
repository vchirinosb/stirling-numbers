"""Stirling Numbers: https://en.wikipedia.org/wiki/Stirling_number."""


def get_numero_particiones(n, k):
    """
    Obtener numero de particiones de un conjunto con 'n' elementos en 'k'
    subconjuntos.
    
    Numeros de Stirling
    S(n, k) = Nro de particiones distintas del conjunto {1, ..., n} en k
    bloques no vacios

    :param n: Int, nro de elementos. Ejemplo: 4.
    :param k: Int, nro de subconjuntos.  Ejemplo: 2.

    :return: Int, nro de diferentes particiones de 'n' elementos en 'k'
        subconjuntos.
    """
    # Inicializamos la matriz de valores.
    # Ejemplo para n=4, k=2:
    # [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    matriz = [[0 for i in range(k + 1)] for j in range(n + 1)]
 
    # Calculamos los valores de las entradas de la matriz.
    # Ejemplo para n=4, k=2:
    # [[0, 0, 0], [0, 1, 0], [0, 1, 1], [0, 1, 3], [0, 1, 7]]
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            if j == 1 or i == j:
                matriz[i][j] = 1
            else:
                matriz[i][j] = j * matriz[i - 1][j] + matriz[i - 1][j - 1]
    
    # Ejemplo para n=4, k=2:
    # matriz[n][k] = 7          
    return matriz[n][k]


def obtener_particiones_n_k(lista_n, k):
    """
    Obtener particiones de un conjunto con 'n' elementos en 'k' subconjuntos.
    
    Representacion:

    n-1, k        n-1, k-1
          \      /
           \    /
            n, k

    Ejemplo: 123(2)

    123|-     12|3  13|2      1|23
       \      /        \      /
        \    /          \    /
         12|-            1|2
              \         /
               \       /
                  1|-
                   |
                   |
                  -|-

    :param lista_n: List, lista de elementos. Ejemplo: [1, 2, 3, 4].
    :param k: Int, nro de subconjuntos.  Ejemplo: 2.

    :return: particiones de 'n' elementos en 'k' subconjuntos.
    """
    def agregar_particion_valida(n, a):
        """Agregar particion valida."""
        particion = [[] for i in range(k)]
        for j in range(n):
            particion[a[j + 1]].append(lista_n[j])

        return particion

    def get_particion_izq(k_prima, n_prima, sigma, n, aux):
        """Obtener particion de forma recursiva. Rama izquierda."""
        if k_prima == 2:
            yield agregar_particion_valida(n, aux)
        else:
            for v in get_particion_izq(
                    k_prima - 1, n_prima - 1, (k_prima + sigma) % 2, n, aux):
                yield v
        if n_prima == k_prima + 1:
            aux[k_prima] = k_prima - 1
            yield agregar_particion_valida(n, aux)
            while aux[n_prima] > 0:
                aux[n_prima] = aux[n_prima] - 1
                yield agregar_particion_valida(n, aux)
        elif n_prima > k_prima + 1:
            if (k_prima + sigma) % 2 == 1:
                aux[n_prima - 1] = k_prima - 1
            else:
                aux[k_prima] = k_prima - 1
            if (aux[n_prima] + sigma) % 2 == 1:
                for v in get_particion_der(k_prima, n_prima - 1, 0, n, aux):
                    yield v
            else:
                for v in get_particion_izq(k_prima, n_prima - 1, 0, n, aux):
                    yield v
            while aux[n_prima] > 0:
                aux[n_prima] = aux[n_prima] - 1
                if (aux[n_prima] + sigma) % 2 == 1:
                    for v in get_particion_der(
                            k_prima, n_prima - 1, 0, n, aux):
                        yield v
                else:
                    for v in get_particion_izq(
                            k_prima, n_prima - 1, 0, n, aux):
                        yield v

    def get_particion_der(k_prima, n_prima, sigma, n, aux):
        """Obtener particion de forma recursiva. Rama derecha."""
        if n_prima == k_prima + 1:
            while aux[n_prima] < k_prima - 1:
                yield agregar_particion_valida(n, aux)
                aux[n_prima] = aux[n_prima] + 1
            yield agregar_particion_valida(n, aux)
            aux[k_prima] = 0
        elif n_prima > k_prima + 1:
            if (aux[n_prima] + sigma) % 2 == 1:
                for v in get_particion_izq(k_prima, n_prima - 1, 0, n, aux):
                    yield v
            else:
                for v in get_particion_der(k_prima, n_prima - 1, 0, n, aux):
                    yield v
            while aux[n_prima] < k_prima - 1:
                aux[n_prima] = aux[n_prima] + 1
                if (aux[n_prima] + sigma) % 2 == 1:
                    for v in get_particion_izq(
                            k_prima, n_prima - 1, 0, n, aux):
                        yield v
                else:
                    for v in get_particion_der(
                            k_prima, n_prima - 1, 0, n, aux):
                        yield v
            if (k_prima + sigma) % 2 == 1:
                aux[n_prima - 1] = 0
            else:
                aux[k_prima] = 0
        if k_prima == 2:
            yield agregar_particion_valida(n, aux)
        else:
            for v in get_particion_der(
                    k_prima - 1, n_prima - 1, (k_prima + sigma) % 2, n, aux):
                yield v

    # Ejemplo de ejecucion
    # n=4, k=2
    # Inicializamos: a=[0, 0, 0, 0, 0]
    n = len(lista_n)
    aux = [0] * (n + 1)
    for j in range(1, k + 1):
        aux[n - k + j] = j - 1
    # Establecemos: aux=[0, 0, 0, 0, 1]
    return get_particion_izq(k, n, 0, n, aux)

def imprimir_particiones(particiones):
    """
    Imprimir lista de particiones.
    
    :param particiones: List, lista de listas.
    """
    for particion in particiones:
        print(*particion)


if __name__ == '__main__':
    n = input('Ingrese el valor de N: ')
    k = input('Ingrese el valor de K: ')
    n = int(n)
    k = int(k)
    
    # Ejemplo para n=4
    # lista_n = [1,2,3,4]
    lista_n = list(range(1, n+1))
    print('')
    print('OUTPUT:')
    print('{} particiones'.format(get_numero_particiones(n, k)))
    print('')
    print('PARTICIONES:')
    # print(list(obtener_particiones_n_k(lista_n, k)))
    particiones = list(obtener_particiones_n_k(lista_n, k))
    imprimir_particiones(particiones)
