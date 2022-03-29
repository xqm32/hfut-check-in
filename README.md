# hfut-check-in

[English](README.md) | [中文](README_zh.md)

Auto check in via GitHub Actions

# Recent update

1. Fixed bug unable to check in

# Usage

1. Fork this repository

2. To enable workflow, click `Actions` - `Workflows` - `Python application` - `Enable workflow`

3. To add your infomation, click `Settings` - `Secrets` - `New Secrets` and add the following secrets

   `username` - Your student ID, 10 numbers in general

   `password` - Your password for one.hfut.edu.cn

   `address` - Shushan, Hefei, Anhui in general

To check the action's status, click `Actions` - `Workflows` - `All workflows` and enter the lastest workflow run. Then you can see the status in `build` - `Run code`

To disable GitHub Actions' notifications(both email and web), click your avatar, then go to `Settings` - `Notifications` - `Actions` and uncheck `Email` and `Web`

**ATTENTION**: You should enable the workflow manually if there hasn't been activity for at least 60 days

# TODO

- [ ] Use WebVPN
- [ ] Remove `address` variable
- [X] Prompt wrong password
- [X] Retry if timeout
- [X] More formal log output

# Thanks

[@qdddz/HFUT_AutoSubmit](https://github.com/qdddz/HFUT_AutoSubmit)

[@HowardZorn/hfut_auto_check-in](https://github.com/HowardZorn/hfut_auto_check-in)
