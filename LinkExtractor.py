from html.parser import HTMLParser


class LinkExtractor(HTMLParser):

    def __init__(self):
        self.hrefs = []
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, val in attrs:
                if name == 'href':
                    self.hrefs.append(val)

    def extract_hrefs(self, html):
        self.feed(html)
        return self.hrefs

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
    extractor = LinkExtractor()
    hrefs = extractor.extract_hrefs(html)
    print(hrefs)