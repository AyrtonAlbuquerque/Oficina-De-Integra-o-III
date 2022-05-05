#/usr/bin/bash

docker run \
  --name some-postgres \
  -p 5432:5432 \
  -e POSTGRES_USER=admin  \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_DB=SmartRecyclerDb \
  -v /custom/mount:/var/lib/postgresql/data \
  -d postgres