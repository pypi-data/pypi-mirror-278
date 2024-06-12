from youqu_button_center import ButtonCenter

center = ButtonCenter(
    app_name="dde-file-manager",
    config_path="./ui.ini"
)
a = center.btn_center("test")
print(a)
