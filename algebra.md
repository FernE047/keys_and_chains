r(`[]`) = `[]`
r(`[[]]`) = `[[]]`
r(`[`n`]`) = `[`n`]`
r(`k[]k`) = `k[]k`
r(`k`n`k`) = `k`n`k`
r(`[[]k]`) = `[k[]]`; `[[]k]` ≡ `[k[]]`
r(`[[]k[]]`) = `[[][]k]`; `[[]k[]]` ≡ `[[][]k]`
e(`[]`) = `[]`
e(`[[]]`) = `[[]]`
e(`[[]k]`) = `[[k]]`; `[[]k]` ≡ `[[k]]`
e(`[k[]]`) = `([[]])`;

r(n) ≡ n
e(n) ≡ n

`[[]k]` ≡ `[k[]]` ≡ `[[k]]`

`[]` + `[]` = `[[]]`
`[[]k]` + `[[]k]` =? `[[]k]` + `[[]k]`
`[[]k[[]k]]` = `[[]k[[]k]]`

a + b = b + a when a = b

`[[]k]` + `[k[]]` =? `[k[]]` + `[[]k]`
`[[]k[k[]]]` =? `[k[][[]k]]`
`[[k[]][]k]` =? `[k[][[]k]]`
`[k[][[]k]]` ≡ `[k[][[]k]]`

a + b ≡ b + a when a ≡ b

`[[]k]` + `[]` = `[[]k[]]`
`[]` + `[[]k]` = `[[[]k]]` ≡ `[[]k[]]`

`[[]k]` + `[[[]]k]` =? `[[[]]k]` + `[[]k]`
`[[]k[[[]]k]]` =? `[[[]]k[[]k]]` ≡
`[[[]k][[]]k]` ≡ `[[]k[[[]]k]]`
`[[]k[[[]]k]]` ≡ `[[[]]k[[]k]]`

a + b ≡ b + a when a ≡/ b or a =/ b
a + b ≡/ ra + b when ra =/ a
a + b ≡/ ea + b when ea =/ a

(`[[]k]` + `[]`) + `[[[]]]` =? `[[]k]` + (`[]` + `[[[]]]`)
`[[]k[][[[]]]]` =? `[[]k[[[[]]]]]` nope

okay... é hora de formalizar.

# Teoria dos Molhos

## Formalização

Um Molho é uma estrutura de elos e chaves que possui múltiplas Imagens onde algumas regras se aplicam:

1. Chaves só se conectam a elos
2. Elos não fazem ciclos dentro do molho.

Uma Imagem é uma representação visual de um Molho de chaves quando segurada em uma chave ou elo.
Utilizamos esse sistema de imagem para podermos manipular mais facilmente o molho igual fazemos fisicamente.
Duas imagens podem ser diferentes e pertencer ao mesmo molho.
Utilizaremos = para igualdade entre imagens logo os molhos também são iguais nesse caso.
E utilizaremos ≡ para igualdade entre molhos. ≡/ É desigualdade entre molhos.
A ordem no qual um elemento está dentro de um elo importa. É a ordem no qual os elementos aparecem em sentido anti-horário.
 - Exemplo: `[[]k[]k]` ≡ `[k[]k[]]`, enquanto `[[]k[]k]` ≡/ `[[]kk[]]`

Cada chave e elo em um molho é denominado um Elemento Primitivo.
Um molho sem Elementos Primitivos é um molho vazio denominado {}
A chave ou elo segurado na imagem é chamado de elemento principal.
Todo elemento conectado ao elemento principal está abaixo do elemento principal.
O elemento principal está acima de todos os outros.
O elemento principal de uma imagem possui profundidade 1, Cada elemento abaixo recebe +1 de profundidade recursivamente.
A notação [] descreve um elo, letras descreve chaves. Dentro de [] ficam elementos do elo em ordem anti-horário.
 - Exemplo: `[[]abc[d]]` Nesse molho temos um elo principal com (1 elo vazio, 3 chaves sendo elas a,b e c, e temos outro elo que possui uma chave d dentro dele). Nem sempre é possivel descrever facilmente em texto um molho de chaves.

A notação ... serve para representar que existem elementos não especificados entre os elementos descritos
O elemento principal na notação é o elo ou chave que segura toda os elementos da imagem dentro dela.
 - Exemplo: `[[][]abc[d]]`, o elemento principal é o elo externo `[...]`

