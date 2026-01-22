import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import socket
import datetime
import random
import time
import threading

# --- DỮ LIỆU TEST ---
FULL_DB = [
    # --- Huyết học (Group 1) ---
    {"group": 1, "code": "B-GROUP", "name": "Xác định nhóm máu (Hệ ABO, Rh)", "unit": "", "type": "b_type"},
    {"group": 1, "code": "HBA1C", "name": "Kiểm tra đường huyết 3 tháng", "unit": "%", "min": 4.0, "max": 6.4, "type": "range"},
    {"group": 1, "code": "WBC", "name": "Bach cau (WBC)", "unit": "mg/L", "min": 4.0, "max": 10.0, "type": "range"},
    {"group": 1, "code": "NEU", "name": "Bach cau trung tinh", "unit": "%", "min": 40, "max": 74, "type": "range"},
    {"group": 1, "code": "LYM", "name": "Bach cau Lympho", "unit": "%", "min": 19, "max": 48, "type": "range"},
    {"group": 1, "code": "RBC", "name": "Hong cau (RBC)", "unit": "T/L", "min": 4.0, "max": 5.5, "type": "range"},
    {"group": 1, "code": "HGB", "name": "Huyet sac to", "unit": "g/L", "min": 120, "max": 165, "type": "range"},
    {"group": 1, "code": "HCT", "name": "Hematocrit", "unit": "L/L", "min": 0.35, "max": 0.47, "type": "range"},
    {"group": 1, "code": "MCV", "name": "The tich TB HC", "unit": "fL", "min": 80, "max": 100, "type": "range"},
    {"group": 1, "code": "MCH", "name": "Luong HGB TB HC", "unit": "pg", "min": 27, "max": 32, "type": "range"},
    {"group": 1, "code": "PLT", "name": "Tieu cau (PLT)", "unit": "G/L", "min": 150, "max": 450, "type": "range"},

    # --- Sinh hóa (Group 2) ---
    {"group": 2, "code": "GLU", "name": "Glucose", "unit": "mmol/L", "min": 3.9, "max": 6.1, "type": "range"},
    {"group": 2, "code": "URE", "name": "Urea", "unit": "mmol/L", "min": 2.5, "max": 7.5, "type": "range"},
    {"group": 2, "code": "CRE", "name": "Creatinine", "unit": "umol/L", "min": 53, "max": 115, "type": "range"},
    {"group": 2, "code": "AST", "name": "AST (SGOT)", "unit": "U/L", "max": 40, "type": "upper_limit"},
    {"group": 2, "code": "ALT", "name": "ALT (SGPT)", "unit": "U/L", "max": 40, "type": "upper_limit"},
    {"group": 2, "code": "GGT", "name": "GGT", "unit": "U/L", "min": 5, "max": 60, "type": "range"},
    {"group": 2, "code": "CHO", "name": "Cholesterol", "unit": "mmol/L", "max": 5.2, "type": "upper_limit"},
    {"group": 2, "code": "TRI", "name": "Triglyceride", "unit": "mmol/L", "max": 1.7, "type": "upper_limit"},
    {"group": 2, "code": "HDL", "name": "HDL-C", "unit": "mmol/L", "min": 0.9, "type": "lower_limit"},
    {"group": 2, "code": "LDL", "name": "LDL-C", "unit": "mmol/L", "max": 3.4, "type": "upper_limit"},

    # --- Nước tiểu (Group 3) ---
    {"group": 3, "code": "U_LEU", "name": "Urine Leukocytes", "unit": "/uL", "type": "qualitative"},
    {"group": 3, "code": "U_NIT", "name": "Nitrite", "unit": "", "type": "qualitative"},
    {"group": 3, "code": "U_URO", "name": "Urobilinogen", "unit": "mg/dL", "min": 0.2, "max": 1.0, "type": "range"},
    {"group": 3, "code": "U_PRO", "name": "Protein", "unit": "mg/dL", "type": "qualitative"},
    {"group": 3, "code": "U_PH",  "name": "pH", "unit": "", "min": 5.0, "max": 8.0, "type": "range_1decimal"},
    {"group": 3, "code": "U_BLD", "name": "Blood", "unit": "/uL", "type": "qualitative"},
    {"group": 3, "code": "U_SG",  "name": "Specific Gravity", "unit": "", "min": 1.005, "max": 1.030, "type": "range_3decimal"},
    {"group": 3, "code": "U_KET", "name": "Ketone", "unit": "mg/dL", "type": "qualitative"},
    {"group": 3, "code": "U_BIL", "name": "Bilirubin", "unit": "", "type": "qualitative"},
    {"group": 3, "code": "U_GLU", "name": "Urine Glucose", "unit": "mg/dL", "type": "qualitative"},

    # --- Miễn dịch & Vi sinh (Group 4) ---
    {"group": 4, "code": "HBsAg", "name": "HBsAg", "unit": "S/CO", "type": "qualitative"},
    {"group": 4, "code": "AHCV", "name": "Anti-HCV", "unit": "S/CO", "type": "qualitative"},
    {"group": 4, "code": "HIV", "name": "HIV Ab/Ag", "unit": "S/CO", "type": "qualitative"},
    {"group": 4, "code": "HP-AB", "name": "HP-AB", "unit": "U/mL", "type": "qualitative"},
    {"group": 4, "code": "CRP", "name": "CRP", "unit": "mg/L", "min": 0, "max": 5, "type": "range"},
]


