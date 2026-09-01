# 10 Figure and Table Engine

## Purpose

Generate publication-quality or thesis-quality visuals that support real arguments.

## Before Drawing

For every figure/table, define:

- purpose;
- claim supported;
- audience;
- data source;
- required elements;
- paper/thesis placement;
- caption logic;
- reproducibility status.

Also define:

- final physical size and expected viewing context;
- plot/table/schematic role and why it is preferable to alternatives;
- statistical annotation and uncertainty source;
- editable source format and required raster/vector exports;
- color, grayscale, contrast, and accessibility constraints;
- source-data and code path.

## Common Figures

- Figure 1: central idea / motivation / pipeline.
- Method pipeline.
- Architecture diagram.
- Experimental result table.
- Ablation table.
- Performance plot.
- Robustness/sensitivity plot.
- Case study / error analysis.
- System architecture / module diagram for graduation project.
- UI/demo screenshots for graduation project.

## Quality Gate

A figure is not ready unless:

- readable at paper size;
- labels and units are clear;
- caption states the takeaway;
- scales are not misleading;
- data source is known;
- schematic vs actual result is clearly distinguished;
- figure supports a real argument.

The gate also requires:

- rendered inspection at final size, not only source-code review;
- consistent typography, terminology, panel labels, units, precision, and legend order;
- uncertainty intervals and sample sizes shown where they affect interpretation;
- colorblind-safe encoding with a non-color cue when categories or direction matter;
- no clipped labels, distorted images, unreadable dense panels, or unsupported decoration;
- editable source plus export metadata, software/backend, and regeneration command;
- cross-check against manuscript numbers, captions, and source data.

## Tooling

Use external figure tools if helpful, but validate outputs. Do not use AI-generated decorative figures as scientific evidence.

Resolve `nature-figure` for venue-specific high-impact figure production or `scientific-visualization` for general publication visualization when installed and suitable. Follow the selected provider's backend, layout, export, and QA instructions in full.
