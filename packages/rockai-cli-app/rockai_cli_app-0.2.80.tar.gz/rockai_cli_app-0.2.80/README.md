# Setup

Python SDK for inference and training for RockAI

```shell
# Install package using pip
pip install rockai-cli-app
```

```python
from rockai_cli_app import Client
import asyncio

my_client = Client()


# Function to run the asynchronous function and print the result
async def main():
    
    result = await my_client.run_async(
        version="001bb81139b01780380407b4106ac681df46108e002eafbeb9ccb2d8faca42e1",
        input={
            "width": 1024,
            "height": 1024,
            "prompt": "a cartoon of a IRONMAN fighting with HULK, wall painting",
            "guidance_scale": 3,
            "negative_prompt": "(deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation, NSFW",
            "num_inference_steps": 15,
        }
    )
    print("Result:", result)


# Run the main function using asyncio.run
if __name__ == "__main__":
    asyncio.run(main())
```

```shell
# clean docker space
docker system prune --all --force --volumes
```

# Development
* Python version 3.9.19