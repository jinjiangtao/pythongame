import tkinter as tk
from tkinter import ttk, messagebox, Menu
import datetime

class MainView:
    VERSION = "V2.0"
    
    def __init__(self, root):
        self.root = root
        self.root.title("员工考勤管理系统 " + self.VERSION)
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        
        self.setup_styles()
        self.create_menu()
        self.create_widgets()
        self.update_status_time()
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('Header.TFrame', background='#4A6FA5')
        self.style.configure('Sidebar.TFrame', background='#F5F7FA')
        self.style.configure('Content.TFrame', background='#FFFFFF')
        self.style.configure('Status.TFrame', background='#E8ECF0')
        
        self.style.configure('Sidebar.TButton', 
                            background='#F5F7FA',
                            foreground='#333333',
                            borderwidth=0,
                            padding=12,
                            font=('Microsoft YaHei', 10))
        self.style.map('Sidebar.TButton',
                       background=[('active', '#E0E5EC'), ('selected', '#4A6FA5')],
                       foreground=[('selected', '#FFFFFF')])
        
        self.style.configure('Header.TLabel', 
                            background='#4A6FA5', 
                            foreground='#FFFFFF',
                            font=('Microsoft YaHei', 12, 'bold'))
        
        self.style.configure('Status.TLabel',
                            background='#E8ECF0',
                            foreground='#666666',
                            font=('Microsoft YaHei', 9))
        
        self.style.configure('Title.TLabel',
                            background='#FFFFFF',
                            foreground='#333333',
                            font=('Microsoft YaHei', 14, 'bold'))
        
        self.style.configure('Treeview',
                            background='#FFFFFF',
                            foreground='#333333',
                            rowheight=24,
                            font=('Microsoft YaHei', 9))
        self.style.configure('Treeview.Heading',
                            background='#F5F7FA',
                            foreground='#333333',
                            font=('Microsoft YaHei', 10, 'bold'))
        
        self.style.map('Treeview',
                       background=[('selected', '#4A6FA5')],
                       foreground=[('selected', '#FFFFFF')])
        
        self.style.configure('Accent.TButton',
                            background='#4A6FA5',
                            foreground='#FFFFFF',
                            font=('Microsoft YaHei', 10),
                            padding=6)
        self.style.map('Accent.TButton',
                       background=[('active', '#3D5A8A')])
        
        self.style.configure('Warning.TButton',
                            background='#E74C3C',
                            foreground='#FFFFFF',
                            font=('Microsoft YaHei', 10),
                            padding=6)
        self.style.map('Warning.TButton',
                       background=[('active', '#C0392B')])
        
    def create_menu(self):
        self.menubar = Menu(self.root)
        
        self.sys_menu = Menu(self.menubar, tearoff=0)
        self.sys_menu.add_command(label="数据备份", command=self.on_backup)
        self.sys_menu.add_command(label="数据清空", command=self.on_clear_data)
        self.sys_menu.add_separator()
        self.sys_menu.add_command(label="退出", command=self.on_exit)
        self.menubar.add_cascade(label="系统", menu=self.sys_menu)
        
        self.emp_menu = Menu(self.menubar, tearoff=0)
        self.emp_menu.add_command(label="员工列表", command=self.on_employee_list)
        self.emp_menu.add_command(label="新增员工", command=self.on_add_employee)
        self.menubar.add_cascade(label="员工管理", menu=self.emp_menu)
        
        self.att_menu = Menu(self.menubar, tearoff=0)
        self.att_menu.add_command(label="打卡", command=self.on_checkin)
        self.att_menu.add_command(label="考勤记录", command=self.on_attendance_list)
        self.menubar.add_cascade(label="考勤管理", menu=self.att_menu)
        
        self.stat_menu = Menu(self.menubar, tearoff=0)
        self.stat_menu.add_command(label="个人统计", command=self.on_personal_stats)
        self.stat_menu.add_command(label="部门统计", command=self.on_department_stats)
        self.menubar.add_cascade(label="数据统计", menu=self.stat_menu)
        
        self.help_menu = Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="操作日志", command=self.on_logs)
        self.help_menu.add_command(label="关于", command=self.on_about)
        self.menubar.add_cascade(label="帮助", menu=self.help_menu)
        
        self.root.config(menu=self.menubar)
        
    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.header_frame = ttk.Frame(self.main_frame, style='Header.TFrame', height=60)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)
        self.header_frame.pack_propagate(False)
        
        self.header_title = ttk.Label(self.header_frame, text="员工考勤管理系统", style='Header.TLabel')
        self.header_title.pack(side=tk.LEFT, padx=20, pady=18)
        
        self.header_user = ttk.Label(self.header_frame, text="登录状态: 管理员", style='Header.TLabel')
        self.header_user.pack(side=tk.RIGHT, padx=20, pady=18)
        
        self.sidebar_frame = ttk.Frame(self.main_frame, style='Sidebar.TFrame', width=180)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)
        
        self.sidebar_separator = ttk.Separator(self.sidebar_frame, orient=tk.HORIZONTAL)
        self.sidebar_separator.pack(fill=tk.X, pady=10)
        
        self.create_sidebar_buttons()
        
        self.content_frame = ttk.Frame(self.main_frame, style='Content.TFrame')
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_employee_tab()
        self.create_checkin_tab()
        self.create_attendance_tab()
        self.create_statistics_tab()
        
        self.status_frame = ttk.Frame(self.root, style='Status.TFrame', height=30)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_frame.pack_propagate(False)
        
        self.status_time = ttk.Label(self.status_frame, text="", style='Status.TLabel')
        self.status_time.pack(side=tk.LEFT, padx=15)
        
        self.status_separator1 = ttk.Label(self.status_frame, text="|", style='Status.TLabel')
        self.status_separator1.pack(side=tk.LEFT, padx=5)
        
        self.status_login = ttk.Label(self.status_frame, text="登录状态: 在线", style='Status.TLabel')
        self.status_login.pack(side=tk.LEFT, padx=5)
        
        self.status_separator2 = ttk.Label(self.status_frame, text="|", style='Status.TLabel')
        self.status_separator2.pack(side=tk.LEFT, padx=5)
        
        self.status_message = ttk.Label(self.status_frame, text="就绪", style='Status.TLabel')
        self.status_message.pack(side=tk.LEFT, padx=5)
        
        self.status_separator3 = ttk.Label(self.status_frame, text="|", style='Status.TLabel')
        self.status_separator3.pack(side=tk.LEFT, padx=5)
        
        self.status_version = ttk.Label(self.status_frame, text=f"版本: {self.VERSION}", style='Status.TLabel')
        self.status_version.pack(side=tk.RIGHT, padx=15)
        
    def create_sidebar_buttons(self):
        self.sidebar_buttons = []
        
        emp_icon = tk.PhotoImage(width=24, height=24)
        check_icon = tk.PhotoImage(width=24, height=24)
        record_icon = tk.PhotoImage(width=24, height=24)
        stat_icon = tk.PhotoImage(width=24, height=24)
        
        self.emp_btn = ttk.Button(self.sidebar_frame, text="员工管理", style='Sidebar.TButton',
                                  compound=tk.TOP, image=emp_icon, command=self.switch_to_employee)
        self.emp_btn.image = emp_icon
        self.emp_btn.pack(fill=tk.X, padx=5, pady=2)
        self.sidebar_buttons.append(self.emp_btn)
        
        self.check_btn = ttk.Button(self.sidebar_frame, text="考勤打卡", style='Sidebar.TButton',
                                    compound=tk.TOP, image=check_icon, command=self.switch_to_checkin)
        self.check_btn.image = check_icon
        self.check_btn.pack(fill=tk.X, padx=5, pady=2)
        self.sidebar_buttons.append(self.check_btn)
        
        self.record_btn = ttk.Button(self.sidebar_frame, text="考勤记录", style='Sidebar.TButton',
                                     compound=tk.TOP, image=record_icon, command=self.switch_to_attendance)
        self.record_btn.image = record_icon
        self.record_btn.pack(fill=tk.X, padx=5, pady=2)
        self.sidebar_buttons.append(self.record_btn)
        
        self.stat_btn = ttk.Button(self.sidebar_frame, text="数据统计", style='Sidebar.TButton',
                                    compound=tk.TOP, image=stat_icon, command=self.switch_to_statistics)
        self.stat_btn.image = stat_icon
        self.stat_btn.pack(fill=tk.X, padx=5, pady=2)
        self.sidebar_buttons.append(self.stat_btn)
        
    def create_employee_tab(self):
        self.employee_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.employee_tab, text='员工管理')
        
        self.emp_search_frame = ttk.Frame(self.employee_tab)
        self.emp_search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(self.emp_search_frame, text="工号:").pack(side=tk.LEFT, padx=5)
        self.emp_id_entry = ttk.Entry(self.emp_search_frame, width=12)
        self.emp_id_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.emp_search_frame, text="姓名:").pack(side=tk.LEFT, padx=5)
        self.emp_name_entry = ttk.Entry(self.emp_search_frame, width=12)
        self.emp_name_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.emp_search_frame, text="部门:").pack(side=tk.LEFT, padx=5)
        self.emp_dept_combo = ttk.Combobox(self.emp_search_frame, width=12, state='readonly')
        self.emp_dept_combo.pack(side=tk.LEFT, padx=5)
        
        self.search_emp_btn = ttk.Button(self.emp_search_frame, text="查询", style='Accent.TButton', width=8)
        self.search_emp_btn.pack(side=tk.LEFT, padx=10)
        
        self.reset_emp_btn = ttk.Button(self.emp_search_frame, text="重置", width=8)
        self.reset_emp_btn.pack(side=tk.LEFT, padx=5)
        
        self.emp_form_frame = ttk.Frame(self.employee_tab)
        self.emp_form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        fields = [
            ('工号', 'emp_id_form', 15),
            ('姓名', 'emp_name_form', 15),
            ('部门', 'emp_dept_form', 15),
            ('职位', 'emp_pos_form', 15),
            ('电话', 'emp_phone_form', 15),
            ('邮箱', 'emp_email_form', 20),
            ('入职日期', 'emp_hire_form', 12),
            ('状态', 'emp_status_combo', 10)
        ]
        
        self.emp_form_entries = {}
        for i, (label, name, width) in enumerate(fields):
            ttk.Label(self.emp_form_frame, text=label).grid(row=0, column=i*2, padx=5, pady=5, sticky=tk.W)
            if name == 'emp_status_combo':
                entry = ttk.Combobox(self.emp_form_frame, width=width, state='readonly', values=['在职', '离职'])
            else:
                entry = ttk.Entry(self.emp_form_frame, width=width)
            entry.grid(row=0, column=i*2+1, padx=5, pady=5)
            self.emp_form_entries[name] = entry
        
        self.emp_action_frame = ttk.Frame(self.employee_tab)
        self.emp_action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.add_emp_btn = ttk.Button(self.emp_action_frame, text="新增员工", style='Accent.TButton', width=12)
        self.add_emp_btn.pack(side=tk.LEFT, padx=5)
        
        self.modify_emp_btn = ttk.Button(self.emp_action_frame, text="修改员工", style='Accent.TButton', width=12)
        self.modify_emp_btn.pack(side=tk.LEFT, padx=5)
        
        self.del_emp_btn = ttk.Button(self.emp_action_frame, text="删除员工", style='Warning.TButton', width=12)
        self.del_emp_btn.pack(side=tk.LEFT, padx=5)
        
        self.emp_tree_frame = ttk.Frame(self.employee_tab)
        self.emp_tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.emp_tree = ttk.Treeview(self.emp_tree_frame, columns=('工号', '姓名', '部门', '职位', '电话', '邮箱', '入职日期', '状态'), show='headings')
        for col in ['工号', '姓名', '部门', '职位', '电话', '邮箱', '入职日期', '状态']:
            self.emp_tree.heading(col, text=col)
            self.emp_tree.column(col, width=80)
        
        self.emp_tree.column('工号', width=70)
        self.emp_tree.column('姓名', width=70)
        self.emp_tree.column('部门', width=90)
        self.emp_tree.column('职位', width=80)
        self.emp_tree.column('电话', width=100)
        self.emp_tree.column('邮箱', width=150)
        self.emp_tree.column('入职日期', width=90)
        self.emp_tree.column('状态', width=60)
        
        self.emp_tree_scroll = ttk.Scrollbar(self.emp_tree_frame, orient=tk.VERTICAL, command=self.emp_tree.yview)
        self.emp_tree.configure(yscroll=self.emp_tree_scroll.set)
        
        self.emp_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.emp_tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_checkin_tab(self):
        self.checkin_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.checkin_tab, text='考勤打卡')
        
        self.checkin_main_frame = ttk.Frame(self.checkin_tab)
        self.checkin_main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.checkin_left_frame = ttk.Frame(self.checkin_main_frame)
        self.checkin_left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.checkin_title = ttk.Label(self.checkin_left_frame, text="考勤打卡", style='Title.TLabel')
        self.checkin_title.pack(pady=20)
        
        self.check_id_frame = ttk.Frame(self.checkin_left_frame)
        self.check_id_frame.pack(pady=10)
        
        ttk.Label(self.check_id_frame, text="工号:", font=('Microsoft YaHei', 12)).pack(side=tk.LEFT, padx=10)
        self.check_id_entry = ttk.Entry(self.check_id_frame, width=25, font=('Microsoft YaHei', 12))
        self.check_id_entry.pack(side=tk.LEFT, padx=10)
        
        self.check_action_frame = ttk.Frame(self.checkin_left_frame)
        self.check_action_frame.pack(pady=30)
        
        self.check_in_btn = ttk.Button(self.check_action_frame, text="签 到", style='Accent.TButton', width=15, padding=15)
        self.check_in_btn.pack(side=tk.LEFT, padx=20)
        
        self.check_out_btn = ttk.Button(self.check_action_frame, text="签 退", style='Accent.TButton', width=15, padding=15)
        self.check_out_btn.pack(side=tk.LEFT, padx=20)
        
        self.check_status_frame = ttk.Frame(self.checkin_left_frame)
        self.check_status_frame.pack(pady=20)
        
        self.check_status_label = ttk.Label(self.check_status_frame, text="", font=('Microsoft YaHei', 14))
        self.check_status_label.pack()
        
        self.check_info_text = tk.Text(self.check_status_frame, height=4, width=60, font=('Microsoft YaHei', 10), state=tk.DISABLED)
        self.check_info_text.pack(pady=10)
        
        self.checkin_right_frame = ttk.Frame(self.checkin_main_frame, width=300)
        self.checkin_right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)
        self.checkin_right_frame.pack_propagate(False)
        
        self.today_stats_title = ttk.Label(self.checkin_right_frame, text="今日统计", style='Title.TLabel')
        self.today_stats_title.pack(pady=10)
        
        self.today_stats_frame = ttk.Frame(self.checkin_right_frame)
        self.today_stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        stats_items = [('今日出勤', 'today_attendance'),
                       ('今日迟到', 'today_late'),
                       ('今日早退', 'today_early'),
                       ('今日缺勤', 'today_absent')]
        
        self.today_stats_labels = {}
        for i, (label, name) in enumerate(stats_items):
            frame = ttk.Frame(self.today_stats_frame)
            frame.pack(fill=tk.X, pady=5)
            ttk.Label(frame, text=label, width=10).pack(side=tk.LEFT)
            value_label = ttk.Label(frame, text="0", font=('Microsoft YaHei', 12, 'bold'))
            value_label.pack(side=tk.RIGHT)
            self.today_stats_labels[name] = value_label
        
        self.leave_request_frame = ttk.Frame(self.checkin_right_frame)
        self.leave_request_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(self.leave_request_frame, text="请假申请:", font=('Microsoft YaHei', 10)).pack(pady=5)
        
        self.leave_type_combo = ttk.Combobox(self.leave_request_frame, values=['事假', '病假', '年假', '婚假', '产假'], state='readonly', width=15)
        self.leave_type_combo.pack(pady=5)
        
        self.apply_leave_btn = ttk.Button(self.leave_request_frame, text="申请请假", style='Accent.TButton', width=15)
        self.apply_leave_btn.pack(pady=5)
        
    def create_attendance_tab(self):
        self.attendance_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.attendance_tab, text='考勤记录')
        
        self.att_search_frame = ttk.Frame(self.attendance_tab)
        self.att_search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(self.att_search_frame, text="工号:").pack(side=tk.LEFT, padx=5)
        self.att_emp_id_entry = ttk.Entry(self.att_search_frame, width=12)
        self.att_emp_id_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.att_search_frame, text="开始日期:").pack(side=tk.LEFT, padx=5)
        self.att_start_date = ttk.Entry(self.att_search_frame, width=12)
        self.att_start_date.pack(side=tk.LEFT, padx=5)
        self.att_start_date.insert(0, datetime.date.today().strftime('%Y-%m-%d'))
        
        ttk.Label(self.att_search_frame, text="结束日期:").pack(side=tk.LEFT, padx=5)
        self.att_end_date = ttk.Entry(self.att_search_frame, width=12)
        self.att_end_date.pack(side=tk.LEFT, padx=5)
        self.att_end_date.insert(0, datetime.date.today().strftime('%Y-%m-%d'))
        
        ttk.Label(self.att_search_frame, text="状态:").pack(side=tk.LEFT, padx=5)
        self.att_status_combo = ttk.Combobox(self.att_search_frame, width=10, state='readonly', 
                                              values=['全部', '正常', '迟到', '早退', '缺勤', '请假', '加班'])
        self.att_status_combo.current(0)
        self.att_status_combo.pack(side=tk.LEFT, padx=5)
        
        self.search_att_btn = ttk.Button(self.att_search_frame, text="查询", style='Accent.TButton', width=8)
        self.search_att_btn.pack(side=tk.LEFT, padx=10)
        
        self.reset_att_btn = ttk.Button(self.att_search_frame, text="重置", width=8)
        self.reset_att_btn.pack(side=tk.LEFT, padx=5)
        
        self.att_tree_frame = ttk.Frame(self.attendance_tab)
        self.att_tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.att_tree = ttk.Treeview(self.att_tree_frame, columns=('工号', '姓名', '签到时间', '签退时间', '状态', '请假类型', '工作时长', '加班时长'), show='headings')
        for col in ['工号', '姓名', '签到时间', '签退时间', '状态', '请假类型', '工作时长', '加班时长']:
            self.att_tree.heading(col, text=col)
        
        self.att_tree.column('工号', width=70)
        self.att_tree.column('姓名', width=70)
        self.att_tree.column('签到时间', width=140)
        self.att_tree.column('签退时间', width=140)
        self.att_tree.column('状态', width=70)
        self.att_tree.column('请假类型', width=80)
        self.att_tree.column('工作时长', width=80)
        self.att_tree.column('加班时长', width=80)
        
        self.att_tree_scroll = ttk.Scrollbar(self.att_tree_frame, orient=tk.VERTICAL, command=self.att_tree.yview)
        self.att_tree.configure(yscroll=self.att_tree_scroll.set)
        
        self.att_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.att_tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_statistics_tab(self):
        self.statistics_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.statistics_tab, text='数据统计')
        
        self.stat_tabs = ttk.Notebook(self.statistics_tab)
        self.stat_tabs.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.personal_stat_tab = ttk.Frame(self.stat_tabs)
        self.stat_tabs.add(self.personal_stat_tab, text='个人统计')
        
        self.personal_stat_frame = ttk.Frame(self.personal_stat_tab)
        self.personal_stat_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(self.personal_stat_frame, text="工号:").pack(side=tk.LEFT, padx=5)
        self.personal_emp_id_entry = ttk.Entry(self.personal_stat_frame, width=12)
        self.personal_emp_id_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.personal_stat_frame, text="月份:").pack(side=tk.LEFT, padx=5)
        self.personal_month_entry = ttk.Entry(self.personal_stat_frame, width=10)
        self.personal_month_entry.pack(side=tk.LEFT, padx=5)
        self.personal_month_entry.insert(0, datetime.date.today().strftime('%Y-%m'))
        
        self.personal_stat_btn = ttk.Button(self.personal_stat_frame, text="查询", style='Accent.TButton', width=8)
        self.personal_stat_btn.pack(side=tk.LEFT, padx=10)
        
        self.personal_result_frame = ttk.Frame(self.personal_stat_tab)
        self.personal_result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.personal_cards_frame = ttk.Frame(self.personal_result_frame)
        self.personal_cards_frame.pack(fill=tk.X, pady=10)
        
        self.personal_cards = {}
        stat_categories = [('出勤天数', 'attendance_days', '#4A6FA5'),
                           ('迟到次数', 'late_count', '#E74C3C'),
                           ('早退次数', 'early_count', '#E67E22'),
                           ('缺勤次数', 'absent_count', '#9B59B6'),
                           ('请假天数', 'leave_count', '#1ABC9C'),
                           ('加班时长', 'overtime_hours', '#3498DB')]
        
        for i, (label, name, color) in enumerate(stat_categories):
            card = ttk.Frame(self.personal_cards_frame, borderwidth=1, relief=tk.SUNKEN)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
            
            title_label = ttk.Label(card, text=label, font=('Microsoft YaHei', 10))
            title_label.pack(pady=10)
            
            value_label = ttk.Label(card, text="0", font=('Microsoft YaHei', 24, 'bold'), foreground=color)
            value_label.pack(pady=5)
            
            self.personal_cards[name] = value_label
        
        self.department_stat_tab = ttk.Frame(self.stat_tabs)
        self.stat_tabs.add(self.department_stat_tab, text='部门统计')
        
        self.department_stat_frame = ttk.Frame(self.department_stat_tab)
        self.department_stat_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(self.department_stat_frame, text="部门:").pack(side=tk.LEFT, padx=5)
        self.department_combo = ttk.Combobox(self.department_stat_frame, width=15, state='readonly')
        self.department_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.department_stat_frame, text="月份:").pack(side=tk.LEFT, padx=5)
        self.department_month_entry = ttk.Entry(self.department_stat_frame, width=10)
        self.department_month_entry.pack(side=tk.LEFT, padx=5)
        self.department_month_entry.insert(0, datetime.date.today().strftime('%Y-%m'))
        
        self.department_stat_btn = ttk.Button(self.department_stat_frame, text="查询", style='Accent.TButton', width=8)
        self.department_stat_btn.pack(side=tk.LEFT, padx=10)
        
        self.department_result_frame = ttk.Frame(self.department_stat_tab)
        self.department_result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.department_cards_frame = ttk.Frame(self.department_result_frame)
        self.department_cards_frame.pack(fill=tk.X, pady=10)
        
        self.department_cards = {}
        for i, (label, name, color) in enumerate(stat_categories):
            card = ttk.Frame(self.department_cards_frame, borderwidth=1, relief=tk.SUNKEN)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
            
            title_label = ttk.Label(card, text=label, font=('Microsoft YaHei', 10))
            title_label.pack(pady=10)
            
            value_label = ttk.Label(card, text="0", font=('Microsoft YaHei', 24, 'bold'), foreground=color)
            value_label.pack(pady=5)
            
            self.department_cards[name] = value_label
        
    def update_status_time(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.status_time.config(text=f"当前时间: {now}")
        self.root.after(1000, self.update_status_time)
        
    def switch_to_employee(self):
        self.notebook.select(self.employee_tab)
        
    def switch_to_checkin(self):
        self.notebook.select(self.checkin_tab)
        
    def switch_to_attendance(self):
        self.notebook.select(self.attendance_tab)
        
    def switch_to_statistics(self):
        self.notebook.select(self.statistics_tab)
        
    def set_status(self, text):
        self.status_message.config(text=text)
        
    def show_message(self, title, message, type='info'):
        if type == 'error':
            messagebox.showerror(title, message)
        elif type == 'warning':
            messagebox.showwarning(title, message)
        else:
            messagebox.showinfo(title, message)
            
    def show_confirm(self, title, message):
        return messagebox.askyesno(title, message)
        
    def on_exit(self):
        if messagebox.askyesno("退出", "确定要退出系统吗？"):
            self.root.quit()
            
    def on_about(self):
        messagebox.showinfo("关于", f"员工考勤管理系统 {self.VERSION}\n\n基于 Python + Tkinter 开发\n\n支持员工管理、考勤打卡、数据统计等功能")
        
    def on_backup(self):
        pass
        
    def on_clear_data(self):
        pass
        
    def on_employee_list(self):
        self.switch_to_employee()
        
    def on_add_employee(self):
        self.switch_to_employee()
        
    def on_checkin(self):
        self.switch_to_checkin()
        
    def on_attendance_list(self):
        self.switch_to_attendance()
        
    def on_personal_stats(self):
        self.switch_to_statistics()
        self.stat_tabs.select(self.personal_stat_tab)
        
    def on_department_stats(self):
        self.switch_to_statistics()
        self.stat_tabs.select(self.department_stat_tab)
        
    def on_logs(self):
        pass