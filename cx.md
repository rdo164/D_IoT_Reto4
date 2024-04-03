 curl --silent -w "%{response_code}: %{errormsg}\n" \
  -XPOST "https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/buckets" \
  --header "Authorization: Token dkDgvTztFb0s95R2Hi_YdpxW6LIlo5_TkA7S9doiKtQhL9uvTTzmN_r6vV-MOt1CT40bbiEw8vq_c2khWm0IQg==" \
  --header "Content-type: application/json" \
  --data @- << EOF
  {
    "orgID": "f1237642dc0cea57",
    "name": "pop",
    "retentionRules": [
      {
        "type": "expire",
        "everySeconds": 86400
      }
    ]
  }
EOF

