# run 1 front_end
oc run cs6620-fall21-dedup-nodes-front-end \
--image=image-registry.openshift-image-registry.svc:5000/cs6620-fall21-intelligentassignment-dedupnodes/cs6620-fall21-dedup-nodes-front-end \
--restart=Never \
--port=50051 \
--env="SERVER_IP=$(oc get pods --selector app=cs6620-fall21-dedup-nodes-back-end -o jsonpath='{.items[0].status.podIP}')" \
--env="SIMULATOR_MODE=DEMO"

# run parallel front_end
oc run cs6620-fall21-dedup-nodes-front-end \
--image=image-registry.openshift-image-registry.svc:5000/cs6620-fall21-intelligentassignment-dedupnodes/cs6620-fall21-dedup-nodes-front-end \
--restart=Never \
--port=50051 \
--env="BACKEND_IPS=$(oc get pods --selector app=cs6620-fall21-dedup-nodes-back-end \
-o jsonpath='{range .items[:-1]}{.status.podIP}{","}{end}{.items[-1].status.podIP}') " \
--env="SIMULATOR_MODE=DEMO"

# run with mounted volume
oc run scs6620-fall21-dedup-nodes-front-end --overrides='
{
        "spec": {
            "containers": [{
                    "name": "cs6620-fall21-dedup-nodes-front-end",
                    "image": "image-registry.openshift-image-registry.svc:5000/cs6620-fall21-intelligentassignment-dedupnodes/cs6620-fall21-dedup-nodes-front-end",
                    "volumeMounts": [{
                        "mountPath": "/var/input",
                        "name": "input-traces"
                    }]
            }],
            "volumes": [{
                    "name": "input-traces",
                    "persistentVolumeClaim": {
                        "claimName": "input-trace-files"
                    }
            }]
        }
}
'  --image=notused --restart=Never --port=50051 \
--env="SERVER_IP=$(oc get pods --selector app=cs6620-fall21-dedup-nodes-back-end -o jsonpath='{.items[0].status.podIP}')" \
--env="SIMULATOR_MODE=DEMO"