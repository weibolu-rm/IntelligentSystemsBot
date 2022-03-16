#!/bin/bash

mkdir -p $1

pushd $1
curl -O https://opendata.concordia.ca/datasets/sis/CU_SR_OPEN_DATA_CATALOG.csv \
    -O https://opendata.concordia.ca/datasets/sis/CU_SR_OPEN_DATA_CATALOG_DESC.csv
popd
