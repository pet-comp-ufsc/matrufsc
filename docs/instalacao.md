# Instalação

Para rodar esse projeto, temos duas opções:

### Docker Compose

Para rodar esse projeto com docker, é nessesário ter tanto o [Docker e Docker Compose](https://docs.docker.com/engine/install) instalados. Após a instalação, podemos rodar o comando:

```
docker compose -f docker-compose.dev.yaml up -d
```

Após isso os containers irão subir e teremos a aplicação rodando. Para parar os containers, basta rodar:

```
docker compose -f docker-compose.dev.yaml down
```

### Manualmente

Também é possível rodar partes da aplicação manualmente.

#### Web

Para a parte web, basta rodar este comando dentro da pasta `web`:

```
npm install
npm run dev
```

`npm install` pode ser rodado apenas uma vez.