def get_random_result(test_config, abnormal_rate=0.1):
    t_type = test_config.get("type", "range")
    is_abnormal = random.random() < abnormal_rate

    if t_type == "qualitative":
        if is_abnormal: return random.choice(["Dương tính", "Dương tính +"])
        return "Âm tính"

    if t_type == "b_type":
        if is_abnormal: return random.choice(["A", "B", "AB", "O"])
        return "O"

    val = 0.0
    if t_type == "range":
        val = random.uniform(test_config["min"], test_config["max"])
        if is_abnormal: val = val * random.choice([0.8, 1.2])
    elif t_type == "range_1decimal": val = random.uniform(test_config["min"], test_config["max"]); return "{:.1f}".format(val)
    elif t_type == "range_3decimal": val = random.uniform(test_config["min"], test_config["max"]); return "{:.3f}".format(val)
    elif t_type == "upper_limit": val = random.uniform(0, test_config["max"])
    elif t_type == "lower_limit": val = random.uniform(test_config["min"], test_config["min"]*1.5)
   
    if val > 100: return str(int(val))
    return "{:.2f}".format(val)

def create_oru_message(barcode_id, test_info, result_value):
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    msh = f"MSH|^~\\&|GUI_SIM|LAB|LIS|HOST|{now}||ORU^R01|MSG{now}|P|2.3|||AL|NE\r"
    pid = f"PID|1||{barcode_id}||GUI^PATIENT||19900101|M||||||||||||||||||\r"
    obr = f"OBR|1||{barcode_id}|{test_info['code']}^{test_info['name']}^L|||{now}||||||||||||F\r"
    obx = f"OBX|1|ST|{test_info['code']}^{test_info['name']}^L||{result_value}|{test_info['unit']}||N|||F|||{now}\r"
    return msh + pid + obr + obx

def send_hl7_socket(ip, port, msg):
    try:
        framed_msg = b'\x0B' + msg.encode('utf-8') + b'\x1C\r'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((ip, int(port)))
            s.sendall(framed_msg)
        return True, "OK"
    except Exception as e:
        return False, str(e)

