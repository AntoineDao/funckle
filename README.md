# Functions + Speckle  = Funckle ❤️

This repository contains infrastructure as code for deploying a Speckle Functions Platform on Google Cloud Platform.

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [gcloud](https://cloud.google.com/sdk/docs/install)

## Folder Structure

```bash
├── k8s
│   ├── funckle-pipeline # Contains Tekton Pipeline configurations to build and deploy user's Speckle Functions
│   ├── knative # Contains Knative operator manifests which will be used to deploy user's Speckle Functions
│   └── tekton # Contains Tekton operator manifests which will be used to build and deploy user's Speckle Functions
├── terraform # Contains Terraform configurations to deploy the infrastructure required for the Speckle Functions Platform
├── samples
│   ├── functions # Contains sample Speckle Functions
```

## Additional Resources

### Docker Credentials Creation

We need to create a Kubernetes secret to allow the Knative build process to push/pull images from the Google Artifact Registry. We also need a similar secret to allow the Knative serving process to pull images from the Google Artifact Registry.

To create the secret for the Knative build process, run the following command:


```bash
kubectl create secret docker-registry regcred --docker-server=https://europe-west2-docker.pkg.dev --docker-username=_json_key_base64 --docker-password=<your-pword>
```

#### References
* [Google Auth source](https://cloud.google.com/artifact-registry/docs/docker/authentication#linux-macos)
* [Kubernetes secret source](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#:~:text=A%20Kubernetes%20cluster%20uses%20the,to%20pull%20a%20private%20image.&text=If%20you%20need%20more%20control,the%20Secret%20before%20storing%20it.)