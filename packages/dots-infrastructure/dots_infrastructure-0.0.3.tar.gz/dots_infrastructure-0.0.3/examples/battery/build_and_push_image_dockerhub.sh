VERSION=0.0.1
REPOSITORY="dotsenergyframework/helics-example-battery"

docker build -t ${REPOSITORY}:${VERSION} .

docker push ${REPOSITORY}:${VERSION}
