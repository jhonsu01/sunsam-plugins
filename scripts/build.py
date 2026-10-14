"""Build the Claude Code plugin folders of the Craft Bridges from their published releases.

For every Craft connector listed in the Sunsam Code marketplace (marketplace.json), this script downloads the
released .mcpb, checks its SHA-256 against the marketplace, and writes plugins/<app>-bridge/ with:
  .claude-plugin/plugin.json   name, metadata, userConfig and the local MCP server (node dist/bundle.cjs)
  dist/bundle.cjs              the connector, exactly as released (readable, not minified)
  README.md, LICENSE, assets/icon.png (and assets/screenshot.png when present in screenshots/)
and the root .claude-plugin/marketplace.json, so the repository is also a Claude Code marketplace.

Usage: python scripts/build.py            (re-run after any connector release)
"""
import hashlib, io, json, os, re, shutil, sys, urllib.request, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKETPLACE = 'https://raw.githubusercontent.com/jhonsu01/marketplace-SunsamCode/main/marketplace.json'
REPO = 'https://github.com/jhonsu01/sunsam-plugins'
CRAFT = ['designcraft', 'effectcraft', 'lightcraft', 'photocraft', 'vectorcraft', 'filmcraft', 'pdfcraft', 'wordcraft', 'soundcraft', 'deckcraft', 'gridcraft']
USER_CONFIG_KEYS = {'type', 'title', 'description', 'required', 'default', 'sensitive', 'min', 'max'}


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'sunsam-plugins-build'})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


def readme(app, m, c, has_shot):
    App = m['display_name'].replace(' Bridge', '')
    env = m['server']['mcp_config'].get('env', {})
    tools = '\n'.join(f"| `{t['name']}` | {t['description']} |" for t in m.get('tools', []))
    config = '\n'.join(f"| `{k}` | {v['title']} | {v['description']} |" for k, v in m.get('user_config', {}).items())
    long = m['long_description'].split('\n\nThe connector drives')[0]
    shot = f"\n![{App} Bridge: example result](assets/screenshot.png)\n" if has_shot else ''
    return f"""# {m['display_name']}

{m['description']}
{shot}
{long}

## Requirements

- **{App}** installed on Windows, macOS or Linux, with its command-line engine `{app}-cli` ([{App} releases](https://github.com/storytold/{app}/releases); on macOS also the separate `{app}-cli` zip). The plugin finds it in the standard install folders or on `PATH`; otherwise set its folder in the plugin settings.
- **Node.js 20 or later** on `PATH` (the plugin's MCP server runs with `node`).
- Claude Code or another Claude app that runs local MCP servers from plugins.

## Tools

| Tool | What it does |
| --- | --- |
{tools}

## Settings

All settings are optional; leave them empty to auto-detect.

| Setting | Title | Meaning |
| --- | --- | --- |
{config}

## What this plugin runs, reads and sends

- It starts one **local MCP server**: `node ${{CLAUDE_PLUGIN_ROOT}}/dist/bundle.cjs`. `dist/bundle.cjs` is the readable, unminified build of [{c['repository'].split('github.com/')[1]}]({c['repository']}) version {m['version']} (source code, tests and changelog are in that repository).
- The server runs the **{App} engine installed on your computer** (`{app}-cli`) as a child process, one private engine per job in a temporary folder that is deleted afterwards. Only with `open_in_{app}` does it start the {App} desktop app; with `control=true` that app listens on a loopback-only port on your own machine (`127.0.0.1`).
- It **reads only the files you name** (absolute paths) and **writes new files only where you ask**, never overwriting an existing file unless you set `overwrite: true`.
- It makes **no network requests**, sends no telemetry and stores no data. Its environment variables are only the settings above ({', '.join(f'`{k}`' for k in env)}).
- It installs nothing and runs no package manager: everything it needs is in this folder.

## Install

In Claude Code:

```
/plugin marketplace add jhonsu01/sunsam-plugins
/plugin install {app}-bridge@sunsam-plugins
```

The same connector is also available as a Claude Desktop extension (`.mcpb`), for Codex and DeepSeek Harness, and in the Sunsam Code marketplace: see [{c['repository'].split('github.com/')[1]}]({c['repository']}).

## Support

Issues and questions: [{c['repository']}/issues]({c['repository']}/issues). Privacy: [PRIVACY.md]({REPO}/blob/main/PRIVACY.md).

## License

{m['license']}. {App} is an open-source project by Storytold (MIT or Apache-2.0). This plugin is a community project by {m['author']['name']}; it is not affiliated with or endorsed by {App}, Storytold or Anthropic.
"""


