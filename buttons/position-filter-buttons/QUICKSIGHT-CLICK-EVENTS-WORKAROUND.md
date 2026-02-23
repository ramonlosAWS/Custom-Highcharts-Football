# QuickSight Embedded Dashboard Click Events - Workaround Guide

## The Problem

QuickSight's embedded dashboards do NOT emit click events from Highcharts visuals (or most native visuals) to the embedding SDK. The events you listed:

- `SELECTION_CHANGED` - Only fires for native QuickSight controls
- `Q_SELECTION_CHANGED` - Q&A specific
- `VISUAL_CLICKED` - Not implemented for Highcharts
- `CLICK` - Not propagated from iframe
- `FILTER_CHANGED` - Only fires when filters change via controls
- `DRILL_DOWN` / `DRILL_UP` - Native drill actions only
- `CONTENT_LOADED` - ✅ Works
- `PARAMETERS_CHANGED` - ✅ Works
- `SELECTED_SHEET_CHANGED` - ✅ Works
- `VISUAL_INTERACTION` - Limited support
- `DATA_POINT_CLICKED` - Not propagated from Highcharts
- `CHART_ELEMENT_CLICKED` - Not propagated from Highcharts

**Root Cause:** The Highcharts visual runs inside a sandboxed iframe. The `["triggerClick", {...}]` action only triggers QuickSight's internal filter/action system - it does NOT emit events to the embedding SDK.

## Working Events

These events DO propagate to the embedding SDK:

| Event | Description |
|-------|-------------|
| `CONTENT_LOADED` | Dashboard finished loading |
| `PARAMETERS_CHANGED` | Parameter values changed |
| `SELECTED_SHEET_CHANGED` | User switched sheets |
| `ERROR_OCCURRED` | Error in dashboard |

## Recommended Solutions

### Solution 1: Overlay Buttons (Best for Custom UI)

Render your custom buttons OUTSIDE the QuickSight iframe, in your micro-app's DOM:

```javascript
// Your micro-app code
const buttonBar = document.createElement('div');
buttonBar.style.cssText = `
  position: absolute;
  top: 10px;
  left: 20px;
  z-index: 1000;
  display: flex;
  gap: 8px;
`;

const positions = ['ALL', 'QB', 'RB', 'WR', 'TE', 'OT', 'IOL', 'DT', 'EDGE', 'LB', 'S', 'CB', 'ST'];

positions.forEach(pos => {
  const btn = document.createElement('button');
  btn.textContent = pos;
  btn.onclick = () => handlePositionFilter(pos);
  buttonBar.appendChild(btn);
});

dashboardWrapper.appendChild(buttonBar);

function handlePositionFilter(position) {
  // Use QuickSight SDK to set parameters
  embeddedDashboard.setParameters([
    { Name: 'PositionFilter', Values: position === 'ALL' ? [] : [position] }
  ]);
}
```

**Pros:**
- Full control over click events
- No iframe restrictions
- Can style buttons however you want
- Immediate response (no iframe latency)

**Cons:**
- Buttons are outside QuickSight (positioning requires care)
- Need to sync visual state manually

### Solution 2: Parameter-Based Communication

Use QuickSight parameters as the communication channel:

**In QuickSight:**
1. Create a parameter: `PositionFilter` (String, multi-value)
2. Create a control linked to the parameter (can be hidden)
3. Use the parameter in visual filters

**In Your Micro-App:**
```javascript
// Set parameter from your app
embeddedDashboard.setParameters([
  { Name: 'PositionFilter', Values: ['QB'] }
]);

// Listen for parameter changes (this DOES work)
embeddedDashboard.on('PARAMETERS_CHANGED', (event) => {
  const positionParam = event.changedParameters?.find(p => p.Name === 'PositionFilter');
  if (positionParam) {
    updateUIState(positionParam.Values[0]);
  }
});
```

**Pros:**
- Uses QuickSight's native parameter system
- Bi-directional communication
- Works with QuickSight's filter cascade