É possível fazer que uma chave seja um elemento principal nesse caso fazemos a imagem do molho começar e terminar com a letra que descreve a chave `k...k`.
Esse sistema aplica-se para caso chaves sejam diferentes, só utilizar diferentes letras para representar cada chave.
Se estivermos falando de elos diferentes e identificaveis, adicionamos um número após [ e ] para identificar qual o tipo de elo. Afinal alguns molhos de chave possuem elos de diferentes formatos ou tamanhos.
 - Exemplo: `[0[1k]1p]0` é um elo 0 ligado a um elo 1 e uma chave p, dentro do elo 1 temos uma outra chave k, segue abaixo as outras imagens desse molho:

`[0[1k]1p]0`

1. `[0[1k]1p]0`
2. `[0p[1k]1]0`
3. `[1k[0p]0]1`
4. `[1[0p]0k]1`
5. `p[0[1k]1]0p`
6. `k[1[0p]0]1k`

Como as representações de molhos possuem letras e números, usamos "" ou `` para diferenciarmos o que é variavel ou função, e o que é parte do molho assim conseguirmos encapsular lógicas.
Quando falarmos de função, a imagem é representada pelas variaveis i,j ou k. molhos representados por m, n, p, q. equações usam a, b, c, d, f.

## 1. Funções Numéricas

Algumas funções númericas que auxiliam o estudo de Molhos. Essas funções são aplicadas a imagens ou molhos que retornam números

### 1.1. F(i): contagem no elemento principal

A função F(i) retorna quantos elementos existem no elemento principal em um imagem
 - Exemplo 1: F(`[[]abc[d]]`) = 5
 - Exemplo 2: F(`[k[][][[[]]]kkk]`) = 7
 - Exemplo 3: F(`[]`) = 0
 - Exemplo 4: F(`k[]l[]k`) = 3

### 1.2. E(m): Elos em um molho

A função E(m) retorna quantos elos existem em uma imagem de um molho
 - Exemplo 1: E(`[[]abc[d]]`) = 3
 - Exemplo 2: E(`[k[][][[[]]]kkk]`) = 6
 - Exemplo 3: E(`[]`) = 1
 - Exemplo 4: E(`k[]l[]k`) = 2

### 1.3. K(m): chaves em um molhos

A função K(m) retorna quantas chaves existem em uma imagem de um molho
 - Exemplo 1: K(`[[]abc[d]]`) = 4
 - Exemplo 2: K(`[k[][][[[]]]kkk]`) = 4
 - Exemplo 3: K(`[]`) = 0
 - Exemplo 4: K(`k[]l[]k`) = 2

### 1.4. G(m): tipos de elos no molho

A função G(m) retorna quantos tipos de elos existem em uma imagem de um molho
 - Exemplo 1: G(`[0[1]1abc[0d]0]0`) = 2
 - Exemplo 2: G(`[0k[1]1[2]2[3[2[1]1]2]3kkk]0`) = 4
 - Exemplo 3: G(`[20]20`) = 1
 - Exemplo 4: G(`[0[1]1]0`) = 2
 - Exemplo 5: G(`k[]l[]k`) = 1

### 1.5. L(m): tipos de chave no molho

A função L(m) retorna quantas tipos de chaves existem em uma imagem de um molho
 - Exemplo 1: L(`[[]abc[d]]`) = 4
 - Exemplo 2: L(`[k[][][[[]]]kkk]`) = 1
 - Exemplo 3: L(`[]`) = 0
 - Exemplo 4: L(`k[]l[]k`) = 2

### 1.6. P(m): elementos primitivos em molho

A função P(m) retorna quantos elementos primitivos existem em um molho
 - Exemplo 1: L(`[[]abc[d]]`) = 7
 - Exemplo 2: L(`[k[][][[[]]]kkk]`) = 10
 - Exemplo 3: L(`[]`) = 1
 - Exemplo 4: L(`k[]l[]k`) = 4

P(m) = K(m) + E(m)

### 1.7. Q(m): tipos de elementos primitivos em molho

A função Q(m) retorna quantos tipo de elementos primitivos existem em um molho
 - Exemplo 1: L(`[[]abc[d]]`) = 5
 - Exemplo 2: L(`[k[][][[[]]]kkk]`) = 2
 - Exemplo 3: L(`[]`) = 1
 - Exemplo 4: L(`[0[1]1abc[0d]0]0`) = 6

Q(m) = G(m) + L(m)

### 1.8. D(i): profundidade máxima

