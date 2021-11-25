oc delete jobs cs6620-fall21-dedup-nodes-back-end-ex0 ;
oc delete pods cs6620-fall21-dedup-nodes-front-end-ex0 ;
oc create -f back-end-job.yaml ;
