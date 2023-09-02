IMAGE_VERSION=0.2.5

docker:
	docker buildx build --platform linux/amd64 --load -t europe-west2-docker.pkg.dev/hack-space-dev/funckle-user-functions/funckle:$(IMAGE_VERSION) .
	docker push europe-west2-docker.pkg.dev/hack-space-dev/funckle-user-functions/funckle:$(IMAGE_VERSION)


kustomize: docker
	cd k8s/funckle && kustomize edit set image europe-west2-docker.pkg.dev/hack-space-dev/funckle-user-functions/funckle:$(IMAGE_VERSION)
	kubectl apply -k k8s/funckle