#! /bin/bash

kill_old_pods () {
  oc delete jobs cs6620-fall21-dedup-nodes-back-end-ex2
  oc delete pods cs6620-fall21-dedup-nodes-front-end-ex2
}

create_back_end () {
  echo '{
    "apiVersion": "batch/v1",
    "kind": "Job",
    "metadata": {
        "name": "cs6620-fall21-dedup-nodes-back-end-ex2",
        "namespace": "cs6620-fall21-intelligentassignment-dedupnodes"
    },
    "spec": {
        "parallelism": '"$num_pods"',
        "selector": {
            "app": "cs6620-fall21-dedup-nodes-back-end-ex2"
        },
        "template": {
            "metadata": {
                "labels": {
                    "app": "cs6620-fall21-dedup-nodes-back-end-ex2"
                }
            },
            "spec": {
                "automountServiceAccountToken": false,
                "containers": [
                    {
                        "env": [
                            {
                                "name": "SIMULATOR_MODE",
                                "value": "RUN"
                            }
                        ],
                        "resources": {
                            "limits": {
                                    "cpu": "500m",
                                    "memory": "1Gi"
                            },
                            "requests": {
                                    "cpu": "500m",
                                    "memory": "500Mi"
                            }
                        },
                        "image": "image-registry.openshift-image-registry.svc:5000/cs6620-fall21-intelligentassignment-dedupnodes/cs6620-fall21-dedup-nodes-back-end",
                        "name": "cs6620-fall21-dedup-nodes-back-end-ex2",
                        "ports": [
                            {
                                "containerPort": 50051
                            }
                        ]
                    }
                ],
                "restartPolicy": "Never"
            }
        }
    }
}' | oc create -f -
}

create_front_end () {
  oc run cs6620-fall21-dedup-nodes-front-end-ex2 --overrides='
  {
          "spec": {
              "containers": [{
                      "name": "cs6620-fall21-dedup-nodes-front-end-ex2",
                      "image": "image-registry.openshift-image-registry.svc:5000/cs6620-fall21-intelligentassignment-dedupnodes/cs6620-fall21-dedup-nodes-front-end",
                      "ports": [{ "containerPort": 50051 }],
                      "env": [{
                              "name": "SIMULATOR_RUN_NAME",
                              "value": "ex2-run'"$run_num"'"
                      },{
                              "name": "SIMULATOR_MODE",
                              "value": "RUN"
                      },{
                              "name": "SIMULATOR_TRACES_LISTS",
                              "value": "'"$dataset"'"
                      },{
                              "name": "SIMULATOR_REGION_ALGO",
                              "value": "'"$region_algo"'"
                      },{
                              "name": "SIMULATOR_REGION_SIZE",
                              "value": "'"$region_size"'"
                      },{
                              "name": "SIMULATOR_MIN_REGION_SIZE",
                              "value": "'"$min_region"'"
                      },{
                              "name": "SIMULATOR_MAX_REGION_SIZE",
                              "value": "'"$max_region"'"
                      },{
                              "name": "SIMULATOR_BIT_MASK",
                              "value": "'"$bitmask_size"'"
                      },
                      {
                                "name" : "SIMULATOR_MAIN_D",
                                "value" : "'"$main_d"'"
                      },
                      {
                                "name" : "SIMULATOR_SECOND_D",
                                "value" : "'"$second_d"'"
                      },
                      {
                              "name": "SIMULATOR_ROUTING",
                              "value": "'"$assign_algo"'"
                      },{
                              "name": "SIMULATOR_DOMAINS",
                              "value": "'"$dedup_domains"'"
                      },{
                              "name": "SIMULATOR_BACKEND_IPS",
                              "value": "'"$(oc get pods --selector app=cs6620-fall21-dedup-nodes-back-end-ex2 --field-selector status.phase=Running -o jsonpath='{range .items[:-1]}{.status.podIP}{","}{end}{.items[-1].status.podIP}')"'"
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
}

print_all_params () {
  echo "run_num: $run_num"
  echo "dedup_domains: $dedup_domains"
  echo "num_pods: $num_pods"
  echo "region_size: $region_size"
  echo "region_algo: $region_algo"
  echo "min_region: $min_region"
  echo "max_region: $max_region"
  echo "bitmask_size: $bitmask_size"
  echo "assign_algo: $assign_algo"
  echo "dataset: $dataset"
  echo "results_file: $results_file"
  echo "main_d : $main_d"
  echo "second_d : $second_d"
  echo ""

}

exec < run_combinations.tsv
for i in {1..27}; do read skip_these_lines; done;
while IFS=$'\t' read -r run_num dedup_domains num_pods region_algo region_size min_region max_region main_d second_d bitmask_size assign_algo dataset results_file
do
  kill_old_pods
  create_back_end
  sleep 5

  while [[ $(oc get pods --field-selector status.phase=Running) == *Terminating* ]]
  do
    echo "Waiting 5s for terminating pods..."
    sleep 5
  done

  while [[ $(oc get pods --field-selector status.phase=Running) != *Running* ]]
  do
    echo "Waiting 5s for back_end to start..."
    sleep 5
  done

  create_front_end
  sleep 5

  print_all_params

  while [[ $(oc get pods --field-selector metadata.name=cs6620-fall21-dedup-nodes-front-end-ex2) != *Completed* ]]
  do
    echo "Waiting 60s for front_end to finish..."
    sleep 60
  done

  ## stop early
  if [ "$run_num" -eq 136 ]; then
    break
  fi
done