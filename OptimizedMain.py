# OptimizedMain.py
import wx
import requests
import datetime
import time

class MyFrame(wx.Frame):
    def __init__(self, parent, title, size):
        super(MyFrame, self).__init__(parent, title=title, size=size)
        self.language = "中文"
        self.language_mapping = {
            "中文": {
                "enter_api_url": "API URL：",
                "enter_api_key": "API Key：",
                "option_0": "退出",
                "option_1": "查询余额",
                "option_2": "获取模型列表",
                "option_3": "测试模型",
                "option_4": "切换语言",
                "select_language": "请选择语言",
                "language_selected": "已选择语言：",
                "balance_info": "余额信息：",
                "total_amount": "总额：",
                "used_amount": "已用：",
                "remaining_amount": "剩余：",
                "currency": "美元",
                "error_occurred": "发生错误：",
                "get_models_error": "获取模型列表时出错：",
                "test_model_prompt": "请输入要测试的模型名称（默认为gpt-3.5-turbo）：",
                "model_input": "模型输入",
                "unknown_model": "未知模型",
                "no_content": "无内容",
                "user_call_model": "用户调用模型：",
                "actual_response_model": "实际响应模型：",
                "response_time": "响应时间：",
                "response_success": "请求成功！",
                "response_content": "响应内容：",
                "request_failed": "请求失败，状态码："
            },
            "English": {
                "enter_api_url": "API URL:",
                "enter_api_key": "API Key:",
                "option_0": "Exit",
                "option_1": "Check Balance",
                "option_2": "Get Models",
                "option_3": "Test Model",
                "option_4": "Switch Language",
                "select_language": "Please select language",
                "language_selected": "Language selected:",
                "balance_info": "Balance Information:",
                "total_amount": "Total:",
                "used_amount": "Used:",
                "remaining_amount": "Remaining:",
                "currency": "USD",
                "error_occurred": "Error occurred:",
                "get_models_error": "Error getting models:",
                "test_model_prompt": "Enter model name to test (default is gpt-3.5-turbo):",
                "model_input": "Model Input",
                "unknown_model": "Unknown model",
                "no_content": "No content",
                "user_call_model": "User called model:",
                "actual_response_model": "Actual response model:",
                "response_time": "Response time:",
                "response_success": "Request successful!",
                "response_content": "Response content:",
                "request_failed": "Request failed, status code:"
            }
        }
        self.init_ui()

    def init_ui(self):
        # 创建菜单栏
        menubar = wx.MenuBar()
        language_menu = wx.Menu()
        switch_language = language_menu.Append(wx.ID_ANY, self.language_mapping[self.language]["option_4"])
        menubar.Append(language_menu, "Language")
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.on_select_language, switch_language)

        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        url_sizer = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label=self.language_mapping[self.language]["enter_api_url"])
        self.tc1 = wx.TextCtrl(panel)
        url_sizer.Add(st1, flag=wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=8)
        url_sizer.Add(self.tc1, proportion=1)
        main_sizer.Add(url_sizer, flag=wx.EXPAND|wx.ALL, border=10)

        # API Keys输入区域
        key_sizer = wx.BoxSizer(wx.VERTICAL)
        st2 = wx.StaticText(panel, label=self.language_mapping[self.language]["enter_api_key"])
        self.tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.HSCROLL, size=(-1, 60))
        key_sizer.Add(st2, flag=wx.BOTTOM, border=5)
        key_sizer.Add(self.tc2, proportion=1, flag=wx.EXPAND)
        main_sizer.Add(key_sizer, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)

        button_panel = wx.Panel(panel)
        button_sizer = wx.GridBagSizer(10, 10)
        self.btn1 = wx.Button(button_panel, label=self.language_mapping[self.language]["option_1"])
        self.btn2 = wx.Button(button_panel, label=self.language_mapping[self.language]["option_2"])
        self.btn3 = wx.Button(button_panel, label=self.language_mapping[self.language]["option_3"])

        button_size = wx.Size(150, 30)
        self.btn1.SetMinSize(button_size)
        self.btn2.SetMinSize(button_size)
        self.btn3.SetMinSize(button_size)

        self.btn1.Bind(wx.EVT_BUTTON, self.on_get_balance)
        self.btn2.Bind(wx.EVT_BUTTON, self.on_get_models)
        self.btn3.Bind(wx.EVT_BUTTON, self.on_test_model)

        button_sizer.Add(self.btn1, pos=(0, 0), flag=wx.ALL, border=5)
        button_sizer.Add(self.btn2, pos=(0, 1), flag=wx.ALL, border=5)
        button_sizer.Add(self.btn3, pos=(0, 2), flag=wx.ALL, border=5)

        button_panel.SetSizer(button_sizer)
        main_sizer.Add(button_panel, flag=wx.ALIGN_CENTER|wx.ALL, border=10)

        # Add ListCtrl for displaying table data
        self.result_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        main_sizer.Add(self.result_list, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)

        self.result_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)
        main_sizer.Add(self.result_text, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)

        panel.SetSizer(main_sizer)
        self.SetMinSize((600, 400))
        self.Centre()

    def on_get_balance(self, event):
        api_keys = [key.strip() for key in self.tc2.GetValue().split('\n') if key.strip()]
        self.url = self.tc1.GetValue()
        if not api_keys or not self.url:
            wx.MessageBox("Please enter both API URL and at least one API Key.", "Error", wx.OK | wx.ICON_ERROR)
            return

        self.result_list.ClearAll()
        self.result_list.InsertColumn(0, "API Key", width=100)
        self.result_list.InsertColumn(1, self.language_mapping[self.language]['total_amount'], width=100)
        self.result_list.InsertColumn(2, self.language_mapping[self.language]['used_amount'], width=100)
        self.result_list.InsertColumn(3, self.language_mapping[self.language]['remaining_amount'], width=100)
        self.result_list.InsertColumn(4, "Status", width=200)

        row = 0
        for api_key in api_keys:
            try:
                headers = {'Authorization': f'Bearer {api_key}', "Content-Type": "application/json"}
                
                # 设置请求超时和重试
                session = requests.Session()
                session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
                
                # 获取订阅信息
                subscription_url = "/v1/dashboard/billing/subscription"
                try:
                    print(f'正在请求: {self.url + subscription_url}')
                    subscription_response = session.get(
                        self.url + subscription_url,
                        headers=headers,
                        timeout=(5, 15)  # (连接超时, 读取超时)
                    )
                    print(f'DNS解析结果: {subscription_response.raw._connection.sock.getpeername() if subscription_response.raw._connection else "无连接信息"}')
                    print('响应状态码:', subscription_response.status_code)
                    print('响应内容:', subscription_response.text)
                except requests.exceptions.ConnectTimeout:
                    print('连接超时')
                    index = self.result_list.InsertItem(row, api_key[:8] + "...")
                    self.result_list.SetItem(index, 4, "Error: Connection timeout")
                    row += 1
                    continue
                except requests.exceptions.ReadTimeout:
                    print('读取超时')
                    index = self.result_list.InsertItem(row, api_key[:8] + "...")
                    self.result_list.SetItem(index, 4, "Error: Read timeout")
                    row += 1
                    continue
                except requests.exceptions.ConnectionError as e:
                    print(f'连接错误: {str(e)}')
                    index = self.result_list.InsertItem(row, api_key[:8] + "...")
                    self.result_list.SetItem(index, 4, f"Error: Connection error - {str(e)}")
                    row += 1
                    continue
                if subscription_response.status_code != 200:
                    index = self.result_list.InsertItem(row, api_key[:8] + "...")
                    self.result_list.SetItem(index, 4, f"Error: {subscription_response.text}")
                    row += 1
                    continue

                subscription_data = subscription_response.json()
                total = subscription_data.get("hard_limit_usd")

                # 获取使用量
                start_date = (datetime.datetime.now() - datetime.timedelta(days=99)).strftime("%Y-%m-%d")
                end_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                billing_url = f"{self.url}/v1/dashboard/billing/usage?start_date={start_date}&end_date={end_date}"
                billing_response = requests.get(billing_url, headers=headers)
                
                if billing_response.status_code != 200:
                    index = self.result_list.InsertItem(row, api_key[:8] + "...")
                    self.result_list.SetItem(index, 4, f"Error: {billing_response.text}")
                    row += 1
                    continue

                billing_data = billing_response.json()
                total_usage = billing_data.get("total_usage") / 100
                remaining = total - total_usage

                if total is None or total_usage is None or remaining is None:
                    index = self.result_list.InsertItem(row, api_key[:8] + "...")
                    self.result_list.SetItem(index, 4, f"Error: Invalid data received")
                    row += 1
                    continue

                index = self.result_list.InsertItem(row, api_key[:8] + "...")
                self.result_list.SetItem(index, 1, f"{total:.2f}")
                self.result_list.SetItem(index, 2, f"{total_usage:.2f}")
                self.result_list.SetItem(index, 3, f"{remaining:.2f}")
                self.result_list.SetItem(index, 4, "Success")
                row += 1

            except requests.exceptions.RequestException as e:
                index = self.result_list.InsertItem(row, api_key[:8] + "...")
                self.result_list.SetItem(index, 4, f"Error: {str(e)}")
                row += 1
    
    def on_get_models(self, event):
        api_keys = [key.strip() for key in self.tc2.GetValue().split('\n') if key.strip()]
        self.url = self.tc1.GetValue()
        if not api_keys or not self.url:
            wx.MessageBox("Please enter both API URL and at least one API Key.", "Error", wx.OK | wx.ICON_ERROR)
            return

        self.result_list.ClearAll()
        self.result_list.InsertColumn(0, "API Key", width=100)
        self.result_list.InsertColumn(1, "Company", width=150)
        self.result_list.InsertColumn(2, "Model", width=200)
        self.result_list.InsertColumn(3, "Status", width=150)

        row = 0
        for api_key in api_keys:
            try:
                response = requests.get(
                    self.url + '/v1/models',
                    headers={'Authorization': f'Bearer {api_key}', "Content-Type": "application/json"}
                )
                
                if response.status_code != 200:
                    index = self.result_list.InsertItem(row, api_key[:8] + "...")
                    self.result_list.SetItem(index, 3, f"Error: {response.text}")
                    row += 1
                    continue

                models_data = response.json()
                models = models_data.get('data', [])

                if not models:
                    index = self.result_list.InsertItem(row, api_key[:8] + "...")
                    self.result_list.SetItem(index, 3, "No models found")
                    row += 1
                    continue

                categorized_models = self.categorize_and_color_models(models)
                for company, model_list in categorized_models.items():
                    for model, _ in model_list:
                        index = self.result_list.InsertItem(row, api_key[:8] + "...")
                        self.result_list.SetItem(index, 1, company.capitalize())
                        self.result_list.SetItem(index, 2, model)
                        self.result_list.SetItem(index, 3, "Available")
                        row += 1

            except requests.exceptions.RequestException as e:
                index = self.result_list.InsertItem(row, api_key[:8] + "...")
                self.result_list.SetItem(index, 3, f"Error: {str(e)}")
                row += 1
                # row += 1

    def on_test_model(self, event):
        api_keys = [key.strip() for key in self.tc2.GetValue().split('\n') if key.strip()]
        self.url = self.tc1.GetValue()
        if not api_keys or not self.url:
            wx.MessageBox("Please enter both API URL and at least one API Key.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # 让用户选择要使用的API Key
        key_dlg = wx.SingleChoiceDialog(
            self,
            "Select API Key to test:",
            "Select Key",
            [f"{key[:8]}..." for key in api_keys]
        )
        
        if key_dlg.ShowModal() == wx.ID_OK:
            selected_index = key_dlg.GetSelection()
            selected_key = api_keys[selected_index]
            
            # 选择模型
            model_dlg = wx.TextEntryDialog(
                self,
                self.language_mapping[self.language]["test_model_prompt"],
                self.language_mapping[self.language]["model_input"]
            )
            
            if model_dlg.ShowModal() == wx.ID_OK:
                model = model_dlg.GetValue().strip() or "gpt-3.5-turbo"
                data = {
                    "model": model,
                    "messages": [
                        {"role": "user", "content": "say this is text!"}
                    ]
                }
                
                self.result_list.ClearAll()
                self.result_list.InsertColumn(0, "API Key", width=100)
                self.result_list.InsertColumn(1, self.language_mapping[self.language]['user_call_model'], width=150)
                self.result_list.InsertColumn(2, self.language_mapping[self.language]['actual_response_model'], width=150)
                self.result_list.InsertColumn(3, self.language_mapping[self.language]['response_time'], width=100)
                self.result_list.InsertColumn(4, self.language_mapping[self.language]['response_content'], width=200)
                
                try:
                    start_time = time.time()
                    response = requests.post(
                        self.url + "/v1/chat/completions",
                        headers={'Authorization': f'Bearer {selected_key}', "Content-Type": "application/json"},
                        json=data
                    )
                    end_time = time.time()
                    response_time = end_time - start_time

                    index = self.result_list.InsertItem(0, f"{selected_key[:8]}...")
                    
                    if response.status_code != 200:
                        self.result_list.SetItem(index, 4, f"Error: {response.text}")
                        return

                    response_json = response.json()
                    model_name = response_json.get('model', self.language_mapping[self.language]['unknown_model'])
                    content = response_json.get('choices', [{}])[0].get('message', {}).get('content', self.language_mapping[self.language]['no_content'])

                    if not content:
                        self.result_list.SetItem(index, 4, "Error: No content received")
                        return

                    self.result_list.SetItem(index, 1, model)
                    self.result_list.SetItem(index, 2, model_name)
                    self.result_list.SetItem(index, 3, f"{response_time:.2f}s")
                    self.result_list.SetItem(index, 4, content)

                except requests.exceptions.RequestException as e:
                    index = self.result_list.InsertItem(0, f"{selected_key[:8]}...")
                    self.result_list.SetItem(index, 4, f"Error: {str(e)}")

    def on_select_language(self, event):
        dlg = wx.SingleChoiceDialog(
            self,
            self.language_mapping[self.language]["select_language"],
            "Language",
            ["中文", "English"]
        )
        
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            selected_language = dlg.GetStringSelection()
            if selected_language != self.language:
                self.language = selected_language
                # 保存当前的 API URL 和 Key
                current_url = self.tc1.GetValue()
                current_key = self.tc2.GetValue()
                
                # 清除当前面板
                self.DestroyChildren()
                
                # 重新初始化UI
                self.init_ui()
                
                # 恢复之前的 API URL 和 Key
                self.tc1.SetValue(current_url)
                self.tc2.SetValue(current_key)
                
                # 刷新布局
                self.Layout()
                
                wx.MessageBox(
                    f"{self.language_mapping[self.language]['language_selected']} {self.language}",
                    "Info",
                    wx.OK | wx.ICON_INFORMATION
                )
        
    def categorize_and_color_models(self, models):
        categorized_models = {}
        company_names = {model['owned_by'] for model in models}
        colors = ["red", "green", "blue", "yellow", "magenta", "cyan"]
        color_mapping = {company: colors[i % len(colors)] for i, company in enumerate(company_names)}

        for model in models:
            model_name = model['id']
            owned_by = model.get('owned_by', 'unknown')
            if owned_by not in categorized_models:
                categorized_models[owned_by] = []
            color = color_mapping.get(owned_by, "black")
            categorized_models[owned_by].append((model_name, color))

        return categorized_models

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None, title="API Tool", size=(600, 400))
    frame.Show()
    app.MainLoop()
