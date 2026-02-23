# Highcharts Interactive Controls for QuickSight

Non-button interactive controls built with Highcharts scatter plots + click events. These push the boundaries of what's possible within QuickSight's security constraints (no JavaScript, no CSS, no input elements).

## Controls Library

### Basic Controls (`test-all-controls.html`)

| # | Control | Type | Parameter Example |
|---|---------|------|-------------------|
| 1 | Discrete Slider | Single value | `SliderValue = 5` |
| 2 | Star Rating | Single value | `StarRating = 3` |
| 3 | Increment/Decrement Stepper | Single value | `StepperValue = 5` |
| 4 | Toggle Switch | Boolean | `ToggleState = ON` |
| 5 | Color Swatch Picker | Single value | `ColorTheme = Blue` |
| 6 | Progress Stepper / Wizard | Single value | `WizardStep = 2` |
| 7 | Heatmap Grid Selector | Composite key | `GridSelection = Q2-Product B` |
| 8 | Thumbnail Card Selector | Single value | `CardSelection = Analytics` |
| 9 | Radial Dial Selector | Single value | `DialValue = 7` |

### Advanced Controls (`test-advanced-controls.html`)

| # | Control | Type | Parameter Example |
|---|---------|------|-------------------|
| 10 | On-Screen Keyboard | Text input (hack) | `KeyboardText = HELLO` |
| 11 | Multi-Select Checkboxes | Multi-value (pipe-delimited) | `Selections = QB\|WR\|TE` |
| 12 | Chip / Tag Selector | Multi-value (pipe-delimited) | `ChipSelect = Speed\|Power` |
| 13 | Range Selector (Min/Max) | Two parameters | `RangeMin=3, RangeMax=8` |
| 14 | Priority Ranker | Ordered list | `RankerOrder = Speed,Accuracy,Power` |
| 15 | Numeric Keypad | Number input (hack) | `NumpadText = 42` |
| 16 | Segmented Gauge | Single value + zones | `GaugeValue = 6` |
| 17 | Month/Year Picker | Date selection | `DatePicker = 2026-03` |
| 18 | Emoji Reaction Bar | Single value | `EmojiReaction = 👍` |
| 19 | Breadcrumb Navigator | Hierarchy drill | `BreadcrumbLevel = AFC West` |
| 20 | Sort Direction Control | Column + direction | `SortColumn=Rating, SortDir=DESC` |
| 21 | Volume / Level Bars | Single value | `VolumeLevel = 7` |

## How They All Work

Every control uses the same underlying mechanism:

```
Scatter plot → positioned data points → HTML dataLabels → triggerClick → navigation action → set parameter → pointRender updates visual state
```

### The Communication Channel

QuickSight Highcharts has exactly ONE way to communicate back to the dashboard:

1. User clicks a data point
2. `triggerClick` fires
3. Navigation action sets a parameter value (from the clicked point's data)
4. Dashboard re-renders with new parameter value
5. `pointRender` updates the visual state of all points

This means:
- Every interaction must be a **click on a data point**
- The value passed must be **derivable from that point's data**
- No continuous values (sliders snap to discrete ticks)
- No keyboard capture (but we can build an on-screen keyboard)
- No drag interactions

## Multi-Select Pattern (IMPORTANT)

Multi-select is the trickiest pattern because QuickSight parameters are single values. The workaround:

### Approach: Pipe-Delimited String Parameter

Store selections as a pipe-delimited string: `QB|WR|TE`

**Parameter:** `Selections` (String, default: `ALL`)

**Button Dataset Calc Field:**
```
SelectedOptions = ${Selections}
```

**Target Dataset Calc Field:**
```
ShowByFilter = ifelse(
  ${Selections} = 'ALL', 1,
  ifelse(locate(PositionGroup, ${Selections}) > 0, 1, 0)
)
```

**The Challenge:** Each click needs to toggle one item in the string. In QuickSight, the navigation action can only set a parameter to a field value from the clicked row. You can't do string manipulation in the action itself.

**Workaround Options:**

1. **Pre-computed toggle states** — For small option sets (≤8), pre-compute all possible toggle results as columns in your dataset. Each row has a column for "what the parameter should be if this item is toggled." This works but gets combinatorially explosive.

2. **Separate toggle widgets** — Each checkbox is its own tiny Highcharts widget with its own navigation action. The action sets a dedicated parameter (`Show_QB = YES/NO`), and the target dataset checks all individual parameters.

3. **Lambda-backed approach** — Use a QuickSight action to call an API Gateway → Lambda that computes the new string and writes it back. Overkill but works for complex cases.

**Recommended: Option 2 (Separate Toggle Widgets)**

For each option, create a minimal 1-point Highcharts widget:
- Dataset: 1 row with `ToggleValue` calc field = `${Show_QB}`
- Config: Single point with checkbox visual
- Action: Sets `Show_QB` parameter to opposite of current value
- pointRender: Shows checked/unchecked based on parameter

Target dataset calc field:
```
ShowByFilter = ifelse(
  ${Show_QB} = 'YES' AND PositionGroup = 'QB', 1,
  ifelse(${Show_WR} = 'YES' AND PositionGroup = 'WR', 1,
  ... 0)
)
```

## Text Input Pattern (ON-SCREEN KEYBOARD)

The keyboard is the most creative hack. Each key is a data point. But the fundamental challenge is the same as multi-select: you can't do string concatenation in a navigation action.

**Practical Approaches:**

1. **Character-by-character with multiple parameters** — Use parameters `Char1`, `Char2`, ... `Char10`. Each key press sets the next empty `CharN` parameter. A calc field concatenates them: `${Char1} & ${Char2} & ...`. Backspace clears the last non-empty one.

2. **Pre-defined options keyboard** — Instead of free-form text, show a grid of pre-defined search terms or filter values. User clicks one to select it. This is more practical for dashboards.

3. **Alphabet filter** — Show A-Z buttons. Clicking a letter filters data to items starting with that letter. Simple and effective.

## Date Picker Pattern

Uses two parameters: `SelectedYear` and `SelectedMonth`.

- Year arrows: Navigation action sets `SelectedYear` to year ± 1
- Month cells: Navigation action sets `SelectedMonth` to clicked month number
- Target dataset: Filter where `year(DateField) = ${SelectedYear} AND month(DateField) = ${SelectedMonth}`

**Limitation:** Year cycling requires pre-computed year values in the dataset (e.g., rows for 2024, 2025, 2026, 2027). You can't do arithmetic in navigation actions.

## Performance Notes

All controls should use:
```json
"chart": { "animation": false },
"plotOptions": { "series": { "animation": false } }
```

Keep datasets tiny (1-20 rows). Use SPICE. The bottleneck is QuickSight's parameter → re-query → re-render cycle, not the Highcharts rendering.

## Files

### HTML Test Pages
- `test-all-controls.html` — Basic controls (1-9)
- `test-advanced-controls.html` — Advanced controls (10-21)

### QuickSight Configs
- `quicksight-discrete-slider.json`
- `quicksight-star-rating.json`
- `quicksight-stepper.json`
- `quicksight-toggle-switch.json`
- `quicksight-color-swatch.json`
- `quicksight-progress-stepper.json`
- `quicksight-grid-selector.json`
- `quicksight-card-selector.json`
- `quicksight-radial-dial.json`
- `quicksight-multiselect-checkboxes.json`
- `quicksight-chip-selector.json`
- `quicksight-segmented-gauge.json`
- `quicksight-volume-bars.json`
- `quicksight-emoji-reaction.json`
- `quicksight-sort-control.json`

### Sample Datasets
- `control-data-*.csv` — One per control type
