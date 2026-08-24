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

Um Molho é uma estrutura de elos e chaves que possui múltiplas Imagens onde algumas regras se aplicam:

1. Chaves só se conectam a elos
2. Elos não fazem ciclos dentro do molho.

Uma Imagem é uma representação visual de um Molho de chaves quando segurada em uma chave ou elo.
Utilizamos esse sistema de imagem para podermos manipular mais facilmente o molho igual fazemos fisicamente.
Duas imagens podem ser diferentes e pertencer ao mesmo molho.
Utilizaremos = para igualdade entre imagens logo os molhos também são iguais nesse caso.
E utilizaremos ≡ para igualdade entre molhos. ≡/ É desigualdade entre molhos.
A chave ou elo segurado na imagem é chamado de elemento principal.
A notação [] descreve um elo, letras descreve chaves. Dentro de [] ficam elementos do elo em ordem anti-horário.
 - Exemplo: `[[]abc[d]]` Nesse molho temos um elo principal com (1 elo vazio, 3 chaves sendo elas a,b e c, e temos outro elo que possui uma chave d dentro dele). Nem sempre é possivel descrever facilmente em texto um molho de chaves.

O elemento principal na notação é o elo ou chave que segura toda os elementos da imagem dentro dela.
 - Exemplo: `[[][]abc[d]]`, o elemento principal é o elo externo `[...]`

É possível fazer que uma chave seja um elemento principal nesse caso fazemos a imagem do molho começar e terminar com a letra que descreve a chave `k[...]k`.
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
A função F(i) retorna quantos elementos existem no elemento principal em um imagem
 - Exemplo 1: F(`[[]abc[d]]`) = 5
 - Exemplo 2: F(`[k[][][[[]]]kkk]`) = 7
 - Exemplo 3: F(`[]`) = 0
 - Exemplo 4: F(`k[]l[]k`) = 3

A função E(m) retorna quantos elos existem em uma imagem de um molho
 - Exemplo 1: E(`[[]abc[d]]`) = 3
 - Exemplo 2: E(`[k[][][[[]]]kkk]`) = 6
 - Exemplo 3: E(`[]`) = 1
 - Exemplo 4: E(`k[]l[]k`) = 2

A função K(m) retorna quantas chaves existem em uma imagem de um molho
 - Exemplo 1: K(`[[]abc[d]]`) = 4
 - Exemplo 2: K(`[k[][][[[]]]kkk]`) = 4
 - Exemplo 3: K(`[]`) = 0
 - Exemplo 4: K(`k[]l[]k`) = 2

A função G(m) retorna quantos tipos de elos existem em uma imagem de um molho
 - Exemplo 1: G(`[0[1]1abc[0d]0]0`) = 2
 - Exemplo 2: G(`[0k[1]1[2]2[3[2[1]1]2]3kkk]0`) = 4
 - Exemplo 3: G(`[20]20`) = 1
 - Exemplo 4: G(`[0[1]1]0`) = 2
 - Exemplo 5: G(`k[]l[]k`) = 1

A função L(m) retorna quantas tipos de chaves existem em uma imagem de um molho
 - Exemplo 1: L(`[[]abc[d]]`) = 4
 - Exemplo 2: L(`[k[][][[[]]]kkk]`) = 1
 - Exemplo 3: L(`[]`) = 0
 - Exemplo 4: L(`k[]l[]k`) = 2



Função Tipo Mede/faz
r M→M rotaciona
r' M→M anti-rotaciona
e M→M entra
x M→M extrai o elemento mais à direita
l M×M→M linka dois molhos