def main():
    market = json.loads(fetch(MARKETPLACE))
    conns = {c['name'].replace('-mcp-server', ''): c for c in market['connectors']}
    entries = []
    for app in CRAFT:
        c = conns[app]
        blob = fetch(c['mcpb']['url'])
        digest = hashlib.sha256(blob).hexdigest()
        if digest != c['mcpb']['sha256']:
            sys.exit(f'{app}: SHA-256 mismatch ({digest} != {c["mcpb"]["sha256"]})')
        z = zipfile.ZipFile(io.BytesIO(blob))
        m = json.loads(z.read('manifest.json'))
        name = f'{app}-bridge'
        out = os.path.join(ROOT, 'plugins', name)
        shutil.rmtree(out, ignore_errors=True)
        os.makedirs(os.path.join(out, '.claude-plugin'))
        os.makedirs(os.path.join(out, 'dist'))
        os.makedirs(os.path.join(out, 'assets'))
        open(os.path.join(out, 'dist', 'bundle.cjs'), 'wb').write(z.read('dist/bundle.cjs'))
        open(os.path.join(out, 'LICENSE'), 'wb').write(z.read('LICENSE'))
        open(os.path.join(out, 'assets', 'icon.png'), 'wb').write(z.read('icon.png'))
        shot = os.path.join(ROOT, 'screenshots', f'{app}.png')
        has_shot = os.path.exists(shot)
        if has_shot:
            shutil.copyfile(shot, os.path.join(out, 'assets', 'screenshot.png'))
        server = app
        env = {k: re.sub(r'\$\{user_config\.(\w+)\}', r'${user_config.\1}', v) for k, v in m['server']['mcp_config'].get('env', {}).items()}
        plugin = {
            'name': name,
            'displayName': m['display_name'],
            'version': m['version'],
            'description': m['description'],
            'author': {'name': m['author']['name'], 'url': m['author'].get('url', 'https://github.com/jhonsu01')},
            'homepage': c['repository'],
            'repository': REPO,
            'license': m['license'],
            'keywords': [k for k in m.get('keywords', []) if re.fullmatch(r'[a-z0-9-]+', k)][:12],
            'icon': './assets/icon.png',
            'documentationUrl': c['repository'] + '#readme',
            'supportUrl': c['repository'] + '/issues',
            'privacyPolicyUrl': REPO + '/blob/main/PRIVACY.md',
            # every option gets a default: Cowork ignores a server whose ${user_config.*} option has none (it never prompts);
            # an empty value means "auto-detect" to the server
            'userConfig': {k: {**{kk: vv for kk, vv in v.items() if kk in USER_CONFIG_KEYS}, 'default': v.get('default', '')} for k, v in m.get('user_config', {}).items()},
            'mcpServers': {server: {'command': 'node', 'args': ['${CLAUDE_PLUGIN_ROOT}/dist/bundle.cjs'], 'env': env}},
        }
        with open(os.path.join(out, '.claude-plugin', 'plugin.json'), 'w', encoding='utf-8', newline='\n') as f:
            json.dump(plugin, f, indent=2, ensure_ascii=False)
            f.write('\n')
        with open(os.path.join(out, 'README.md'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(readme(app, m, c, has_shot))
        entries.append({'name': name, 'source': f'./plugins/{name}', 'description': m['description'], 'version': m['version'], 'category': (c.get('category') or 'productivity').lower(), 'keywords': plugin['keywords'][:6]})
        print(f'{name} {m["version"]} ok')
    mk = {
        'name': 'sunsam-plugins',
        'owner': {'name': 'Jhon Supelano', 'url': 'https://github.com/jhonsu01'},
        'metadata': {'description': 'Craft Bridges: community Claude Code plugins that connect Claude to the open-source Craft apps installed on your computer.', 'version': '1.0.0'},
        'plugins': entries,
    }
    os.makedirs(os.path.join(ROOT, '.claude-plugin'), exist_ok=True)
    with open(os.path.join(ROOT, '.claude-plugin', 'marketplace.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(mk, f, indent=2, ensure_ascii=False)
        f.write('\n')


if __name__ == '__main__':
    main()
