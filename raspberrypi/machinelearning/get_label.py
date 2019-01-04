# 用来操控电脑相关文件属性与档案路径的模块
import os
# 用来操控图片，导入摄像头，处理色彩超级模块
import cv2
# 这是一个 matplotlib 下面的类，主要功能是制图
import matplotlib.pyplot as plt
# 这是一个 matplotlib 下面的类，提供格式小工具，这边使用的是方形选取
from matplotlib.widgets import RectangleSelector
# 一个用来处理 xml 文本的包，这边用来重新排布文本段落，使之更可视化
from lxml import etree
# 同上，只是它的引用名太长了，给个短的名字方便
import xml.etree.cElementTree as ET

# 人工输入一个我们目标的文件夹路径，让代码从此展开执行的旅程
folder_path = input("Enter the directory of the targeted folder: ")
# 一开始要全选出来的东西的名字也需要在这里 ”初始化“
Label_name = input("The object name being specified: ")
# 设置一个 list 容器，分别用来容纳之后经过鼠标产出的数据
TL_corner = []
BR_corner = []
Labels_list = []


# 定义一个 “事件“ 名为 mouse_click 的函数，在下面与 “RectangleSelector" 相连接
def mouse_click(press, release):
    # 当需要对这些变量在函数里面被修改的时候，用上 global 会比较精确且保险
    global TL_corner
    global BR_corner
    global Labels_list
    # 如果第一个参数按下去的 .button 按钮是鼠标左键的话
    if press.button == 1:
        # 就把这个框框左上与右下的值分别贴到两个空的 list 中做保存，并且把一开始我们取好名字的 Label 也存入 list 中
        TL_corner.append((int(press.xdata), int(press.ydata)))
        BR_corner.append((int(release.xdata), int(release.ydata)))
        Labels_list.append(Label_name)

    # 如果第二个参数放开鼠标的 .button 按钮是左键的话
    elif release.button == 3:
        # 就把最近一次存进去 list 里面的元素给删了，并且打印字串告知
        del TL_corner[-1]
        del BR_corner[-1]
        del Labels_list[-1]
        print('-- Latest bounding box has been removed --')


# 定义一个函数，用来在中途改变我们要标记的物体
def change_label(event):
    # 当需要对这些变量在函数里面被修改的时候，用上 global 会比较精确且保险
    global Label_name
    # 如果按下的按钮是滑鼠中间的滚轮（如果你的滑鼠没有滚轮那就 GG 了）
    if event.button == 2:
        # 继续让方框选择的功能开启
        selectImg_RS.set_active(True)
        # 重新输入定义标签名称
        Label_name = input('The other object name being specified: ')
        # 即便鼠标按下的功能不是滚轮，也还是要确保方框选择功能是被开启的状态
    elif event.button != 2:
        selectImg_RS.set_active(True)

    '''
这只是个用来学习和测试的代码部分，之所以留下来就是为了深刻告诉自己：
在 matplotlib.widgets 这个模块中的 RectangleSelector 和诸多 plt.connect(‘event name’, function)
的不同之处，当时用 RectangleSelector 的时候，他所链接到的自定义 function 就可以有两个 arguments，
他们分别表示按下和放开方框的时候鼠标的坐标轴位置，而 connect 的 event 就不同。
def mouse_press(press):
    global TL_corner
    if press.button == 1:
        TL_corner.append((int(press.xdata), int(press.ydata)))
    elif press.button == 3:
        print('-- Release button to remove your latest bounding box --')
    else:
        print('-- Please use mosue left click to select an area --')
def mouse_release(release):
    global BR_corner
    if release.button == 1:
        BR_corner.append((int(release.xdata), int(release.ydata)))
    elif release.button == 3:
        del TL_corner[-1]
        del BR_corner[-1]
    else:
        print('-- Please use mosue left click to select an area --')
拿这两个 function 做举例他们分别连接到的是 ‘button_press_event’ 和 ‘button_release_event’，
只容许他们在定义函数的时候有一个 argument 表示按下或是放开的瞬间鼠标坐标点的位置。
而那个 argument 自带的 .xdata | .ydata | .button 属性也是在 .connect 链接起来后自己产生的 attribute，
如果没有 connect，那是没有 .xdata 这类功能的。
'''

