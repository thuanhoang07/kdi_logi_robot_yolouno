// Định nghĩa block: Set dimensions
Blockly.Blocks['unoarm_set_dimensions'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Khai báo kích thước");
    this.appendValueInput("D1")
        .setCheck("Number")
        .appendField("d1");
    this.appendValueInput("D2")
        .setCheck("Number")
        .appendField("d2");
    this.appendValueInput("D3")
        .setCheck("Number")
        .appendField("d3");
    this.appendValueInput("D4")
        .setCheck("Number")
        .appendField("d4");
    this.appendValueInput("D5")
        .setCheck("Number")
        .appendField("d5");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(230);
    this.setTooltip("Set the five dimension parameters d1 to d5");
    this.setHelpUrl("");
  }
};

// Định nghĩa block: Check valid angles S2, S3 (value block)
Blockly.Blocks['unoarm_check_valid'] = {
  init: function() {
    // this.appendValueInput("S2")
    //     .setCheck("Number")
    //     .appendField("Check valid S2");
    // this.appendValueInput("S3")
    //     .setCheck("Number")
    //     .appendField("S3");
    this.appendDummyInput()
        .appendField("Kiểm tra tính hợp lệ của góc S2:");
    this.appendValueInput("S2")
        .setCheck("Number");
    this.appendDummyInput()
        .appendField("S3:");
    this.appendValueInput("S3")
        .setCheck("Number");
    // Quan trọng: khai báo là output block và kiểu Boolean
    this.setOutput(true, "Boolean");
    this.setColour(210);
    this.setTooltip("Returns true if the (S2, S3) angles are within valid range");
    this.setHelpUrl("");
  }
};

// Generator cho block Set dimensions
Blockly.Python['unoarm_set_dimensions'] = function(block) {
  Blockly.Python.definitions_['import_kdi_unoarm'] = 'import kdi_unoarm';
  var d1 = Blockly.Python.valueToCode(block, 'D1', Blockly.Python.ORDER_ATOMIC) || '0';
  var d2 = Blockly.Python.valueToCode(block, 'D2', Blockly.Python.ORDER_ATOMIC) || '0';
  var d3 = Blockly.Python.valueToCode(block, 'D3', Blockly.Python.ORDER_ATOMIC) || '0';
  var d4 = Blockly.Python.valueToCode(block, 'D4', Blockly.Python.ORDER_ATOMIC) || '0';
  var d5 = Blockly.Python.valueToCode(block, 'D5', Blockly.Python.ORDER_ATOMIC) || '0';
  return 'kdi_unoarm.set_dimensions(' + d1 + ', ' + d2 + ', ' + d3 + ', ' + d4 + ', ' + d5 + ')\n';
};

// Generator cho block Check valid S2, S3
Blockly.Python['unoarm_check_valid'] = function(block) {
  Blockly.Python.definitions_['import_kdi_unoarm'] = 'import kdi_unoarm';
  var s2 = Blockly.Python.valueToCode(block, 'S2', Blockly.Python.ORDER_ATOMIC) || '0';
  var s3 = Blockly.Python.valueToCode(block, 'S3', Blockly.Python.ORDER_ATOMIC) || '0';
  var code = 'kdi_unoarm.kiem_tra_tinh_hop_le(' + s2 + ', ' + s3 + ')';
  return [code, Blockly.Python.ORDER_FUNCTION_CALL];
};

// 1) Block: Go to S2, S3
Blockly.Blocks['unoarm_go_to_s2_s3'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Đi đến góc S2:");
    this.appendValueInput("TO_S2")
        .setCheck("Number");
    this.appendDummyInput()
        .appendField("S3:");
    this.appendValueInput("TO_S3")
        .setCheck("Number");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(230);
    this.setTooltip("Move the arm to the specified S2 and S3 angles");
    this.setHelpUrl("");
  }
};

