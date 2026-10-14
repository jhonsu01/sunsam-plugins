# Privacy policy

Applies to every plugin in this repository (the Craft Bridges: DesignCraft, EffectCraft, LightCraft, PhotoCraft,
VectorCraft, FilmCraft, PdfCraft, WordCraft, SoundCraft, DeckCraft and GridCraft Bridge). Last updated 2026-10-14.

## What the plugins do with your data

- Each plugin starts a local MCP server on your own computer. The server runs the open-source Craft app you installed
  (its command-line engine) to read the files you name and to write the files you ask for.
- **Nothing leaves your computer.** The servers make no network requests, send no telemetry or analytics, and contact
  no service run by the author or anyone else.
- **Nothing is stored.** The servers keep no logs, databases or caches of your files or conversations. Each job runs in
  a temporary folder that is deleted when the job ends. Files you ask to create are written where you choose and stay
  under your control.
- **No personal data is collected.** The plugins only see the file paths and settings you give them. Their settings
  (an install folder, an executable path, a port number) are stored by Claude in your own settings.
- The only network socket is optional and local: when you ask a plugin to open a Craft app with its control channel,
  that app listens on `127.0.0.1` (your own machine) so the plugin can drive it.

## Third parties

The Craft apps are open-source projects by Storytold, installed and run by you; their own privacy terms apply to them.
Claude, the app you use the plugins from, is provided by Anthropic under its own terms and privacy policy.

## Children

The plugins are general-purpose productivity tools and are not directed at children under 18.

## Contact

Questions or concerns: open an issue at https://github.com/jhonsu01/sunsam-plugins/issues.
