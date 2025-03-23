from api.dmx.chat import ChatAPI
from api.dmx.vision import VisionAPI
from api.gemini.client import GeminiAPIClient
from utils.to_pdf import convert_markdown_to_pdf
from utils.extract_tasks import extract_tasks
from utils.loads_output import write_task_file
from prompt.extract_generate import before, md
import json
import os

DMX_KEY = os.environ.get('DMX_KEY')
GEN_KEY = os.environ.get('GEN_KEY')


# 初始化客户端
chat_client = ChatAPI(api_key=DMX_KEY)
vision_client = VisionAPI(api_key=DMX_KEY)
genai_clent = GeminiAPIClient(api_key=GEN_KEY)



OUTPUT_DIR = 'output'

tasks = extract_tasks('./tasks')
print('[chaos] 处理任务 {} 个'.format(len(tasks)))

for task in tasks[1:2]:
    content = task['content']
    entry = task['entry']
    imgs = task['imgs']
    response = chat_client.create_completion(
       messages=[{"role": "system", "content": 'you are a formatter'}, {"role": "user", "content": before()+ content}],
       model="Doubao-1.5-lite-32k"
    )
    
    format_task = None
    try:
        format_task = json.loads(response)
        write_task_file(task_name=entry, base_dir=OUTPUT_DIR, data=format_task,content_type='json', filename='task.json')
        print('[chaos] [{}] tasks loads success'.format(entry))
    except Exception as e:
        print('[chaos] [{}] tasks loads config error'.format(entry))
        print(response, e)
        continue
    
    # 开始填充 md

    
    try:
        response = chat_client.create_completion(
       messages=[{"role": "user", "content": md()+ response}],
       system_prompt='注意生成的文案除模板其他都要全英文，背景是我这个是亚马逊商品的生成，需要符合亚马逊商品的风格。生成目标：markdown',
       model="gemini-2.0-flash"
        )
        write_task_file(task_name=entry, base_dir=OUTPUT_DIR, data=response, content_type='md', filename='README.md')
        print('[chaos] [{}] tasks write markdown success'.format(entry))

    except Exception as e:
        print('[chaos] [{}] tasks write markdown error'.format(entry))
        print(response, e)
        continue
    
    # 最后开始生成图片

    with open('./templates/empty.png', 'rb') as f:
      empty_image = f.read()

    image_tasks = []
    for key, value in format_task.items():
        if(isinstance(value, str)): 
            continue
        for part in value:
            if(part['type'] == 'image'):
                image_tasks.append(part)

    for image_item in image_tasks:
        try:
            path = image_item['path']
            image = genai_clent.generate_image_from_prompt(
              prompt=image_item['prompt'],
              image_paths=imgs,
            )
            if(image):
                write_task_file(task_name=entry, base_dir=OUTPUT_DIR, data=image, content_type='image', filename=path)
                print('[chaos] [{}] [{}] tasks write image success'.format(entry, path))

            else:
                write_task_file(task_name=entry, base_dir=OUTPUT_DIR, data=empty_image, content_type='image', filename=path)

        except Exception as e:
                print('[chaos] [{}] [{}] tasks write image error {}'.format(entry, path, e))
                write_task_file(task_name=entry, base_dir=OUTPUT_DIR, data=empty_image, content_type='image', filename=path)
                continue

    # 最后输出 pdf
    convert_markdown_to_pdf(os.path.join(OUTPUT_DIR, entry))

    print('[chaos] [{}] tasks done'.format(entry))