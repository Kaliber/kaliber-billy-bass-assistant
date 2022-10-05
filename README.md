# Billy Bassistant
Follow the setup: [Embed the Google Assistant](https://developers.google.com/assistant/sdk/guides/service/python)

## Credentials
`billy` / `KaliberBilly3513`

*Login via SSH:*

`ssh billy@10.211.200.43` (hostname: billy)

### .asoundrc config
```bash
pcm.!default {
  type asym
  capture.pcm "mic"
  playback.pcm "speaker"
}
pcm.mic {
  type plug
  slave {
    pcm "hw:1,0"
  }
}
pcm.speaker {
  type plug
  slave {
    pcm "hw:0,0"
  }
}
```

### Google Developer Project

Use the `kalibervoice@gmail.com` account for this (see LastPass for credentials)

> https://console.actions.google.com/project/kaliber-billy-bassistant-prd/deviceregistration/

Python installation not in the environment, but in root. When using the oauth tool, use the following command:
> /home/billy/.local/bin/google-oauthlib-tool --scope https://www.googleapis.com/auth/assistant-sdk-prototype \
      --save --headless --client-secrets /home/billy/client_secret_<id>.json
