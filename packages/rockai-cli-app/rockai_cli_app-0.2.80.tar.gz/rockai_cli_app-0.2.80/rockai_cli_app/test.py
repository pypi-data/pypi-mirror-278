import asyncio
from rockai_cli_app import Client

version = [{'torch_version':'2.3.0','linux':{}}]

# Run a image generation model using asyncio
async def main():
    # input = {"prompt": "a cartoon of a IRONMAN fighting with HULK, wall painting"}
    # client = Client(api_token="<API_TOKEN_HERE>")
    # result = await client.run_async(
    #     version="001bb81139b01780380407b4106ac681df46108e002eafbeb9ccb2d8faca42e1",
    #     input=input,
    # )
    # print("Result:", result)
    a = [
        {
            "pytorch_version": "v2.2.2",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "12.1",
                            "install_cmd": "pip install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cu121",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v2.2.1",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "12.1",
                            "install_cmd": "pip install torch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 --index-url https://download.pytorch.org/whl/cu121",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v2.2.0",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "12.1",
                            "install_cmd": "pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cu121",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v2.1.2",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "12.1",
                            "install_cmd": "pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu121",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v2.1.1",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "12.1",
                            "install_cmd": "pip install torch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 --index-url https://download.pytorch.org/whl/cu121",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v2.1.0",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "12.1",
                            "install_cmd": "pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v2.0.1",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "11.8",
                            "install_cmd": "pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v2.0.0",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "11.8",
                            "install_cmd": "pip install torch==2.0.0 torchvision==0.15.1 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cu118",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.13.1",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "11.7",
                            "install_cmd": "pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.13.0",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "11.7",
                            "install_cmd": "pip install torch==1.13.0+cu117 torchvision==0.14.0+cu117 torchaudio==0.13.0 --extra-index-url https://download.pytorch.org/whl/cu117",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.12.1",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "11.6",
                            "install_cmd": "pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu116",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.12.0",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "11.6",
                            "install_cmd": "pip install torch==1.12.0+cu116 torchvision==0.13.0+cu116 torchaudio==0.12.0 --extra-index-url https://download.pytorch.org/whl/cu116",
                        }
                    ]
                }
            },
        },
    ] + [
        {
            "pytorch_version": "v1.11.0",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "11.5",
                            "install_cmd": "pip install torch==1.11.0+cu115 torchvision==0.12.0+cu115 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu115",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.10.2",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "11.3",
                            "install_cmd": "pip install torch==1.10.2+cu113 torchvision==0.11.3+cu113 torchaudio==0.10.2 --extra-index-url https://download.pytorch.org/whl/cu113",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.10.1",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "11.3",
                            "install_cmd": "pip install torch==1.10.1+cu113 torchvision==0.11.2+cu113 torchaudio==0.10.1 --extra-index-url https://download.pytorch.org/whl/cu113",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.10.0",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "11.3",
                            "install_cmd": "pip install torch==1.10.0+cu113 torchvision==0.11.1+cu113 torchaudio==0.10.0 --extra-index-url https://download.pytorch.org/whl/cu113",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.9.1",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "11.1",
                            "install_cmd": "pip install torch==1.9.1+cu111 torchvision==0.10.1+cu111 torchaudio==0.9.1 --extra-index-url https://download.pytorch.org/whl/cu111",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.9.0",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "11.1",
                            "install_cmd": "pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 --extra-index-url https://download.pytorch.org/whl/cu111",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.8.2",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "11.1",
                            "install_cmd": "pip install torch==1.8.2+cu111 torchvision==0.9.2+cu111 torchaudio==0.8.2 --extra-index-url https://download.pytorch.org/whl/cu111",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.8.1",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "11.1",
                            "install_cmd": "pip install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio==0.8.1 --extra-index-url https://download.pytorch.org/whl/cu111",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.8.0",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "11.1",
                            "install_cmd": "pip install torch==1.8.0+cu111 torchvision==0.9.0+cu111 torchaudio==0.8.0 --extra-index-url https://download.pytorch.org/whl/cu111",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.7.1",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "11.0",
                            "install_cmd": "pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio==0.7.2 --extra-index-url https://download.pytorch.org/whl/cu110",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.7.0",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "11.0",
                            "install_cmd": "pip install torch==1.7.0+cu110 torchvision==0.8.1+cu110 torchaudio==0.7.0 --extra-index-url https://download.pytorch.org/whl/cu110",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.6.0",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "10.2",
                            "install_cmd": "pip install torch==1.6.0+cu102 torchvision==0.7.0+cu102 torchaudio==0.6.0 --extra-index-url https://download.pytorch.org/whl/cu102",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.5.1",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "10.2",
                            "install_cmd": "pip install torch==1.5.1+cu102 torchvision==0.6.1+cu102 torchaudio==0.5.1 --extra-index-url https://download.pytorch.org/whl/cu102",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.5.0",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "10.2",
                            "install_cmd": "pip install torch==1.5.0+cu102 torchvision==0.6.0+cu102 torchaudio==0.5.0 --extra-index-url https://download.pytorch.org/whl/cu102",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.4.0",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "10.1",
                            "install_cmd": "pip install torch==1.4.0+cu101 torchvision==0.5.0+cu101 torchaudio==0.4.0 --extra-index-url https://download.pytorch.org/whl/cu101",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.3.1",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "10.1",
                            "install_cmd": "pip install torch==1.3.1+cu101 torchvision==0.4.2+cu101 --extra-index-url https://download.pytorch.org/whl/cu101",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.3.0",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "10.1",
                            "install_cmd": "pip install torch==1.3.0+cu101 torchvision==0.4.1+cu101 --extra-index-url https://download.pytorch.org/whl/cu101",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.2.0",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "10.0",
                            "install_cmd": "pip install torch==1.2.0+cu100 torchvision==0.4.0+cu100 --extra-index-url https://download.pytorch.org/whl/cu100",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.1.0",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "10.0",
                            "install_cmd": "pip install torch==1.1.0+cu100 torchvision==0.3.0+cu100 --extra-index-url https://download.pytorch.org/whl/cu100",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.0.1",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "10.0",
                            "install_cmd": "pip install torch==1.0.1+cu100 torchvision==0.2.2+cu100 --extra-index-url https://download.pytorch.org/whl/cu100",
                        }
                    ]
                }
            },
        },
        {
            "pytorch_version": "v1.0.0",
            "Wheel": {
                "linux": {
                    "cuda_version": [
                        {
                            "cuda": "9.0",
                            "install_cmd": "pip install torch==1.0.0 torchvision==0.2.1 --extra-index-url https://download.pytorch.org/whl/cu90",
                        }
                    ]
                }
            },
        },
    ]


# Run the main function using asyncio.run
if __name__ == "__main__":
    asyncio.run(main())
