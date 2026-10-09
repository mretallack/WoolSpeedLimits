<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" encoding="iso-8859-1"/>
<xsl:template match="/">
sampledSeconds,id,CO2_abs,HC_abs,PMx_abs,NOx_abs,fuel_abs,electricity_abs,CO_normed,CO2_normed,HC_normed,PMx_normed,NOx_normed,fuel_normed,electricity_normed
<xsl:text>&#xD;</xsl:text>
<xsl:for-each select="meandata/interval/edge">
<xsl:if test=" @id = '-169755898#4' ">
<xsl:value-of select="@sampledSeconds"/>,<xsl:value-of select="@id"/>,<xsl:value-of select="@CO_abs"/>,<xsl:value-of select="@CO2_abs"/>,<xsl:value-of select="@HC_abs"/>,<xsl:value-of select="@PMx_abs"/>,<xsl:value-of select="@NOx_abs"/>,<xsl:value-of select="@fuel_abs"/>,<xsl:value-of select="@electricity_abs"/>,<xsl:value-of select="@CO_normed"/>,<xsl:value-of select="@CO2_normed"/>,<xsl:value-of select="@HC_normed"/>,<xsl:value-of select="@PMx_normed"/>,<xsl:value-of select="@NOx_normed"/>,<xsl:value-of select="@fuel_normed"/>,<xsl:value-of select="@electricity_normed"/>
<xsl:text>&#xD;</xsl:text>
</xsl:if>
</xsl:for-each>
</xsl:template>
</xsl:stylesheet>

