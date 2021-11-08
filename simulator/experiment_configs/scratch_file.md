# how we might do it if we use deployments

# set number of backend pods
`oc scale dc cs6620-fall21-dedup-nodes-back-end --replicas=10`

# check status of back_end pods
`oc get pods --selector app=cs6620-fall21-dedup-nodes-back-end -o wide`

# get back_end IPs and set them as env variable of front_end
`oc set env rc/cs6620-fall21-dedup-nodes-front-end-1 --overwrite \
BACKEND_IPS=$(oc get pods --selector app=cs6620-fall21-dedup-nodes-back-end \
-o jsonpath='{range .items[:-1]}{.status.podIP}{","}{end}{.items[-1].status.podIP}') \
;oc set env rc/cs6620-fall21-dedup-nodes-front-end-1 --list`

# set experiment parameters
`oc set env rc/cs6620-fall21-dedup-nodes-front-end-1 --overwrite \
REGION_FORMATION=FIXED \
REGION_SIZE=4 \
ROUTING=SIMPLE \
SIMULATOR_MODE=RUN \
;oc set env rc/cs6620-fall21-dedup-nodes-front-end-1 --list`

# start front_end
`oc scale dc cs6620-fall21-dedup-nodes-front-end --replicas=1 \
;oc get pods --selector app=cs6620-fall21-dedup-nodes-front-end -o wide`
