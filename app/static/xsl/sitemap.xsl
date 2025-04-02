<?xml version="1.0" encoding="UTF-8"?>
<!--
MIT License

Copyright (c) 2017 Pedro Borges

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

https://github.com/pedroborges/xml-sitemap-stylesheet
-->
<xsl:stylesheet
        version="1.0"
        xmlns:sm="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:fo="http://www.w3.org/1999/XSL/Format"
        xmlns:xhtml="http://www.w3.org/1999/xhtml"
        xmlns="http://www.w3.org/1999/xhtml">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    <xsl:template match="/">
        <html lang="en">
            <head>
                <title>
                    Sitemap
                    <xsl:if test="sm:sitemapindex">Index</xsl:if>
                </title>
                <meta charset="UTF-8"/>
                <link rel="stylesheet" href="/static/xml-sitemap.css" media="screen,print"/>
            </head>
            <body>
                <h1>
                    Sitemap
                    <xsl:if test="sm:sitemapindex">index</xsl:if>
                </h1>
                <p>
                    <xsl:choose>
                        <xsl:when test="sm:sitemapindex">
                            This XML Sitemap Index file contains
                            <xsl:value-of select="count(sm:sitemapindex/sm:sitemap)"/>
                            sitemaps.
                        </xsl:when>
                        <xsl:otherwise>
                            This XML Sitemap contains
                            <xsl:value-of select="count(sm:urlset/sm:url)"/>
                            URLs.
                        </xsl:otherwise>
                    </xsl:choose>
                </p>
                <xsl:apply-templates/>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="sm:sitemapindex">
        <table cellpadding="0" cellspacing="0" border="0">
        <thead>
            <tr>
                <th></th>
                <th>URL</th>
            </tr>
            </thead>
            <tbody>
            <xsl:for-each select="sm:sitemap">
                <tr>
                    <xsl:variable name="loc">
                        <xsl:value-of select="sm:loc"/>
                    </xsl:variable>
                    <xsl:variable name="pno">
                        <xsl:value-of select="position()"/>
                    </xsl:variable>
                    <td>
                        <xsl:value-of select="$pno"/>
                    </td>
                    <td>
                        <a href="{$loc}">
                            <xsl:value-of select="sm:loc"/>
                        </a>
                    </td>
                    <xsl:apply-templates/>
                </tr>
            </xsl:for-each>
            </tbody>
        </table>
    </xsl:template>

    <xsl:template match="sm:urlset">
        <table cellSpacing="0" cellPadding="0" border="0">
        <thead>
            <tr>
                <th></th>
                <th>URL</th>
                <xsl:if test="sm:url/sm:lastmod">
                    <th>Last Modified</th>
                </xsl:if>
            </tr>
            </thead>
            <tbody>
            <xsl:for-each select="sm:url">
                <tr>
                    <xsl:variable name="loc">
                        <xsl:value-of select="sm:loc"/>
                    </xsl:variable>
                    <xsl:variable name="pno">
                        <xsl:value-of select="position()"/>
                    </xsl:variable>
                    <td>
                        <xsl:value-of select="$pno"/>
                    </td>
                    <td>
                        <a href="{$loc}">
                            <xsl:value-of select="sm:loc"/>
                        </a>
                    </td>
                    <xsl:apply-templates select="sm:*"/>
                </tr>
            </xsl:for-each>
            </tbody>
        </table>
    </xsl:template>

    <xsl:template match="sm:loc">
    </xsl:template>

    <xsl:template match="sm:lastmod">
        <td>
            <xsl:apply-templates/>
        </td>
    </xsl:template>
</xsl:stylesheet>