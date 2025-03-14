<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="3.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:atom="http://www.w3.org/2005/Atom">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    <xsl:template match="/">
        <html lang="en">
            <head>
                <meta charset="UTF-8"/>
                <title><xsl:value-of select="atom:feed/atom:title"/> Atom Feed</title>
                <meta name="description">
                    <xsl:attribute name="content">
                        <xsl:value-of select="atom:feed/atom:subtitle"/>
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
                    p + p{margin-top: 0.25rem;}
                    ul{margin-left: 2.25rem; list-style-position: outside; margin-top: 0.5rem; margin-bottom: 1rem;}
                    ol{margin-left: 2.25rem; list-style: none; margin-top: 1rem; counter-reset: item;}
                    ol li{counter-increment: item; position: relative;}
                    ol li::before{content: counter(item) ". "; position: absolute; top: 0; right: 100%; width: 1.75rem; padding-right: 0.5rem; text-align: right; font-weight: bold; line-height: 27px;}
                    article{margin-bottom: 1.5rem;}
                    footer{font-size: 14px; margin-top: 0.25rem;}
                </style>
            </head>
            <body>
                <header>
                    <h1>
                        Atom feed for
                        <xsl:value-of select="atom:feed/atom:title"/>
                    </h1>
                    <p>An Atom feed is a data format that contains the latest content from a website, blog, or podcast. You can use feeds to subscribe to websites and get the latest content in one place.</p>
                    <ul>
                        <li>Feeds put you in control. Unlike social media apps, there is no algorithm deciding what you see or read. You always get the latest content.</li>
                        <li>Feed are open and public by design. No one is harvesting your personal information and profiting by selling it to advertisers.</li>
                        <li>Feeds are spam-proof. Had enough? Easy, just unsubscribe from the feed.</li>
                    </ul>
                    <h2>About this blog</h2>
                    <p>
                        <xsl:value-of select="atom:feed/atom:subtitle"/>
                    </p>
                    <p>
                        <a>
                            <xsl:attribute name="href">
                                <xsl:value-of select="atom:feed/atom:link/@href"/>
                            </xsl:attribute>
                            Visit website &#x2192;
                        </a>
                    </p>
                </header>
                <main>
                    <h2>Recent posts</h2>
                    <!-- <p>This is a list of the <xsl:value-of select="count(atom:feed/atom:entry)"/> most recent posts.</p> -->
                    <ol>
                    <xsl:for-each select="atom:feed/atom:entry">
                        <li>
                            <article>
                                <h3>
                                    <a>
                                        <xsl:attribute name="href">
                                            <xsl:value-of select="atom:link/@href"/>
                                        </xsl:attribute>
                                        <xsl:value-of select="atom:title"/>
                                    </a>
                                </h3>
                                <p>
                                    <xsl:value-of select="atom:summary"/>
                                </p>
                                <footer>
                                    Published by
                                    <xsl:choose>
                                        <xsl:when test="atom:author/atom:uri">
                                            <a>
                                                <xsl:attribute name="href">
                                                    <xsl:value-of select="atom:author/atom:uri"/>
                                                </xsl:attribute>
                                                <xsl:value-of select="atom:author/atom:name"/>
                                            </a>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:value-of select="atom:author/atom:name"/>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                    on
                                    <time>
                                        <xsl:value-of select="substring-before(atom:published, 'T')"/>
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