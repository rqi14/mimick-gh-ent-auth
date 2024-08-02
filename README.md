# mimick-github-enterprise-auth
模拟一下github enterprise的登录方式，没有什么其他用

If you don't have an account but want to use copilot and override. This is the way to go.

The only dependency is flask

call `python main.py` to run. 
It listens to localhost:5201

These two lines need to be appended to hosts

`127.0.0.1 api.localhost`

`127.0.0.1 copilot-telemetry-service.localhost`
