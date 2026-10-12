---
title: "Professional Esports Logo Generator JSON Prompt"
description: "Create esports team logos with a reusable JSON prompt, six adaptive styles, consistent lettering, and three examples: modern, fantasy, and pixel retro."
seo_title: "Esports Logo Generator JSON Prompt"
keywords: "esports logo prompt, gaming team logo, JSON image prompt, mascot logo, pixel logo, fantasy esports logo"
custom_url: professional-esports-logo-generator-json-prompt
date: 2026-10-12
author: Robert DeVore
categories: ["images"]
tags: ["json prompts", "esports", "logos", "design", "ai images"]
featured_image: /assets/images/ascii-grunge/esports-logo-generator.webp
og_image: /assets/social/professional-esports-logo-generator-json-prompt-social.png
og_image_alt: "Esports Logo Generator JSON Prompt with gold ASCII trophy and shield artwork on black"
og_image_width: 1200
og_image_height: 630
---

Give your team a name, pick its colors, and use this JSON prompt to build an esports identity around them. The adaptive professional esports logo generator includes six style profiles, with shared rules for readable wordmarks, balanced badges, clean silhouettes, and consistent letter geometry.

The default look uses flat vector-style fills and hard-edged shading. A theme or rendering preference takes priority over the style inferred from your team name and palette.

## How to Use It

1. Copy the complete JSON prompt below into an image-generation tool that accepts detailed text instructions.
2. Add a short sentence with your exact team name and preferred colors.
3. Include a mascot, theme, or rendering preference if you have one. For example: “Team name: Rogue Rebels. Colors: black, red, white, and gray. Use a hooded mascot in a flat vector style.”
4. Generate a square logo and check the spelling, letter spacing, outline weight, and silhouette at avatar size. Ask for a focused revision if a detail needs work.

The JSON describes the design; it is not an API request body. The prompt recommends at least 2048 × 2048 pixels, but output size depends on the image tool. Generated images have a vector-like appearance; they are raster artwork, not editable vector files.

## Six Adaptive Styles

- **Modern esports:** sharp mascots, masked figures, high-contrast shields, and angular lettering.
- **Pixel retro:** arcade mascots, stepped borders, and grid-based block text.
- **Military tactical:** disciplined patches, monograms, and compact nameplates.
- **Fantasy darkcore:** knights, dragons, gothic crests, and restrained magical accents.
- **Anime action:** expressive character heads, sharp cel shading, and motion cuts.
- **Minimal pro:** simple geometry, negative space, and restrained wordmarks.

You can request a style explicitly. Otherwise, the generator uses the team name, colors, mascot, and genre cues, with modern esports as its fallback.

## Three Example Variations

These AI-generated examples demonstrate three directions from the same design system. Each keeps the team name and palette in the brief while changing the mascot, badge, and lettering treatment.

### Rogue Rebels — Modern Esports

**Example input:** “Team name: Rogue Rebels. Colors: black, red, white, and gray. Use a hooded, masked rebel mascot in a flat vector style.”

A centered hooded figure and angular shield sit above a stacked wordmark. The red accent separates the badge from the black background, while beveled letter terminals carry the same sharp geometry through the name.

<figure>
<img src="/assets/images/esports-rogue-rebels.webp" alt="Rogue Rebels esports logo with a hooded masked mascot, red shield, and stacked white and red lettering" width="1254" height="1254" loading="lazy" decoding="async">
<figcaption>Modern esports variation: Rogue Rebels in black, red, white, and gray.</figcaption>
</figure>

### Dungeon Lords — Fantasy Darkcore

**Example input:** “Create an esports logo for Dungeon Lords using purple, black, silver, and flame orange. Use an armored void knight with gothic horns.”

The knight, horn shapes, and pointed crest bring the fantasy theme into the silhouette. Orange eyes and flame accents add contrast without hiding the silver wordmark.

<figure>
<img src="/assets/images/esports-dungeon-lords.webp" alt="Dungeon Lords esports logo with a horned silver knight, purple crest, orange eyes and flames, and stacked silver lettering" width="1254" height="1254" loading="lazy" decoding="async">
<figcaption>Fantasy darkcore variation: Dungeon Lords in purple, black, silver, and flame orange.</figcaption>
</figure>

### Pixel Runners — Pixel Retro

**Example input:** “Team name: Pixel Runners. Colors: gold, purple, and black. Use a running arcade mascot with crisp pixel lettering.”

Stepped edges, a running character, and chunky gold lettering give this variation an arcade identity. Purple shadow blocks keep the mascot and badge distinct against black.

<figure>
<img src="/assets/images/esports-pixel-runners.webp" alt="Pixel Runners esports logo with a gold running arcade mascot, purple pixel shadows, and stacked gold block lettering" width="1254" height="1254" loading="lazy" decoding="async">
<figcaption>Pixel retro variation: Pixel Runners in gold, purple, and black.</figcaption>
</figure>

## JSON Prompt

Copy the full version 2.0.0 profile below, then add your team brief.

