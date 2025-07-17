# UnoArm Blockly Extension

A lightweight add-on that brings basic UnoArm controls into your Blockly workspace.

## Key Features

* **Configure Arm Geometry**
  Input the five primary link lengths to match your hardware setup.

* **Simplified Motion Blocks**
  High-level blocks let you move the arm to specified coordinates or angles without worrying about underlying trigonometry.

* **State Feedback**
  Read back the arm’s current position in a few clicks.

## Quick Start

1. **Install the Extension**
   Copy the extension folder into your Blockly (or OhStem) `extensions` directory.

2. **Add to Toolbox**
   Ensure your `toolbox.xml` includes the UnoArm category.

3. **Drag & Drop**

   * First, set your dimensions.
   * Then use the motion blocks to send the arm to a target.
   * Optionally read the current position with the feedback blocks.

4. **Generate & Run**
   Preview the Python code in your IDE or console and execute against the `kdi_unoarm` library.

## Notes

* Keep the setup block first to avoid runtime errors.
* Blocks are designed to work out of the box with the provided Python module—no extra tweaking needed.

---

**KDI EDUCATION**
