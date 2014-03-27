#!/bin/sh
echo "Linking uploads directory"
ln  -sf $OPENSHIFT_DATA_DIR/upload  $OPENSHIFT_REPO_DIR/wsgi/static   