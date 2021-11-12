oc run scs6620-fall21-dedup-nodes-front-end-ex0 --overrides='
{
        "spec": {
            "containers": [{
                    "name": "cs6620-fall21-dedup-nodes-front-end-ex0",
                    "image": "image-registry.openshift-image-registry.svc:5000/cs6620-fall21-intelligentassignment-dedupnodes/cs6620-fall21-dedup-nodes-front-end",
                    "ports": [{ "containerPort": 50051 }],
                    "env": [{
                            "name": "SIMULATOR_RUN_NAME",
                            "value": "ex0"
                    },{
                            "name": "SIMULATOR_MODE",
                            "value": "RUN"
                    },{
                            "name": "SIMULATOR_TRACES_LISTS",
                            "value": "fslhomes_2011-8kb-only_018,fslhomes_2012-8kb-only_018,fslhomes_2012_018"
                    },{
                            "name": "SIMULATOR_REGION_ALGO",
                            "value": "FIXED-SIZE"
                    },{
                            "name": "SIMULATOR_REGION_SIZE",
                            "value": "4"
                    },{
                            "name": "SIMULATOR_ROUTING",
                            "value": "SIMPLE"
                    },{
                            "name": "SIMULATOR_DOMAINS",
                            "value": "100"
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