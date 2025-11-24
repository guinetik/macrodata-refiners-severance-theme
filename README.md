# Macrodata Refiners Theme

A collection of Severance-inspired themes for [Visual Studio Code](https://code.visualstudio.com/), capturing the distinct visual aesthetics from different locations within Lumon Industries.

_"Please enjoy each theme equally."_ - Ms Casey.

## Themes

### Macrodata Refiners (dark)

Inspired by the MDR department's teal-tinted screens and workstations. This theme captures the clinical, sterile environment of the severed floor where the refiners work.

![Reference](https://cdn.jsdelivr.net/gh/guinetik/macrodata-refiners-severance-theme@1.0.0/screenshots/severance_1.jpg)
![Preview](https://cdn.jsdelivr.net/gh/guinetik/macrodata-refiners-severance-theme@1.0.0/screenshots/01-classic.png)

### Cold Harbor (dark)

Inspired by Lumon's data visualization screens showing the Cold Harbor project metrics. A dark theme featuring graduated shades of cyan and blue, reminiscent of the analytical charts and progress bars displayed throughout the severed floor.

![Reference](https://cdn.jsdelivr.net/gh/guinetik/macrodata-refiners-severance-theme@1.0.0/screenshots/severance_2.png)
![Preview](https://cdn.jsdelivr.net/gh/guinetik/macrodata-refiners-severance-theme@1.0.0/screenshots/02-cold-harbor.png)

### ORTBO (light)

Based on the cold, wintery outdoor testing grounds where severed employees are tested. A bright, stark theme inspired by snow-covered landscapes and the harsh light of the exterior world beyond Lumon's walls.

![Reference](https://cdn.jsdelivr.net/gh/guinetik/macrodata-refiners-severance-theme@1.0.0/screenshots/severance_3.jpg)
![Preview](https://cdn.jsdelivr.net/gh/guinetik/macrodata-refiners-severance-theme@1.0.0/screenshots/03-ortbo.png)

### Sweet Vitriol (light)

Inspired by Ms. Cobel's cottage, this light theme balances warm cream backgrounds with teal, blue, and wood tones - perfect for those who prefer coding under the influence of ether while pretending to live in a rustic cottage.

![Reference](https://cdn.jsdelivr.net/gh/guinetik/macrodata-refiners-severance-theme@1.0.0/screenshots/severance_4.jpg)
![Preview](https://cdn.jsdelivr.net/gh/guinetik/macrodata-refiners-severance-theme@1.0.0/screenshots/04-sweet-vitriol.png)

### Defiant Jazz (dark)

Inspired by the vibrant, rebellious dance scene with dramatic colored lighting. A bold dark theme featuring electric cyans, vivid magentas, bright blues, and warm red-orange accents - capturing the energy and defiance of breaking free from control.

![Reference](https://cdn.jsdelivr.net/gh/guinetik/macrodata-refiners-severance-theme@1.0.3/screenshots/severance_5.jpg)
![Preview](https://cdn.jsdelivr.net/gh/guinetik/macrodata-refiners-severance-theme@1.0.3/screenshots/05-defiant-jazz.png)

## Features

- **Darker, more atmospheric colors** extracted from actual Severance scenes
- **Comprehensive syntax highlighting** with support for many languages including:
  - JavaScript/TypeScript (including JSX/TSX)
  - Python
  - CSS/SCSS
  - HTML
  - JSON
  - Markdown
  - And many more...
- **Semantic color system** for consistent theming across all UI elements
- **Carefully chosen accent colors** that match the show's aesthetic

## Installation

1. Open **Extensions** sidebar in VS Code (\`Ctrl+Shift+X\` / \`⌘+Shift+X\`)
2. Search for \`Macrodata Refiners Theme\`
3. Click **Install**
4. Go to **Color Themes** (\`Ctrl+K Ctrl+T\` / \`⌘+K ⌘+T\`)
5. Select one of the Macrodata Refiners themes

## Development

This theme uses a custom build system for easy color management. Instead of editing large JSON files, colors are defined in YAML palette files and automatically generated.

### Building themes

\`\`\`bash
# Install dependencies
npm install

# Build all themes
npm run build
\`\`\`

### Project structure

- \`src/palettes/\` - Color palette definitions for each theme
- \`src/templates/\` - Shared theme template
- \`themes/\` - Generated theme JSON files (output)
- \`build.js\` - Build script (Node.js)

See [BUILD_SYSTEM.md](BUILD_SYSTEM.md) for detailed documentation on the build system.

### Color extraction

Color palettes were extracted from official Severance promotional images using custom Python scripts (utility tools, not part of the build process):

\`\`\`bash
# Install Python dependencies (one-time setup for color extraction)
pip3 install Pillow

# Extract colors from reference images
python3 extract_colors_advanced.py reference-mdr.jpg
\`\`\`

## Contributing

Contributions are welcome! If you'd like to:
- Suggest color improvements
- Add new themes
- Improve syntax highlighting
- Fix bugs

Please open an issue or pull request on [GitHub](https://github.com/guinetik/macrodata-refiners-severance-theme).
