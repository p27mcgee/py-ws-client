from html.parser import HTMLParser
from html.entities import name2codepoint

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        for attr in attrs:
            print("     attr:", attr)

    def handle_endtag(self, tag):
        print("End tag  :", tag)

    def handle_data(self, data):
        print("Data     :", data)

    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)

    def handle_decl(self, data):
        print("Decl     :", data)

parser = MyHTMLParser()

html = """
<!DOCTYPE html>
<html>

<head>
	<title>Central Repository: org/springframework</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<style>
body {
	background: #fff;
}
	</style>
</head>

<body>
	<header>
		<h1>org/springframework</h1>
	</header>
	<hr/>
	<main>
		<pre id="contents">
<a href="../">../</a>
<a href="amqp/" title="amqp/">amqp/</a>                                                            -         -      
<a href="analytics/" title="analytics/">analytics/</a>                                                       -         -      
<a href="android/" title="android/">android/</a>                                                         -         -      
<a href="aws/" title="aws/">aws/</a>                                                             -         -      
<a href="batch/" title="batch/">batch/</a>                                                           -         -      
<a href="beandoc/" title="beandoc/">beandoc/</a>                                                         -         -      
<a href="boot/" title="boot/">boot/</a>                                                            -         -      
<a href="build/" title="build/">build/</a>                                                           -         -      
<a href="cloud/" title="cloud/">cloud/</a>                                                           -         -      
<a href="commons/" title="commons/">commons/</a>                                                         -         -      
<a href="credhub/" title="credhub/">credhub/</a>                                                         -         -      
<a href="data/" title="data/">data/</a>                                                            -         -      
<a href="flex/" title="flex/">flex/</a>                                                            -         -      
<a href="geode/" title="geode/">geode/</a>                                                           -         -      
<a href="guice/" title="guice/">guice/</a>                                                           -         -      
<a href="hateoas/" title="hateoas/">hateoas/</a>                                                         -         -      
<a href="integration/" title="integration/">integration/</a>                                                     -         -      
<a href="javaconfig/" title="javaconfig/">javaconfig/</a>                                                      -         -      
<a href="kafka/" title="kafka/">kafka/</a>                                                           -         -      
<a href="ldap/" title="ldap/">ldap/</a>                                                            -         -      
<a href="maven/" title="maven/">maven/</a>                                                           -         -      
<a href="metrics/" title="metrics/">metrics/</a>                                                         -         -      
<a href="mobile/" title="mobile/">mobile/</a>                                                          -         -      
<a href="osgi/" title="osgi/">osgi/</a>                                                            -         -      
<a href="plugin/" title="plugin/">plugin/</a>                                                          -         -      
<a href="restdocs/" title="restdocs/">restdocs/</a>                                                        -         -      
<a href="retry/" title="retry/">retry/</a>                                                           -         -      
<a href="roo/" title="roo/">roo/</a>                                                             -         -      
<a href="security/" title="security/">security/</a>                                                        -         -      
<a href="session/" title="session/">session/</a>                                                         -         -      
<a href="shell/" title="shell/">shell/</a>                                                           -         -      
<a href="social/" title="social/">social/</a>                                                          -         -      
<a href="spring/" title="spring/">spring/</a>                                                          -         -      
<a href="spring-agent/" title="spring-agent/">spring-agent/</a>                                                    -         -      
<a href="spring-aop/" title="spring-aop/">spring-aop/</a>                                                      -         -      
<a href="spring-asm/" title="spring-asm/">spring-asm/</a>                                                      -         -      
<a href="spring-aspects/" title="spring-aspects/">spring-aspects/</a>                                                  -         -      
<a href="spring-beandoc/" title="spring-beandoc/">spring-beandoc/</a>                                                  -         -      
<a href="spring-beans/" title="spring-beans/">spring-beans/</a>                                                    -         -      
<a href="spring-binding/" title="spring-binding/">spring-binding/</a>                                                  -         -      
<a href="spring-context/" title="spring-context/">spring-context/</a>                                                  -         -      
<a href="spring-context-indexer/" title="spring-context-indexer/">spring-context-indexer/</a>                                          -         -      
<a href="spring-context-support/" title="spring-context-support/">spring-context-support/</a>                                          -         -      
<a href="spring-core/" title="spring-core/">spring-core/</a>                                                     -         -      
<a href="spring-dao/" title="spring-dao/">spring-dao/</a>                                                      -         -      
<a href="spring-expression/" title="spring-expression/">spring-expression/</a>                                               -         -      
<a href="spring-framework-bom/" title="spring-framework-bom/">spring-framework-bom/</a>                                            -         -      
<a href="spring-full/" title="spring-full/">spring-full/</a>                                                     -         -      
<a href="spring-hibernate/" title="spring-hibernate/">spring-hibernate/</a>                                                -         -      
<a href="spring-hibernate2/" title="spring-hibernate2/">spring-hibernate2/</a>                                               -         -      
<a href="spring-hibernate3/" title="spring-hibernate3/">spring-hibernate3/</a>                                               -         -      
<a href="spring-ibatis/" title="spring-ibatis/">spring-ibatis/</a>                                                   -         -      
<a href="spring-instrument/" title="spring-instrument/">spring-instrument/</a>                                               -         -      
<a href="spring-instrument-tomcat/" title="spring-instrument-tomcat/">spring-instrument-tomcat/</a>                                        -         -      
<a href="spring-jca/" title="spring-jca/">spring-jca/</a>                                                      -         -      
<a href="spring-jcl/" title="spring-jcl/">spring-jcl/</a>                                                      -         -      
<a href="spring-jdbc/" title="spring-jdbc/">spring-jdbc/</a>                                                     -         -      
<a href="spring-jdo/" title="spring-jdo/">spring-jdo/</a>                                                      -         -      
<a href="spring-jms/" title="spring-jms/">spring-jms/</a>                                                      -         -      
<a href="spring-jmx/" title="spring-jmx/">spring-jmx/</a>                                                      -         -      
<a href="spring-jpa/" title="spring-jpa/">spring-jpa/</a>                                                      -         -      
<a href="spring-ldap/" title="spring-ldap/">spring-ldap/</a>                                                     -         -      
<a href="spring-messaging/" title="spring-messaging/">spring-messaging/</a>                                                -         -      
<a href="spring-mock/" title="spring-mock/">spring-mock/</a>                                                     -         -      
<a href="spring-ojb/" title="spring-ojb/">spring-ojb/</a>                                                      -         -      
<a href="spring-orm/" title="spring-orm/">spring-orm/</a>                                                      -         -      
<a href="spring-oxm/" title="spring-oxm/">spring-oxm/</a>                                                      -         -      
<a href="spring-parent/" title="spring-parent/">spring-parent/</a>                                                   -         -      
<a href="spring-portlet/" title="spring-portlet/">spring-portlet/</a>                                                  -         -      
<a href="spring-remoting/" title="spring-remoting/">spring-remoting/</a>                                                 -         -      
<a href="spring-struts/" title="spring-struts/">spring-struts/</a>                                                   -         -      
<a href="spring-support/" title="spring-support/">spring-support/</a>                                                  -         -      
<a href="spring-test/" title="spring-test/">spring-test/</a>                                                     -         -      
<a href="spring-tomcat-weaver/" title="spring-tomcat-weaver/">spring-tomcat-weaver/</a>                                            -         -      
<a href="spring-toplink/" title="spring-toplink/">spring-toplink/</a>                                                  -         -      
<a href="spring-tuple/" title="spring-tuple/">spring-tuple/</a>                                                    -         -      
<a href="spring-tuple-parent/" title="spring-tuple-parent/">spring-tuple-parent/</a>                                             -         -      
<a href="spring-tx/" title="spring-tx/">spring-tx/</a>                                                       -         -      
<a href="spring-web/" title="spring-web/">spring-web/</a>                                                      -         -      
<a href="spring-webflow/" title="spring-webflow/">spring-webflow/</a>                                                  -         -      
<a href="spring-webflux/" title="spring-webflux/">spring-webflux/</a>                                                  -         -      
<a href="spring-webmvc/" title="spring-webmvc/">spring-webmvc/</a>                                                   -         -      
<a href="spring-webmvc-portlet/" title="spring-webmvc-portlet/">spring-webmvc-portlet/</a>                                           -         -      
<a href="spring-webmvc-struts/" title="spring-webmvc-struts/">spring-webmvc-struts/</a>                                            -         -      
<a href="spring-websocket/" title="spring-websocket/">spring-websocket/</a>                                                -         -      
<a href="springloaded/" title="springloaded/">springloaded/</a>                                                    -         -      
<a href="statemachine/" title="statemachine/">statemachine/</a>                                                    -         -      
<a href="various/" title="various/">various/</a>                                                         -         -      
<a href="vault/" title="vault/">vault/</a>                                                           -         -      
<a href="webflow/" title="webflow/">webflow/</a>                                                         -         -      
<a href="ws/" title="ws/">ws/</a>                                                              -         -      
<a href="xd/" title="xd/">xd/</a>                                                              -         -      
		</pre>
	</main>
	<hr/>
</body>

</html>
"""

if __name__ == '__main__':
    parser.feed(html)
