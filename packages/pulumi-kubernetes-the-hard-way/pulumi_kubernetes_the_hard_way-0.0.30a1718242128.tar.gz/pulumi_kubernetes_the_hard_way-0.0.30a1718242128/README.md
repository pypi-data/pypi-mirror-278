# Pulumi Kubernetes the Hard Way

This is a Pulumi implementation of Kelsey Hightower's [Kubernetes the Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way). It attempts to provide a set of building blocks to build a kubernetes cluster from scratch.

## Development

Note that the generated provider plugin (`pulumi-resource-kubernetes-the-hard-way`) must be on your `PATH` to be used by Pulumi deployments.

## Prerequisites

- Go 1.21
- Pulumi CLI
- Node.js (to build the Node.js SDK)
- Yarn (to build the Node.js SDK)
- Python 3.6+ (to build the Python SDK)
- .NET Core SDK (to build the .NET SDK)
- Gradle (to build the Java SDK)

## Build and Test

```bash
# Build and install the provider (plugin copied to ./bin)
make install_provider

# Regenerate schema, schema-types, and SDKs
make generate

# Test Node.js SDK
$ make install_nodejs_sdk
$ cd examples/simple-ts
$ yarn install
$ yarn link @unmango/pulumi-kubernetes-the-hard-way
$ pulumi stack init test
$ pulumi up
```

## Naming

The `kubernetes-the-hard-way` provider's plugin binary must be named `pulumi-resource-kubernetes-the-hard-way` (in the format `pulumi-resource-<provider>`).