// 2) Python generator cho block Go to S2, S3
Blockly.Python['unoarm_go_to_s2_s3'] = function(block) {
  // đảm bảo import module có ở definitions_ (nếu chưa có, thêm vào đầu file)
  Blockly.Python.definitions_['import_kdi_unoarm'] =
    'import kdi_unoarm\n' +
    'import math\n' + 'import time';

  var toS2 = Blockly.Python.valueToCode(block, 'TO_S2', Blockly.Python.ORDER_ATOMIC) || '0';
  var toS3 = Blockly.Python.valueToCode(block, 'TO_S3', Blockly.Python.ORDER_ATOMIC) || '0';
  return 'kdi_unoarm.go_to_S2_S3(' + toS2 + ', ' + toS3 + ')\n';
};

// 1. Định nghĩa block UNOARM_GO_TO_R_H
Blockly.Blocks['unoarm_go_to_r_h'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Di chuyển đến r:");
    this.appendValueInput("R")
        .setCheck("Number");
    this.appendDummyInput()
        .appendField("h:");
    this.appendValueInput("H")
        .setCheck("Number");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(230);
    this.setTooltip("Di chuyển UnoArm đến toạ độ (r, h)");
    this.setHelpUrl("");
  }
};

// 2. Python generator cho block UNOARM_GO_TO_R_H
Blockly.Python['unoarm_go_to_r_h'] = function(block) {
  var r = Blockly.Python.valueToCode(block, 'R', Blockly.Python.ORDER_ATOMIC) || '0';
  var h = Blockly.Python.valueToCode(block, 'H', Blockly.Python.ORDER_ATOMIC) || '0';
  Blockly.Python.definitions_['import_kdi_unoarm'] =
    'import kdi_unoarm\n' +
    'import math\n' + 'import time';  
  var code = 'kdi_unoarm.go_to_r_h(' + r + ', ' + h + ')\n';
  return code;
};

// --- Block: Get current r_now (Number) ---
Blockly.Blocks['unoarm_get_r_now'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Giá trị r hiện tại");
    this.setOutput(true, "Number");
    this.setColour(230);
    this.setTooltip("Trả về giá trị r_now hiện tại");
    this.setHelpUrl("");
  }
};
Blockly.Python['unoarm_get_r_now'] = function(block) {
  Blockly.Python.definitions_['import_kdi_unoarm'] = 'import kdi_unoarm';
  return ['kdi_unoarm.r_now', Blockly.Python.ORDER_ATOMIC];
};

// --- Block: Get current h_now (Number) ---
Blockly.Blocks['unoarm_get_h_now'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Giá trị h hiện tại");
    this.setOutput(true, "Number");
    this.setColour(230);
    this.setTooltip("Trả về giá trị h_now hiện tại");
    this.setHelpUrl("");
  }
};
Blockly.Python['unoarm_get_h_now'] = function(block) {
  Blockly.Python.definitions_['import_kdi_unoarm'] = 'import kdi_unoarm';
  return ['kdi_unoarm.h_now', Blockly.Python.ORDER_ATOMIC];
};

// --- Block: Get current S2 (Number) ---
Blockly.Blocks['unoarm_get_S2'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Giá trị S2 hiện tại");
    this.setOutput(true, "Number");
    this.setColour(230);
    this.setTooltip("Trả về giá trị S2 hiện tại");
    this.setHelpUrl("");
  }
};
Blockly.Python['unoarm_get_S2'] = function(block) {
  Blockly.Python.definitions_['import_kdi_unoarm'] = 'import kdi_unoarm';
  return ['kdi_unoarm.S2_now', Blockly.Python.ORDER_ATOMIC];
};

// --- Block: Get current h_now (Number) ---
Blockly.Blocks['unoarm_get_S3'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Giá trị S3 hiện tại");
    this.setOutput(true, "Number");
    this.setColour(230);
    this.setTooltip("Trả về giá trị S3 hiện tại");
    this.setHelpUrl("");
  }
};
Blockly.Python['unoarm_get_S3'] = function(block) {
  Blockly.Python.definitions_['import_kdi_unoarm'] = 'import kdi_unoarm';
  return ['kdi_unoarm.S3_now', Blockly.Python.ORDER_ATOMIC];
};
