# Craft Bridges for Claude

Community **Claude Code plugins** that connect Claude to the open-source **Craft apps** by Storytold installed on your
computer, on Windows, macOS and Linux. Each plugin adds a local MCP server whose tools create, edit, convert and preview
files with the app's own engine: page layouts, motion graphics, photos, vector art, video, PDFs, documents, music,
presentations and spreadsheets. Everything runs locally; nothing is sent anywhere.

| Plugin | What it does |
| --- | --- |
| [DesignCraft Bridge](plugins/designcraft-bridge) | Page layout, data merge, InDesign IDML, print-ready PDF/X, PNG, EPUB and HTML |
| [EffectCraft Bridge](plugins/effectcraft-bridge) | Motion graphics, animated titles, effects on videos, templates; MP4, ProRes, WebM, GIF, Lottie |
| [LightCraft Bridge](plugins/lightcraft-bridge) | Raw development: auto tone, sliders, presets, masks, HDR and panoramas; JPEG, TIFF, WebP, AVIF, DNG |
| [PhotoCraft Bridge](plugins/photocraft-bridge) | Photo editing: resize, crop, adjustments, filters, background removal, text and designs |
| [VectorCraft Bridge](plugins/vectorcraft-bridge) | Vector art: image trace, designs from shapes, text and charts, recolor; SVG, PDF, AI, EPS, DXF |
| [FilmCraft Bridge](plugins/filmcraft-bridge) | Video editing: split, trim, effects, color looks, titles, speed, join with transitions |
| [PdfCraft Bridge](plugins/pdfcraft-bridge) | PDF work: merge, split, pages, OCR, forms, signatures, redaction, passwords, conversion |
| [WordCraft Bridge](plugins/wordcraft-bridge) | Documents: headings, lists, tables, images, table of contents, tracked changes, mail merge |
| [SoundCraft Bridge](plugins/soundcraft-bridge) | Music and audio: multitrack songs, synth and drum notes, effects, mixdowns with LUFS, stems, MIDI |
| [DeckCraft Bridge](plugins/deckcraft-bridge) | Presentations: slides with bullets, pictures, charts, tables, notes, themes; PowerPoint pptx and PDF |
| [GridCraft Bridge](plugins/gridcraft-bridge) | Spreadsheets: live formulas, tables, conditional formatting, charts and PivotTables; xlsx, csv, PDF |

## Install in Claude Code

```
/plugin marketplace add jhonsu01/sunsam-plugins
/plugin install wordcraft-bridge@sunsam-plugins
```

Each plugin needs its Craft app (with its `-cli` engine) and Node.js 20 or later on `PATH`. See the plugin's README.

## How the plugins are built

`scripts/build.py` downloads each connector's released `.mcpb` from its own repository, checks its SHA-256 against
the [Sunsam Code marketplace](https://github.com/jhonsu01/marketplace-SunsamCode), and writes the plugin folder:
`.claude-plugin/plugin.json`, the readable server bundle `dist/bundle.cjs`, the README, the license, the icon and a
screenshot (`screenshots/`). The source code, tests and changelog of every server are in its repository, linked from
each plugin's README. The same servers are also published as Claude Desktop extensions (`.mcpb`), for Codex and
DeepSeek Harness ([craft-marketplace](https://github.com/jhonsu01/craft-marketplace)) and for Sunsam Code.

## Privacy

The plugins run only on your computer, make no network requests and store nothing. See [PRIVACY.md](PRIVACY.md).

## License

Apache-2.0 (see each plugin's LICENSE). The Craft apps are © Storytold (MIT or Apache-2.0). These plugins are a
community project by Jhon Supelano and are not affiliated with or endorsed by Storytold or Anthropic.
