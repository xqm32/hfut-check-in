# hfut-check-in

[English](README.md) | [中文](README_zh.md)

Auto check in via GitHub Actions

**ATTENTION**: Be sure to submit screenshots yourself in the Campus Today app starting May 6, or you will submit screenshots from the previous day.

# Recent update

1. Fixed bug unable to check in

2. Use previous check in address instead of `address` variable

   Since `address` variable removed, you should get detailed address by GPS at least once, or your `address` will be your current district

# Usage

1. Fork this repository

2. To enable workflow, click `Actions` - `Workflows` - `Python application` - `Enable workflow`

3. To add your information, click `Settings` - `Secrets` - `New Secrets` and add the following secrets

   `username` - Your student ID, 10 numbers in general

   `password` - Your password for one.hfut.edu.cn

To check the action's status, click `Actions` - `Workflows` - `All workflows` and enter the lastest workflow run. Then you can see the status in `build` - `Run code`

To disable GitHub Actions' notifications(both email and web), click your avatar, then go to `Settings` - `Notifications` - `Actions` and uncheck `Email` and `Web`

**ATTENTION**: You should enable the workflow manually if there hasn't been activity for at least 60 days

# Use Aliyun Function Compute

1. Click `Code` - `Download ZIP` on the repository page

2. (If you do not have an Aliyun account, please register first) Enter the [Aliyun function console](https://www.aliyun.com/product/fc/)

3. Click on `Services and Functions` and create a service

4. Click `Create function`, select `Create from scratch`, and modify the configuration as follows

   `Running Environment`: `Python 3.9`

   `Function trigger method`: `Triggered by event request`

   `instance type`: `flex instance`

   `Memory Specifications`: `128 MB`

   `Trigger Type`: `Timed Trigger`

   `Trigger method`: `custom`

   `CRON expression`: `0 10 6,7,8,9,10,11,12 * * *`

5. Upload the `hfut-check-in-main.zip` downloaded in step `1` to the cloud function IDE explorer

6. Type `unzip hfut-check-in-main.zip` in the cloud function IDE terminal and execute it. At this time, the `hfut-check-in-main` folder should appear in the cloud function IDE resource manager

7. Move the `utils` folder and `requirements.txt` in the `hfut-check-in-main` folder to the same directory as `index.py`

8. Type `pip3 install -t . -r requirements.txt` in the terminal and execute

9. Modify the contents of `index.py` as follows

   ```python3
   from utils.HFUT import main

   def handler(event, context):
      main()

   if __name__ == "__main__":
      main()
   ```

10. Use any of the following methods to configure the information

    1. Click `Function Configuration`, fill in `username`, `password` in the environment variable column.

    2. Create a new `config.json` in the cloud function IDE resource manager and configure it according to the following template

       ```json
       {
         "username": "",
         "password": ""
       }
       ```

**ATTENTION**: There is no free quota for public network outbound traffic of Aliyun Function Compute. For detailed billing, please refer to [Public Network Outbound Traffic](https://help.aliyun.com/document_detail/54301.html?spm=5176.fcnext.help.dexternal.5a1278c82su1sN#h3-url-3)

# TODO

- [ ] Use WebVPN
- [x] Remove `address` variable
- [x] Prompt wrong password
- [x] More formal log output

# Thanks

[@qdddz/HFUT_AutoSubmit](https://github.com/qdddz/HFUT_AutoSubmit)

[@HowardZorn/hfut_auto_check-in](https://github.com/HowardZorn/hfut_auto_check-in)
