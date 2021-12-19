# hfut-check-in

[English](README.md) | [中文](README_zh.md)

通过 GitHub Actions 的自动打卡程序

# 使用方法

1. Fork 这个仓库

2. 启用工作流（workflow），请点击 `Actions` - `Workflows` - `Python application` - `Enable workflow`

3. 通过 GitHub Secrets 添加你的信息，请点击 `Settings` - `Secrets` - `New Secrets` 并添加如下信息

   `username` - 你的学号，通常是 10 位数

   `password` - 你在 one.hfut.edu.cn 中的密码（即新版信息门户的密码）

   `address` - 通常应当填入「安徽省合肥市蜀山区」

检查程序的工作状态，请点击 `Actions` - `Workflows` - `All workflows` 并点击进入最后的程序运行结果，之后你便可以在 `build` - `Run code` 中看到程序的工作状态了

关闭 GitHub Actions 的提醒(邮件和网页)，请点击你的头像，之后点击 `Settings` - `Notifications` - `Actions` 并取消勾选 `Email` 和 `Web`

**注意**：若此仓库至少 60 天未活动，请手动地启用该工作流

# 鸣谢

[@qdddz/HFUT_AutoSubmit](https://github.com/qdddz/HFUT_AutoSubmit)

[@HowardZorn/hfut_auto_check-in](https://github.com/HowardZorn/hfut_auto_check-in)
