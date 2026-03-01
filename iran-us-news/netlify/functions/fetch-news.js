// netlify/functions/fetch-news.js
const axios = require('axios');
const Parser = require('rss-parser');
const parser = new Parser();

exports.handler = async (event) => {
    const SOURCES = [
        { name: 'الجزيرة', url: 'https://www.aljazeera.net/xml/rss/all.xml', lang: 'ar' },
        { name: 'العربية', url: 'https://www.alarabiya.net/ar/tools/rss.xml', lang: 'ar' },
        { name: 'سكاي نيوز', url: 'https://www.skynewsarabia.com/web/rss', lang: 'ar' },
        { name: 'Reuters', url: 'https://www.reutersagency.com/feed/?best-topics=political-general&format=xml', lang: 'en' },
        { name: 'BBC News', url: 'https://feeds.bbci.co.uk/news/world/rss.xml', lang: 'en' }
    ];

    try {
        const promises = SOURCES.map(async (src) => {
            try {
                const feed = await parser.parseURL(src.url);
                return feed.items.map(item => ({
                    title: item.title,
                    link: item.link,
                    date: new Date(item.pubDate),
                    source: src.name,
                    lang: src.lang,
                    description: item.contentSnippet ? item.contentSnippet.slice(0, 150) + '...' : ''
                }));
            } catch (err) {
                console.error(`Error fetching ${src.name}:`, err);
                return [];
            }
        });

        const results = await Promise.all(promises);
        const allNews = results.flat().sort((a, b) => b.date - a.date);

        return {
            statusCode: 200,
            headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
            body: JSON.stringify(allNews)
        };
    } catch (error) {
        return { statusCode: 500, body: JSON.stringify({ error: "Failed to fetch news" }) };
    }
};