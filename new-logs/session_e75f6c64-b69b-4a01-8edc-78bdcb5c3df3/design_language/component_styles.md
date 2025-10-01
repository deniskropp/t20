# Qdrant Service Frontend Component Styles (Bootstrap 5 Aligned)

This document outlines the styling guidelines for common UI components, ensuring consistency and adherence to the Qdrant Service visual design language.

## General Principles:

*   **Minimalism:** Avoid unnecessary ornamentation. Focus on clean lines, ample whitespace, and clear visual hierarchy.
*   **Natural Aesthetic:** Incorporate soft curves where appropriate, and use the defined color palette to evoke a sense of calm and clarity.
*   **Bootstrap 5 Alignment:** Leverage Bootstrap 5's utility classes and component structure. Customizations should extend or override Bootstrap styles thoughtfully.
*   **Accessibility:** Ensure sufficient color contrast, focus states, and readable typography across all components.

## Color Usage:

*   **Primary:** Use for primary buttons, active states, navigation highlights, and key interactive elements.
*   **Secondary:** Use for secondary buttons, less critical actions, and informational callouts.
*   **Accent:** Reserve for prominent calls to action, important alerts, or to draw attention to specific features.
*   **Neutrals:** Form the backbone of the UI for backgrounds, text, borders, and dividers.

## Typography:

*   Utilize the defined `typography.json` for font families, sizes, weights, and line heights.
*   Ensure text elements have sufficient line height for readability (e.g., `1.6` for body text).
*   Maintain contrast ratios as defined in `typography.json` (min WCAG AA 4.5:1 for normal text, 3:1 for large text).

## Component Specifics:

### Buttons:

*   **Primary Button:**
    *   `bg-primary` (Deep Ocean Blue: `#0A2A4F`)
    *   `text-white`
    *   `border-0` (unless a subtle border is needed for definition)
    *   `rounded` (Bootstrap's default rounded corners, or slightly more rounded if needed)
    *   `hover`: Darker shade of primary or `primary` with `opacity-90`.
    *   `active`: Even darker shade or `primary` with `opacity-80`.
    *   `focus`: Bootstrap's default focus ring, ensuring high contrast.
*   **Secondary Button:**
    *   `bg-secondary` (Misty Seafoam: `#A3D7E1`)
    *   `text-primary` (Deep Ocean Blue: `#0A2A4F`)
    *   `border-0`
    *   `rounded`
    *   `hover`: Darker shade of secondary or `secondary` with `opacity-90`.
*   **Outline Button (Accent):**
    *   `btn-outline-accent` (Coral Sunset: `#FF8A65`)
    *   `text-accent`
    *   `border-accent`
    *   `hover`: `bg-accent`, `text-white`.

### Forms:

*   **Input Fields:**
    *   `form-control` (Bootstrap default)
    *   `border-neutral-medium` (`#CED4DA`)
    *   `focus`: Bootstrap's default focus ring, potentially using `primary` or `accent` color for the ring border.
    *   `bg-white` (`#F8F9FA`)
    *   `text-neutral-dark` (`#343A40`)
    *   `placeholder-color`: `neutral-medium`.
    *   `rounded`
*   **Labels:** Use `form-label` class with appropriate heading styles if needed, or standard body text styling.

### Cards:

*   Use Bootstrap's `card` component.
*   `bg-white` (`#F8F9FA`)
*   `border-0` (remove default border)
*   `shadow-sm` (subtle shadow for depth)
*   `rounded`
*   **Card Header/Footer:** Use neutral backgrounds (`#F8F9FA`) with `neutral-dark` text, or apply primary/secondary colors subtly.

### Navigation (Sidebar/Header):

*   **Header:**
    *   `bg-primary` (`#0A2A4F`)
    *   `text-white`
    *   Logo prominently displayed.
*   **Sidebar (if applicable):**
    *   `bg-light` (e.g., `neutral-light` or a slightly off-white)
    *   Navigation links should use `text-neutral-dark` with clear hover and active states using `primary` or `secondary` colors.
    *   Consider subtle dividers between sections.

### Tables:

*   Use Bootstrap's `table` classes.
*   `table-striped` with `bg-neutral-light` for alternate rows.
*   `border-neutral-medium` for table borders and cell dividers.
*   Header row: `bg-neutral-light`, `text-neutral-dark`, `font-weight-bold`.

### Modals:

*   Bootstrap modal structure.
*   `bg-white` for modal content.
*   `border-0`, `shadow-lg`.
*   Ensure close button (`.btn-close`) is clearly visible against the modal background.

### Alerts:

*   Use Bootstrap's alert classes (`.alert`).
*   Apply defined feedback colors (success, warning, danger).
*   Ensure text color has sufficient contrast against the background (e.g., `text-white` for darker alert backgrounds).

## Iconography:

*   **Style:** Use a clean, line-based icon set that complements the minimalist aesthetic (e.g., Feather Icons, Bootstrap Icons).
*   **Color:** Icons should generally use `text-neutral-dark`. Use `primary` or `accent` colors sparingly for emphasis or active states.
*   **Size:** Maintain consistent sizing, typically aligning with font sizes (e.g., 1.25rem or 1.5rem).