**Cons:**
- Requires parameter setup in QuickSight
- Slight latency for parameter propagation

### Solution 3: Hybrid Approach (Recommended)

Combine both approaches:

1. **Visual Display:** Use Highcharts for visual styling (shows current state)
2. **Interaction:** Overlay transparent click targets or use native QuickSight controls
3. **Communication:** Use parameters for state sync

```javascript
// Overlay invisible click targets over the Highcharts visual
const clickOverlay = document.createElement('div');
clickOverlay.style.cssText = `
  position: absolute;
  top: 50px;  /* Position over the Highcharts buttons */
  left: 20px;
  display: flex;
  gap: 8px;
`;

positions.forEach((pos, index) => {
  const clickTarget = document.createElement('div');
  clickTarget.style.cssText = `
    width: 60px;
    height: 40px;
    cursor: pointer;
    /* transparent - the Highcharts visual shows through */
  `;
  clickTarget.onclick = () => handlePositionFilter(pos);
  clickOverlay.appendChild(clickTarget);
});
```

### Solution 4: URL Actions (Limited Use)

QuickSight supports URL actions that can call external URLs:

**In QuickSight Analysis:**
```json
{
  "Actions": [{
    "CustomActionId": "position-callback",
    "Name": "Position Callback",
    "Status": "ENABLED",
    "Trigger": "DATA_POINT_CLICK",
    "ActionOperations": [{
      "URLOperation": {
        "URLTarget": "NEW_TAB",
        "URLTemplate": "javascript:window.parent.postMessage({type:'POSITION_CLICK',position:'<<Position>>'},'*')"
      }
    }]
  }]
}
```

**Note:** This approach is unreliable and may be blocked by browser security policies.

## QuickSight Setup for Parameter-Based Solution

### 1. Create Parameter

In QuickSight Analysis:
- Parameters → Create parameter
- Name: `PositionFilter`
- Data type: String
- Default: (empty or "ALL")

### 2. Create Control (Optional - Can Be Hidden)

- Add control → Parameter control
- Link to `PositionFilter` parameter
- Style: Dropdown or Button group
- Can set visibility to hidden if using overlay buttons

### 3. Create Filter Using Parameter

- Add filter to your visual
- Field: Position
- Filter type: Custom filter
- Condition: Equals parameter `PositionFilter`
- Handle null: Show all when parameter is empty

### 4. Embedding SDK Setup

```javascript
import { createEmbeddingContext } from 'amazon-quicksight-embedding-sdk';

async function initDashboard() {
  const context = await createEmbeddingContext();
  
  const dashboard = await context.embedDashboard({
    url: EMBED_URL,
    container: document.getElementById('dashboard-container'),
    parameters: [
      { Name: 'PositionFilter', Values: ['ALL'] }
    ]
  });
  
  // Listen for parameter changes
  dashboard.on('PARAMETERS_CHANGED', handleParameterChange);
  
  return dashboard;
}

function handleParameterChange(event) {
  console.log('Parameters changed:', event);
  // Update your UI state based on new parameter values
}
```

## Complete Working Example

See `embedded-overlay-buttons.html` for a complete implementation demonstrating:
- Overlay button rendering
- Click handling
- SDK integration pattern
- Event logging

## Summary

| Approach | Complexity | Reliability | UX Quality |
|----------|------------|-------------|------------|
| Overlay Buttons | Low | High | Excellent |
| Parameter Communication | Medium | High | Good |
| Hybrid | Medium | High | Excellent |
| URL Actions | High | Low | Poor |

**Recommendation:** Use the **Overlay Buttons** approach for custom button interactions, combined with **Parameter Communication** for state synchronization. This gives you full control over click events while maintaining integration with QuickSight's filtering system.

## Files

- `embedded-overlay-buttons.html` - Complete working example
- `quicksight-position-filter-buttons.json` - Highcharts config (for visual display only)
- `QUICKSIGHT-CLICK-EVENTS-WORKAROUND.md` - This document