# 定义一个 xml 文件生成函数，需要方框的两个顶点坐标信息，图片放置位置，与最一开始的手动输入的目标文件位置
def xml_maker(TL_corner, BR_corner, file_path, folder_path):
    # os.path 生成的 object 有一个 .name 功能打印改路径的最后一个文件名称
    target_img = file_path.name
    # 告知 xml 文件最后面应该存在哪个资料夹，os.path.split() 可以把最后一个文件名和前面路径分开成为一个 tuple 里面的两个不同元素
    xml_save_dir = os.path.join(os.path.split(folder_path)[0],
                                os.path.split(folder_path)[1] + "_xml")
    # 如果没有这个文件夹名字的话，创造一个该路径下的文件夹
    if not os.path.isdir(xml_save_dir):
        os.mkdir(xml_save_dir)
    # 开始编辑 xml 文件内容，最外层的 Tag 叫 annotation
    main_tag = ET.Element('annotation')
    # main_tag 下面有许多子 tags，分别他们的内容要装的是对应到的文件夹名称，对应图片名称
    ET.SubElement(main_tag, 'folder').text = os.path.split(folder_path)[1]
    ET.SubElement(main_tag, 'filename').text = target_img
    ET.SubElement(main_tag, 'segmented').text = str(0)
    # 同理上面编辑步骤，把图片的尺寸资料记录于此
    size_tag = ET.SubElement(main_tag, 'size')
    ET.SubElement(size_tag, 'width').text = str(width)
    ET.SubElement(size_tag, 'height').text = str(height)
    ET.SubElement(size_tag, 'depth').text = str(depth)
    # 由于 object 可能有很多个，甚至很多个 objects 要记录，这边需要迭代，把三个 list 容器重新 zip 在一起会方便许多
    for La, TL, BR in zip(Labels_list, TL_corner, BR_corner):
        # 同理上面编辑步骤，把 object 对应的名字等信息记录于此
        object_tag = ET.SubElement(main_tag, 'object')
        ET.SubElement(object_tag, 'name').text = La
        ET.SubElement(object_tag, 'pose').text = 'Unspecified'
        ET.SubElement(object_tag, 'truncated').text = str(0)
        ET.SubElement(object_tag, 'difficult').text = str(0)
        # 同理上面编辑步骤，把方框起来的坐标记录于此
        bndbox_tag = ET.SubElement(object_tag, 'bndbox')
        ET.SubElement(bndbox_tag, 'xmin').text = str(TL[0])
        ET.SubElement(bndbox_tag, 'ymin').text = str(TL[1])
        ET.SubElement(bndbox_tag, 'xmax').text = str(BR[0])
        ET.SubElement(bndbox_tag, 'ymax').text = str(BR[1])
    # 为了让 xml 排布能够漂亮，pretty_print=True 前面的 root 必须是对应的 object，所以做了一个转换过去然后又变回来的过程
    xml_str = ET.tostring(main_tag)
    root = etree.fromstring(xml_str)
    xml_str = etree.tostring(root, pretty_print=True)
    # 重新命名文件夹并重新整合储存路径，修改意味着先要拆开
    #  os.path.splitext 可以良好的把文件名和档名分成两个元素放在一个 tuple 里面
    save_path = os.path.join(xml_save_dir,
                             str(os.path.splitext(target_img)[0] + '.xml'))
    # 储存文件于该位置
    with open(save_path, 'wb') as xml_file:
        xml_file.write(xml_str)
    # 定义一个函数，当对一张图片的事情做好了之后，跳到下一张图片时候需要做的事情
def next_image(release):
    global TL_corner
    global BR_corner
    global Labels_list
    # 如果按下的按钮是 Space 键，且方框选取功能是开着的
    if release.key in [' '] and selectImg_RS.active:
        # 那就呼叫刚定义好的生成 xml 函数
        xml_maker(TL_corner, BR_corner, file_path, folder_path)
        # 为了给自己方便看存了什么，在内容还没背归零最前先打印出来给我看看
        print(TL_corner, BR_corner, Labels_list)
        # 归零，并关掉该窗口
        TL_corner = []
        BR_corner = []
        Labels_list = []
        plt.close()
    # 如果按的不是 Space 键，则打印下面句子
    else:
        print('-- Press "space" to jump to the next pic --')
    # 只有当前 .py 文件呼叫的函数可以被执行，如果是 import 进来的文本里面有函数执行指令，该函数就会被挡住不执行
if __name__ == '__main__':
    # 遍历每个一开始输入进去的路径里面的文件路径
    for file_path in os.scandir(folder_path):
        # 如果里面有些文件不符合预期，让程序报错了，用此跳开进到下一个文件
        try:
            # 习惯的画图手法，可以一次创造 figure 和 axis 两个 objects 并且还同时描绘了几个子窗口，非常方便
            fig, ax = plt.subplots(1)
            # 使用 opencv 读取图片信息，找出其长宽深度值
            image = cv2.imread(file_path.path, -1)
            height, width, depth = image.shape
            # 并且由于在 matplotlib 显示图片是 RGB 格式，和 opencv 的BGR 顺序不同，需要转制
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # 在 matpolotlib 基础上秀出图片内容
            ax.imshow(image)
            # 把 widgets 里面的 RectangleSelector 跟 mouse_click 做关联，给他一个名字原因纯粹是太长了，要开要关不方便
            selectImg_RS = RectangleSelector(
                ax, mouse_click, drawtype='box',
                useblit=True, minspanx=5, minspany=5,
                spancoords='pixels', interactive=True)
            # 一样把其他上面设定好的函数与图片关联
            plt.connect('button_press_event', change_label)
            plt.connect('key_release_event', next_image)
            # plt.connect('button_press_event', mouse_press)
            # plt.connect('button_release_event', mouse_release)
            #  这里把在图片上面做的事情 show 出来
            plt.show()
            # 如果报错，则直接跳到下一个循环中
        except:
            continue