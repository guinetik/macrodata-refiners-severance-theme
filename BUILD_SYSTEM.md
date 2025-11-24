# Theme Build System

This project uses a custom DSL (Domain-Specific Language) to manage theme colors and generate VS Code theme JSON files.

## Overview

Instead of manually editing large JSON files with hardcoded hex values, this build system allows you to:

1. **Define color palettes** in YAML files with semantic names
2. **Use a shared template** that defines the VS Code theme structure
3. **Generate theme JSON files** automatically with properly resolved colors

## Directory Structure

```
src/
├── palettes/           # Color palette definitions
│   ├── macrodata-refiners.yaml
│   ├── ortbo.yaml
│   ├── cold-harbor.yaml
│   └── sweet-vitriol.yaml
└── templates/
    └── theme-template.yaml   # VS Code theme structure template

themes/                 # Generated theme JSON files (output)
├── macrodata-refiners.json
├── ortbo.json
├── cold-harbor.json
└── sweet-vitriol.json

build.js               # Build script (Node.js)
```

## How It Works

### 1. Color Palette Definition (`src/palettes/*.yaml`)

Each theme has a palette file that defines:

- **palette**: Raw color values with semantic names
- **colors**: Semantic mappings for UI elements
- **tokens**: Syntax highlighting color definitions

Example:

```yaml
name: "My Theme"
type: "dark"

palette:
  bg_darkest: "#0a1211"
  cyan_bright: "#00e5e5"
  green_primary: "#6a9080"
  # ... more colors

colors:
  editor_background: "bg_darkest"
  editor_foreground: "green_primary"
  editor_cursor: "cyan_bright"
  # ... more mappings

tokens:
  keyword:
    foreground: "cyan_bright"
    fontStyle: "bold"
  # ... more token definitions
```

### 2. Theme Template (`src/templates/theme-template.yaml`)

The template defines the VS Code theme structure using placeholders that reference palette colors:

```yaml
vscode_colors:
  "editor.background": "{color.editor_background}"
  "editor.foreground": "{color.editor_foreground}"
  "editorCursor.foreground": "{color.editor_cursor}"
  # Can also reference palette directly:
  "someColor": "{palette.cyan_bright}"
```

### 3. Build Process

The `build.js` script:

1. Loads the palette YAML file (using `js-yaml`)
2. Loads the template YAML file
3. Resolves all color references (`{color.xxx}` and `{palette.xxx}`)
4. Generates the final theme JSON file

## Building Themes

### Prerequisites

```bash
npm install
```

### Build All Themes

```bash
npm run build
```

Or directly:

```bash
node build.js
```

This generates all four themes in the `themes/` directory.

## Creating a New Theme

1. Create a new palette file in `src/palettes/your-theme.yaml`
2. Define your color palette, semantic colors, and tokens
3. Add your theme to the `themes` list in `build.py`:

```python
themes = [
    # ... existing themes
    ('your-theme', 'Your Theme Name'),
]
```

4. Run `npm run build`
5. Add your theme to `package.json`:

```json
{
  "contributes": {
    "themes": [
      {
        "label": "Your Theme Name",
        "uiTheme": "vs-dark",
        "path": "./themes/your-theme.json"
      }
    ]
  }
}
```

## Color Reference System

The build system supports two types of color references:

### Semantic Colors (`{color.xxx}`)

References colors defined in the `colors:` section of the palette file. These can chain-resolve to palette colors:

```yaml
palette:
  cyan_bright: "#00e5e5"

colors:
  editor_cursor: "cyan_bright"

# In template:
"editorCursor.foreground": "{color.editor_cursor}"
# Resolves to: "#00e5e5"
```

### Direct Palette Colors (`{palette.xxx}`)

Directly references colors from the `palette:` section:

```yaml
# In template:
"someColor": "{palette.cyan_bright}"
# Resolves to: "#00e5e5"
```

### Color Modifiers

You can append alpha/opacity values:

```yaml
# In template:
"editor.selectionBackground": "{color.editor_selection}AA"
# If editor_selection resolves to #1f3938, result is: #1f3938AA
```

## Advantages

1. **Centralized color management**: Change a color once, it updates everywhere
2. **Semantic naming**: Use meaningful names like `editor_cursor` instead of hex values
3. **Consistency**: All themes use the same structure
4. **Easy theme variants**: Create new color schemes without duplicating structure
5. **Better syntax highlighting**: Template includes comprehensive language support
6. **Type safety**: YAML validation catches errors early

## Tips

- **Color aliases**: Add compatibility aliases in your palette for template colors you don't use
- **Test incrementally**: Build and test after each color change
- **Use semantic colors**: Define UI element colors in `colors:` rather than hardcoding in template
- **Share common colors**: Put frequently used colors in the palette, reference them in tokens

## Troubleshooting

### Warning: "Palette color 'xxx' not found"

The template references a color that doesn't exist in your palette. Either:
1. Add the color to your palette
2. Add an alias that maps to an equivalent color in your theme

### Colors not updating

Make sure you:
1. Saved your palette file
2. Ran `python3 build.py`
3. Reloaded VS Code to pick up the new theme

### Build errors

Check that:
- YAML files are valid (use a YAML validator)
- Color references match exactly (case-sensitive)
- No duplicate keys in YAML files (YAML doesn't allow the same key twice in the same object)
- Required dependencies are installed (`npm install`)
