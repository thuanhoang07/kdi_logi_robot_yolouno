// Định nghĩa block: reset_PID
Blockly.Blocks['logi_robot_reset_pid'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Reset PID");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(230);
    this.setTooltip("Reset tất cả các thông số PID");
    this.setHelpUrl("");
  }
};

// Generator cho block reset_PID
Blockly.Python['logi_robot_reset_pid'] = function(block) {
  Blockly.Python.definitions_['import_logi_robot'] = 'import logi_robot';
  return 'await logi_robot.reset_PID()\n';
};

// Định nghĩa block: stop
Blockly.Blocks['logi_robot_stop'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Dừng robot");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(230);
    this.setTooltip("Dừng cả hai động cơ");
    this.setHelpUrl("");
  }
};

// Generator cho block stop
Blockly.Python['logi_robot_stop'] = function(block) {
  Blockly.Python.definitions_['import_logi_robot'] = 'import logi_robot';
  return 'await logi_robot.stop()\n';
};

// Định nghĩa block: di_thang
Blockly.Blocks['logi_robot_di_thang'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Di chuyển thẳng");
    this.appendValueInput("quang_duong")
        .setCheck("Number")
        .appendField("quãng đường");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(230);
    this.setTooltip("Di chuyển thẳng với quãng đường chỉ định");
    this.setHelpUrl("");
  }
};

// Generator cho block di_thang
Blockly.Python['logi_robot_di_thang'] = function(block) {
  Blockly.Python.definitions_['import_logi_robot'] = 'import logi_robot';
  var quang_duong = Blockly.Python.valueToCode(block, 'quang_duong', Blockly.Python.ORDER_ATOMIC) || '0';
  return 'await logi_robot.di_thang(' + quang_duong + ')\n';
};

// Định nghĩa block: di_den_n4
Blockly.Blocks['logi_robot_di_den_n4'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Di đến ngã tư");
    this.appendValueInput("h")
        .setCheck("Number")
        .appendField("hướng");
    this.appendValueInput("k")
        .setCheck("Number")
        .appendField("ngã tư số");
    this.appendDummyInput()
        .appendField("hành động")
        .appendField(new Blockly.FieldDropdown([
          ["Dừng", "D"],
          ["Rẽ trái", "T"],
          ["Rẽ phải", "P"]
        ]), "hanh_dong");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(230);
    this.setTooltip("Di chuyển đến ngã tư chỉ định và thực hiện hành động");
    this.setHelpUrl("");
  }
};

// Generator cho block di_den_n4
Blockly.Python['logi_robot_di_den_n4'] = function(block) {
  Blockly.Python.definitions_['import_logi_robot'] = 'import logi_robot';
  var h = Blockly.Python.valueToCode(block, 'h', Blockly.Python.ORDER_ATOMIC) || '1';
  var k = Blockly.Python.valueToCode(block, 'k', Blockly.Python.ORDER_ATOMIC) || '1';
  var hanh_dong = block.getFieldValue('hanh_dong');
  return 'await logi_robot.di_den_n4(' + h + ', ' + k + ', "' + hanh_dong + '")\n';
};

// Định nghĩa block: chinh_thang_line
Blockly.Blocks['logi_robot_chinh_thang_line'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Chỉnh thẳng với line");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(230);
    this.setTooltip("Điều chỉnh robot thẳng với line đang dò");
    this.setHelpUrl("");
  }
};

// Generator cho block chinh_thang_line
Blockly.Python['logi_robot_chinh_thang_line'] = function(block) {
  Blockly.Python.definitions_['import_logi_robot'] = 'import logi_robot';
  return 'await logi_robot.chinh_thang_line()\n';
};

// Định nghĩa block: bam_line
Blockly.Blocks['logi_robot_bam_line'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Bám line");
    this.appendValueInput("toc_do")
        .setCheck("Number")
        .appendField("tốc độ");
    this.appendValueInput("he_so_chenh_lech")
        .setCheck("Number")
        .appendField("hệ số chênh lệch");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(230);
    this.setTooltip("Bám theo line với tốc độ và hệ số chênh lệch chỉ định");
    this.setHelpUrl("");
  }
};

// Generator cho block bam_line
Blockly.Python['logi_robot_bam_line'] = function(block) {
  Blockly.Python.definitions_['import_logi_robot'] = 'import logi_robot';
  var toc_do = Blockly.Python.valueToCode(block, 'toc_do', Blockly.Python.ORDER_ATOMIC) || '70';
  var he_so_chenh_lech = Blockly.Python.valueToCode(block, 'he_so_chenh_lech', Blockly.Python.ORDER_ATOMIC) || '30';
  return 'await logi_robot.bam_line(' + toc_do + ', ' + he_so_chenh_lech + ')\n';
};

// Định nghĩa block: doc_line
Blockly.Blocks['logi_robot_doc_line'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Đọc line");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(230);
    this.setTooltip("Đọc giá trị cảm biến line và tính toán vị trí");
    this.setHelpUrl("");
  }
};

// Generator cho block doc_line
Blockly.Python['logi_robot_doc_line'] = function(block) {
  Blockly.Python.definitions_['import_logi_robot'] = 'import logi_robot';
  return 'await logi_robot.doc_line()\n';
};

// Định nghĩa block: xoay_trai
Blockly.Blocks['logi_robot_xoay_trai'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Xoay trái");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(230);
    this.setTooltip("Xoay robot sang trái cho đến khi phát hiện line");
    this.setHelpUrl("");
  }
};

