#!/bin/bash
export GOOGLE_APPLICATION_CREDENTIALS=<PATH_TO_SERVICE_ACCOUNT_KEY_FILE> # Example: /home/me/keys/my_service_account_key.json
export BEARER_TOKEN=<YOUR_BEARER_TOKEN_PROVIDED_BY_TWITTER> # Example: AAAAAAAAAYYYYYAAAAAAAIij9QAAAAAAuuuuuuYYJnGru%2FUI%2F80n%2BzMA8%3DjUUUUUdZDJyywOHaEodMOLLVveYHeLLoTuXx
./<YOUR_GOOGLE_SDK_FOLDER>/bin/gcloud init  # EXAMPLE: ./home/me/google-cloud-sdk/bin/gcloud init