<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="3.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:media="http://search.yahoo.com/mrss/">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    <xsl:template match="/">
        <html lang="en">
            <head>
                <meta charset="UTF-8"/>
                <title><xsl:value-of select="/rss/channel/title"/> RSS Feed</title>
                <meta name="description">
                    <xsl:attribute name="content">
                        <xsl:value-of select="/rss/channel/description"/>
                    </xsl:attribute>
                </meta>
                <style type="text/css">
                    *{margin: 0; padding: 0;}
                    body{color: #333; font-family: Arial; padding: 1.5rem; line-height: 1.5;}
                    h1, h2, p{margin-bottom: 0.75rem;}
                    h1{font-size: 32px;}
                    h2{font-size: 24px; margin-top: 1rem;}
                    h3{font-size: 18px;}
                    p{font-size: 16px; margin-bottom: 0;}
                    ul{margin-left: 2.25rem; list-style-position: outside; margin-top: 0.5rem;}
                    ol{margin-left: 2.25rem; list-style: none; margin-top: 1rem; counter-reset: item;}
                    ol li{counter-increment: item; position: relative;}
                    ol li::before{content: counter(item) ". "; position: absolute; top: 0; right: 100%; width: 1.75rem; padding-right: 0.5rem; text-align: right; font-weight: bold; line-height: 27px;}
                    header{margin-bottom: 1rem;}
                    article{margin-bottom: 1.5rem; display: grid; grid-template-columns: clamp(6rem, 25vw, 12rem) 1fr; grid-template-rows: repeat(2, min-content) 1fr; grid-gap: 0.25rem 1rem; vertical-align: middle;}
                    article h3{grid-area: 1 / 2 / 2 / 3;}
                    article p {grid-area: 2 / 2 / 3 / 3;}
                    article footer {grid-area: 3 / 2 / 4 / 3;}
                    article img{display: block; max-width: 100%; grid-area: 1 / 1 / 4 / 2;}
                    footer{font-size: 14px;}
                </style>
            </head>
            <body>
                <header>
                    <h1>RSS Feed</h1>
                    <p>An RSS feed is a data format that contains the latest content from a website, blog, or podcast. You can use feeds to subscribe to websites and get the latest content in one place.</p>
                    <ul>
                        <li>Feeds put you in control. Unlike social media apps, there is no algorithm deciding what you see or read. You always get the latest content.</li>
                        <li>Feed are open and public by design. No one is harvesting your personal information and profiting by selling it to advertisers.</li>
                        <li>Feeds are spam-proof. Had enough? Easy, just unsubscribe from the feed.</li>
                    </ul>
                    <h2>
                        <xsl:value-of select="/rss/channel/title"/>
                    </h2>
                    <p>
                        <xsl:value-of select="/rss/channel/description"/>
                    </p>
                    <a>
                        <xsl:attribute name="href">
                            <xsl:value-of select="/rss/channel/link"/>
                        </xsl:attribute>
                        Visit website &#x2192;
                    </a>
                </header>
                <main>
                    <h2>Recent posts</h2>
                    <p>This is a list of the <xsl:value-of select="count(/rss/channel/item)"/> most recent posts.</p>
                    <ol>
                    <xsl:for-each select="/rss/channel/item">
                        <li>
                            <article>
                                <h3>
                                    <a hreflang="en" target="_blank">
                                        <xsl:attribute name="href">
                                            <xsl:value-of select="link"/>
                                        </xsl:attribute>
                                        <xsl:value-of select="title"/>
                                    </a>
                                </h3>
                                <img alt="">
                                    <xsl:attribute name="src">
                                        <xsl:value-of select="media:content/@url"/>
                                    </xsl:attribute>
                                </img>
                                <p>
                                    <xsl:value-of select="description"/>
                                </p>
                                <footer>
                                    Published by

                                    <xsl:value-of select="dc:creator" disable-output-escaping="yes"/>
                                    on
                                    <time>
                                        <xsl:value-of select="pubDate"/>
                                    </time>
                                </footer>
                            </article>
                        </li>
                    </xsl:for-each>
                    </ol>
                </main>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>