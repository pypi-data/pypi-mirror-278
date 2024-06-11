# Batch Commander

batchcommander 是一个使用给定的命令行模板批量处理文件的工具。

和本工具集中的其它工具一样，batchcommander的核心是 PathExpander 功能，
通过它可以快速展开多层文件夹。另外，还使用到了TagReplacer进行命令的模式匹配。
它是本工具集各个工具基础功能的高度凝练。

## ~~基础用法~~

> 这是一个高级工具，所以**没有基础用法** :)

## 高级用法

正常使用 batchcommander，必须指定：

- 需要进行处理的源文件路径，一个或多个
- 需要对文件执行的操作

### 路径展开

默认情况下，batchcommander 将会对用户提供的源文件路径进行一系列预处理：

1. 将路径中的通配符展开为文件列表
2. 如果指定了 `--recursive` 参数，则会将输入列表中的各级目录全部展开
3. 根据 `--processing-mode` 的选项准备源文件列表：
    - `file` 模式： 只保留文件，忽略目录
    - `folder` 模式： 只处理目录，忽略文件
    - `none` 或 `未设置` ： 默认情况下，将会保留所有的文件和文件夹
4. 对来源列表按照绝对路径排序

### 使用模式标签定义命令

因为将要批量处理文件，所以当然不能使用普通的命令来定义操作。
batchcommander 引入了 **模式标签** 功能。

和 mediakiller 的配置文件类似，模式标签使用大括号括起来，
里面使用 `数据源:参数` 的形式引用信息，
batchcommander 将在执行时进行填充。

**"source"** 源文件数据源的参数定义如下：

| 参数                     | 说明            | 用例                                              |
|------------------------|---------------|-------------------------------------------------|
| 无参数                    | 直接输出输入的源文件路径  | {source} -> 'folder/file.1.txt' *以下用例都会以此路径为例。* |
| absolute               | 源文件的绝对路径      | {source:absolute} -> 'root/folder/file.1.txt'   |
| name                   | 源文件的文件名       | {source:name} -> 'file.1.txt'                   |
| basename               | 源文件不包含扩展名的文件名 | {source:basename} -> 'file'                     |
| complete_basename      | 不包含最后扩展名的文件名  | {source:complete_basename} -> 'file.1'          |
| suffix                 | 源文件的扩展名       | {source:suffix} -> '.txt'                       |
| suffix_no_dot          | 不包含点号的扩展名     | {source:suffix_no_dot} -> 'txt'                 |
| complete_suffix        | 完整的扩展名        | {source:complete_suffix} -> '.1.txt'            |
| complete_suffix_no_dot | 不包含第一个点的完整扩展名 | {source:complete_suffix_no_dot} -> '1.txt'      |
| parent                 | 原始输入中的父级路径    | {source:parent} -> 'folder'                     |
| parent_absolute        | 父级文件夹的绝对路径    | {source:parent_absolute} -> '/root/folder'      |
| parent_name            | 父目录的名称        | {source:parent_name} -> 'folder'                |

另外，batchcommander 还提供 `{sep}` 标签，用于自动替换为当前系统下正确的路径分隔符。

> batchcommander 将会针对每个输入文件填充命令中的标签并执行。

### 综合应用

下面是一些例子：

```shell
batchcommander -c "cp -r {source} target_folder/{source:basename}.bak{source:suffix}" a.txt,b.txt,...
# 此命令将会拷贝每个源文件到指定的目录并改名
```

```shell
batchcommander -c "ffmpeg -i {source} -i {source:parent}/{source:basename}.srt {source:basename}.mkv" a.mp4,b.mp4,...
# 此命令将会按照文件名读取字幕文件并和视频合并为mkv视频 
```

## 测试运行

指定 `--verbose` `-v` 参数时，将会直接输出执行命令的标准输出。

指定 `--pretend` 参数可以启用干转模式，
subconv 将会处理所有的内容，但是不会真的输出文件。

也可以使用 `--debug` 参数，将会输出所有工作过程的信息，方便查看。

两个选项可以一起使用。

-----
项目主页: https://gitee.com/xiii_1991/cxalio-studio-tools

作者: xiii_1991@163.com