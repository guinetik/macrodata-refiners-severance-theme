#!/usr/bin/env node
/**
 * Theme Builder - Generate VS Code themes from palette + template
 */
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

/**
 * Load YAML file
 */
function loadYaml(filePath) {
  const fileContents = fs.readFileSync(filePath, 'utf8');
  return yaml.load(fileContents);
}

/**
 * Resolve a color reference like {palette.cyan_bright} or {color.editor_background}
 */
function resolveColorReference(ref, palette, colors) {
  if (!ref.startsWith('{') || !ref.endsWith('}')) {
    // Check if it's a direct palette reference without braces
    if (palette[ref]) {
      return palette[ref];
    }
    return ref;
  }

  // Remove braces
  const innerRef = ref.slice(1, -1);

  // Handle palette references
  if (innerRef.startsWith('palette.')) {
    const colorKey = innerRef.replace('palette.', '');
    if (palette[colorKey]) {
      return palette[colorKey];
    } else {
      console.warn(`Warning: Palette color '${colorKey}' not found`);
      return ref;
    }
  }

  // Handle color references (semantic names)
  if (innerRef.startsWith('color.')) {
    const colorKey = innerRef.replace('color.', '');
    if (colors[colorKey]) {
      const semanticValue = colors[colorKey];
      // Check if semantic value is a palette key
      if (palette[semanticValue]) {
        return palette[semanticValue];
      }
      return resolveColorReference(semanticValue, palette, colors);
    } else {
      console.warn(`Warning: Semantic color '${colorKey}' not found`);
      return ref;
    }
  }

  return ref;
}

/**
 * Process a value, replacing color references with actual colors
 */
function processValue(value, palette, colors) {
  if (typeof value !== 'string') {
    return value;
  }

  // Check if the entire value is a single reference
  if (value.startsWith('{') && value.endsWith('}') && (value.match(/\{/g) || []).length === 1) {
    return resolveColorReference(value, palette, colors);
  }

  // Handle embedded references (e.g., "{color.editor_selection}AA")
  const result = value.replace(/\{(?:palette|color)\.[^}]+\}/g, (match) => {
    return resolveColorReference(match, palette, colors);
  });

  return result;
}

/**
 * Build the VS Code colors object
 */
function buildVscodeColors(templateColors, palette, colors) {
  const result = {};
  for (const [key, value] of Object.entries(templateColors)) {
    result[key] = processValue(value, palette, colors);
  }
  return result;
}

/**
 * Build the token colors array
 */
function buildTokenColors(templateTokens, palette, colors, themeTokens) {
  const result = [];

  for (const tokenDef of templateTokens) {
    let scope = tokenDef.scope || [];
    if (typeof scope === 'string') {
      scope = [scope];
    }

    const tokenEntry = { scope };

    // Check if this uses a named token from the theme
    if (tokenDef.token) {
      const tokenName = tokenDef.token;
      if (themeTokens[tokenName]) {
        const tokenConfig = themeTokens[tokenName];
        const settings = {};

        if (tokenConfig.foreground) {
          const fgValue = tokenConfig.foreground;
          // Check if it's a direct palette reference
          if (palette[fgValue]) {
            settings.foreground = palette[fgValue];
          } else {
            settings.foreground = processValue(fgValue, palette, colors);
          }
        }

        if (tokenConfig.background) {
          const bgValue = tokenConfig.background;
          // Check if it's a direct palette reference
          if (palette[bgValue]) {
            settings.background = palette[bgValue];
          } else {
            settings.background = processValue(bgValue, palette, colors);
          }
        }

        if (tokenConfig.fontStyle) {
          settings.fontStyle = tokenConfig.fontStyle;
        }

        if (Object.keys(settings).length > 0) {
          tokenEntry.settings = settings;
        }
      } else {
        console.warn(`Warning: Token '${tokenName}' not found in theme`);
        continue;
      }
    } else {
      // Direct foreground/background/fontStyle specified
      const settings = {};

      if (tokenDef.foreground) {
        settings.foreground = processValue(tokenDef.foreground, palette, colors);
      }

      if (tokenDef.background) {
        settings.background = processValue(tokenDef.background, palette, colors);
      }

      if (tokenDef.fontStyle) {
        settings.fontStyle = tokenDef.fontStyle;
      }

      if (Object.keys(settings).length > 0) {
        tokenEntry.settings = settings;
      }
    }

    if (tokenEntry.settings) {
      result.push(tokenEntry);
    }
  }

  return result;
}

/**
 * Build a theme from palette and template
 */
function buildTheme(paletteFile, templateFile, outputFile) {
  console.log(`\nBuilding theme from:`);
  console.log(`  Palette:  ${paletteFile}`);
  console.log(`  Template: ${templateFile}`);
  console.log(`  Output:   ${outputFile}`);

  // Load palette
  const themeDef = loadYaml(paletteFile);
  const palette = themeDef.palette;
  const colors = themeDef.colors;
  const tokens = themeDef.tokens;

  // Load template
  const template = loadYaml(templateFile);

  // Build theme
  const theme = {
    name: themeDef.name,
    type: themeDef.type,
    colors: buildVscodeColors(template.vscode_colors, palette, colors),
    tokenColors: buildTokenColors(template.token_colors, palette, colors, tokens)
  };

  // Write output
  const outputDir = path.dirname(outputFile);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  fs.writeFileSync(outputFile, JSON.stringify(theme, null, 2));

  console.log(`  ✓ Theme built successfully!\n`);
}

/**
 * Main build process
 */
function main() {
  console.log('='.repeat(70));
  console.log('THEME BUILDER - Macrodata Refiners Severance Themes');
  console.log('='.repeat(70));

  const themes = [
    ['macrodata-refiners', 'Macrodata Refiners - Classic'],
    ['ortbo', 'ORTBO'],
    ['cold-harbor', 'Cold Harbor'],
    ['sweet-vitriol', 'Sweet Vitriol'],
  ];

  for (const [themeSlug, themeName] of themes) {
    buildTheme(
      `src/palettes/${themeSlug}.yaml`,
      'src/templates/theme-template.yaml',
      `themes/${themeSlug}.json`
    );
  }

  console.log('='.repeat(70));
  console.log(`Build complete! Generated ${themes.length} themes.`);
  console.log('='.repeat(70));
}

// Run if called directly
if (require.main === module) {
  try {
    main();
  } catch (error) {
    console.error('Error:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

module.exports = { buildTheme, main };
