#!/bin/bash
subs_pod=$(kubectl get pods -A | grep subscri | awk '{print $2}')
kubectl exec -it -n pmn $subs_pod -- bash
