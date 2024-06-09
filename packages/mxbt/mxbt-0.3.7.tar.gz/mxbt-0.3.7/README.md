# mxbt 

Yet another Matrix bot library, built on [matrix-nio](https://github.com/matrix-nio/matrix-nio).

## Feauters

- [x] Simple and powerfull bots creating
- [ ] Custom emojis support
    - [x] Getting
    - [x] Sending
    - [ ] Creating
- [x] Files sending (external & internal)
- [x] Native mentions
- [x] Access to `matrix-nio` features
- [x] Event filters
- [x] Bot modules support
- [ ] Wait for event system
- [x] E2EE support (check [docs](docs/encryption.md) before)

## Installation

**With pip:**

```sh
$ pip install mxbt
```

**With git and python:**

```sh
$ git clone https://codeberg.org/librehub/mxbt
$ cd mxbt
$ python -m pip install . 
```

## Getting started

More examples [here](examples/) or in [docs](https://librehub.codeberg.page/mxbt/).

```python
from mxbt import Bot, Context, Creds, Config, Filter, Listener
import asyncio

bot = Bot(
    creds=Creds.from_env(               # You also can use Creds.from_json and just Creds() 
        homeserver="MATRIX_HOMESERVER",
        username="MATRIX_USERNAME",
        password="MATRIX_PASSWORD"
    ),                               
    config=Config()                     # Config has many options for bot, like prefix, selfbot, encryption, etc...
)
lr = Listener(bot)

@lr.on_command(prefix="?", aliases=["test", "t"])
async def ctx_echo(ctx: Context) -> None:       # Context object contains main info about event
    await ctx.reply(ctx.body)                   # Reply message to event room

if __name__ == "__main__":
    asyncio.run(lr.start_polling())
```

**.env** structure
```env
MATRIX_HOMESERVER=https://matrix.org/
MATRIX_USERNAME=user
MATRIX_PASSWORD=password
```

## Built with mxbt

| Project                                               | Description                       | Project                                           | Description                           |
| :---                                                  | :---                              | :---                                              | :---                                  |
| [sofie](https://codeberg.org/librehub/sofie)          | A simple selfbot                  | [charon](https://codeberg.org/librehub/charon)    | Simple bridge between some messengers |
| [cryptomx](https://codeberg.org/librehub/cryptomx)    | A crytpocurrency notification bot | [taskmx](https://codeberg.org/librehub/taskmx)    | Simple project tasks bot              |

## Special thanks

* [matrix.org](https://matrix.org) for beautiful protocol.
* [simplematrixbotlib](https://codeberg.org/imbev/simplematrixbotlib) for base parts of API, Listener and Callbacks code ideas. 
Code from simplematrixbotlib is included under the terms of the MIT license - Copyright (c) 2021-2024 Isaac Beverly
* [matrix-nio](https://github.com/poljar/matrix-nio) for cool client library.

## Support

Any contacts and crytpocurrency wallets you can find on my [profile page](https://warlock.codeberg.page).


