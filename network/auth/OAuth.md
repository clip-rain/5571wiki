## OAuth2

### 一、定义
OAuth2是一个授权框架，或者说是一个标准，[规范RFC6749](https://datatracker.ietf.org/doc/html/rfc6749). 它使得第三方应用能够以资源所有者的身份或者第三方应用自己的身份来获取目标应用的部分权限。

下面是OAuth2的流程示意。这里注意一下，不同的厂商，在实现该框架的时候会有一些差别，并不一定是图中所示的流程。

![Oauth2 flow](../../static/oauth2.png)

### 二、场景



### 三、Grant Type
- 1、 Authorization code （目前People的系统基本都是这种方式， https://developer.okta.com/blog/2018/04/10/oauth-authorization-code-grant-type）
- 2、Implicit flow             （简化版，token直接返回，而不是通过code来交换）
- 3、password Grant      （用户名和密码都告诉给client）
- 4、Client Credentials   （client代替用户）
- 5、PKCE （proof key of code exchange) 这个主要是app或者桌面应用无法像web应用那样在server端用一个固定的client_secret来防止authorization code被中间人盗窃。所以使用一个†动态生成secret的方式来完成认证流程。

### 四、Authoriztion Code


### 五、PKCE（Proof Key of Code Exchange)



### 六、reference

- https://developer.okta.com/blog/2018/04/10/oauth-authorization-code-grant-type
- https://oauth.net/2/grant-types/
- https://www.oauth.com/oauth2-servers/background/
