import json

output_demo_1 = {
    "标题": [
        {
            "type": "text",
            "prompt": "XXXX"
        }
    ],
    "A Plus": [
        {
            "type": "image",
            "prompt": "XXXX",
            "path": "./image-1.png"
        },
        {
            "type": "image",
            "prompt": "XXXX",
            "path": "./image-2.png"
        }
    ],
    "自己的商品参考": "XXX",
    "竞对参考": "XXX",
}



def before(): 
    return "我需要你提取出下列的内容，规范格式化为一个 JSON 数组key有：标题、描述、主图、 A Plus 、自己的商品参考、竞对参考这几个，可以缺省。输出为 JSON 格式。其中如果遇到 [文本]XXX, [图片]XXX 的时候，就是下属 key 的任务。分别为 文本对应text, 图片对应image, 如果发现的是 image，请随机生成一个 path， 其中，自己的商品参考和竞对参考直接文本即可不需要 list。最终输出参考：{}".format(json.dumps(output_demo_1))


def md(): 
    with open('./templates/OUTPUT.md') as f:
        return "模板是：{}, 需要生成的目标我需要你基于这个 JSON 的内容以及规范，按照 prompt 顺序生成出文本和图片的路径，如果发现是text类型，请直接按照里面的prompt，结合自己的商品参考，竞对参考生成，并以自己的商品参考为主。遇到图片在markdown 里，用![](path)表示，切记要按照顺序生成。标题如果有多个提示，也需要按照要求生成多个。".format(f.read())