# --- GUI ---
class HL7SimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tool giả lập máy xét nghiệm")
        self.root.geometry("600x650")
       
        # 0. Cấu hình Kết nối (Vẫn để trên cùng để dễ chỉnh IP)
        frame_config = ttk.LabelFrame(root, text="Cấu hình Kết nối (Server)")
        frame_config.pack(padx=10, pady=5, fill="x")
       
        ttk.Label(frame_config, text="IP:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_ip = ttk.Entry(frame_config)
        self.entry_ip.insert(0, "192.168.0.102")
        self.entry_ip.grid(row=0, column=1, padx=5, pady=5)
       
        ttk.Label(frame_config, text="Port:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_port = ttk.Entry(frame_config, width=10)
        self.entry_port.insert(0, "5000")
        self.entry_port.grid(row=0, column=3, padx=5, pady=5)

        # Chọn máy xét nghiệm
        frame_machines = ttk.LabelFrame(root, text="1. Chọn máy xét nghiệm")
        frame_machines.pack(padx=10, pady=5, fill="x")

        self.var_hem = tk.BooleanVar(value=False)
        self.var_bio = tk.BooleanVar(value=False)
        self.var_uri = tk.BooleanVar(value=False)
        self.var_imv = tk.BooleanVar(value=False)

        chk_hem = ttk.Checkbutton(frame_machines, text="Huyết học", variable=self.var_hem)
        chk_hem.pack(side="left", padx=20, pady=10)

        chk_bio = ttk.Checkbutton(frame_machines, text="Sinh hóa", variable=self.var_bio)
        chk_bio.pack(side="left", padx=20, pady=10)

        chk_uri = ttk.Checkbutton(frame_machines, text="Nước tiểu", variable=self.var_uri)
        chk_uri.pack(side="left", padx=20, pady=10)

        chk_imv = ttk.Checkbutton(frame_machines, text="Miễn dịch & Vi sinh", variable=self.var_imv)
        chk_imv.pack(side="left", padx=20, pady=10)

        # Nhập mã mẫu
        frame_patient = ttk.LabelFrame(root, text="2. Nhập mã mẫu")
        frame_patient.pack(padx=10, pady=5, fill="x")
       
        self.entry_barcode = ttk.Entry(frame_patient, font=('Arial', 11), width=20)
        self.entry_barcode.pack(side="left", padx=10, pady=10)
        self.entry_barcode.focus()

        # Nút chạy máy
        btn_style = ttk.Style()
        btn_style.configure('Run.TButton', font=('Arial', 10, 'bold'), foreground='green')

        self.btn_run = ttk.Button(root, text="▶ CHẠY MÁY", style='Run.TButton',
                                  command=self.on_run_click)
        # ipady làm nút cao hơn cho dễ bấm
        self.btn_run.pack(padx=10, pady=10, fill="x", ipady=5)

        #Log
        ttk.Label(root, text="Nhật ký (Log):").pack(padx=10, anchor="w")
        self.log_area = scrolledtext.ScrolledText(root, height=12, state='disabled')
        self.log_area.pack(padx=10, pady=5, fill="both", expand=True)
       
        btn_clear = ttk.Button(root, text="Xóa Log", command=self.clear_log)
        btn_clear.pack(pady=5)

    def log(self, msg):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, msg + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def clear_log(self):
        self.log_area.config(state='normal')
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state='disabled')

    def on_run_click(self):
        ip = self.entry_ip.get()
        port = self.entry_port.get()
        barcode = self.entry_barcode.get().strip()
       
        if not barcode:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã mẫu!")
            self.entry_barcode.focus()
            return

        selected_groups = []
        if self.var_hem.get(): selected_groups.append(1)
        if self.var_bio.get(): selected_groups.append(2)
        if self.var_uri.get(): selected_groups.append(3)
        if self.var_imv.get(): selected_groups.append(4)

        if not selected_groups:
            messagebox.showwarning("Chưa chọn máy", "Vui lòng chọn ít nhất một máy xét nghiệm!")
            return

        self.btn_run.config(state="disabled")
        t = threading.Thread(target=self.sending_process, args=(ip, port, barcode, selected_groups))
        t.start()

    def sending_process(self, ip, port, barcode, selected_groups):
        self.log("=" * 45)
       
       
        tests_to_run = [t for t in FULL_DB if t['group'] in selected_groups]
       
        active_machines = []
        if 1 in selected_groups: active_machines.append("Huyết học")
        if 2 in selected_groups: active_machines.append("Sinh hóa")
        if 3 in selected_groups: active_machines.append("Nước tiểu")
       
        self.log(f"Máy đang chạy: {', '.join(active_machines)}")
        self.log(f"Tổng số xét nghiệm: {len(tests_to_run)}")
        self.log(f"BẮT ĐẦU PHÂN TÍCH... Mã mẫu: {barcode}")

        self.log(f"ĐÃ PHÂN TÍCH XONG! Mã mẫu: {barcode}")

        self.log(f"BẮT ĐẦU GỬI KẾT QUẢ... Mã mẫu: {barcode}")
        self.log("-" * 45)

        count_ok = 0
        total = len(tests_to_run)

        for i, t in enumerate(tests_to_run):
            res = get_random_result(t)
            msg = create_oru_message(barcode, t, res)
            success, err_msg = send_hl7_socket(ip, port, msg)
           
            if success:
                self.log(f"[{i+1}/{total}] {t['code']:<6} : {res:<6} {t['unit']:<6} -> PASS")
                count_ok += 1
            else:
                self.log(f"[{i+1}/{total}] {t['code']:<6} : LỖI ({err_msg})")
           
            time.sleep(0.1)
           
        self.log("-" * 45)
        self.log(f"HOÀN TẤT: {count_ok}/{total} thành công.")
       
        self.root.after(0, lambda: self.btn_run.config(state="normal"))

if __name__ == "__main__":
    root = tk.Tk()
    app = HL7SimulatorApp(root)
    root.mainloop()

