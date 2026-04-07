#!/usr/bin/env bash

TARGET_DIR=./data/mkdocs/docs
cp ../README.md $TARGET_DIR
cp -r ../Arduino $TARGET_DIR
cp -r ../Boxes $TARGET_DIR
cp -r ../Displays $TARGET_DIR
cp -r ../Generic $TARGET_DIR
cp -r ../Lights $TARGET_DIR
cp -r ../Network $TARGET_DIR
cp -r ../Sensors $TARGET_DIR
cp -r ../Sound $TARGET_DIR
cp -r ../Switches $TARGET_DIR

cp mkdocs.yaml ./data/mkdocs/