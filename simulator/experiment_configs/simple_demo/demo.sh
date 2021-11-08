# run 1 front_end
oc run cs6620-fall21-dedup-nodes-front-end \
--image=image-registry.openshift-image-registry.svc:5000/cs6620-fall21-intelligentassignment-dedupnodes/cs6620-fall21-dedup-nodes-front-end \
--restart=Never \
--port=50051 \
--env="SERVER_IP=$(oc get pods --selector app=cs6620-fall21-dedup-nodes-back-end -o jsonpath='{.items[0].status.podIP}')" \
--env="SIMULATOR_MODE=DEMO"
