# Hooks

Hooks são funções auxiliares que podem modificar o comportamento do componente. Abaixo vamos abordar os principais Hooks usados.

---

## `useState`

É utilizado para declarar variáveis de estado dentro de componentes funcionais. Retorna uma tupla com o valor atual do estado e uma função para atualizá-lo.

```javascript
import { useState } from "react";

function Contador() {
  const [contador, setContador] = useState(0);

  return (
    <button onClick={() => setContador((c) => c + 1)}>
      Cliques: {contador}
    </button>
  );
}
```

Veja mais [aqui](https://react.dev/reference/react/useState).

---

## `useEffect`

Gerencia efetios colaterais (side effects) em componentes, como chamadas de APIs, manipulações manuais no DOM e etc.

```javascript
import { useEffect, useState } from "react";

function BuscaDados({ id }) {
  const [dados, setDados] = useState(null);

  useEffect(() => {
    // Executa ao montar o componente ou quando 'id' mudar
    let ativo = true;
    fetch(`/api/dados/${id}`)
      .then((res) => res.json())
      .then((data) => ativo && setDados(data));

    // Função de cleanup (executa ao desmontar ou antes da próxima execução)
    return () => {
      ativo = false;
    };
  }, [id]); // Array de dependências

  // ...
}
```

Veja mais [aqui](https://react.dev/reference/react/useEffect).

## `useContext`

Permite consumir valores de um contexto Global sem precisar passar props manualmente em cada nível da árvore (evita o prop drilling).

```javascript
import { useContext } from "react";
import { TemaContext } from "./TemaContext";

function BotaoTematico() {
  const tema = useContext(TemaContext);
  return <button style={{ background: tema.background }}>Clique</button>;
}
```

Veja mais [aqui](https://react.dev/reference/react/useContext).

## `useRef`

Retorna um objeto mutável cuja propriedade `.current` é inicializada com o argumento passado. O valor persiste durante todo o ciclo de vida do componente. Usado principalmente para acessar elementos DOM diretamente ou armazenar valores mutáveis que não devem engatilhar re-renderizações.

```javascript
import { useRef } from "react";

function InputFocado() {
  const inputRef = useRef(null);

  const focar = () => inputRef.current.focus();

  return (
    <>
      <input ref={inputRef} type="text" />
      <button onClick={focar}>Focar no Input</button>
    </>
  );
}
```

Veja mais [aqui](https://react.dev/reference/react/useRef).

## Hooks de otimização

Esses hooks servem para garantir que o componente re-renderize apenas quando necessário, fazendo com que tenhamos ganho de performance na interface.

### `useMemo`

Memoriza um **valor** calculado, recalculando-o apenas quando uma de suas dependências muda. Evita cálculos pesados em renderizações desnecessárias.
Veja mais [aqui](https://react.dev/reference/react/useMemo).

### `useCallback`

Memoriza uma função, garantindo que a referência da função não mude entre renderizações (útil ao passar funções como props para componentes filhos otimizados com `React.memo`).
Veja mais [aqui](https://react.dev/reference/react/useCallback).

O exemplo a seguir aplica os dois hooks apresentados

```javascript
import { useState, useMemo, useCallback, memo } from "react";

// O 'memo' garante que este componente só volta a renderizar se a prop 'aoClicar' mudar.
const BotaoOtimizado = memo(({ aoClicar }) => {
  console.log("Botão renderizado no ecrã!");
  return <button onClick={aoClicar}>Incrementar Contador</button>;
});

export function Contador() {
  const [contador, setContador] = useState(0);
  const [texto, setTexto] = useState("");

  // USEMEMO: Memoriza um valor.
  // Só volta a fazer esta conta se o 'contador' sofrer alterações.
  const dobro = useMemo(() => {
    return contador * 2;
  }, [contador]);

  // USECALLBACK: Memoriza uma função.
  // Garante que a função é a mesma na memória, evitando que o BotaoOtimizado re-renderize.
  const incrementar = useCallback(() => {
    setContador((c) => c + 1);
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      {/* Escrever aqui atualiza o estado 'texto', causando uma re-renderização do componente Contador */}
      <input
        type="text"
        value={texto}
        onChange={(e) => setTexto(e.target.value)}
        placeholder="Escreva algo..."
      />

      <p>Contador: {contador}</p>
      <p>O dobro é: {dobro}</p>

      {/* Graças ao useCallback, esta prop não muda de referência, logo o botão não re-renderiza ao escrevermos no input */}
      <BotaoOtimizado aoClicar={incrementar} />
    </div>
  );
}
```
