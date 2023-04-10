# Robot-Arm

## Folder Import Follow Designed Architecture
- web-ui (include 3rd party server of openapi)
- pi-server (arm controller and pi camera server)

## SETTING UP
```
// Frontend and GPT
cd web-ui
yarn install
// ADD OPENAPI KEY
```

```
// PI SERVER and Camera
cd pi-server
bash install.sh
```

## START DEV
start web ui
```
cd web-ui
yarn dev
```

and start camera server and arm controller server

```
cd pi-server
bash start.sh
```
