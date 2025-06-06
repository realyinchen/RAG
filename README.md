# RAG
RAG 系列教程源码仓库

![rag_landscape](https://github.com/realyinchen/RAG/blob/main/imgs/rag_landscape.png)

关注我的微信公众号获取最新推送

![wechat_qrcode](https://github.com/realyinchen/RAG/blob/main/imgs/wechat_qrcode.jpg)


## 运行环境

1. 安装[miniconda](https://docs.anaconda.com/miniconda/miniconda-install/)
2. 创建虚拟环境  
    ```
    $ conda create -n rag python=3.12
    ```
    我使用的是 python==3.12.7
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