```json
{
  "profileName": "adaptive_professional_esports_logo_generator",
  "version": "2.0.0",
  "purpose": "Generate polished, professional esports logos from a simple sentence containing a team name, colors, and optional theme cues. The AI should automatically choose the most relevant style profile while enforcing clean vector geometry, consistent wordmark construction, balanced symmetry, and studio-quality logo polish.",
  "inputMode": {
    "expectedUserInput": "A short sentence or prompt containing the team name, preferred colors, and optional theme direction.",
    "exampleInputs": [
      "Team name: Rogue Rebels. Colors: black, red, white, and gray.",
      "Create an esports logo for Dungeon Lords using purple, black, silver, and flame orange.",
      "Team name: Pixel Runners. Colors: gold, purple, and black.",
      "Team name: Bravo Unit X. Colors: olive, black, silver, and dark gray."
    ],
    "requiredFields": {
      "teamName": "Required. Use the exact team name provided by the user.",
      "colors": "Required when provided. Use the exact colors requested by the user as the primary palette."
    },
    "optionalFields": {
      "theme": "Optional. If provided, use it to influence mascot, symbol, background energy, and style profile selection.",
      "mascot": "Optional. If provided, prioritize it over automatically inferred mascot ideas.",
      "renderingPreference": "Optional. Examples: flat vector, glow, pixel, tactical, fantasy, minimal, mascot-only, badge-only."
    }
  },
  "globalOutputRequirements": {
    "format": "Professional esports logo",
    "aspectRatio": "1:1 square logo composition",
    "recommendedResolution": "2048x2048px minimum",
    "background": "Dark, transparent, or team-color-based depending on usage",
    "primaryUseCases": [
      "Team logo",
      "Gaming clan identity",
      "Streaming profile",
      "Merchandise",
      "Social avatar",
      "Discord server icon",
      "Tournament branding"
    ],
    "mustPreserve": [
      "Exact team name spelling",
      "Requested color palette",
      "Professional esports logo structure",
      "Clean vector-like edges",
      "Readable typography",
      "Balanced icon and text hierarchy"
    ],
    "avoid": [
      "Misspelled team names",
      "Random extra text",
      "Overly rounded letters when the rest of the wordmark is angular",
      "Mismatched letter terminals",
      "Uneven outlines",
      "Unbalanced badge shapes",
      "Excessive glow that changes the flat logo style",
      "Messy gradients",
      "Generic template-like mascots",
      "Low-resolution raster effects",
      "Unclear silhouettes"
    ]
  },
  "globalRenderingDefaults": {
    "preferredBaseLook": "flat-vector-shaded",
    "description": "Default to bold flat vector fills with hard-edged cel shading, clean shadows, and controlled highlight shapes. The logo should feel like a polished esports vector illustration, not a glossy 3D render.",
    "flatColorRules": {
      "useSolidColorRegions": true,
      "useHardVectorShadows": true,
      "useCelShading": true,
      "allowSubtleTexture": false,
      "avoidPhotorealism": true,
      "avoidPainterlyBlending": true,
      "avoidSoftAirbrushGradients": true
    },
    "glowRules": {
      "glowIsOptional": true,
      "defaultGlowIntensity": "low",
      "allowedUse": [
        "Thin outer rim glow",
        "Eye glow",
        "Small tech accent glow",
        "Background separation glow"
      ],
      "avoid": [
        "Heavy neon bloom",
        "Glow covering the whole logo",
        "Glow replacing the core flat fills",
        "Overly cyberpunk color wash unless explicitly requested"
      ]
    },
    "gradientRules": {
      "defaultGradientUse": "minimal",
      "allowedUse": [
        "Very subtle shade variation inside large flat areas",
        "Small bevel illusion on text",
        "Controlled shadow planes"
      ],
      "avoid": [
        "Large smooth gradients",
        "Glossy chrome effects",
        "3D plastic rendering",
        "Uncontrolled color fading across entire letters"
      ]
    }
  },
  "globalWordmarkRules": {
    "exactText": true,
    "teamNameHandling": {
      "useExactTeamName": true,
      "splitLongNamesIntoLines": true,
      "lineBreakGuidance": "For two-word names, place the first word above the second word unless the design works better as a single compact line.",
      "noExtraWords": true,
      "noTaglinesUnlessProvided": true
    },
    "typographyStyle": {
      "default": "custom block esports lettering",
      "traits": [
        "bold",
        "wide",
        "angular",
        "highly readable",
        "vector-clean",
        "slightly condensed when needed",
        "built for logo use"
      ]
    },
    "letterformConsistency": {
      "description": "All letters in the same wordmark must share the same design logic, including angles, cut corners, terminal shapes, stroke width, bevel style, and outline thickness.",
      "mustMatch": [
        "terminal angle style",
        "corner radius",
        "inner cutout geometry",
        "baseline shape",
        "outline thickness",
        "shadow direction",
        "bevel thickness",
        "letter slant",
        "letter height",
        "visual weight"
      ],
      "criticalRule": "If one letter has a sharp pointed foot, notch, spike, bevel, or angled terminal, other compatible letters should echo that geometry. Do not mix a sharp angular R with a soft rounded S unless the user explicitly asks for mixed typography.",
      "specificLetterRules": {
        "S": {
          "problemToAvoid": "A rounded bottom-right S terminal that does not match the pointed angular feet of letters like R, E, L, or A.",
          "preferredTreatment": "Use an angular esports S with a pointed or beveled bottom-right terminal when surrounding letters use sharp pointed geometry.",
          "terminalShape": "pointed, chamfered, or beveled, not soft-rounded",
          "baselineBehavior": "The bottom of the S should visually align with the baseline geometry of neighboring letters."
        },
        "R": {
          "preferredTreatment": "Strong diagonal leg with a sharp or beveled foot.",
          "matchAgainst": ["S", "E", "L", "A"]
        },
        "E": {
          "preferredTreatment": "Squared or angled horizontal bars with consistent cut angles.",
          "avoid": "Randomly rounded arms unless all typography is intentionally rounded."
        },
        "G": {
          "preferredTreatment": "Angular inner notch and consistent outer curve-to-corner logic.",
          "avoid": "Overly soft circular G if the rest of the wordmark is blocky."
        }
      }
    },
    "outlineRules": {
      "description": "Text outlines must be consistent and symmetrical.",
      "outerStroke": "Uniform unless deliberately layered",
      "innerStroke": "Consistent within each word",
      "shadowOffset": "Same direction and thickness across all letters",
      "avoid": [
        "one letter having a different outline thickness",
        "rounded outline corners beside pointed letter corners",
        "uneven lower terminals",
        "misaligned baselines"
      ]
    }
  },
  "globalProfessionalPolish": {
    "symmetryEnforcement": {
      "description": "Ensure visual elements are mirror-balanced when the logo uses a centered badge, mascot, crest, or shield.",
      "appliesTo": [
        "Mascot face",
        "Eyes",
        "Shoulders",
        "Hood",
        "Helmet",
        "Shield",
        "Outer border",
        "Wordmark",
        "Letter terminals"
      ],
      "rules": [
        "Left and right visual weight should feel balanced.",
        "If a border point appears on one side, the opposite side should have an equivalent point unless the design is intentionally asymmetric.",
        "Mascot faces may be expressive, but eye size, brow angle, and head placement must feel professionally controlled.",
        "Badge borders should not randomly bulge, flatten, or round on only one side."
      ]
    },
    "anchorRefinement": {
      "description": "Vector-like shapes should have clean anchor logic, controlled transitions, and intentional corners.",
      "rules": [
        "No jagged accidental edges.",
        "No floating points.",
        "No awkward bumps in curves.",
        "No uneven corners on mirrored forms.",
        "Angular corners should use consistent bevel angles."
      ]
    },
    "strokeConsistency": {
      "description": "Outer borders, inner outlines, shadows, and highlights should use a clear visual hierarchy.",
      "rules": [
        "Primary outer stroke should be the thickest.",
        "Secondary inner strokes should be thinner but consistent.",
        "Highlight strokes should not overpower the mascot or wordmark.",
        "Typography stroke thickness should remain consistent across all letters."
      ]
    },
    "spacingAlignment": {
      "description": "Spacing should feel calculated, not accidental.",
      "rules": [
        "Maintain even kerning across the wordmark.",
        "Keep consistent padding between text and badge border.",
        "Avoid cramped letters.",
        "Avoid text touching mascot elements unless intentionally overlapped.",
        "Center the wordmark under the mascot or icon."
      ]
    },
    "compositionBalance": {
      "description": "The full logo should work as a single identity mark.",
      "rules": [
        "Mascot, wordmark, and badge must feel integrated.",
        "Top and bottom sections should have balanced mass.",
        "The icon should not overpower the team name.",
        "The team name should remain readable at small sizes.",
        "The silhouette should be recognizable even without inner detail."
      ]
    }
  },
  "styleSelectionLogic": {
    "selectionMethod": "Choose the style profile whose keywords, subject matter, and color behavior best match the user's team name, colors, and optional theme.",
    "priorityOrder": [
      "Explicit user theme or rendering preference",
      "Team name semantic meaning",
      "Color palette",
      "Mascot implied by team name",
      "Genre cues such as cyber, fantasy, tactical, retro, horror, anime, minimal, or military"
    ],
    "fallbackStyle": "modern-esports",
    "styleMatchingExamples": [
      {
        "input": "Rogue Rebels, black red white gray",
        "selectedStyle": "modern-esports",
        "reason": "Aggressive team name, strong esports palette, mascot-friendly identity."
      },
      {
        "input": "Dungeon Lords, purple black orange",
        "selectedStyle": "fantasy-darkcore",
        "reason": "Fantasy naming, dark palette, mystical visual direction."
      },
      {
        "input": "Pixel Runners, gold purple black",
        "selectedStyle": "pixel-retro",
        "reason": "Pixel keyword strongly indicates arcade or retro treatment."
      },
      {
        "input": "Bravo Unit X, olive black silver",
        "selectedStyle": "military-tactical",
        "reason": "Military naming and tactical color palette."
      }
    ]
  },
  "styleProfiles": {
    "modern-esports": {
      "name": "Modern Esports Logo Style",
      "description": "A bold, aggressive, professional esports logo style built around mascots, sharp wordmarks, badge shapes, and high-contrast team colors. This style should look like a polished competitive gaming identity, using flat vector fills, hard-edged shading, and controlled accent lighting.",
      "keywords": [
        "aggressive",
        "competitive",
        "modern",
        "mascot",
        "neon",
        "sharp",
        "rebels",
        "rogue",
        "cyber",
        "elite",
        "clan",
        "gaming"
      ],
      "bestFor": [
        "General esports teams",
        "Streaming brands",
        "Competitive clans",
        "Mascot logos",
        "Hooded figures",
        "Masked characters",
        "Cyber animals",
        "Sharp badge logos"
      ],
      "visualCharacteristics": {
        "colorScheme": {
          "default": ["#FF0033", "#FFFFFF", "#111111", "#555555"],
          "styleNote": "Use the user-provided colors as the main palette. For black, red, white, and gray, keep the design flatter and more classic, using red as the main accent, white for text or highlights, gray for secondary shading, and black for the base mass."
        },
        "lineQuality": "Clean bold vector lines with sharp corners, smooth intentional curves, and no messy raster texture.",
        "edgeStyle": "Angular with controlled curves only where needed for hair, masks, animals, or clothing.",
        "fillType": "Flat solid fills with hard cel-shaded shadow shapes.",
        "contrast": "Very high contrast with strong silhouette clarity.",
        "stroke": "Thick outer stroke with consistent inner stroke hierarchy."
      },
      "renderingStyle": {
        "baseStyle": "flat-vector-shaded",
        "description": "Use flat esports vector illustration with hard-edged shadows and highlights. Avoid excessive glow, heavy gradients, or glossy 3D rendering unless explicitly requested.",
        "allowedEffects": [
          "hard-edged cel shadows",
          "flat color blocking",
          "subtle rim accent",
          "small eye glow",
          "small controlled highlight planes"
        ],
        "restrictedEffects": [
          "heavy neon bloom",
          "soft airbrush gradients",
          "full-letter gradient fills",
          "3D glossy bevels",
          "plastic shine",
          "overly cyberpunk lighting"
        ],
        "notes": "The logo should feel like the original flat-color esports style, not a glowing poster or semi-3D illustration."
      },
      "subjectMatter": {
        "type": "Mascot, masked figure, animal, emblem, tech symbol, custom wordmark",
        "exampleSubjects": [
          "Masked Rogue",
          "Hooded Rebel",
          "Cyber Wolf",
          "Angry Tiger",
          "Mecha Owl",
          "Glitched Phoenix",
          "Sharp Monogram Badge"
        ],
        "poseVariety": [
          "Forward-facing intense mascot",
          "Centered masked figure",
          "Angled aggressive animal head",
          "Badge with mascot above wordmark",
          "Symbol and wordmark hybrid"
        ]
      },
      "wordmarkTreatment": {
        "style": "bold angular block esports typography",
        "preferredLineBreak": "Two-word names should usually be stacked, with the first word larger or equal to the second depending on composition.",
        "terminalRules": {
          "useSharpTerminals": true,
          "usePointedFeetWhenAppropriate": true,
          "avoidRoundedBottomRightS": true,
          "matchLetterGeometryAcrossWord": true
        },
        "specificInstruction": "For names like Rogue Rebels, the S in Rebels must have an angular pointed or beveled bottom-right terminal that visually matches the pointed bottom geometry of the R and other block letters."
      },
      "professionalPolish": {
        "symmetryEnforcement": {
          "description": "Ensure left and right visual elements are mirror-balanced when applicable.",
          "appliesTo": ["Letterforms", "Mascot Faces", "Outlines", "Shield Shapes", "Shoulders", "Hair Mass"],
          "notes": "If one side has a pointed edge, mirror it precisely or balance it with an equivalent angular detail on the opposite side."
        },
        "anchorRefinement": {
          "description": "Control anchor handles to create precise curves and angle junctions.",
          "appliesTo": ["Fonts", "Mascot Lines", "Inner Shadows", "Outer Badge"],
          "notes": "Avoid uneven curvature, floating anchor points, abrupt inflection angles, or accidental bumps."
        },
        "strokeConsistency": {
          "description": "Use uniform stroke widths or a deliberate stroke hierarchy for layered depth.",
          "appliesTo": ["Text Outlines", "Outer Badge Shapes", "Hair", "Mask", "Clothing Folds"],
          "notes": "Visually harmonize all stroke widths unless layering for depth."
        },
        "spacingAlignment": {
          "description": "Use even spacing between letters, shapes, and boundaries.",
          "appliesTo": ["Letter Kerning", "Text-to-Badge Padding", "Mascot-to-Text Gap"],
          "notes": "Avoid crowded glyphs or inconsistent whitespace between text elements."
        },
        "compositionBalance": {
          "description": "Ensure the full logo feels centered, stable, and evenly weighted.",
          "appliesTo": ["Full Badge Shape", "Mascot Inside Shield", "Typography and Icon Stack"],
          "notes": "Use an implied grid to verify that everything aligns logically."
        },
        "letterformConsistency": {
          "description": "All characters in a wordmark must visually match in angle, curve style, terminal shape, and base logic.",
          "appliesTo": ["Custom Fonts", "Wordmarks", "Stacked Team Names"],
          "notes": "If one character has a pointed base, others in the same word should match that geometry. Avoid mismatched terminals, such as a sharp R beside a rounded S."
        }
      }
    },
    "pixel-retro": {
      "name": "Retro Pixel Arcade Style",
      "description": "A nostalgic esports logo style inspired by arcade cabinets, 8-bit and 16-bit games, CRT displays, and retro game mascots. It should use pixel-perfect block construction while still feeling like a clean competitive team identity.",
      "keywords": [
        "pixel",
        "retro",
        "arcade",
        "8-bit",
        "16-bit",
        "low-res",
        "joystick",
        "crt",
        "classic",
        "runner"
      ],
      "bestFor": [
        "Retro gaming teams",
        "Arcade-inspired clans",
        "Pixel mascots",
        "Old-school streaming brands",
        "Gamepad or joystick identities"
      ],
      "visualCharacteristics": {
        "colorScheme": {
          "default": ["#FFD700", "#8A2BE2", "#000000", "#FFFFFF"],
          "styleNote": "Use bold arcade colors, strong contrast, and limited palette discipline."
        },
        "lineQuality": "Pixel-snapped edges with grid-based precision.",
        "edgeStyle": "Square, stepped, and block-based.",
        "fillType": "Flat pixel fills with no smooth gradients.",
        "contrast": "Medium to high.",
        "stroke": "Consistent pixel outline, usually 1 to 3 pixel units depending on scale."
      },
      "renderingStyle": {
        "baseStyle": "pixel-flat",
        "description": "Use pixel art logic with clean grid snapping, crisp block silhouettes, and no anti-aliased painterly effects.",
        "allowedEffects": [
          "limited dithering",
          "pixel highlights",
          "CRT-inspired framing",
          "small glitch blocks"
        ],
        "restrictedEffects": [
          "smooth vector curves",
          "soft gradients",
          "photorealistic shading",
          "messy pixel sizes",
          "inconsistent grid units"
        ]
      },
      "subjectMatter": {
        "type": "Pixel mascot, gamepad, joystick, arcade monster, retro badge",
        "exampleSubjects": [
          "Pixel Skull",
          "Retro Joystick",
          "CRT Monster",
          "Pixel Runner",
          "Arcade Wolf",
          "8-bit Dragon"
        ],
        "poseVariety": [
          "Centered pixel frame",
          "Low-res action pose",
          "Static arcade badge",
          "Pixel mascot above block text"
        ]
      },
      "wordmarkTreatment": {
        "style": "chunky pixel block lettering",
        "preferredLineBreak": "Use stacked block text when the team name has two words.",
        "terminalRules": {
          "useSharpTerminals": false,
          "useGridAlignedTerminals": true,
          "avoidRoundedTerminals": true,
          "matchPixelUnitAcrossLetters": true
        }
      },
      "professionalPolish": {
        "symmetryEnforcement": {
          "description": "Ensure symmetry in pixel art by using mirrored or aligned blocks.",
          "appliesTo": ["Characters", "Text", "Badge Edges", "Pixel Borders"],
          "notes": "Pixel outlines should be clean and consistently mirrored on both sides."
        },
        "anchorRefinement": {
          "description": "All edges should snap to the pixel grid.",
          "appliesTo": ["Sprites", "Fonts", "Outlines"],
          "notes": "Avoid diagonal staircasing unless intentionally stylized."
        },
        "strokeConsistency": {
          "description": "Use consistent pixel stroke weight throughout.",
          "appliesTo": ["Text Borders", "Character Outlines", "Frames"],
          "notes": "Avoid inconsistent pixel width or non-integer placements."
        },
        "spacingAlignment": {
          "description": "Ensure uniform spacing between text and icon blocks.",
          "appliesTo": ["HUD Layouts", "Team Names", "Mascot Position"],
          "notes": "Every element should snap to a base grid, such as 8px or 16px."
        },
        "compositionBalance": {
          "description": "Centralize mascot and ensure logo reads clearly even at small sizes.",
          "appliesTo": ["Icons", "Text Blocks", "Frames"],
          "notes": "Optimize for readability at both small avatar sizes and large merchandise sizes."
        },
        "letterformConsistency": {
          "description": "Ensure pixel characters use the same pixel size and styling logic throughout.",
          "appliesTo": ["Bitmap Fonts", "Lettered Wordmarks"],
          "notes": "Avoid inconsistent pixel width or clashing pixel edge behavior."
        }
      }
    },
    "military-tactical": {
      "name": "Tactical Military Logo Style",
      "description": "A clean, serious esports logo style with military, tactical, squad, FPS, and elite-unit influences. It should feel disciplined, precise, and operational rather than flashy.",
      "keywords": [
        "military",
        "tactical",
        "fps",
        "unit",
        "squad",
        "stealth",
        "bravo",
        "alpha",
        "ops",
        "strike",
        "ranger",
        "recon"
      ],
      "bestFor": [
        "FPS teams",
        "Tactical squads",
        "Military-themed clans",
        "Serious competitive brands",
        "Patch-style logos",
        "Monogram emblems"
      ],
      "visualCharacteristics": {
        "colorScheme": {
          "default": ["#556B2F", "#CCCCCC", "#101010", "#2F2F2F"],
          "styleNote": "Desaturated greens, blacks, grays, metallic tones, tan, and controlled accent colors."
        },
        "lineQuality": "Precise vector lines with minimal flare.",
        "edgeStyle": "Sharply defined geometric edges.",
        "fillType": "Flat fill with subtle inner detail.",
        "contrast": "Moderate to high.",
        "stroke": "Thin to medium borders with military patch discipline."
      },
      "renderingStyle": {
        "baseStyle": "flat-tactical-vector",
        "description": "Use flat emblem construction, clean patch geometry, disciplined spacing, and controlled contrast.",
        "allowedEffects": [
          "subtle metal shading",
          "flat camo panels",
          "rank-stripe accents",
          "crosshair geometry",
          "patch stitching implied through simple shapes"
        ],
        "restrictedEffects": [
          "heavy glow",
          "cartoonish neon",
          "overly playful mascots",
          "messy grunge",
          "unreadable tactical clutter"
        ]
      },
      "subjectMatter": {
        "type": "Weapon silhouette, monogram, emblem patch, tactical skull, shield, crosshair",
        "exampleSubjects": [
          "Sniper Scope",
          "Tactical Skull",
          "Winged Shield",
          "Crosshair Monogram",
          "Stealth Wolf",
          "Unit Patch"
        ],
        "poseVariety": [
          "Patch-style layout",
          "Centered monogram",
          "Weapon-centric mark",
          "Shield with squad symbol"
        ]
      },
      "wordmarkTreatment": {
        "style": "military block lettering or stencil-inspired esports typography",
        "preferredLineBreak": "Use a compact nameplate below or across the badge.",
        "terminalRules": {
          "useSharpTerminals": true,
          "useStencilCutsWhenRelevant": true,
          "avoidSoftRoundedLetters": true,
          "matchCutAnglesAcrossLetters": true
        }
      },
      "professionalPolish": {
        "symmetryEnforcement": {
          "description": "Logos should feel centered and evenly distributed like military patches.",
          "appliesTo": ["Crests", "Weapon Balance", "Shield Halves", "Patch Borders"],
          "notes": "All visual weight must be harmonized between left, right, top, and bottom."
        },
        "anchorRefinement": {
          "description": "Bevels, cutouts, and corners should have consistent vector transitions.",
          "appliesTo": ["Weapon Edges", "Fonts", "Patches", "Rank Symbols"],
          "notes": "No floating points or unfinished strokes."
        },
        "strokeConsistency": {
          "description": "Stroke widths should remain consistent across all elements.",
          "appliesTo": ["Crest Lines", "Letter Outlines", "Patch Borders"],
          "notes": "Create hierarchy through scale and placement, not random stroke weights."
        },
        "spacingAlignment": {
          "description": "Keep text and emblems properly aligned with military precision.",
          "appliesTo": ["Rank Icons", "Nameplates", "Symbols"],
          "notes": "Spacing should feel calculated and uniform."
        },
        "compositionBalance": {
          "description": "Visual hierarchy should place importance on the team identity first, not decoration.",
          "appliesTo": ["Team Monograms", "Unit Symbols", "Patch Frames"],
          "notes": "Avoid overdesigning. Clarity is key."
        },
        "letterformConsistency": {
          "description": "Letterforms should share stroke weight, cut angles, stencil gaps, and width proportions.",
          "appliesTo": ["Military Text", "Nameplates", "Unit Labels"],
          "notes": "No mismatched corners or unrelated font weights in the same wordmark."
        }
      }
    },
    "fantasy-darkcore": {
      "name": "Fantasy Dark-Core Style",
      "description": "A dark, mystical esports logo style with fantasy, gothic, horror, demon, rune, and RPG-inspired elements. It should feel powerful, dramatic, and emblematic while remaining readable as a competitive logo.",
      "keywords": [
        "dark",
        "fantasy",
        "magic",
        "gothic",
        "demon",
        "dragon",
        "dungeon",
        "lord",
        "rune",
        "shadow",
        "void",
        "mythic"
      ],
      "bestFor": [
        "Fantasy teams",
        "RPG-inspired clans",
        "Dark mascots",
        "Demonic crests",
        "Dragon logos",
        "Magic guild identities",
        "Gothic esports brands"
      ],
      "visualCharacteristics": {
        "colorScheme": {
          "default": ["#4B0082", "#D3D3D3", "#0D0D0D", "#FF4500"],
          "styleNote": "Use dark purples, black, silver, bone white, ember orange, crimson, or eerie accent colors."
        },
        "lineQuality": "Illustrative vector lines with rune-like or blade-like detail.",
        "edgeStyle": "Curved organic forms mixed with sharp gothic points.",
        "fillType": "Mostly flat fills with controlled shadow planes and optional magical glow accents.",
        "contrast": "High contrast in central figures.",
        "stroke": "Strong outer outline with controlled inner ornamentation."
      },
      "renderingStyle": {
        "baseStyle": "flat-fantasy-emblem",
        "description": "Use flat emblem construction with sharp fantasy silhouettes, hard shadows, and controlled magical accents.",
        "allowedEffects": [
          "small rune glow",
          "ember accents",
          "hard-edged aura shapes",
          "blade highlights",
          "stone-like flat texture"
        ],
        "restrictedEffects": [
          "overly soft fantasy painting",
          "complex unreadable runes",
          "heavy smoke covering the wordmark",
          "random asymmetrical glow",
          "thin decorative lines that disappear at small sizes"
        ]
      },
      "subjectMatter": {
        "type": "Demonic figure, dragon, sword crest, arcane symbol, skull, hooded mage, beast",
        "exampleSubjects": [
          "Shadow Wizard",
          "Two-Headed Dragon",
          "Flaming Rune Blade",
          "Demonic Skull",
          "Void Knight",
          "Arcane Wolf"
        ],
        "poseVariety": [
          "Symmetrical crest",
          "Cloaked stance",
          "Arcane sigil form",
          "Dragon head above wordmark",
          "Weapon and rune badge"
        ]
      },
      "wordmarkTreatment": {
        "style": "dark angular fantasy lettering with esports readability",
        "preferredLineBreak": "Use stacked wordmark or crest-integrated text.",
        "terminalRules": {
          "useSharpTerminals": true,
          "useGothicPointsWhenRelevant": true,
          "avoidOverlyCurlyUnreadableLetters": true,
          "matchSerifAndSpikeLogicAcrossLetters": true
        }
      },
      "professionalPolish": {
        "symmetryEnforcement": {
          "description": "Sigils, magical icons, horns, wings, and crests must be symmetrical or radially balanced.",
          "appliesTo": ["Runes", "Glyphs", "Crests", "Horns", "Wings", "Weapon Pairs"],
          "notes": "Uneven glow or asymmetry should feel intentional, not accidental."
        },
        "anchorRefinement": {
          "description": "Use smooth vector transitions and clean loops for scrolls, horns, flames, and cloth.",
          "appliesTo": ["Wings", "Hood Folds", "Eyes", "Flames", "Runes"],
          "notes": "Avoid over-clutter or inconsistent anchor weight."
        },
        "strokeConsistency": {
          "description": "Match inner detail line weights and outer edges for harmonious flow.",
          "appliesTo": ["Glowing Cracks", "Weapon Outlines", "Horns", "Crest Borders"],
          "notes": "Glows should fade evenly from center shapes and should not destroy the flat logo read."
        },
        "spacingAlignment": {
          "description": "Balance complex shapes with clean spacing so central figures stand out.",
          "appliesTo": ["Mystical Circles", "Runic Borders", "Wordmarks"],
          "notes": "Use space to emphasize hierarchy, not overload the eye."
        },
        "compositionBalance": {
          "description": "Maintain center mass and mystical aura around the core icon.",
          "appliesTo": ["Floating Elements", "Spellmarks", "Crests"],
          "notes": "Ensure no part overpowers the main identity symbol."
        },
        "letterformConsistency": {
          "description": "All runic, gothic, or fantasy lettering must share geometry logic, stroke width, serif logic, and terminal shape.",
          "appliesTo": ["Crest Names", "Magical Words", "Fantasy Wordmarks"],
          "notes": "No inconsistent serif shapes, mismatched spikes, or misaligned decoration."
        }
      }
    },
    "anime-action": {
      "name": "Anime Action Esports Style",
      "description": "A high-energy esports logo style inspired by anime protagonists, villains, speed lines, dramatic eyes, and stylized character mascots. It should feel expressive and dynamic without becoming a full illustration poster.",
      "keywords": [
        "anime",
        "ninja",
        "samurai",
        "hero",
        "villain",
        "speed",
        "katana",
        "spirit",
        "fighter",
        "shonen"
      ],
      "bestFor": [
        "Anime-inspired teams",
        "Fast aggressive brands",
        "Character mascots",
        "Ninja or samurai identities",
        "Stylized human avatars"
      ],
      "visualCharacteristics": {
        "colorScheme": {
          "default": ["#FF1744", "#00E5FF", "#111111", "#FFFFFF"],
          "styleNote": "Use strong contrast, dramatic accent colors, and flat anime shadow shapes."
        },
        "lineQuality": "Clean manga-inspired vector lines with bold silhouette control.",
        "edgeStyle": "Sharp hair, sharp eyes, angular clothing folds, and dynamic diagonal energy.",
        "fillType": "Flat anime-style cel shading.",
        "contrast": "Very high.",
        "stroke": "Bold outer stroke with thinner interior expression lines."
      },
      "renderingStyle": {
        "baseStyle": "flat-anime-cel-shaded",
        "description": "Use flat cel shading and stylized character energy while maintaining esports logo readability.",
        "allowedEffects": [
          "hard anime shadows",
          "speed-line accents",
          "small eye glow",
          "controlled aura shapes"
        ],
        "restrictedEffects": [
          "full-body complex illustration",
          "soft painterly anime rendering",
          "busy manga backgrounds",
          "thin facial details that disappear at small sizes"
        ]
      },
      "subjectMatter": {
        "type": "Anime mascot, masked fighter, ninja, samurai, cyber hero, villain face",
        "exampleSubjects": [
          "Masked Ninja",
          "Cyber Samurai",
          "Anime Wolf Spirit",
          "Villain Hero Face",
          "Katana Crest"
        ],
        "poseVariety": [
          "Forward-facing intense expression",
          "Three-quarter angled character head",
          "Mascot above wordmark",
          "Weapon silhouette behind badge"
        ]
      },
      "wordmarkTreatment": {
        "style": "angular esports lettering with anime motion cues",
        "preferredLineBreak": "Stacked or diagonal wordmark depending on motion direction.",
        "terminalRules": {
          "useSharpTerminals": true,
          "useMotionCuts": true,
          "avoidRoundedTerminals": true,
          "matchMotionAngleAcrossLetters": true
        }
      },
      "professionalPolish": {
        "symmetryEnforcement": {
          "description": "Character expression may be dynamic, but the logo must remain visually balanced.",
          "appliesTo": ["Eyes", "Hair Mass", "Mask", "Shoulders", "Badge"],
          "notes": "Do not let one side become unintentionally heavier unless the pose clearly explains it."
        },
        "anchorRefinement": {
          "description": "Hair spikes, mask edges, and clothing folds should have deliberate vector angles.",
          "appliesTo": ["Hair", "Eyes", "Mask", "Clothing", "Weapons"],
          "notes": "Avoid random spikes or uneven cuts."
        },
        "strokeConsistency": {
          "description": "Outer strokes and interior anime lines should have clear hierarchy.",
          "appliesTo": ["Character Outline", "Wordmark", "Speed Accents"],
          "notes": "Thin detail lines should not compete with the main silhouette."
        },
        "spacingAlignment": {
          "description": "Keep the wordmark readable under or beside the character.",
          "appliesTo": ["Team Name", "Badge Padding", "Character-to-Text Gap"],
          "notes": "Do not let speed lines interfere with text readability."
        },
        "compositionBalance": {
          "description": "The mascot should feel dynamic but logo-ready.",
          "appliesTo": ["Full Mark", "Character Head", "Weapon Accents"],
          "notes": "Favor iconic shape over detailed scene."
        },
        "letterformConsistency": {
          "description": "All letters should share the same slash angle, terminal shape, and motion logic.",
          "appliesTo": ["Anime Wordmarks", "Custom Type"],
          "notes": "Avoid mixing rounded cartoon lettering with sharp anime battle shapes."
        }
      }
    },
    "minimal-pro": {
      "name": "Minimal Pro Esports Style",
      "description": "A refined, clean esports logo style focused on simple geometry, strong negative space, premium restraint, and instantly recognizable identity marks.",
      "keywords": [
        "minimal",
        "clean",
        "pro",
        "premium",
        "simple",
        "monogram",
        "sleek",
        "modern",
        "brand"
      ],
      "bestFor": [
        "Premium teams",
        "Streamer brands",
        "Monograms",
        "Simple mascot marks",
        "Merch-friendly logos",
        "Professional organizations"
      ],
      "visualCharacteristics": {
        "colorScheme": {
          "default": ["#000000", "#FFFFFF", "#FF0033", "#777777"],
          "styleNote": "Use two to four colors maximum. Prioritize contrast and restraint."
        },
        "lineQuality": "Very clean vector geometry.",
        "edgeStyle": "Simple angular edges with precise curves only where needed.",
        "fillType": "Flat fills only.",
        "contrast": "High.",
        "stroke": "Minimal or none unless needed for readability."
      },
      "renderingStyle": {
        "baseStyle": "flat-minimal-vector",
        "description": "Use simple geometric forms, negative space, and precise alignment. Avoid decoration unless it strengthens recognition.",
        "allowedEffects": [
          "negative-space cuts",
          "simple bevels",
          "one accent color",
          "subtle shadow separation"
        ],
        "restrictedEffects": [
          "heavy glow",
          "busy mascots",
          "complex gradients",
          "too many colors",
          "overly detailed badge shapes"
        ]
      },
      "subjectMatter": {
        "type": "Monogram, symbol, simplified mascot, abstract mark",
        "exampleSubjects": [
          "RR Monogram",
          "Sharp Wolf Head",
          "Minimal Dragon",
          "Negative-Space Skull",
          "Lightning Crest"
        ],
        "poseVariety": [
          "Centered monogram",
          "Minimal mascot above wordmark",
          "Single compact badge",
          "Standalone icon"
        ]
      },
      "wordmarkTreatment": {
        "style": "clean custom sans-serif esports lettering",
        "preferredLineBreak": "Single line for short names, stacked layout for two-word names.",
        "terminalRules": {
          "useSharpTerminals": true,
          "avoidDecorativeExcess": true,
          "matchCornerRadiusAcrossLetters": true,
          "matchTerminalGeometryAcrossLetters": true
        }
      },
      "professionalPolish": {
        "symmetryEnforcement": {
          "description": "Minimal marks must be highly balanced because small errors are more visible.",
          "appliesTo": ["Monograms", "Icons", "Wordmarks", "Badge Shapes"],
          "notes": "Use strict alignment and avoid accidental asymmetry."
        },
        "anchorRefinement": {
          "description": "Every anchor point should feel necessary.",
          "appliesTo": ["Symbols", "Letters", "Negative Space"],
          "notes": "Remove visual noise and unnecessary points."
        },
        "strokeConsistency": {
          "description": "Stroke and shape thickness should be mathematically consistent.",
          "appliesTo": ["Monograms", "Wordmarks", "Simple Icons"],
          "notes": "Avoid accidental thickness changes."
        },
        "spacingAlignment": {
          "description": "Use precise spacing and proportional relationships.",
          "appliesTo": ["Letter Spacing", "Icon Padding", "Badge Margins"],
          "notes": "Minimal logos need strong spacing discipline."
        },
        "compositionBalance": {
          "description": "The mark should feel stable, compact, and instantly recognizable.",
          "appliesTo": ["Full Logo", "Icon", "Wordmark"],
          "notes": "Do not add elements that do not improve recognition."
        },
        "letterformConsistency": {
          "description": "All letters must share the same geometry system.",
          "appliesTo": ["Custom Sans Wordmarks", "Monograms"],
          "notes": "Do not mix rounded and sharp terminals unless the whole system is designed around that contrast."
        }
      }
    }
  },
  "generationChecklist": {
    "beforeFinalOutput": [
      "Confirm the exact team name is spelled correctly.",
      "Confirm the requested colors are used as the dominant palette.",
      "Confirm the selected style matches the team name and theme.",
      "Confirm the logo uses flat vector-style fills unless glow or gradient was explicitly requested.",
      "Confirm the mascot and badge are visually centered.",
      "Confirm the outer border is consistent.",
      "Confirm wordmark letters share the same geometry system.",
      "Confirm sharp letters have matching sharp terminals.",
      "Confirm the S does not have a rounded bottom-right terminal when neighboring letters use pointed feet.",
      "Confirm the logo remains readable at small sizes.",
      "Confirm the silhouette is clear without inner detail."
    ],
    "qualityBar": "The final image should feel like a finished professional esports logo, not a rough AI-generated concept."
  }
}
```

## Refine the Result

Check the exact team name first. Then compare the letters: their cut angles, terminals, outline thickness, and baseline should feel like one designed wordmark. In an angular name such as Rogue Rebels, pay particular attention to the bottom-right terminal of the S.

Review the badge at small size, simplify details that disappear, and keep the mascot and name balanced. Ask for one change at a time so a typography correction does not also alter the palette or mascot.

For a fabric-based identity, try the [military patch JSON prompt](/blog/top-secret-military-patches-json-prompt/). For a different icon treatment, explore the [glowing neon icon prompt](/blog/glowing-neon-icon-json-prompt/) or browse all [image prompts](/images/).
