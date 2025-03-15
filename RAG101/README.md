# 🚀 RAG 从入门到精通

关注我的微信公众号获取最新推送

![wechat_qrcode](https://github.com/realyinchen/RAG/blob/main/imgs/wechat_qrcode.jpg)

### 主要特点
🧠 最先进的 RAG 增强功能  
📚 每种技术的综合文档  
🛠️ 实用的实施指南  
🌟 定期更新最新进展  

# 教程概述

本教程将以 LangChain/LangGraph 框架为主介绍了各种当今流行的 RAG 技术。  

### 运行环境

本教程中的代码全部在 VS Code 编辑器中使用 jupyter notebook 编写。  

首先需要安装 VS Code，[点击下载](https://code.visualstudio.com/Download)。

1. 安装 [miniconda](https://docs.anaconda.com/miniconda/miniconda-install/)
2. 创建虚拟环境  
    ```
    $ conda create -n rag python=3.12
    ```
3. 激活虚拟环境  
    ```
    $ conda activate rag
    ```
4. 配置 jupyter kernel  
    ```
    $ conda install -c anaconda ipykernel
    $ python -m ipykernel install --user --name rag
    ```
5. 将项目根目录下的环境变量配置文件重命名，并根据实际情况，填入你的配置信息  
    ```
    $ mv .example.env .env
    ```

6. 安装依赖包
    ```
    pip install -r requirements.txt
    ```

# 鸣谢

本教程灵感来自 [RAG_Techniques](https://github.com/NirDiamant/RAG_Techniques/tree/main)  
