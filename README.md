## 本地视频播放器

用于目录中的所有视频进行浏览，单击后便可以播放

## 项目简介

django 项目，默认 sqlite3 数据库， 

视频文件放在根目录下`media`中

local_video_viewer 为项目配置名称,  
videos 为主应用名

为什么要用 django ？ 答：用于练手  
为什么要写这个项目？ 答：满足自己需求，看小电影手机存储太小了，直接用电脑存，然后就可以躺着在局域网中浏览器看。主要还是练手（笑。

## 版本更替

### 0.1 版本

django 项目搭建， 配置 django；对media目录下的视频进行展示，并且单击后可以播放。

下版本需求：

- 由于视频文件过大，导致必须要将视频加载完成后才能拖动进度条。启用视频流式传输，确保视频在下载的同时就开始播放，从而允许用户拖动进度条。

### 0.11 版本

在使用使用静态路径来返回视频文件，如果视频比较小，可以一次性传递完成，如果大视频文件，会造成无法使用进度条拖动。

使用流文件传递可以很好的解决这个问题，web 内置的`<video>`，有内置请求，当拖动进度条时，会想服务器请求带有 `RANGE` 请求头， 像服务器请求视频二进制文件流的位置，服务器只要返回相应的二进制文件流即可

- 实现流文件传递，拖动进度条时可以实时传输数据

下版本需求：

- 视频图片简略图展示，同时需要展示文件夹的图片，以提供参考
- 显示的视频缩略图最好可以显示视频的主体
- 文件夹图片可以自己手动上传，也可以拿文件夹下的视频文件的缩略图进行展示

### 0.12 版本

将页面进行美化，提高人机交互，同样适用于手机。  
可以显示视频的缩略图。  

显示视频缩略图的逻辑是，当单击某个分类后，如果这是第一次打开，便开始获取这个视频的缩略图，在同一个根目录中创建一个 `thumbnails` 文件夹来存储缩略图，

获取视频最中间的帧来当缩略图。

目前只适用于mp4视频文件

考虑到目前项目没有太高的需求，所以显示视频主体暂时搁置，主要原因有这些情况：

- 对视频主体的显示需要 `YOLO` 或者其他机器学习框架，暂时还不太会
- 目前项目只是需要对缩略图快速进行显示，能看个大概就行；不要求太高的算力，使用这些框架会影响主页加载速度
- 最主要原因：不想搞训练集，太枯燥了，太麻烦了。

对于缩略图工具包的选择，还是还是选择 `PyAV` ，`opencv` 不太适合目前的使用环境，因为当前的环境对图片的处理并不是太重要，主要还是视频处理的比较多，之后可能会考虑到视频的编码以及压缩。

### 1.0 版本

实现大部分基础功能，第一个稳定版本

添加的功能： 
- 为分类项显示其项目中包含的缩略图
- 添加的返回按钮，可以返回到上一个打开的页面