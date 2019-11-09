#! /bin/bash
set -e
COMMIT_SHA1=$CIRCLE_SHA1

eval $(printenv | awk -F= '{ print "export " $1 }')
export COMMIT_SHA1=$COMMIT_SHA1

# since the only way for envsubst to work on files is using input/output redirection,
#  it's not possible to do in-place substitution, so we need to save the output to another file
#  and overwrite the original with that one.
# "beat" "flower"
declare -a arr=("django" "worker")
for pod in "${arr[@]}"
do

    if [[ -f ./deploy/kube/${pod}/configmap.yaml ]]; then
        envsubst <./deploy/kube/${pod}/configmap.yaml >./deploy/kube/${pod}/configmap.yaml.out
        mv ./deploy/kube/${pod}/configmap.yaml.out ./deploy/kube/${pod}/configmap.yaml
    fi

    envsubst <./deploy/kube/${pod}/deployment.yaml >./deploy/kube/${pod}/deployment.yaml.out
    mv ./deploy/kube/${pod}/deployment.yaml.out ./deploy/kube/${pod}/deployment.yaml

    # envsubst <./kube/django/job-migration.yaml >./kube/django/job-migration.yaml.out
    # mv ./kube/django/job-migration.yaml.out ./kube/django/job-migration.yaml

    echo "$KUBERNETES_CLUSTER_CERTIFICATE" | base64 --decode > cert.crt

    ./kubectl \
      --kubeconfig=/dev/null \
      --server=$KUBERNETES_SERVER \
      --certificate-authority=cert.crt \
      --token=$KUBERNETES_TOKEN \
      apply -f ./deploy/kube/${pod}/
done