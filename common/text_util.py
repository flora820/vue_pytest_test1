from pathlib import Path

base_dir = Path(__file__).parent.parent

def read_txt(text_file):
    """读取txt文件"""
    with open(text_file, 'r', encoding='utf-8') as f:
        return f.read()


def write_txt(text_file, data):
    """追加写入txt文件"""
    with open(text_file, 'a') as f:
        f.write(data)


def extract_txt(text_file, data):
    """覆盖写入txt文件"""
    # 覆盖保存
    with open(text_file, 'w+') as f:
        f.write(data)
    # 读取
    # return read_txt(text_file)


def truncate_txt(text_file):
    """清空txt文件"""
    with open(text_file, 'w') as f:
        f.truncate()


def read_txt_handel(text_file):
    #"""将保存运行结果的txt数据，处理成想要的格式"""
    value = read_txt(text_file=text_file)

if __name__ = '__main__':

        read_txt_handel(text_file)

