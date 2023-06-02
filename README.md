
# VideoParsing

用于解析短视频源视频的地址

## 当前支持

### 国内网站

| **名称**                                     | **说明**                          | **示例**                                                                              | **是否去水印**             | **源代码**                                                                                  |
|--------------------------------------------|---------------------------------|-------------------------------------------------------------------------------------|-----------------------|------------------------------------------------------------------------------------------|
| [抖音](https://www.douyin.com/)              |                                 | https://v.douyin.com/UQbUk8P/                                                       | ✅                     | [SourceCode](https://github.com/gantianca/VideoParsing/blob/main/video_list/douyin.py)   |
| [快手](https://www.kuaishou.com/)            |                                 | https://www.kuaishou.com/f/Xa5uAnvebm1L1Hv                                          | ✅                     | [SourceCode](https://github.com/gantianca/VideoParsing/blob/main/video_list/kuaishou.py) |
| [Bilibili](https://www.bilibili.com/)      | 需要cookie，目前不支持番剧和综艺等，仅支持up主上传视频 | https://www.bilibili.com/video/BV1KV4y1k7xG?spm_id_from=333.1007.tianma.1-2-2.click | ❌                     | [SourceCode](https://github.com/gantianca/VideoParsing/blob/main/video_list/bilibili.py) |
| [西瓜视频](https://www.ixigua.com/)            |                                 | https://www.ixigua.com/7238084020184023585?logTag=c7295b06c939cc63b2e3              | ✅                     | [SourceCode](https://github.com/gantianca/VideoParsing/blob/main/video_list/ixigua.py)   |
| [小红书](https://www.xiaohongshu.com/explore) |                                 | https://www.xiaohongshu.com/explore/6475357f0000000012030b52                        | ✅                     | [SourceCode](https://github.com/gantianca/VideoParsing/blob/main/video_list/xhs.py)      |
| [AcFun](https://www.acfun.cn/)             | 解析结果是m3u8链接                     | https://www.acfun.cn/v/ac41468577                                                   | ✅                     | [SourceCode](https://github.com/gantianca/VideoParsing/blob/main/video_list/acfun.py)    |
| [微博](https://weibo.com/)                   | 微博视频种类太多，解析前最好找到最原始的视频页面        | https://weibo.com/tv/show/1034:4908221480239143?from=old_pc_videoshow               | ❌                     | [SourceCode](https://github.com/gantianca/VideoParsing/blob/main/video_list/weibo.py)    |

### 国外网站

| 名称                                      | 说明                                                                                   | 示例                                                                                             | 是否去水印 | 源代码                                                                                       |
|-----------------------------------------|--------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|-------|-------------------------------------------------------------------------------------------|
| [YouTube](https://www.youtube.com/)     | 使用[yt_dlp](https://github.com/yt-dlp/yt-dlp)实现，因为我尝试了几种方式获取到的链接都会受到限速，那就直接用现成的好了(😀) | https://www.youtube.com/watch?v=w43sgDbYH3A                                                    | ✅     | [SourceCode](https://github.com/gantianca/VideoParsing/blob/main/video_list/youtube.py)   |
| [TikTok](https://www.tiktok.com/en/)    | 解析的时候代理位置不能在TikTok不提供服务的地区，如香港                                                       | https://www.tiktok.com/@qwertyaaz9/video/7239183982493994242?is_from_webapp=1&sender_device=pc | ✅     | [SourceCode](https://github.com/gantianca/VideoParsing/blob/main/video_list/tiktok.py)    |
| [instagram](https://www.instagram.com/) | 需要cookie                                                                             | https://www.instagram.com/p/Cm_apxxvg2G/                                                       | ✅     | [SourceCode](https://github.com/gantianca/VideoParsing/blob/main/video_list/instagram.py) |
| [Facebook](https://www.facebook.com/)   | 需要cookie                                                                             | https://fb.watch/iInbMAf4Hm/                                                                   | ✅     | [SourceCode](https://github.com/gantianca/VideoParsing/blob/main/video_list/Facebook.py)  |

以上展示一些主流网址，更多请查看[支持网站列表](https://github.com/gantianca/VideoParsing/blob/main/video_data_list.yaml)
