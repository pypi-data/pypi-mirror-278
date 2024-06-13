# GCP Asyncio PubSub RPC Client

Google Cloud PubSub RPC Client is a lightweight Python package
designed for managing and orchestrating job submissions across
asynchronous environments using Google Cloud Pub/Sub. This package
facilitates seamless integration of job queues, providing tools to
submit jobs, and handle their responses
efficiently. With built-in support for Prometheus metrics, it allows
users to monitor job submission rates, success rates, processing
times, and more, ensuring optimal performance and reliability. Whether
you're handling sporadic tasks or managing continuous streams of jobs,
PubSub RPC Client ensures that your job processing is scalable,
efficient, and fully monitored.

## Getting Started

Go to the examples folder to see how to quickly get a sample client
and server up and running.

### Creating Google Cloud Pub/Sub Topics Using `gcloud`

To create the Pub/Sub topics `job-topic` and `response-topic` from
your command line, follow these steps:

**Create `job-topic` and `response-topic`**:

Run the following command to create the `job-topic`:

``` sh
gcloud pubsub topics create job-topic
gcloud pubsub topics create response-topic
```

These commands will create the specified topics in your Google Cloud
project, allowing you to publish and subscribe to messages.

### Running examples

After creating topics, install the dependencies with `poetry install`.
The `project-name` is the GCP project where your topics are defined.

**Running a client**:

To run the client (streaming or non-streaming):

``` sh
# Streaming client
poetry run python examples/stream_client.py project-name response-topic job-topic

# Non-streaming client
poetry run python examples/client.py project-name response-topic job-topic
```

**Running the server**:

To run the server:

``` sh
poetry run python examples/stream_server.py project-name job-topic response-topic
```

The server supports both streaming and non-streaming results out of
the box. To extend the server, subclass `PubSubRPCServer` and provide
definitions for `process_stream_message` and `process_message`.

The server will handle terminating the stream and routing the messages
back to the client.
