# SorareAsyncWebsocket
Created following the example given in the official Sorare API docs, but implemented in a async way. Creating a websocket connection is needed in the case of a **subscription query**. This is not useful for a simple query.

## Usage example
```
import asyncio

sorare_ws = SorareAsyncWebsocket()

# Your graphql query
query = """subscription onAnyCardUpdated { 
              aCardWasUpdated { 
                id
                slug 
                onSale
                name
                pictureUrl 
			  }
			}
		"""

# Start the websocket as a task
asyncio.create_task(sorare_ws.connectWS(query))
```