A função D(i) retorna qual a profundidade máxima dos elementos primitivos da imagem de um molho
 - Exemplo 1: L(`[[]abc[d]]`) = 3
 - Exemplo 2: L(`[k[][][[[]]]kkk]`) = 4
 - Exemplo 3: L(`[]`) = 1
 - Exemplo 4: L(`k[]l[]k`) = 2

### Futuras implementações

Outras funções que podem ser úteis e serão adicionadas no futuro:
 - Uma função que retorna quantas imagens um molho possui.
 - Uma função que retorna um conjunto de quais molhos estão abaixo do elemento principal.

## Funções Imagéticas

Funções imagéticas são imagens que alteram a imagem mantendo o molho o mesmo. Há somente duas funções imagéticas principais, outras funções imagéticas são composições das funções principais.
Agora definimos funções que alteram a imagem mantendo o molho:

### 1. r(i): Rotation

A função r(i) retorna uma imagem no qual o último elemento do elemento principal se torna o primeiro. Rotacionando a ordem dos elementos.
Fisicamente é o mesmo que rotacionar os elementos de um elo no sentido anti-horário
Se o elemento principal não possui elementos abaixo ou possui apenas um elemento, aplicar r é nulo e retorna a mesma imagem.
Se o elemento principal de uma imagem é uma chave, não há como rotacionar os elementos abaixo, logo aplicar r é nulo e retorna a mesma imagem. r(`k...k`) = `k...k`
Aplicar r ao molho vazio retorna o molho vazio
 - r(`[k[]k[]]`) = `[[]k[]k]`
 - r(`[kk[[]]]`) = `[[[]]kk]`
 - r(`[]`) = `[]`
 - r(`[[k[]k]]`) = `[[k[]k]]`
 - r(`{}`) = `{}`
 - r(`k[][k[]k]]k`) = `k[][k[]k]]k`

r(i) = j então i ≡ j

Dada uma função Numérica N, qualquer N descrita nos itens 1.1. a 1.8. temos N(r(i)) = N(i)
Uma Função de uma entrada só aplicada mais de uma vez é denotada por f^n(i) com f sendo a função (r, r', e, e*) n pode ser uma expressão entre parenteses quando necessário.
f^0 é uma função nula.
f^-1 desfaz a operação
 - r^2(`[kk[[]]]`) = r(r(`[kk[[]]]`)) = r(`[[[]]kk]`) = `[k[[]]k]` => r^2(`[kk[[]]]`) = `[k[[]]k]`
 - r^3(`[k[]k[]]`) = r(r(r(`[k[]k[]]`))) = r(r(`[[]k[]k]`)) = r(`[k[]k[]]`) = `[[]k[]k]` => r^3(`[k[]k[]]`) = `[[]k[]k]`
 - r^1(`[[]k]`) = r(`[[]k]`) = `[[]k]` => r^1(`[[]k]`) = `[[]k]`
 - r^0(`[[]k]`) = `[[]k]`
 - r^1000(`[]`) = `[]`

Como a rotação é algo cíclico, a cada F(i) rotações obtemos a mesma imagem que inicialmente: r^(F(i))(i) = i
Pela mesma propriedade cíclica, r^m = r^(m mod F(i))
r^(F(i)-1) = r^-1

Algumas imagens altamente simétricas possuem ciclos menores. defino aqui a função C(i) que retorna o menor ciclo de rotações de uma imagem maior que zero. logo r^(C(i)) = i
 - C(`[k[]k[]]`) = 2, porque r^2(`[k[]k[]]`) = `[k[]k[]]`
 - C(`[k[[]k[]][]k[[]k[]][]]`) = 3, porque r(r(r(`[k[[]k[]][]k[[]k[]][]]`))) = `[k[[]k[]][]k[[]k[]][]]`
 - C(`[k[]kk[][][[[]]]]`) = 7 = F(`[k[]kk[][][[[]]]]`).

### 2. r'(i): Anti-Rotation

A função r'(i) retorna uma imagem no qual o primeiro elemento do elemento principal se torna o último. Rotacionando a ordem dos elementos.
Fisicamente é o mesmo que rotacionar os elementos de um elo no sentido horário
Todas as propriedades de uma rotação normal se aplicam a anti-rotação.
Como a anti-rotação age como inverso da rotação, temos a identidade r^-1 = r'

### 3. e(i): Enter



Função Tipo Mede/faz
e M→M entra
e* M→M sai
x M→M extrai o elemento mais à direita, ficamos com o resto
x* M→M extrai o elemento mais à direita e ficamos com ele 
l M×M→M linka dois molhos
