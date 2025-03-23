# from api.dmx.chat import ChatAPI
# from api.dmx.vision import VisionAPI

# 初始化客户端
# chat_client = ChatAPI(api_key="")
# vision_client = VisionAPI(api_key="")

# 文本生成示例
# response = chat_client.create_completion(
#     messages=[{"role": "user", "content": "}],
#     model="Qwen/Qwen2.5-7B-Instruct"
# )
# print(response)

# # 图片分析示例
# analysis = vision_client.analyze_image(
#     image_url="https://m.media-amazon.com/images/I/71I1XRg9zPL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
#     prompt="请帮我修改这个图片包装盒颜色为黄色",
#     model="gemini-2.0-flash"
# )
# print(analysis)

import api.gemini.client 