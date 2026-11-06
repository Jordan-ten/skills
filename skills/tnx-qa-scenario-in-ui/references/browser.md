# Driving the browser

Connection and dev login: `tnx-dev-mcp-local-dev`. What follows is only what makes a UI verdict
wrong when it is ignored.

## Traps that produce a false failure

**The same element is often rendered twice.** A modal can hold a sticky header and a visible
properties block that both render the same component. The accessibility snapshot may show only the
hidden copy, so a click or a hover lands on something the user cannot see and nothing happens.

Before interacting, keep only the visible instance:

```js
() => [...document.querySelectorAll('<selector>')]
  .filter(el => {
    const rect = el.getBoundingClientRect()
    const style = getComputedStyle(el)
    return rect.width > 0 && rect.height > 0
      && style.visibility !== 'hidden' && style.pointerEvents !== 'none' && style.opacity !== '0'
  })
```

A hidden copy usually sits under an ancestor with `pointer-events: none` or `opacity-0`, or is not
displayed (`display: none` gives a zero-size box).

**A tooltip is not in the accessibility snapshot.** Ant Design mounts it on hover, outside the
component. `take_snapshot` will not show it. Read it from the DOM instead:

```js
() => [...document.querySelectorAll('.ant-tooltip')]
  .filter(t => !t.classList.contains('ant-tooltip-hidden'))
  .map(t => t.innerText)
```

**Hovering through the snapshot uid can miss.** When `mcp__chrome-devtools__hover` gives no result,
dispatch the events on the element you picked yourself, then wait for the tooltip to mount:
`pointerover`, `mouseover`, `pointerenter`, `mouseenter`, `mousemove`, then ~1s.

**An empty dialog means it is still loading.** Wait for a text you expect (`wait_for`) before
reading a modal. Do not conclude on a snapshot taken too early.

## What counts as evidence

- A screenshot for anything visual (a layout, a tooltip, a truncated label).
- The text read from the DOM for a list, a label, a tooltip.
- `list_console_messages` with `types: ["error"]` for a scenario about an error.
- The test output when the scenario was checked by an automated test.

## Leave the app as you found it

The dev database is the user's. Do not submit a form, delete a record, or change a setting unless the
scenario is about that action and it was marked as a write in the step 1 list the user accepted. Close what you opened and go
back to the list screen at the end of the run.
