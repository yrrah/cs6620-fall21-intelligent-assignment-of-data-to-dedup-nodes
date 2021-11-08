# run front_end with multiple backends and mounted volume
oc run scs6620-fall21-dedup-nodes-front-end-ex0 --overrides='
{
        "spec": {
            "containers": [{
                    "name": "cs6620-fall21-dedup-nodes-front-end-ex0",
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
--env="SIMULATOR_MODE=RUN" \
--env="INPUT_DIR=/var/input/" \
--env="TRACES_WEBDIR=https://tracer.filesystems.org/traces/" \
--env="TRACES_SUBDIR=fslhomes/2011-8kb-only/" \
--env="TRACES_LIST=/opt/app-root/src/src/traces/user006.txt" \
--env="BACKEND_IPS=$(oc get pods --selector app=cs6620-fall21-dedup-nodes-back-end-ex0 \
-o jsonpath='{range .items[:-1]}{.status.podIP}{","}{end}{.items[-1].status.podIP}') " \
