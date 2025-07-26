# Funny Images for RPM Overflow

This folder contains images that will be displayed when the RPM sensor overflows.

## Supported image names:
- `rpm_overflow.png` (preferred)
- `rpm_overflow.jpg`
- `funny.png`
- `funny.jpg`

## Image requirements:
- **Format**: PNG or JPG
- **Recommended size**: 300x200 pixels or smaller
- **Content**: Any funny image you want to show when RPM goes crazy!

## Examples of good images:
- Memes about broken sensors
- Funny car-related images
- "This is fine" dog meme
- Surprised Pikachu face
- Any humorous reaction image

## How to add your image:
1. Put your funny image file in this folder
2. Name it one of the supported names above
3. The dashboard will automatically display it when RPM overflow occurs

## Current setup:
The popup will try to load images in this order:
1. `rpm_overflow.png`
2. `rpm_overflow.jpg` 
3. `funny.png`
4. `funny.jpg`

If no image is found, it will show a text-based fallback message.
