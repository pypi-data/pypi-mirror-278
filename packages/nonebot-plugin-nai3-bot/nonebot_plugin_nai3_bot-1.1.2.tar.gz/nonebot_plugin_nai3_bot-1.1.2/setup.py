# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_nai3_bot', 'nonebot_plugin_nai3_bot.platfrom']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0',
 'httpx>=0.27.0,<0.28.0',
 'nonebot-adapter-onebot>=2.2.1,<3.0.0',
 'nonebot2>=2.0.0rc3,<3.0.0',
 'openai>=1.30.1,<2.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-nai3-bot',
    'version': '1.1.2',
    'description': '基于GPT4+NovelAI V3,Bot在将自然语言转换为NAI3提示词并绘图发送的同时,还会以自定义人格和你聊天',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-nai3-bot\n</div>\n\n# 介绍\n- 本插件基于GPT4+NovelAI V3/Stable Diffusion API,Bot在将自然语言转换为NAI3提示词并绘图发送的同时以自定义人格与用户聊天。\n- 用户可以正常与指定人格（需要调教prompt,目前插件内置的人格为群友指定的BA角色天童爱丽丝）聊天。在聊天过程中可以使用自然语言描述AI绘图的需求,Bot会根据用户的聊天内容修改AI绘图所用的提示词（见效果图）,并且判断是否需要调用Novel V3模型/Stable Diffusion进行绘画。如果为正常聊天则不会触发绘画功能,如果Bot判断用户有AI绘画的需求,则会调用NAI3绘图,并将图片和提示词发送到群内。\n- 每个用户和Bot有独立的聊天记录。\n\n# 效果\n![Alt](demo1.jpeg)\n\n# 安装\n* 手动安装\n  ```\n  git clone https://github.com/Alpaca4610/nonebot_plugin_nai3_bot.git\n  ```\n\n  下载完成后在bot项目的pyproject.toml文件手动添加插件：\n\n  ```\n  plugin_dirs = ["xxxxxx","xxxxxx",......,"下载完成的插件路径/nonebot-plugin-nai3-bot"]\n  ```\n* 使用 pip\n  ```\n  pip install nonebot-plugin-nai3-bot\n  ```\n# 配置文件\n\n在Bot根目录下的.env文件中追加如下内容：\n\n必填内容：\n```\nnai3_token = "xxxx"  # NovelAI的token,与sd_api二选一\nsd_api = "xxxxxx"    # stable diffusion的API地址，与nai3_token二选一。示例 http://{ip}:{port}/sdapi/v1/txt2img\noneapi_key = "sk-xxxxxxxxxx"  # （必填）OpenAI官方或者是支持OneAPI的大模型中转服务商提供的KEY\n```\n\n可选内容：\n```\noneapi_url = "https://xxxxxxxxx"  # （可选）大模型中转服务商提供的中转地址,使用OpenAI官方服务不需要填写\noneapi_model = "gpt-4" # （可选）使用的语言大模型,建议使用gpt4或gpt4o模型以达到更好的体验效果此项,默认使用gpt-4模型\n```\nNAI3的token获取地址方法：\n![Alt](image.png)\n\n# 使用方法\n- **  聊天内容/绘图需求      （**是触发与Bot对话的关键字）\n- 记忆清除 清除当前用户的聊天记录\n- 切换人格 切换机器人聊天的人格\n\n# 可能存在的问题\n- 由于调教prompt的原因，机器人可能会偶尔出错，此时继续和TA对话或者是使用记忆清除命令重新开始对话即可。\n- 注意语言大模型的token消耗量\n- 插件目前没有实现绘图排队提醒，多用户同时绘图NAI3可能会返回错误。\n# 添加人格\n1. 在机器人运行目录的`data`文件夹下创建文件`nai3_character.json`\n2. 参考[人格调教模版](default_character.txt)，将模版中的第1部分修改成你的新人格和更改剩下部分的人格名称。\n3. 参考[人格列表模版](nai3_character.json)，修改`nai3_character.json`文件。json文件的格式如下：\n   ```json\n   {\n        "name": "人格名称（用于切换人格时区分）",\n        "nickname": "人格昵称",\n        "prompt": "调教prompt的base64编码格式，请参照默认人格模版，将模版中的第1部分修改成你的新人格和更改剩下部分的人格名称即可，然后再将文字转换成base64编码填入此部分"\n    }\n    ```\n    多人格切换请写成json列表的形式\n4. 发送切换人格，根据机器人的提示即可切换当前人格。若切换之前存在历史对话，清除聊天历史记录即可和新人格对话。\n\n# TODO\n- [x] 添加用户自定义人格功能\n- [ ] 代理支持\n- [ ] 支持绘图排队信息提醒(NAI3只支持一次出一张图)\n',
    'author': 'Alpaca',
    'author_email': 'alpaca@bupt.edu.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
