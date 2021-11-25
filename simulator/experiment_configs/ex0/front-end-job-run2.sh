oc run cs6620-fall21-dedup-nodes-front-end-ex0 --overrides='
{
        "spec": {
            "containers": [{
                    "name": "cs6620-fall21-dedup-nodes-front-end-ex0",
                    "image": "image-registry.openshift-image-registry.svc:5000/cs6620-fall21-intelligentassignment-dedupnodes/cs6620-fall21-dedup-nodes-front-end",
                    "ports": [{ "containerPort": 50051 }],
                    "env": [{
                            "name": "SIMULATOR_RUN_NAME",
                            "value": "ex0-run2"
                    },{
                            "name": "SIMULATOR_MODE",
                            "value": "RUN"
                    },{
                            "name": "SIMULATOR_TRACES_LISTS",
                            "value": "fslhomes_2011-8kb-only_018,fslhomes_2012-8kb-only_018"
                    },{
                            "name": "SIMULATOR_REGION_ALGO",
                            "value": "FIXED-SIZE"
                    },{
                            "name": "SIMULATOR_REGION_SIZE",
                            "value": "8"
                    },{
                            "name": "SIMULATOR_ROUTING",
                            "value": "FIRST_FINGERPRINT_7"
                    },{
                            "name": "SIMULATOR_DOMAINS",
                            "value": "1"
                    },{
                            "name": "SIMULATOR_BACKEND_IPS",
                            "value": "'"$(oc get pods --selector app=cs6620-fall21-dedup-nodes-back-end-ex0 -o jsonpath='{range .items[:-1]}{.status.podIP}{","}{end}{.items[-1].status.podIP}')"'"
                    }],
                    "volumeMounts": [{
                        "mountPath": "/var/input",
                        "name": "input-traces"
                    },{
                        "mountPath": "/var/output",
                        "name": "output-logs"
                    }]
            }],
            "volumes": [{
                    "name": "input-traces",
                    "persistentVolumeClaim": {
                        "claimName": "input-trace-files"
                    }
            },{
                    "name": "output-logs",
                    "persistentVolumeClaim": {
                        "claimName": "output-log-files"
                    }
            }]
        }
}
'  --image=notused --restart=Never