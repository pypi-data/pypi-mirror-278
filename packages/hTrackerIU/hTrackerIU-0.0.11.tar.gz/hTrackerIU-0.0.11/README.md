# Installation

```
# pip3 install hTrackerIU
# hTrackerIU
open http://localhost:8095
```

You can also download the source code and choose one of the three options:

#### Using makefile

```
# make start
open http://localhost:8095
```

#### Using Docker

```
# docker compose run --rm init-db
# docker compose up -d htracker-iu
open http://localhost:8095
```

#### Using Python

```
# python3 run.py
open http://localhost:8095
```

# How to use

## Add a New Habit

![](./docs/add.png)

## Mark a Habit

![](./docs/mark.png)

## Current Streak

![](./docs/streak.png)

## Details

![](./docs/details.png)

## Delete Habit

![](./docs/delete.png)

## Analytics

![](./docs/analytics.png)

# Development

#### Run Backend Tests

```
# make test
```

#### Rebuild Backend Docker Container

```
# make build
```

#### Initialize the Database with Samples

```
# make init-db
```

#### Start Backend in Development Mode

```
# make start-be
```

#### Generate Frontend Client Using OpenAPI Generator

```
# make client
```

#### Start Frontend in Development Mode

```
# make start-fe
```

#### Create Production Build of Frontend

```
# make build-fe
```

#### Stop All Containers

```
# make stop
```

#### Run PEP 8 Check

```
# make pep8-check
```

#### Run PEP 8 Fix

```
# make pep8-fix
```
