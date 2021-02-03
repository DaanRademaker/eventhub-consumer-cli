import click
import asyncio
from azure.eventhub.aio import EventHubConsumerClient


async def on_event(partition_context, event):
    """callback function for incoming eventhub event"""

    # Print the event data.
    click.echo(f"{event.body_as_str(encoding='UTF-8')}")


class Consumer:
    """
    An eventhub consumer
    """
    def __init__(self, connection_string, name, consumer):
        self.name = name
        self.connection_string = connection_string
        self.client = EventHubConsumerClient.from_connection_string(
            self.connection_string, consumer_group=consumer, eventhub_name=self.name
        )

    async def main(self):
        """
        the main asynchronious function
        """
        async with self.client:
            # Call the receive method. Read from the beginning of the partition (starting_position: "-1")
            await self.client.receive(on_event=on_event, starting_position="-1")

    def start(self):
        """
        start the async function loop forever
        """
        loop = asyncio.get_event_loop()
        # Run the main method.
        loop.run_until_complete(self.main())


@click.command()
@click.option(
    "--connection_string",
    default=None,
    help="this is the connection string with read permissions to the eventhub",
)
@click.option("--name", default=None, help="this is the name of the eventhub")
@click.option(
    "--consumer",
    default="$Default",
    help="this is the name of the consumergroup you want to use",
)
def cli(connection_string, name, consumer):
    """
    this script consumes an eventhub and prints body to console
    """

    Consumer(connection_string, name, consumer).start()