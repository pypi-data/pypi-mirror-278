# MediaKiller

当前版本 0.2.0

MediaKiller 可以通过配置文件操纵 ffmpeg 批量地对大量媒体文件转码。

> MediaKiller 并不能作为 ffmpeg 的替代。

和直接使用 ffmpeg 相比， MediaKiller 有如下优缺点：

- 可以进行大量视频批量处理
- 使用 **可复用的配置文件** 进行操作管理
- 每个转码任务可以通过文本模板的形式支持多文件输入和多文件输出
- 可以通过指定文件夹作为源文件的方式来批量添加任务
- 可以根据源文件路径保留指定层级的上层目录结构
- 可以读取`xml`、`fcpxml`、`csv`等文件中提供的源文件信息
- 拥有漂亮的进度监控和提示信息

## 配置文件

MediaKiller 使用`toml配置文件`描述工作内容。

使用配置文件可以方便地复用设置，
你可以保存多个不同的配置文件，并在将来对不同的视频文件进行同样的操作；
或者是在源文件修改后，一键重新运行转码任务，以快速更新目标文件。

使用 `--generate` 选项生成一个示例文件：

```shell
mediakiller '文件名.toml' --generate
# 或
mediakiller '文件名.toml' -g
```

> 在示例文件中包含所有选项的说明。

## 执行任务

不加任何选项地，指定配置文件，即可执行任务。

但是如果配置文件中未设置源文件，则仍需要使用`-a`选项添加任务，详情见下一章节。

```shell
mediakiller '配置文件.toml'
mediakiller '配置文件.toml' -a '需要转码的文件.mp4'
```

## 来源文件设置

一种可能的情况是：配置文件中仅仅制定了转码选项和目标位置。
（事实上这也是推荐的使用方式。）

这种情况下可以使用 `--add-source` 添加源文件，
这种情况下增加的源文件会附加在配置文件中指定的源文件列表之后。

例如，在配置文件 `example.toml` 中有如下设置：

```toml
# example.toml
[input]
files = ['a.mov', 'b.mov', 'c.mov']
```

那么运行下面的命令之后——

```shell
mediakiller 'example.toml' --add-source 'one.mp4' -a 'two.mp4'
# -a 是 --add-source 的缩写
```

—— MediaKiller 将会处理全部 5 个目标文件。

所以，如果不在配置文件中制定源文件可以最大程度重复使用它们。

> 注意：`--add-source`选项只能指定一个来源项目，
> 但是你可以多次使用它，或直接指定一个文件夹。
> 这样就可以添加多个源文件了。

## 来源文件的解析

在使用来源文件之前，MediaKiller 将会进行一系列处理：

1. 将`--add-source`指定的文件项目添加到从`配置文件`中解析的来源文件列表之后。
   此列表将会被存储为`input.file`。

2. 遍历`input.file`中的每一项：
    - 若：文件扩展名是被支持的**列表文件**,

      则：读取其中包含的片段信息，并将它们添加到`源文件列表`

    - 若：不是列表文件，

      则：直接添加到`源文件列表`

3. 初始化`扩展名列表`，
    - 将`配置文件`中的`input.suffix_includes`添加到`扩展名列表`，
    - 将`配置文件`中的`input.suffix_excludes`中包含的项目从`扩展名列表`中移除

4. 遍历`源文件列表`，并将所有的文件夹递归地展开，
   并将扩展名符合`扩展名列表`的文件添加到`源文件列表`

5. 根据路径排序`源文件列表`

6. 检查`源文件列表`，去除重复的或不存在的文件

之后才会根据`配置文件`的设置，依次处理来源文件。

## 相对路径 vs 绝对路径

在配置文件中，所有的文件都可以使用相对路径指定，
但是相对路径并非相对于当前的工作目录的，
而是相对于`general.working_folder`所设定的目录，
此目录默认为配置文件所在的目录。

```toml
[general]
working_folder = '.'
```

这允许将配置文件拷贝至不同位置后，
作为一个 *make* 文件展开成为目标文件的用法成为可能。

## 生成可执行脚本

如果指定了`--make-script`选项，
MediaKiller 不会自动转码，而是会生成一个脚本文件。
当然，**必须指定脚本文件的保存位置**。

你可以使用任何手段对脚本文件进行编辑，
也可以将脚本文件复制到没有安装 MediaKiller 的环境中运行。

```shell
mediakiller 'example.toml' --make-script 'script.sh'
# 或
mediakiller 'example.toml' -s 'script.ps1'
# -s 是 --make-script 的缩写
```

生成的脚本文件仅仅是普通的文本文件而已，
既**不包含 shebang**，也**没有运行权限**。
所以运行时你需要自己指定使用的 shell：

```shell
media 'example.toml' --make-script 'script.ps1'
pwsh 'script.ps1'
```

## 调试与测试

MediaKiller 包含 2 个选项用于调试和测试目的。

- `--pretend` `-p` 选项通知 MediaKiller 进入模拟运行状态。

  此状态下会正常运行所有功能，但是并不会运行 ffmpeg 进行转码。
  但是`--make-script`选项仍然会正常输出脚本。

- `--debug` `-d` 选项为 MediaKiller 开启调试模式。

调试模式下将会启用大量的运行细节输出，便于查找到底出了什么问题。

-----
项目主页: https://gitee.com/xiii_1991/cxalio-studio-tools

作者: xiii_1991@163.com

