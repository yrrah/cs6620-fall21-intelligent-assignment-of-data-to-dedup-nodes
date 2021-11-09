oc run scs6620-fall21-dedup-nodes-front-end-ex0 --overrides='
{
        "spec": {
            "containers": [{
                    "name": "cs6620-fall21-dedup-nodes-front-end-ex0",
                    "image": "image-registry.openshift-image-registry.svc:5000/cs6620-fall21-intelligentassignment-dedupnodes/cs6620-fall21-dedup-nodes-front-end",
                    "ports": [{ "containerPort": 50051 }],
                    "env": [{
                            "name": "SIMULATOR_MODE",
                            "value": "RUN"
                    },{
                            "name": "INPUT_DIR",
                            "value": "/var/input/"
                    },{
                            "name": "TRACES_WEBDIR",
                            "value": "https://tracer.filesystems.org/traces/"
                    },{
                            "name": "TRACES_SUBDIR",
                            "value": "fslhomes/2011-8kb-only/"
                    },{
                            "name": "TRACES_LIST",
                            "value": "/opt/app-root/src/src/traces/user006.txt"
                    },{
                            "name": "REGION_ALGO",
                            "value": "FIXED-SIZE"
                    },{
                            "name": "REGION_SIZE",
                            "value": "4"
                    },{
                            "name": "ROUTING",
                            "value": "SIMPLE"
                    },{
                            "name": "DOMAINS",
                            "value": "10"
                    },{
                            "name": "BACKEND_IPS",
                            "value": "'"$(oc get pods --selector app=cs6620-fall21-dedup-nodes-back-end-ex0 -o jsonpath='{range .items[:-1]}{.status.podIP}{","}{end}{.items[-1].status.podIP}')"'"
                    }],
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
'  --image=notused --restart=Never