// Generator cho block xoay_trai
Blockly.Python['logi_robot_xoay_trai'] = function(block) {
  Blockly.Python.definitions_['import_logi_robot'] = 'import logi_robot';
  return 'await logi_robot.xoay_trai()\n';
};

// Định nghĩa block: xoay_phai
Blockly.Blocks['logi_robot_xoay_phai'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Xoay phải");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(230);
    this.setTooltip("Xoay robot sang phải cho đến khi phát hiện line");
    this.setHelpUrl("");
  }
};

// Generator cho block xoay_phai
Blockly.Python['logi_robot_xoay_phai'] = function(block) {
  Blockly.Python.definitions_['import_logi_robot'] = 'import logi_robot';
  return 'await logi_robot.xoay_phai()\n';
};

// Định nghĩa block: robot_chay_voi_toc_doc
Blockly.Blocks['logi_robot_robot_chay_voi_toc_doc'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Robot chạy với tốc độc");
    this.appendValueInput("rpm_trai")
        .setCheck("Number")
        .appendField("RPM trái");
    this.appendValueInput("rpm_phai")
        .setCheck("Number")
        .appendField("RPM phải");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(230);
    this.setTooltip("Điều khiển robot chạy với tốc độc RPM chỉ định cho bánh trái và phải");
    this.setHelpUrl("");
  }
};

// Generator cho block robot_chay_voi_toc_doc
Blockly.Python['logi_robot_robot_chay_voi_toc_doc'] = function(block) {
  Blockly.Python.definitions_['import_logi_robot'] = 'import logi_robot';
  var rpm_trai = Blockly.Python.valueToCode(block, 'rpm_trai', Blockly.Python.ORDER_ATOMIC) || '0';
  var rpm_phai = Blockly.Python.valueToCode(block, 'rpm_phai', Blockly.Python.ORDER_ATOMIC) || '0';
  return 'await logi_robot.robot_chay_voi_toc_doc(' + rpm_trai + ', ' + rpm_phai + ')\n';
};

// Định nghĩa block: set_toc_do_2_motor
Blockly.Blocks['logi_robot_set_toc_do_2_motor'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Đặt tốc độ 2 động cơ");
    this.appendValueInput("toc_do_mong_muon_motor_1")
        .setCheck("Number")
        .appendField("tốc độ mong muốn motor 1");
    this.appendValueInput("toc_do_mong_muon_motor_2")
        .setCheck("Number")
        .appendField("tốc độ mong muốn motor 2");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(230);
    this.setTooltip("Đặt tốc độ mong muốn cho 2 động cơ với điều khiển PID");
    this.setHelpUrl("");
  }
};

// Generator cho block set_toc_do_2_motor
Blockly.Python['logi_robot_set_toc_do_2_motor'] = function(block) {
  Blockly.Python.definitions_['import_logi_robot'] = 'import logi_robot';
  var toc_do_mong_muon_motor_1 = Blockly.Python.valueToCode(block, 'toc_do_mong_muon_motor_1', Blockly.Python.ORDER_ATOMIC) || '0';
  var toc_do_mong_muon_motor_2 = Blockly.Python.valueToCode(block, 'toc_do_mong_muon_motor_2', Blockly.Python.ORDER_ATOMIC) || '0';
  return 'await logi_robot.set_toc_do_2_motor(' + toc_do_mong_muon_motor_1 + ', ' + toc_do_mong_muon_motor_2 + ')\n';
};

// Thêm block để truy cập biến chênh lệch line
Blockly.Blocks['logi_robot_get_chenh_lech_line'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Chênh lệch line hiện tại");
    this.setOutput(true, "Number");
    this.setColour(230);
    this.setTooltip("Lấy giá trị chênh lệch line hiện tại");
    this.setHelpUrl("");
  }
};

Blockly.Python['logi_robot_get_chenh_lech_line'] = function(block) {
  Blockly.Python.definitions_['import_logi_robot'] = 'import logi_robot';
  return ['logi_robot.chenh_lech_line', Blockly.Python.ORDER_ATOMIC];
};

// Thêm block để truy cập biến hướng
Blockly.Blocks['logi_robot_get_huong'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Hướng hiện tại");
    this.setOutput(true, "Number");
    this.setColour(230);
    this.setTooltip("Lấy giá trị hướng hiện tại (1: đi tới, 0: đi lui)");
    this.setHelpUrl("");
  }
};

Blockly.Python['logi_robot_get_huong'] = function(block) {
  Blockly.Python.definitions_['import_logi_robot'] = 'import logi_robot';
  return ['logi_robot.huong', Blockly.Python.ORDER_ATOMIC];
};

// Thêm block để đặt biến hướng
Blockly.Blocks['logi_robot_set_huong'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Đặt hướng")
        .appendField(new Blockly.FieldDropdown([
          ["Đi tới", "1"],
          ["Đi lui", "0"]
        ]), "huong");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(230);
    this.setTooltip("Đặt hướng di chuyển (1: đi tới, 0: đi lui)");
    this.setHelpUrl("");
  }
};

Blockly.Python['logi_robot_set_huong'] = function(block) {
  Blockly.Python.definitions_['import_logi_robot'] = 'import logi_robot';
  var huong = block.getFieldValue('huong');
  return 'logi_robot.huong = ' + huong + '\n';
};