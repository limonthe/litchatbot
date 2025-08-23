

# 基于ChatGLM模型的俄语学习助手

基于ChatGLM模型与streamlit框架

<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />

<p align="center">
  <a href="https://github.com/limonthe/litchatbot/">
    <img src="images/logo.jpg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">俄语学习工具人</h3>
  <p align="center">
    本readme基于<a href="https://github.com/shaojintian/Best_README_template.git">模板</a>
    <br />
    <a href="https://github.com/limonthe/litchatbot"><strong>本项目的文档 »</strong></a>
    <br />
    <br />
    <a href="https://limonthe-litchatbot.streamlit.app/">查看Demo</a>
    ·
    <a href="https://github.com/limonthe/litchatbot/issues">报告Bug</a>
    ·
    <a href="https://github.com/limonthe/litchatbot/issues">提出新特性</a>
  </p>
</p>


## 目录

- [上手指南](#上手指南)
  - [配置要求](#配置要求)
  - [API_KEY获取](#API_KEY获取)
- [更新日志](#更新日志)
- [文件目录说明](#文件目录说明)
- [开发的架构](#开发的架构)
- [部署](#部署)
- [使用到的框架](#使用到的框架)
- [贡献者](#贡献者)
  - [如何参与开源项目](#如何参与开源项目)
- [版本控制](#版本控制)
- [作者](#作者)
- [鸣谢](#鸣谢)

### 上手指南
1. 选择参数
2. 选择预设角色
3. 输入问题
4. 等待机器人响应回答



###### 配置要求
1. Windows/Linux/Mac
2. Chorme内核浏览器
3. 稳定网络环境

###### API_KEY获取
1. 注册智谱开放平台 [https://www.zhipuai.cn/](https://www.zhipuai.cn/)
2. 在“个人面板”处查询api_key
3. 注：demo已内置api_key以供体验

### 更新日志
- v0.2  2025/8/15 在上班摸鱼中完成了大更新，简化了ui，重写了输入框逻辑，加入了角色卡功能，加入了知识库检索功能，并更新glm模型版本
- v0.1x-0.2 2025/7 在暑假的无所事事和摸鱼中修修补补，完善了ui
- v0.1  2025/4 基本完成交互框架，以及参数调整，可顺利响应，并通过结项检查👈重点
- >中间略过多个步骤与版本
- v0.01 2024/7 在立项之后开始搭框架

### 文件目录说明

```
filetree 
├── README.md
├── literature_chat_bot.py
├── requirements.txt
├── images
│  ├── logo.jpg
└── run.bat
```

### 开发的架构 

请阅读[ARCHITECTURE.md](https://github.com/limonthe/litchatbot/blob/master/ARCHITECTURE.md) 查阅为该项目的架构。

### 部署

https://limonthe-litchatbot.streamlit.app/#478b4ed3

### 使用到的框架
- [https://www.zhipuai.cn](https://www.zhipuai.cn)
- [https://streamlit.io/](https://streamlit.io/)
- [https://layui.dev/](https://layui.dev/)
- [https://getbootstrap.com](https://getbootstrap.com)
- [https://jquery.com](https://jquery.com)
- [https://laravel.com](https://laravel.com)

### 贡献者

请阅读**CONTRIBUTING.md** 查阅为该项目做出贡献的开发者。

#### 如何参与开源项目

贡献使开源社区成为一个学习、激励和创造的绝佳场所。你所作的任何贡献都是**非常感谢**的。


1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



### 版本控制

该项目使用Git进行版本管理。您可以在repository参看当前可用版本。

### 作者

@Limonthe

steam:Kpoetry  &ensp; qq:不告诉你w(ﾟДﾟ)w    

 *您也可以在贡献者名单中参看所有参与该项目的开发者。*

### 版权说明

详情请参阅 [LICENSE](https://github.com/limonthe/litchatbot/LICENSE)

### 鸣谢


- [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
- [Img Shields](https://shields.io)
- [Choose an Open Source License](https://choosealicense.com)
- [GitHub Pages](https://pages.github.com)
- [Animate.css](https://daneden.github.io/animate.css)
- [xxxxxxxxxxxxxx](https://connoratherton.com/loaders)

<!-- links -->
[your-project-path]:limonthe/litchatbot/
[contributors-shield]: https://img.shields.io/github/contributors/limonthe/litchatbot.svg?style=flat-square
[contributors-url]: https://github.com/limonthe/litchatbot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/limonthe/litchatbot.svg?style=flat-square
[forks-url]: https://github.com/limonthe/litchatbot/network/members
[stars-shield]: https://img.shields.io/github/stars/limonthe/litchatbot.svg?style=flat-square
[stars-url]: https://github.com/limonthe/litchatbot/stargazers
[issues-shield]: https://img.shields.io/github/issues/limonthe/litchatbot.svg?style=flat-square
[issues-url]: https://img.shields.io/github/issues/limonthe/litchatbot.svg
[license-shield]: https://img.shields.io/github/license/limonthe/litchatbot.svg?style=flat-square
[license-url]: https://github.com/limonthe/litchatbot/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/shaojintian
