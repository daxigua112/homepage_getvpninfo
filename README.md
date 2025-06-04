# homepage_getvpninfo
从机场订阅链接获取流量信息，在 Homepage 上显示
![59a8a57d4208c7e99a4c5bf39b1c96ff.jpeg](https://i.miji.bid/2025/06/04/59a8a57d4208c7e99a4c5bf39b1c96ff.jpeg)

通过抓取 Loon 读取的机场订阅链接 Header 头中的Subscription-Userinfo 信息来获得流量信息。

## 使用方法

在 config.json 中配置机场信息，机场订阅链接需要是 Loon 的订阅链接（可以在机场订阅面板上找到）。

V2Board 系机场可以在原有订阅链接（https://xxx.com/api/v1/client/subscribe?token=xxx） 
后添加&flag=loon 来强制获取 Loon 订阅链接。

脚本生成的 json 文件请放置在可以让 Homepage 访问的目录下，也可以使用 Crontab 设置定时任务来定期刷新流量信息。

## HomePage 设置
HomePage 设置可参考官方文档中-Widgets-Custom API 来设置，也可以参考:

```
- xxxCloud:
        icon: mdi-cloud-outline
        widget:
          type: customapi
          url: https://xxx/xxcloud.json
          refreshInterval: 60000
          method: GET
          display: inline
          mappings:
            - field: upload
              label: 上传流量
              format: text
            - field: download
              label: 下载流量
              format: text
            - field: used
              label: 已用流量
              format: text
            - field: total
              label: 套餐总流量
              format: text
            - field: expire_ts
              label: 套餐到期时间
              format: text

```
