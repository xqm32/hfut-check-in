# hfut-check-in

[English](README.md) | [中文](README_zh.md)

通过 GitHub Actions 的自动打卡程序

**注意**: 从 5 月 6 日开始，请务必自行于今日校园应用程序中提交截图，否则将提交前一天的截图。

# 近期更新

1. 修复了无法打卡的错误

2. 使用先前地址作为打卡地址以代替 `address` 变量

   由于 `address` 变量已经被移除，你应当通过定位获取至少一次详细地址，否则你的 `address` 将会为当前的行政区

# 使用方法

1. Fork 这个仓库

2. 启用工作流（workflow），请点击 `Actions` - `Workflows` - `Python application` - `Enable workflow`

3. 通过 GitHub Secrets 添加你的信息，请点击 `Settings` - `Secrets` - `New Secrets` 并添加如下信息

   `username` - 你的学号，通常是 10 位数

   `password` - 你在 one.hfut.edu.cn 中的密码（即新版信息门户的密码）

检查程序的工作状态，请点击 `Actions` - `Workflows` - `All workflows` 并点击进入最后的程序运行结果，之后你便可以在 `build` - `Run code` 中看到程序的工作状态了

关闭 GitHub Actions 的提醒(邮件和网页)，请点击你的头像，之后点击 `Settings` - `Notifications` - `Actions` 并取消勾选 `Email` 和 `Web`

**注意**：若此仓库至少 60 天未活动，请手动地启用该工作流

# 使用阿里云函数

1. 在此仓库页面点击 `Code` - `Download ZIP`

2. （若尚无阿里云账号请先注册）进入[阿里云函数控制台](https://www.aliyun.com/product/fc/)

3. 点击 `服务及函数`，并创建服务

4. 点击 `创建函数`，选择 `从零开始创建`，修改配置如下

   `运行环境`: `Python 3.9`

   `函数触发方式`: `通过事件请求触发`

   `实例类型`: `弹性实例`

   `内存规格`: `128 MB`

   `触发器类型`: `定时触发器`

   `触发方式`: `自定义`

   `CRON 表达式`: `0 10 6,7,8,9,10,11,12 * * *`

5. 将步骤 `1` 所下载的 `hfut-check-in-main.zip` 上传至云函数 IDE 资源管理器

6. 云函数 IDE 终端键入 `unzip hfut-check-in-main.zip` 并执行，此时云函数 IDE 资源管理器应当出现 `hfut-check-in-main` 文件夹

7. 将 `hfut-check-in-main` 文件夹中 `utils` 文件夹、`requirements.txt` 移动至与 `index.py` 同一目录下

8. 在终端键入 `pip3 install -t . -r requirements.txt` 并执行

9. 修改 `index.py` 中内容如下

   ```python3
   from utils.HFUT import main

   def handler(event, context):
      main()

   if __name__ == "__main__":
      main()
   ```

10. 使用下列任一种方法配置信息

    1. 点击 `函数配置`，在环境变量一栏填入 `username`、`password` 即可

    2. 在云函数 IDE 资源管理器中新建 `config.json` 并按如下模板配置

       ```json
       {
         "username": "",
         "password": ""
       }
       ```

**注意**：阿里云函数的公网出流量没有免费额度，详细计费请参考[公网出流量](https://help.aliyun.com/document_detail/54301.html?spm=5176.fcnext.help.dexternal.5a1278c82su1sN#h3-url-3)

# 待实现

- [ ] 使用 WebVPN
- [x] 删除 `address` 变量
- [x] 密码错误提示
- [x] 更规范的日志输出

# 鸣谢

[@qdddz/HFUT_AutoSubmit](https://github.com/qdddz/HFUT_AutoSubmit)

[@HowardZorn/hfut_auto_check-in](https://github.com/HowardZorn/hfut_auto_check-in)
