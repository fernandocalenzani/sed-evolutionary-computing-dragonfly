# Project Commands

```
1. cd ./mimir
2. cd ./mimir/scripts
3. bash docker_clean_all.sh
4. docker-compose down -v --rmi all
5. docker-compose up --build -d --quiet-pull
6. docker-compose -f logs mimir or docker-compose logs -f -n 100 mimir

z. docker-compose run --rm mimir /bin/bash

```

## Docker

```
1. docker-compose up
2. docker-compose up -d
3. docker-compose down

```

```PUSH CONTAINER
1. cd /docker/file/root
2. docker build -t mimir:TAG .
3. docker login
4. docker tag mimir:TAG fernandocalenzani/mimir:TAG
5. docker push user/mimir:TAG
```

```RUN CONTAINER
1. docker run -p 8080:80 fernandocalenzani/mimir:TAG
```

`LIST CONTAINER`
`1. docker ps` #Listar contêineres em execução
`2. docker ps -a` #Listar todos os contêineres (em execução e parados)
`3. docker ps -a -q` #Listar IDs de contêineres e outros detalhes
`4. docker ps -q` #Listar apenas IDs de contêineres em execução

`STOP CONTAINER`
`1. docker stop <ID_do_Conteiner>` #Encerrar um contêiner pelo ID
`2. docker stop <Nome_do_Conteiner>` #Encerrar um contêiner pelo nome
`3. docker stop $(docker ps -q)` #encerrar todos os contêineres
`4. docker rm <ID_do_Conteiner>` #Se precisar remover (eliminar) os contêineres depois de encerrá-los

`DELETE CONTAINER`
`1. docker rm <ID_do_Conteiner>`
`2. docker container prune`

`LOGS CONTAINER`
`1. docker logs <ID_do_Conteiner>`
`2. docker logs -f <ID_do_Conteiner>`

## docker-compose

```
1.0  docker-compose up
1.1  docker-compose up --build -d --quiet-pull

2.1. docker-compose down
2.2. docker-compose down -v

3.1. docker-compose logs [servico]

5.1. docker-compose ps
5.2. docker-compose ps -q

6.1. docker-compose run --rm nome-do-servico /bin/bash
6.2. docker-compose config --services
6.3. [utilizar comandos linux dentro do docker] ['exit' para sair]
6.4. docker-compose config
```
