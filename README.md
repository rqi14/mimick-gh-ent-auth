# mimick-gh-ent-auth
This repo hosts a script to mock the authentication of `GH enterprise` for `copilot`.
[`override`](https://github.com/linux-do/override) is a software that acts as a custom backend for `copilot` plugin and allows to use any LLM with the `copilot` plugin. 
However, it does not handle the authentication part of `copilot`.
Instead, it requires the user to set `copilot` to `GH enterprise` authentication.
A service providing `GH enterprise` like authentication is hosted by the author and it requires an account for a online discussion forum.
Unfortunately, the registration is not available.
If you don't have an account but want to use `copilot` and `override`. This is the way to go.
This repo mocks the `GH enterprise` authentication and correctly handles `copilot`'s requests.
It can be used to "login" without the need for setting up `GH enterprise` or having an account in the forementioned forum.
It does not ask the user to register anything.
Instead, it tells `copilot` the information of a mock user defined in the script. 
It is designed to host locally on PC instead of providing authentication for multiple users.

The only dependency is flask.
For your reference, the code was made with `python==3.11.6` and `flask==3.0.3`

call `python main.py` to run. 
It listens to localhost:5201

These two lines need to be appended to hosts. This is becaues `copilot` believes api.<your_url> and copilot-telemetry-service.<your_url> are api endpoints, <prefix>.localhost is not available by default.

`127.0.0.1 api.localhost`

`127.0.0.1 copilot-telemetry-service.localhost`
