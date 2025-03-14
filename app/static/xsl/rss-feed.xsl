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
                <link rel="stylesheet" href="/static/xml-feed.css" media="screen,print"/>
            </head>
            <body>
                <header>
                    <h1>
                        RSS feed for
                        <xsl:value-of select="/rss/channel/title"/>
                    </h1>
                    <p>An RSS feed is a data format that contains the latest content from a website, blog, or podcast. You can use feeds to subscribe to websites and get the latest content in one place.</p>
                    <ul>
                        <li>Feeds put you in control. Unlike social media apps, there is no algorithm deciding what you see or read. You always get the latest content.</li>
                        <li>Feed are open and public by design. No one is harvesting your personal information and profiting by selling it to advertisers.</li>
                        <li>Feeds are spam-proof. Had enough? Easy, just unsubscribe from the feed.</li>
                    </ul>
                    <h2>About this blog</h2>
                    <p>
                        <xsl:value-of select="/rss/channel/description"/>
                    </p>
                    <p>
                        <a>
                            <xsl:attribute name="href">
                                <xsl:value-of select="/rss/channel/link"/>
                            </xsl:attribute>
                            Visit website &#x2192;
                        </a>
                    </p>
                </header>
                <main>
                    <h2>Recent posts</h2>
                    <!-- <p>This is a list of the <xsl:value-of select="count(/rss/channel/item)"/> most recent posts.</p> -->
                    <ol>
                    <xsl:for-each select="/rss/channel/item">
                        <li>
                            <article class="grid">
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