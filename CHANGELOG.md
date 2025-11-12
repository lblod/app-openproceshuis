## v2.5.0

#### :rocket: Enhancement

- [#92](https://github.com/lblod/app-openproceshuis/pull/92) OPH-722 | add many relation to process-group for replacements [@JonasVanHoof](https://github.com/JonasVanHoof)
- [#91](https://github.com/lblod/app-openproceshuis/pull/91) OPH-721 | Restrict archiving conceptual-process entities [@JonasVanHoof](https://github.com/JonasVanHoof)
- [#90](https://github.com/lblod/app-openproceshuis/pull/90) BREAKING-CHANGE | OPH-714 | update dv organisational data [@JonasVanHoof](https://github.com/JonasVanHoof)
- [#89](https://github.com/lblod/app-openproceshuis/pull/89) OPH-665 | Allow MATCH on process-group,category & domain [@JonasVanHoof](https://github.com/JonasVanHoof)
- [#88](https://github.com/lblod/app-openproceshuis/pull/88) Feature/oph 671 hyperlinks to relevant bronnen [@JonasVanHoof](https://github.com/JonasVanHoof)
- [#87](https://github.com/lblod/app-openproceshuis/pull/87) OPH-662 | Process service for export [@JonasVanHoof](https://github.com/JonasVanHoof)
- [#85](https://github.com/lblod/app-openproceshuis/pull/85) grant rights to admin to add inventory process ([@andreo141](https://github.com/andreo141))
- [#83](https://github.com/lblod/app-openproceshuis/pull/83) Dispatch all anonymization requests to anonymization service ([@MartijnBogaert](https://github.com/MartijnBogaert))
- [#82](https://github.com/lblod/app-openproceshuis/pull/82) map to conceptualProcess instead of linkedConcept ([@andreo141](https://github.com/andreo141))
- [#81](https://github.com/lblod/app-openproceshuis/pull/81) Populate inventory ([@MartijnBogaert](https://github.com/MartijnBogaert))
- [#80](https://github.com/lblod/app-openproceshuis/pull/80) Add anonymization service ([@andreo141](https://github.com/andreo141))
- [#79](https://github.com/lblod/app-openproceshuis/pull/79) Add conceptual process classes to datamodel ([@MartijnBogaert](https://github.com/MartijnBogaert))

#### :wrench: Maintenance

- [#84](https://github.com/lblod/app-openproceshuis/pull/84) Add missing docker-compose directives missing for impersonation. ([@cecemel](https://github.com/cecemel))

## Deploy instructions

Pull image for the following services:

- bpmn
- process
- frontend

Restart the following services:

- dispatcher
- resource
- cache
- bpmn
- process
- frontend

# v2.4.0

## What's changed

#### :rocket: Enhancement

- [#73](https://github.com/lblod/app-openproceshuis/pull/73) Feature: Relevant administrative units as extra metadata ([@andreo141](https://github.com/andreo141))
- [#74](https://github.com/lblod/app-openproceshuis/pull/74) Update predicate linking IPDC products to processes ([@MartijnBogaert](https://github.com/MartijnBogaert))
- [#71](https://github.com/lblod/app-openproceshuis/pull/71) Introduce classification codes for custom organizations ([@MartijnBogaert](https://github.com/MartijnBogaert))
- [#69](https://github.com/lblod/app-openproceshuis/pull/69) Add VVSG mock user ([@andreo141](https://github.com/andreo141))
- [#68](https://github.com/lblod/app-openproceshuis/pull/68) Add access for VVSG ([@andreo141](https://github.com/andreo141))
- [#67](https://github.com/lblod/app-openproceshuis/pull/67) Add roles for Agentschap Binnenlands Bestuur and Digitaal Vlaanderen ([@MartijnBogaert](https://github.com/MartijnBogaert))
- [#66](https://github.com/lblod/app-openproceshuis/pull/66) Supplier access ([@andreo141](https://github.com/andreo141))
- [#63](https://github.com/lblod/app-openproceshuis/pull/63) Low threshold authorization ([@andreo141](https://github.com/andreo141))
- [#60](https://github.com/lblod/app-openproceshuis/pull/60) Allow governments to create new information assets ([@MartijnBogaert](https://github.com/MartijnBogaert))
- [#59](https://github.com/lblod/app-openproceshuis/pull/59) Make information assets accessible from a process ([@MartijnBogaert](https://github.com/MartijnBogaert))
- [#58](https://github.com/lblod/app-openproceshuis/pull/58) We use this process ([@andreo141](https://github.com/andreo141))
- [#57](https://github.com/lblod/app-openproceshuis/pull/57) Link process to blueprint ([@andreo141](https://github.com/andreo141))
- [#56](https://github.com/lblod/app-openproceshuis/pull/56) Upgrade virtuoso ([@andreo141](https://github.com/andreo141))
- [#54](https://github.com/lblod/app-openproceshuis/pull/54) OPH-464: ICR metadata additions ([@andreo141](https://github.com/andreo141))
- [#53](https://github.com/lblod/app-openproceshuis/pull/53) Integrate updated OP consumer ([@MartijnBogaert](https://github.com/MartijnBogaert))

#### :bug: Bug Fixes

- [#72](https://github.com/lblod/app-openproceshuis/pull/72) Fix typo in process class migration ([@andreo141](https://github.com/andreo141))
- [#70](https://github.com/lblod/app-openproceshuis/pull/70) Reintroduce mock users after consumer deploy ([@MartijnBogaert](https://github.com/MartijnBogaert))
- [#65](https://github.com/lblod/app-openproceshuis/pull/65) Make impersonation work again ([@MartijnBogaert](https://github.com/MartijnBogaert))
- [#55](https://github.com/lblod/app-openproceshuis/pull/55) Don't use custom boolean types ([@andreo141](https://github.com/andreo141))

#### :wrench: Maintenance

- [#64](https://github.com/lblod/app-openproceshuis/pull/64) Upgrade dependencies ([@andreo141](https://github.com/andreo141))
- [#62](https://github.com/lblod/app-openproceshuis/pull/62) Remove mu-search remains ([@MartijnBogaert](https://github.com/MartijnBogaert))
- [#61](https://github.com/lblod/app-openproceshuis/pull/61) Clean up SPARQL parser configuration ([@MartijnBogaert](https://github.com/MartijnBogaert))

## Deploy instructions

### 1. Virtuoso upgrade

#### 1. dump nquads

When upgrading it's recommended (and sometimes required!) to first dump to quads using the dump_nquads procedure:

```sh
docker compose exec virtuoso isql-v
SQL> dump_nquads ('dumps', 1, 1000000000, 1);
```

#### 2. stop the db

```sh
docker compose stop virtuoso
```

#### 3. remove old db and related files

When this has completed move the dumps folder to the toLoad folder. Make sure to remove the following files:

`.data_loaded`
`.dba_pwd_set`
`virtuoso.db`
`virtuoso.trx`
`virtuoso.pxa`
`virtuoso-temp.db`

```sh
mv data/db/dumps/* data/db/toLoad
rm data/db/virtuoso.{db,trx,pxa} data/db/virtuoso-temp.db data/db/.data_loaded data/db/.dba_pwd_set
```

Consider truncating or removing the `virtuoso.log` file as well.

#### 4. update virtuoso version

Modify the docker-compose file to update the virtuoso version

```diff
   virtuoso:
-    image: redpencil/virtuoso:1.0.0
+    image: redpencil/virtuoso:1.2.0-rc.1
```

#### 5. start the db

Start the DB and monitor the logs, importing the nquads might take a long time .

```sh
docker compose up -d virtuoso
docker compose logs -f virtuoso
```

### 2. New OP consumer

1. Add the following to `docker-compose.override.yml`

```yml
services:
  op-public-consumer:
    environment:
      DCR_LANDING_ZONE_DATABASE: "virtuoso" # Only on first run
      DCR_REMAPPING_DATABASE: "virtuoso" # Only on first run
      DCR_DISABLE_INITIAL_SYNC: "false" # Only on first run
      DCR_DISABLE_DELTA_INGEST: "true" # Only on first run
  mock-bestuurseenheid-generator:
    environment:
      MU_SPARQL_ENDPOINT: "http://virtuoso:8890/sparql" # Only on first run
```

2. Run and wait for the migrations to finish

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.override.yml up -d migrations
```

3. Run and wait for the OP consumer to finish

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.override.yml up -d database op-public-consumer
```

4. Run and wait for the mock users to be generated

```bash
 docker compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.override.yml up -d mock-bestuurseenheid-generator
```

5. Update `docker-compose.override.yml`

```yml
services:
  # op-public-consumer:
  #   environment:
  #     DCR_LANDING_ZONE_DATABASE: "virtuoso" # Only on first run
  #     DCR_REMAPPING_DATABASE: "virtuoso" # Only on first run
  #     DCR_DISABLE_INITIAL_SYNC: "false" # Only on first run
  #     DCR_DISABLE_DELTA_INGEST: "true" # Only on first run
  # mock-bestuurseenheid-generator:
  #   environment:
  #     MU_SPARQL_ENDPOINT: "http://virtuoso:8890/sparql" # Only on first run
```

6. Start the (complete) application

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.override.yml up -d
```
