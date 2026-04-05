# x-blocklist-importer

x-blocklist-importer 帮助你将一个 x(twitter) 账号的黑名单导入另一个账号中


<div align="center">

![Python](https://img.shields.io/badge/Python-3.13.5-blue?logo=python&logoColor=white)

</div>

## 注意⚠️

调用 X 平台的 API 过于频繁可能会导致账号异常，请酌情调整参数，本项目不对因此产生的账号问题负责

## 用法

1. 在 X 平台上下载旧账号的资料存档
2. 解压存档找到 data/block.js 文件，将文件放入项目的 data 目录下
3. 在自己的浏览器上用新账号登陆 X，并修改 main.py 的第 29 行为自己的浏览器类型
4. 运行 main.py 并查看屏蔽结果
5. 屏蔽的用户 id 会实时保存到 progress.txt 中作为进度，下次运行时，会从该用户的下一个用户开始屏蔽
