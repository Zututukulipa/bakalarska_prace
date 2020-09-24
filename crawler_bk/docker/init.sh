#!/bin/bash


CQL_COMMAND="CREATE KEYSPACE IF NOT EXISTS scraped WITH replication = {'class':'SimpleStrategy', 'replication_factor':1};"
until echo $CQL_COMMAND | cqlsh; do
  sleep 10 
done &
  
exec /docker-entrypoint.sh "$@"
